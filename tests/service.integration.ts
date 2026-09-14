import {test} from 'node:test';import assert from 'node:assert/strict';import {initializeApp,deleteApp} from 'firebase-admin/app';import {getFirestore} from 'firebase-admin/firestore';import {mutate,list,checkout} from '../server/service';
test('flujo persistente, aislamiento de clientes, conflictos y cobros',async()=>{
 if(process.env.FIRESTORE_EMULATOR_HOST!=='127.0.0.1:8087')throw new Error('This test may only run in the local emulator.');
 const app=initializeApp({projectId:'demo-detailing-experts'},'service-test');const db=getFirestore(app);const admin={uid:'operator',admin:true,email:'operator@ejemplo.test',name:'Operator'};const alice={uid:'alice',admin:false,email:'alice@ejemplo.test',name:'Alice'};const bob={uid:'bob',admin:false,email:'bob@ejemplo.test',name:'Bob'};
 try{
 await mutate(db,alice,'profile',{consent:true,plate:'ABC123'});await mutate(db,bob,'profile',{consent:true,plate:'XYZ789'});
 await assert.rejects(()=>mutate(db,alice,'vehicle',{data:{ownerId:'alice',plate:'ABC123',brand:'Toyota',model:'Prado',year:2024}}));
 const vehicle=await mutate(db,admin,'vehicle',{data:{ownerId:'alice',plate:'ABC123',brand:'Toyota',model:'Prado',year:2024}});
 const jobData={ownerId:'alice',vehicleId:vehicle.id,service:'Detailing',status:'programado',deadline:'2027-01-20',appointmentAt:'2027-01-20T14:00:00Z',nextReview:'2027-03-20'};
 const job=await mutate(db,admin,'job',{data:jobData});
 assert.equal((await list(db,alice,'jobs')).items.length,1);assert.equal((await list(db,bob,'jobs')).items.length,0);
 await assert.rejects(()=>list(db,alice,'users'));
 await assert.rejects(()=>mutate(db,admin,'job',{data:jobData}),'same slot must reject second job');
 await assert.rejects(()=>mutate(db,admin,'job',{id:job.id,version:'stale',data:{...jobData,status:'listo'}}));
 const current=(await db.collection('jobs').doc(job.id!).get()).data()!;
 await mutate(db,admin,'job',{id:job.id,version:current.updatedAt,data:{...jobData,status:'listo'}});
 assert.equal((await db.collection('jobs').doc(job.id!).get()).data()?.status,'listo');
 const invoice=await mutate(db,admin,'invoice',{data:{ownerId:'alice',jobId:job.id,description:'Detailing',amountCents:15000000,dueDate:'2027-01-20'}});
 assert.equal((await list(db,bob,'invoices')).items.length,0);assert.equal((await db.collection('invoices').doc(invoice.id!).get()).data()?.status,'pending');
 await assert.rejects(()=>checkout(db,alice,invoice.id!));
 await assert.rejects(()=>mutate(db,bob,'request',{vehicleId:vehicle.id,preferredDate:'2027-02-01',reason:'Other vehicle'}));
 const request=await mutate(db,alice,'request',{vehicleId:vehicle.id,preferredDate:'2027-02-01',reason:'Revisión'});
 await mutate(db,admin,'resolve-request',{id:request.id,status:'atendida',reply:'Revisaremos la disponibilidad.'});
 await assert.rejects(()=>mutate(db,admin,'resolve-request',{id:request.id,status:'atendida',reply:'Duplicate'}));
 assert.ok((await list(db,alice,'notifications')).items.length>=3);
 const first=(await list(db,alice,'notifications')).items[0];await assert.rejects(()=>mutate(db,bob,'read-notification',{id:first.id}));
 }finally{await db.terminate();await deleteApp(app);}
});
