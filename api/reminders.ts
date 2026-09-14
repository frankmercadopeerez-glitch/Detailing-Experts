import type {IncomingMessage,ServerResponse} from 'node:http';
import {timingSafeEqual,createHash} from 'node:crypto';
import {firebase} from '../server/firebase.js';
import {HttpError,todayBogota} from '../server/domain.js';
import {json,failure} from './portal.js';
export default async function handler(req:IncomingMessage,res:ServerResponse){try{
 if(req.method!=='GET')throw new HttpError(405,'Método no permitido.');const secret=process.env.CRON_SECRET;const auth=req.headers.authorization||'';const expected=`Bearer ${secret}`;if(!secret||auth.length!==expected.length||!timingSafeEqual(Buffer.from(auth),Buffer.from(expected)))throw new HttpError(401,'No autorizado.');
 const {db,messaging}=firebase();const today=todayBogota();let created=0,sent=0;
 const upcoming=todayBogota(new Date(Date.now()+7*86400000));
 // Query by nextReview avoids scanning every job, and stable ids prevent duplicates.
 const due=await db.collection('jobs').where('nextReview','>=',today).where('nextReview','<=',upcoming).limit(200).get();
 for(const doc of due.docs){const job=doc.data();if(job.status==='cancelado')continue;const key=createHash('sha256').update(`${doc.id}:${job.nextReview}`).digest('hex');const ref=db.collection('notifications').doc(`review-${key}`);await db.runTransaction(async tx=>{if((await tx.get(ref)).exists)return;tx.set(ref,{ownerId:job.ownerId,title:'Tu próxima revisión',body:`Tienes una revisión recomendada para el ${job.nextReview}. Solicita una cita en el portal.`,jobId:doc.id,read:false,delivery:'pending',updatedAt:new Date().toISOString()});created++;});}
 if(process.env.NOTIFICATIONS_ENABLED!=='true')return json(res,200,{created,sent,pushEnabled:false});
 const pending=await db.collection('notifications').where('delivery','==','pending').limit(100).get();
 for(const doc of pending.docs){const n=doc.data();const user=await db.collection('users').doc(n.ownerId).get();if(user.data()?.notifications!==true){await doc.ref.update({delivery:'in_app'});continue;}
  const devices=await db.collection('devices').where('ownerId','==',n.ownerId).limit(10).get();if(devices.empty){await doc.ref.update({delivery:'in_app'});continue;}
  // Lease prevents concurrent cron invocations sending the same notification.
  const lease=await db.runTransaction(async tx=>{const current=(await tx.get(doc.ref)).data();if(current?.delivery!=='pending'||(current.leaseUntil||0)>Date.now())return false;tx.update(doc.ref,{leaseUntil:Date.now()+120000});return true;});if(!lease)continue;
  try{const result=await messaging.sendEachForMulticast({tokens:devices.docs.map(d=>d.data().token),data:{notificationId:doc.id},webpush:{headers:{TTL:'86400',Urgency:'normal'}}});sent+=result.successCount;
   const invalid=['messaging/registration-token-not-registered','messaging/invalid-registration-token'];let retry=false;
   for(let i=0;i<result.responses.length;i++){const r=result.responses[i];if(r.error){if(invalid.includes(r.error.code))await devices.docs[i].ref.delete();else retry=true;}}
   await doc.ref.update({delivery:retry&&result.successCount===0?'pending':result.successCount?'sent':'in_app',leaseUntil:0});
  }catch{await doc.ref.update({leaseUntil:0});}
 }
 return json(res,200,{created,sent,pushEnabled:true});
}catch(e){failure(res,e);}}
