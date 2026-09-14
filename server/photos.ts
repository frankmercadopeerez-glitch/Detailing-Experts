import sharp from 'sharp';
import ImageKit from '@imagekit/nodejs';
import {randomUUID} from 'node:crypto';
import {Firestore,FieldValue} from '@google-cloud/firestore';
import {z} from 'zod';
import {id,requireAdmin,HttpError} from './domain';
import {Actor,record} from './service';
function imagekit(){if(!process.env.IMAGEKIT_PRIVATE_KEY||!process.env.IMAGEKIT_URL_ENDPOINT)throw new HttpError(503,'La carga de fotos está pendiente de conectar ImageKit.');return new ImageKit({privateKey:process.env.IMAGEKIT_PRIVATE_KEY});}
export async function compressImage(input:Buffer){
 if(input.length>1500000)throw new HttpError(413,'La imagen supera el tamaño permitido.');
 let output:Buffer;
 try{const meta=await sharp(input,{limitInputPixels:24000000,animated:false}).metadata();if(!['jpeg','png','webp'].includes(meta.format||'')||(meta.pages||1)>1)throw new Error('Unsupported image');output=await sharp(input,{limitInputPixels:24000000,animated:false}).rotate().resize({width:1600,height:1600,fit:'inside',withoutEnlargement:true}).webp({quality:78,effort:4}).toBuffer();}catch{throw new HttpError(400,'Usa una foto JPG, PNG o WebP válida.');}
 if(output.length>1000000)throw new HttpError(413,'La imagen comprimida supera 1 MB. Selecciona una foto más pequeña.');
 return output;
}
export async function uploadPhoto(db:Firestore,actor:Actor,body:any){
 requireAdmin(actor);const client=imagekit();const data=z.object({jobId:id,caption:z.string().trim().max(200),stage:z.enum(['antes','proceso','despues']),base64:z.string().max(2000000).regex(/^[A-Za-z0-9+/]+={0,2}$/)}).strict().parse(body);
 const job=await record(db,'jobs',data.jobId);const output=await compressImage(Buffer.from(data.base64,'base64'));const key=randomUUID();
 const usage=db.collection('_usage').doc('photos');const jobUsage=db.collection('_photoCounts').doc(data.jobId);const photo=db.collection('photos').doc(key);
 const budget=Number(process.env.PHOTO_STORAGE_BUDGET_BYTES||2000000000);
 await db.runTransaction(async tx=>{const u=await tx.get(usage);const j=await tx.get(jobUsage);if((u.data()?.bytes||0)+output.length>budget)throw new HttpError(409,'Se alcanzó el espacio reservado para fotos. Revisa el almacenamiento.');if((j.data()?.count||0)>=30)throw new HttpError(409,'Este trabajo alcanzó el límite de 30 fotos.');tx.set(usage,{bytes:FieldValue.increment(output.length)},{merge:true});tx.set(jobUsage,{count:FieldValue.increment(1)},{merge:true});tx.set(photo,{ownerId:job.ownerId,jobId:job.id,stage:data.stage,caption:data.caption,bytes:output.length,status:'uploading',createdAt:new Date().toISOString()});});
 let uploaded=false;
 try{
  const form=new FormData();form.set('file',new Blob([new Uint8Array(output)],{type:'image/webp'}),`${key}.webp`);form.set('fileName',`${key}.webp`);form.set('folder','/detailing-private');form.set('isPrivateFile','true');form.set('useUniqueFileName','false');
  const response=await fetch('https://upload.imagekit.io/api/v1/files/upload',{method:'POST',headers:{Authorization:`Basic ${Buffer.from(process.env.IMAGEKIT_PRIVATE_KEY+':').toString('base64')}`},body:form,signal:AbortSignal.timeout(25000)});
  if(!response.ok)throw new HttpError(502,'ImageKit no pudo guardar la foto. Vuelve a intentarlo.');
  const file=await response.json() as any;uploaded=true;
  if(typeof file.fileId!=='string'||typeof file.filePath!=='string')throw new Error('Invalid ImageKit response');
  const batch=db.batch();batch.update(photo,{fileId:file.fileId,filePath:file.filePath,status:'ready'});batch.set(db.collection('audit').doc(),{actorId:actor.uid,action:'photo.upload',entityId:key,createdAt:new Date().toISOString()});await batch.commit();
  return {id:key,bytes:output.length};
 }catch(e){
  // If the upload outcome is ambiguous, preserve the reservation for reconciliation.
  // Do not release a quota reservation for a possibly stored file.
  await photo.set({status:uploaded?'reconcile':'retry-review',errorAt:new Date().toISOString()},{merge:true});
  throw e;
 }
}
export async function listPhotos(db:Firestore,job:Record<string,any>){
 const docs=await db.collection('photos').where('jobId','==',job.id).limit(30).get();const ready=docs.docs.filter(d=>d.data().status==='ready');if(!ready.length)return {items:[]};const client=imagekit();
 return {items:ready.map(d=>{const p=d.data();return {id:d.id,caption:p.caption,stage:p.stage,bytes:p.bytes,createdAt:p.createdAt,url:client.helper.buildSrc({urlEndpoint:process.env.IMAGEKIT_URL_ENDPOINT!,src:p.filePath,signed:true,expiresIn:300,transformation:[{width:1600,quality:80}]})};})};
}
