import {Firestore} from '@google-cloud/firestore';
import {z} from 'zod';
import {id,requireAdmin,HttpError} from './domain.js';
import type {Actor,Row} from './service.js';

export async function operations(db:Firestore,actor:Actor,action:string,body:Row){
 const now=new Date().toISOString();
 if(action==='export-data'){
  const ownerId=actor.admin?id.parse(body.ownerId||actor.uid):actor.uid;
  const result:Row={exportedAt:now};const user=await db.collection('users').doc(ownerId).get();
  result.profile=user.data()||{};
  for(const c of ['vehicles','jobs','invoices','requests','notifications','photos']){const rows=await db.collection(c).where('ownerId','==',ownerId).get();result[c]=rows.docs.filter(d=>c!=='photos'||(d.data().status==='ready'&&(actor.admin||!d.data().archived))).map(d=>({id:d.id,...d.data()}));}
  await db.collection('audit').add({actorId:actor.uid,action:'privacy.export',entityId:ownerId,createdAt:now});return result;
 }
 requireAdmin(actor);
 if(action==='customer-edit'){
  const input=z.object({id,version:z.string(),name:z.string().trim().min(3).max(120),phone:z.string().trim().max(24).regex(/^\+?[0-9\s()-]{7,24}$|^$/),email:z.string().trim().email().or(z.literal(''))}).strict().parse(body);
  await db.runTransaction(async tx=>{const ref=db.collection('users').doc(input.id),snap=await tx.get(ref);if(!snap.exists||snap.data()?.updatedAt!==input.version)throw new HttpError(409,'El cliente cambió. Actualiza antes de guardar.');if(snap.data()?.source!=='admin'&&input.email!==snap.data()?.email)throw new HttpError(400,'El correo de acceso debe cambiarlo el titular de la cuenta.');tx.update(ref,{name:input.name,phone:input.phone.replace(/[\s()-]/g,''),email:input.email.toLowerCase(),updatedAt:now});tx.set(db.collection('audit').doc(),{actorId:actor.uid,action,entityId:input.id,createdAt:now});});return {ok:true};
 }
 if(action==='archive'){
  const input=z.object({id,collection:z.enum(['users','vehicles']),archived:z.boolean(),version:z.string()}).strict().parse(body);
  await db.runTransaction(async tx=>{const ref=db.collection(input.collection).doc(input.id),snap=await tx.get(ref);if(!snap.exists||snap.data()?.updatedAt!==input.version)throw new HttpError(409,'El registro cambió. Actualiza antes de continuar.');if(input.archived){const jobs=await tx.get(db.collection('jobs').where(input.collection==='users'?'ownerId':'vehicleId','==',input.id));if(jobs.docs.some(d=>!['entregado','cancelado'].includes(d.data().status)))throw new HttpError(409,'Finaliza o cancela los trabajos activos antes de archivar.');if(input.collection==='users'){const invoices=await tx.get(db.collection('invoices').where('ownerId','==',input.id));if(invoices.docs.some(d=>d.data().status==='pending'))throw new HttpError(409,'Hay cobros pendientes de este cliente.');}}tx.update(ref,{archived:input.archived,updatedAt:now});tx.set(db.collection('audit').doc(),{actorId:actor.uid,action:input.archived?'record.archive':'record.restore',collection:input.collection,entityId:input.id,createdAt:now});});return {ok:true};
 }
 if(action==='manual-payment'){
  const input=z.object({id,method:z.enum(['cash','transfer']),reference:z.string().trim().min(3).max(120),confirmed:z.literal(true)}).strict().parse(body);
  await db.runTransaction(async tx=>{const ref=db.collection('invoices').doc(input.id),snap=await tx.get(ref);if(!snap.exists)throw new HttpError(404,'Cobro no encontrado.');if(snap.data()?.status!=='pending')throw new HttpError(409,'Este cobro ya no está pendiente.');tx.update(ref,{status:'paid',paymentMethod:input.method,paymentReference:input.reference,paidAt:now,paidBy:actor.uid,updatedAt:now});tx.set(db.collection('audit').doc(),{actorId:actor.uid,action,entityId:input.id,method:input.method,reference:input.reference,amountCents:snap.data()!.amountCents,createdAt:now});tx.set(db.collection('notifications').doc(),{ownerId:snap.data()!.ownerId,title:'Pago registrado',body:'El equipo confirmó el pago de tu servicio. Puedes consultar el detalle en Pagos.',read:false,delivery:'pending',updatedAt:now});});return {ok:true};
 }
 if(action==='photo-edit'){
  const input=z.object({id,caption:z.string().trim().max(200),stage:z.enum(['antes','proceso','despues']),archived:z.boolean()}).strict().parse(body);
  await db.runTransaction(async tx=>{const ref=db.collection('photos').doc(input.id),snap=await tx.get(ref);if(!snap.exists||snap.data()?.status!=='ready')throw new HttpError(409,'La foto no está disponible.');tx.update(ref,{caption:input.caption,stage:input.stage,archived:input.archived,updatedAt:now});tx.set(db.collection('audit').doc(),{actorId:actor.uid,action,entityId:input.id,archived:input.archived,createdAt:now});});return {ok:true};
 }
 throw new HttpError(400,'Acción inválida.');
}
