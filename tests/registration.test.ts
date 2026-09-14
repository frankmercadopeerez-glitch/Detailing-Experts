import {test} from 'node:test';
import assert from 'node:assert/strict';
import {registrationSchema} from '../server/domain';
test('registration requires consent and a valid plate',()=>{
 for(const input of [{consent:true},{consent:true,plate:''},{consent:false,plate:'ABC123'},{consent:true,plate:'<script>'},{consent:true,plate:'ABC123',admin:true}])assert.equal(registrationSchema.safeParse(input).success,false);
 assert.deepEqual(registrationSchema.parse({consent:true,plate:' abc123 '}),{consent:true,plate:'ABC123'});
});
