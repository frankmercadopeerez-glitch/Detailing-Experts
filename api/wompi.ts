import type {IncomingMessage,ServerResponse} from 'node:http';
import {firebase} from '../server/firebase.js';
import {HttpError,validEvent,applyPayment} from '../server/domain.js';
import {readBody,json,failure} from './portal.js';
import {createHash} from 'node:crypto';
export default async function handler(req:IncomingMessage,res:ServerResponse){try{
 if(req.method!=='POST')throw new HttpError(405,'Método no permitido.');
 if(process.env.PAYMENTS_ENABLED!=='true'||!process.env.WOMPI_EVENTS_SECRET)throw new HttpError(503,'Pagos desactivados.');
 const event=await readBody(req);if(!validEvent(event,process.env.WOMPI_EVENTS_SECRET))throw new HttpError(401,'Firma inválida.');
 const env=process.env.WOMPI_ENV==='prod'?'prod':'test';if(event.environment!==env)throw new HttpError(400,'Ambiente incorrecto.');
 const t=event.data.transaction;
 // Signed fields do not necessarily include reference/currency. Verify the entire
 // transaction with Wompi before using any of those fields for reconciliation.
 if(typeof t.id!=='string'||!/^[-a-zA-Z0-9]+$/.test(t.id))throw new HttpError(400,'Transacción inválida.');
 const base=env==='prod'?'https://production.wompi.co/v1':'https://sandbox.wompi.co/v1';
 const response=await fetch(`${base}/transactions/${encodeURIComponent(t.id)}`,{headers:{Authorization:`Bearer ${process.env.WOMPI_PUBLIC_KEY}`},signal:AbortSignal.timeout(15000)});if(!response.ok)throw new HttpError(502,'No se pudo verificar el pago.');
 const transaction=(await response.json() as any).data;if(transaction?.id!==t.id||transaction.status!==t.status||transaction.amount_in_cents!==t.amount_in_cents)throw new HttpError(409,'El estado del pago no coincide.');
 const {db}=firebase();const found=await db.collection('invoices').where('reference','==',transaction.reference).limit(1).get();if(found.empty)throw new HttpError(404,'Cobro no encontrado.');
 const ref=found.docs[0].ref;const eventId=createHash('sha256').update(`${t.id}:${t.status}`).digest('hex');const seen=db.collection('paymentEvents').doc(eventId);
 await db.runTransaction(async tx=>{const oldEvent=await tx.get(seen);const invoice=await tx.get(ref);if(oldEvent.exists)return;const old=invoice.data()!;const next=applyPayment(old,transaction);tx.update(ref,{status:next.status,transactionId:transaction.id,transactionStatus:next.transactionStatus||'APPROVED',updatedAt:new Date().toISOString()});tx.set(seen,{transactionId:t.id,status:t.status,invoiceId:ref.id,processedAt:new Date().toISOString()});if(next.status==='paid'&&old.status!=='paid'){tx.set(db.collection('notifications').doc(),{ownerId:old.ownerId,title:'Pago confirmado',body:'Tu pago fue verificado. Puedes consultar el detalle en Pagos.',read:false,delivery:'pending',updatedAt:new Date().toISOString()});}});
 return json(res,200,{received:true});
}catch(e){failure(res,e);}}
