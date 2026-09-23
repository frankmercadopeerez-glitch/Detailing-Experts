import {FieldValue,Firestore,Query} from '@google-cloud/firestore';
import {createHash,randomUUID} from 'node:crypto';
import {z} from 'zod';
import {assertOwner,requireAdmin,HttpError,id,vehicleSchema,customerVehicleSchema,jobSchema,invoiceSchema,requestSchema,registrationSchema,todayBogota,integrity} from './domain.js';
export type Actor={uid:string;admin:boolean;email:string;name:string;phone?:string};
export type Row=Record<string,any>;
export async function record(db:Firestore,collection:string,key:string){const snap=await db.collection(collection).doc(id.parse(key)).get();if(!snap.exists)throw new HttpError(404,'No se encontró el registro.');return {id:snap.id,...snap.data()} as Row;}
const stamp=()=>new Date().toISOString();
export async function rateLimit(db:Firestore,uid:string,action:string,limit=60){
 const key=createHash('sha256').update(uid+':'+action).digest('hex');const ref=db.collection('_limits').doc(key);
 await db.runTransaction(async tx=>{const old=(await tx.get(ref)).data();const now=Date.now();const count=old&&now-old.start<60000?old.count:0;if(count>=limit)throw new HttpError(429,'Demasiadas solicitudes. Espera un minuto.');tx.set(ref,{count:count+1,start:count?old!.start:now});});
}
function audit(db:Firestore,actor:Actor,action:string,entityId:string){return {ref:db.collection('audit').doc(),data:{actorId:actor.uid,action,entityId,createdAt:stamp()}};}
export async function list(db:Firestore,actor:Actor,collection:string,cursor?:string):Promise<{items:Row[];nextCursor:string|null}>{
 if(!['vehicles','jobs','invoices','requests','notifications','users','audit','privacyRequests'].includes(collection))throw new HttpError(400,'Colección inválida.');
 if(['users','audit'].includes(collection))requireAdmin(actor);
 if(collection==='privacyRequests'&&!actor.admin){const own=await db.collection(collection).doc(actor.uid).get();return {items:own.exists?[{id:own.id,...own.data()} as Row]:[],nextCursor:null};}
 let q:Query=db.collection(collection);
 if(!actor.admin||collection==='notifications')q=q.where('ownerId','==',actor.uid);
 const order=collection==='audit'?'createdAt':'updatedAt';q=q.orderBy(order,'desc').orderBy('__name__','desc');
 if(cursor){const ref=await db.collection(collection).doc(id.parse(cursor)).get();if(!ref.exists)throw new HttpError(400,'Página inválida.');if(!actor.admin||collection==='notifications')assertOwner({...actor,admin:false},ref.data()?.ownerId);q=q.startAfter(ref);}
 const page=await q.limit(51).get();const docs=page.docs.slice(0,50);return {items:docs.map(d=>({id:d.id,...d.data()})),nextCursor:page.docs.length>50?docs.at(-1)!.id:null};
}
export async function mutate(db:Firestore,actor:Actor,action:string,body:Row){
 const now=stamp();
 if(action==='profile'){
  const {consent,plate,name}=registrationSchema.parse(body);const ref=db.collection('users').doc(actor.uid);
  await db.runTransaction(async tx=>{const old=await tx.get(ref);tx.set(ref,{ownerId:actor.uid,name:name||actor.name,email:actor.email,phone:actor.phone||'',registrationPlate:plate,plateVerification:'pending',updatedAt:now,...(!old.exists?{createdAt:now,consent,consentVersion:'portal-2026-09',notifications:false}: {})},{merge:true});});return {ok:true};
 }
 if(action==='preferences'){
  const notifications=z.boolean().parse(body.notifications);await db.collection('users').doc(actor.uid).update({notifications,updatedAt:now});return {ok:true};
 }
 if(action==='device'){
  const token=z.string().min(20).max(4096).parse(body.token);const deviceId=createHash('sha256').update(token).digest('hex');
  const ref=db.collection('devices').doc(deviceId);
  await db.runTransaction(async tx=>{const existing=await tx.get(ref);if(body.remove===true){if(existing.exists&&existing.data()?.ownerId===actor.uid)tx.delete(ref);return;}tx.set(ref,{ownerId:actor.uid,token,updatedAt:now});});return {ok:true};
 }
 if(action==='read-notification'){
  const ref=db.collection('notifications').doc(id.parse(body.id));await db.runTransaction(async tx=>{const old=await tx.get(ref);if(!old.exists)throw new HttpError(404,'Aviso no encontrado.');assertOwner({...actor,admin:false},old.data()?.ownerId);tx.update(ref,{read:true});});return {ok:true};
 }
 if(action==='request'){
  const data=requestSchema.parse(body);const vehicle=await record(db,'vehicles',data.vehicleId);assertOwner({...actor,admin:false},vehicle.ownerId);
  if(data.preferredDate<todayBogota())throw new HttpError(400,'Elige una fecha futura.');
  const ref=db.collection('requests').doc();await db.runTransaction(async tx=>{const open=await tx.get(db.collection('requests').where('ownerId','==',actor.uid));const pending=open.docs.filter(d=>d.data().status==='pendiente');if(pending.length>=5)throw new HttpError(409,'Ya tienes solicitudes pendientes. Espera la respuesta del equipo.');if(pending.some(d=>d.data().vehicleId===data.vehicleId&&d.data().preferredDate===data.preferredDate))throw new HttpError(409,'Ya solicitaste una cita para este vehículo en esa fecha. Revisa Mis solicitudes.');tx.set(ref,{...data,ownerId:actor.uid,status:'pendiente',createdAt:now,updatedAt:now});});return {id:ref.id};
 }
 if(action==='privacy-request'){
  const ref=db.collection('privacyRequests').doc(actor.uid);const type=z.enum(['export','delete']).parse(body.type);await db.runTransaction(async tx=>{const old=await tx.get(ref);if(old.data()?.status==='pendiente')throw new HttpError(409,'Ya tienes una solicitud de datos pendiente. El equipo te responderá en el portal.');tx.set(ref,{ownerId:actor.uid,status:'pendiente',type,updatedAt:now});});return {ok:true};
 }
 requireAdmin(actor);
 if(action==='link-customer'){
  const {contactId,accountId,confirmed}=z.object({contactId:id,accountId:id,confirmed:z.literal(true)}).strict().parse(body);
  if(contactId===accountId)throw new HttpError(400,'Selecciona una cuenta diferente.');
  await db.runTransaction(async tx=>{
   const sourceRef=db.collection('users').doc(contactId),targetRef=db.collection('users').doc(accountId);
   const source=await tx.get(sourceRef),target=await tx.get(targetRef);
   if(source.data()?.source!=='admin'||source.data()?.accountStatus!=='pending'||!target.exists||target.data()?.source==='admin'||target.data()?.consent!==true)throw new HttpError(409,'Selecciona un contacto pendiente y una cuenta registrada.');
   const snapshots=await Promise.all(['vehicles','jobs','invoices','requests','notifications','photos'].map(c=>tx.get(db.collection(c).where('ownerId','==',contactId))));
   if(snapshots.reduce((n,s)=>n+s.size,0)>400)throw new HttpError(409,'Este historial requiere una migración asistida por su tamaño.');
   for(const snapshot of snapshots)for(const doc of snapshot.docs)tx.update(doc.ref,{ownerId:accountId,updatedAt:now});
   tx.update(sourceRef,{accountStatus:'linked',linkedAccountId:accountId,updatedAt:now});
   tx.update(targetRef,{plateVerification:'verified',updatedAt:now});
   const log=audit(db,actor,'customer.link',contactId);tx.set(log.ref,{...log.data,accountId,confirmed});
   tx.set(db.collection('notifications').doc(),{ownerId:accountId,title:'Tu historial ya está disponible',body:'El equipo vinculó tus vehículos y servicios a tu cuenta.',read:false,delivery:'pending',updatedAt:now});
  });return {ok:true};
 }
 if(action==='resolve-privacy'){
  const key=id.parse(body.id),reply=z.string().trim().min(3).max(1000).parse(body.reply);
  await db.runTransaction(async tx=>{const ref=db.collection('privacyRequests').doc(key),old=await tx.get(ref);if(!old.exists||old.data()?.status!=='pendiente')throw new HttpError(409,'La solicitud ya no está pendiente.');tx.update(ref,{status:'atendida',reply,updatedAt:now});const log=audit(db,actor,'privacy.resolve',key);tx.set(log.ref,log.data);tx.set(db.collection('notifications').doc(),{ownerId:old.data()!.ownerId,title:'Respuesta sobre tus datos',body:reply,read:false,delivery:'pending',updatedAt:now});});return {ok:true};
 }
 if(action==='customer-vehicle'){
  const data=customerVehicleSchema.parse(body);
  const customerRef=db.collection('users').doc(randomUUID());
  const vehicleRef=db.collection('vehicles').doc(randomUUID());
  await db.runTransaction(async tx=>{
   const duplicate=await tx.get(db.collection('vehicles').where('plate','==',data.vehicle.plate).limit(1));
   if(!duplicate.empty)throw new HttpError(409,'Esta placa ya está registrada. Busca el vehículo antes de crear otro.');
   const phoneMatch=await tx.get(db.collection('users').where('phone','==',data.customer.phone).limit(1));
   const emailMatch=data.customer.email?await tx.get(db.collection('users').where('email','==',data.customer.email).limit(1)):null;
   if(!phoneMatch.empty||emailMatch&&!emailMatch.empty)throw new HttpError(409,'Ya existe un cliente con este contacto. Selecciónalo en Cliente existente.');
   // A contact record is not an authenticated account. Never grant access by an unverified phone or email match.
   tx.create(customerRef,{...data.customer,ownerId:customerRef.id,accountStatus:'pending',source:'admin',createdBy:actor.uid,registrationPlate:data.vehicle.plate,plateVerification:'admin_recorded',createdAt:now,updatedAt:now});
   tx.create(vehicleRef,{...data.vehicle,ownerId:customerRef.id,createdAt:now,updatedAt:now});
   const log=audit(db,actor,'customer-vehicle.create',vehicleRef.id);tx.set(log.ref,log.data);
  });
  return {id:vehicleRef.id,customerId:customerRef.id};
 }
 if(action==='vehicle'){
  const data=vehicleSchema.parse(body.data);await record(db,'users',data.ownerId);
  const ref=db.collection('vehicles').doc(body.id?id.parse(body.id):randomUUID());
  await db.runTransaction(async tx=>{const old=await tx.get(ref);const duplicates=await tx.get(db.collection('vehicles').where('plate','==',data.plate));if(duplicates.docs.some(d=>d.id!==ref.id))throw new HttpError(409,'Esta placa ya está registrada. Vincula su historial en Clientes.');if(old.exists&&(old.data()?.ownerId!==data.ownerId||old.data()?.updatedAt!==body.version))throw new HttpError(409,'El registro cambió o intentaste cambiar de propietario. Recarga antes de guardar.');const log=audit(db,actor,'vehicle.save',ref.id);tx.set(ref,{...data,createdAt:old.data()?.createdAt||now,updatedAt:now});tx.set(log.ref,log.data);});return {id:ref.id};
 }
 if(action==='job'){
  const data=jobSchema.parse(body.data);const vehicle=await record(db,'vehicles',data.vehicleId);if(vehicle.ownerId!==data.ownerId)throw new HttpError(400,'El vehículo no pertenece a ese cliente.');
  const ref=db.collection('jobs').doc(body.id?id.parse(body.id):randomUUID());
  // Appointment capacity: one confirmed appointment per exact start slot.
  const slot=data.appointmentAt?new Date(data.appointmentAt).toISOString():'';
  if(slot&&!slot.endsWith(':00.000Z'))throw new HttpError(400,'La cita debe tener precisión de minutos.');
  await db.runTransaction(async tx=>{
   const currentVehicle=await tx.get(db.collection('vehicles').doc(data.vehicleId));if(currentVehicle.data()?.ownerId!==data.ownerId)throw new HttpError(409,'El propietario cambió. Actualiza el portal antes de guardar.');
   const old=await tx.get(ref);if(old.exists&&(old.data()?.ownerId!==data.ownerId||old.data()?.vehicleId!==data.vehicleId||old.data()?.updatedAt!==body.version))throw new HttpError(409,'El trabajo cambió. Recarga y vuelve a intentarlo.');
   const oldSlot=old.data()?.appointmentAt;const slotRef=slot?db.collection('_slots').doc(Buffer.from(slot).toString('base64url')):null;
   const newSlot=slotRef?await tx.get(slotRef):null;
   const oldSlotRef=oldSlot?db.collection('_slots').doc(Buffer.from(oldSlot).toString('base64url')):null;
   const oldReservation=oldSlotRef?await tx.get(oldSlotRef):null;
   if(data.status!=='cancelado'&&newSlot?.exists&&newSlot.data()?.jobId!==ref.id)throw new HttpError(409,'Ya hay una cita en ese horario. Elige otro.');
   if(oldSlotRef&&(oldSlot!==slot||data.status==='cancelado')&&oldReservation?.data()?.jobId===ref.id)tx.delete(oldSlotRef);
   if(slotRef&&data.status!=='cancelado')tx.set(slotRef,{jobId:ref.id,start:slot});
   tx.set(ref,{...data,appointmentAt:slot,createdAt:old.data()?.createdAt||now,updatedAt:now});
   const log=audit(db,actor,'job.save',ref.id);tx.set(log.ref,log.data);
   const n=db.collection('notifications').doc();tx.set(n,{ownerId:data.ownerId,title:'Actualización de tu vehículo',body:`${data.service}: ${data.status.replaceAll('_',' ')}. Consulta los detalles del trabajo.`,jobId:ref.id,read:false,delivery:'pending',updatedAt:now});
  });return {id:ref.id};
 }
 if(action==='invoice'){
  const data=invoiceSchema.parse(body.data);const job=await record(db,'jobs',data.jobId);if(job.ownerId!==data.ownerId)throw new HttpError(400,'El trabajo no pertenece a ese cliente.');
  const ref=db.collection('invoices').doc();const log=audit(db,actor,'invoice.create',ref.id);await db.runTransaction(async tx=>{const current=await tx.get(db.collection('jobs').doc(data.jobId));if(current.data()?.ownerId!==data.ownerId)throw new HttpError(409,'El propietario cambió. Actualiza el portal antes de guardar.');tx.set(ref,{...data,currency:'COP',status:'pending',reference:`DE-${ref.id}`,createdAt:now,updatedAt:now});tx.set(log.ref,log.data);tx.set(db.collection('notifications').doc(),{ownerId:data.ownerId,title:'Nuevo cobro disponible',body:'El equipo registró un cobro. Consulta el importe y el vencimiento en Pagos.',read:false,delivery:'pending',updatedAt:now});});return {id:ref.id};
 }
 if(action==='resolve-request'){
  const key=id.parse(body.id);const reply=z.string().trim().min(1).max(1000).parse(body.reply);const status=z.enum(['atendida','rechazada']).parse(body.status);const ref=db.collection('requests').doc(key);
  await db.runTransaction(async tx=>{const old=await tx.get(ref);if(!old.exists)throw new HttpError(404,'Solicitud no encontrada.');if(old.data()?.status!=='pendiente')throw new HttpError(409,'La solicitud ya fue atendida.');tx.update(ref,{reply,status,updatedAt:now});const n=db.collection('notifications').doc();tx.set(n,{ownerId:old.data()!.ownerId,title:'Respuesta a tu solicitud',body:reply,read:false,delivery:'pending',updatedAt:now});const log=audit(db,actor,'request.resolve',key);tx.set(log.ref,log.data);});return {ok:true};
 }
 throw new HttpError(400,'Acción inválida.');
}
export function paymentsReady(){return process.env.PAYMENTS_ENABLED==='true'&&!!process.env.WOMPI_PUBLIC_KEY&&!!process.env.WOMPI_INTEGRITY_SECRET&&!!process.env.WOMPI_EVENTS_SECRET;}
export async function checkout(db:Firestore,actor:Actor,key:string){
 if(!paymentsReady())throw new HttpError(503,'Los pagos en línea todavía no están habilitados.');
 const invoice=await record(db,'invoices',key);assertOwner(actor,invoice.ownerId);if(invoice.status!=='pending')throw new HttpError(409,'Este cobro ya no está pendiente.');
 const pub=process.env.WOMPI_PUBLIC_KEY!;const env=process.env.WOMPI_ENV==='prod'?'prod':'test';if(!pub.startsWith(`pub_${env}_`))throw new HttpError(503,'Configuración de pagos inconsistente.');
 const params=new URLSearchParams({'public-key':pub,currency:'COP','amount-in-cents':String(invoice.amountCents),reference:invoice.reference,'signature:integrity':integrity(invoice.reference,invoice.amountCents,'COP',process.env.WOMPI_INTEGRITY_SECRET!),'redirect-url':`${process.env.APP_ORIGIN}/portal/#pagos`});
 return {url:`https://checkout.wompi.co/p/?${params}`,environment:env};
}
