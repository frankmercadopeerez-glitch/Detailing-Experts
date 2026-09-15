import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mutate} from '../server/service';
import {customerVehicleSchema} from '../server/domain';
const body={customer:{name:'Cliente de prueba',phone:'+57 (300) 123-4567',email:'TEST@example.com'},vehicle:{plate:'abc123',brand:'Toyota',model:'Corolla',year:2024,color:'Gris'}};
function database(duplicate=''){
 const writes:any[]=[];
 const db:any={collection:(collection:string)=>({doc:(id='audit')=>({collection,id}),where:(field:string)=>({limit:()=>({collection,field})})}),runTransaction:async(fn:any)=>fn({get:async(q:any)=>({empty:duplicate!==q.collection+':'+q.field}),create:(ref:any,data:any)=>writes.push({ref,data}),set:(ref:any,data:any)=>writes.push({ref,data})})};
 return {db,writes};
}
const admin={uid:'admin',admin:true,email:'admin@example.com',name:'Admin'};
test('registro conjunto crea contacto sin permisos y vehículo con el mismo propietario',async()=>{const {db,writes}=database();const result=await mutate(db,admin,'customer-vehicle',body);assert.equal(writes.length,3);assert.equal(writes[0].data.accountStatus,'pending');assert.equal(writes[0].data.admin,undefined);assert.equal(writes[0].data.consent,undefined);assert.equal(writes[0].data.phone,'+573001234567');assert.equal(writes[0].data.email,'test@example.com');assert.equal(writes[1].data.ownerId,result.customerId);assert.equal(writes[1].data.plate,'ABC123');});
test('cliente no puede crear contactos ni vehículos mediante el flujo administrativo',async()=>{const {db,writes}=database();await assert.rejects(mutate(db,{...admin,admin:false},'customer-vehicle',body),/autorizado/);assert.equal(writes.length,0);});
test('placa o contacto duplicado no deja registros parciales',async()=>{for(const duplicate of ['vehicles:plate','users:phone','users:email']){const {db,writes}=database(duplicate);await assert.rejects(mutate(db,admin,'customer-vehicle',body),/registrada|existe/);assert.equal(writes.length,0);}});
test('valida teléfono y rechaza privilegios o propietario inyectados',()=>{assert.equal(customerVehicleSchema.safeParse({...body,customer:{...body.customer,phone:'abc'}}).success,false);assert.equal(customerVehicleSchema.safeParse({...body,customer:{...body.customer,admin:true}}).success,false);assert.equal(customerVehicleSchema.safeParse({...body,vehicle:{...body.vehicle,ownerId:'other'}}).success,false);});
