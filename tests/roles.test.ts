import {test} from 'node:test';
import assert from 'node:assert/strict';
import {isAdministrator} from '../server/roles.js';
test('designated administrator requires verified Google identity',()=>{
 const account={email:'frankmercadopeerez@gmail.com',email_verified:true,firebase:{sign_in_provider:'google.com'}};
 assert.equal(isAdministrator(account),true);
 assert.equal(isAdministrator({...account,email_verified:false}),false);
 assert.equal(isAdministrator({...account,firebase:{sign_in_provider:'password'}}),false);
 assert.equal(isAdministrator({...account,email:'otro@gmail.com'}),false);
 assert.equal(isAdministrator({admin:'true'}),false);
 assert.equal(isAdministrator({admin:true}),true);
});
