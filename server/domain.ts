import { z } from 'zod';
import { createHash, timingSafeEqual } from 'node:crypto';
export const id = z.string().regex(/^[a-zA-Z0-9_-]{1,128}$/);
const text = (max=200) => z.string().trim().min(1).max(max);
export const day = z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(v=>!Number.isNaN(Date.parse(v))&&new Date(v).toISOString().slice(0,10)===v,'Fecha inválida');
export const optionalDay = z.union([day,z.literal('')]).default('');
export const status = z.enum(['programado','en_proceso','listo','entregado','atrasado','cancelado']);
export const vehicleSchema = z.object({ownerId:id,plate:z.string().trim().toUpperCase().regex(/^[A-Z0-9-]{4,10}$/),brand:text(60),model:text(80),year:z.number().int().min(1900).max(2100),color:z.string().trim().max(50).default('')}).strict();
export const registrationSchema=z.object({consent:z.literal(true),name:z.string().trim().min(3).max(120).optional(),plate:vehicleSchema.shape.plate}).strict();
export const customerVehicleSchema=z.object({
 customer:z.object({name:text(120),phone:z.string().trim().transform(v=>v.replace(/[\s()-]/g,'')).refine(v=>/^\+?[0-9]{7,15}$/.test(v),'Teléfono inválido'),email:z.union([z.string().trim().toLowerCase().email(),z.literal('')]).default('')}).strict(),
 vehicle:vehicleSchema.omit({ownerId:true})
}).strict();
export const jobSchema = z.object({ownerId:id,vehicleId:id,service:text(120),status,deadline:day,appointmentAt:z.string().datetime({offset:true}).or(z.literal('')).default(''),nextReview:optionalDay,notes:z.string().trim().max(3000).default(''),checklist:z.array(z.object({label:text(100),done:z.boolean()}).strict()).max(20).default([]),warrantyUntil:optionalDay,assignedTo:z.string().trim().max(100).default('')}).strict().refine(v=>!v.nextReview||v.nextReview>=v.deadline,'La revisión debe ser posterior a la fecha límite');
export const invoiceSchema=z.object({ownerId:id,jobId:id,description:text(150),amountCents:z.number().int().min(10000).max(2000000000),dueDate:day}).strict();
export const requestSchema=z.object({vehicleId:id,preferredDate:day,reason:text(1000)}).strict();
export function todayBogota(now=new Date()){return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);}
export function effectiveStatus(job:{status:string;deadline:string},today=todayBogota()){return !['listo','entregado','cancelado'].includes(job.status)&&job.deadline<today?'atrasado':job.status;}
export function assertOwner(actor:{uid:string;admin:boolean},ownerId:unknown){if(!actor.admin&&actor.uid!==ownerId)throw new HttpError(403,'No tienes acceso a este registro.');}
export class HttpError extends Error {constructor(public status:number,message:string){super(message);}}
export function requireAdmin(actor:{admin:boolean}){if(!actor.admin)throw new HttpError(403,'Acceso reservado al equipo autorizado.');}
export function integrity(reference:string,amount:number,currency:string,secret:string){return createHash('sha256').update(`${reference}${amount}${currency}${secret}`).digest('hex');}
export function validEvent(event:any,secret:string){
  if(!secret||event?.event!=='transaction.updated'||!Array.isArray(event.signature?.properties)||!Number.isSafeInteger(event.timestamp))return false;
  const props=event.signature.properties;
  if(props.length>20||!['transaction.id','transaction.status','transaction.amount_in_cents'].every(p=>props.includes(p)))return false;
  const vals=[];
  for(const path of props){if(typeof path!=='string'||!/^transaction\.[a-z_]+$/.test(path))return false;const value=event.data?.transaction?.[path.slice(12)];if(!['string','number','boolean'].includes(typeof value))return false;vals.push(String(value));}
  const expected=createHash('sha256').update(vals.join('')+event.timestamp+secret).digest('hex');
  const actual=event.signature.checksum;
  return typeof actual==='string'&&/^[a-f0-9]{64}$/i.test(actual)&&timingSafeEqual(Buffer.from(expected,'hex'),Buffer.from(actual,'hex'));
}
export function paymentMatches(invoice:any,transaction:any){return transaction.reference===invoice.reference&&transaction.currency==='COP'&&transaction.amount_in_cents===invoice.amountCents;}
export function applyPayment(invoice:any,transaction:any){
  if(!paymentMatches(invoice,transaction))throw new HttpError(409,'El pago no coincide con el cobro.');
  if(invoice.status==='paid')return invoice;
  return {...invoice,status:transaction.status==='APPROVED'?'paid':invoice.status,transactionId:transaction.id,transactionStatus:transaction.status};
}
