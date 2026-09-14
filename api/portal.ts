import type {IncomingMessage,ServerResponse} from 'node:http';
import {ZodError} from 'zod';
import {configured,firebase,authenticate} from '../server/firebase.js';
import {HttpError,id} from '../server/domain.js';
import {list,mutate,checkout,rateLimit,paymentsReady,record} from '../server/service.js';
import {assertOwner} from '../server/domain.js';
export async function readBody(req:IncomingMessage,max=65536){
 const parsed=(req as any).body;if(parsed!==undefined){if(Buffer.byteLength(JSON.stringify(parsed))>max)throw new HttpError(413,'Solicitud demasiado grande.');return typeof parsed==='string'?JSON.parse(parsed):parsed;}
 const chunks:Buffer[]=[];let size=0;for await(const chunk of req){size+=chunk.length;if(size>max)throw new HttpError(413,'Solicitud demasiado grande.');chunks.push(Buffer.from(chunk));}
 try{return JSON.parse(Buffer.concat(chunks).toString()||'{}');}catch{throw new HttpError(400,'Solicitud inválida.');}
}
export function json(res:ServerResponse,status:number,data:unknown){res.statusCode=status;res.setHeader('Content-Type','application/json; charset=utf-8');res.setHeader('Cache-Control','no-store');res.setHeader('X-Content-Type-Options','nosniff');res.end(JSON.stringify(data));}
export function sameOrigin(req:IncomingMessage){const origin=req.headers.origin;const allowed=process.env.APP_ORIGIN||'https://detailing-experts.vercel.app';const local=process.env.NODE_ENV!=='production'&&['http://127.0.0.1:5173','http://localhost:5173'].includes(origin||'');if(origin!==allowed&&!local)throw new HttpError(403,'Origen no permitido.');}
export function failure(res:ServerResponse,e:unknown){if(e instanceof HttpError)return json(res,e.status,{error:e.message});if(e instanceof ZodError)return json(res,400,{error:'Revisa los campos del formulario.',fields:e.issues.map(x=>({path:x.path.join('.'),message:x.message}))});console.error('Portal request failed',e instanceof Error?e.name:'Unknown');return json(res,500,{error:'No se pudo completar la operación. Vuelve a intentarlo.'});}
export default async function handler(req:IncomingMessage,res:ServerResponse){try{
 const url=new URL(req.url||'','http://localhost');const action=url.searchParams.get('action')||'status';
 if(!['GET','POST'].includes(req.method||'')){res.setHeader('Allow','GET, POST');return json(res,405,{error:'Método no permitido.'});}
 if(action==='status'&&req.method==='GET')return json(res,200,{configured:configured(),payments:paymentsReady(),photos:!!process.env.IMAGEKIT_PRIVATE_KEY,notifications:process.env.NOTIFICATIONS_ENABLED==='true'});
 if(req.method==='POST'){sameOrigin(req);if(!req.headers['content-type']?.startsWith('application/json'))throw new HttpError(415,'Se requiere JSON.');}
 const actor=await authenticate(req.headers);const {db}=firebase();await rateLimit(db,actor.uid,'api',120);
 if(req.method==='GET'){
  if(action==='me'){const user=await db.collection('users').doc(actor.uid).get();return json(res,200,{...actor,profile:user.data()||null});}
  if(action==='list')return json(res,200,await list(db,actor,url.searchParams.get('collection')||'',url.searchParams.get('cursor')||undefined));
  if(action==='photos'){const job=await record(db,'jobs',id.parse(url.searchParams.get('jobId')));assertOwner(actor,job.ownerId);const {listPhotos}=await import('../server/photos.js');return json(res,200,await listPhotos(db,job));}
  throw new HttpError(400,'Acción inválida.');
 }
 await rateLimit(db,actor.uid,'write',30);const body=await readBody(req);
 if(action==='checkout')return json(res,200,await checkout(db,actor,id.parse(body.id)));
 return json(res,200,await mutate(db,actor,action,body));
}catch(e){failure(res,e);}}
