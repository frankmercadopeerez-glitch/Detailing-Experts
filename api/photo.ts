import type {IncomingMessage,ServerResponse} from 'node:http';
import {authenticate,firebase} from '../server/firebase';
import {requireAdmin,HttpError} from '../server/domain';
import {rateLimit} from '../server/service';
import {readBody,json,failure,sameOrigin} from './portal';
import {uploadPhoto} from '../server/photos';
export default async function handler(req:IncomingMessage,res:ServerResponse){try{if(req.method!=='POST')throw new HttpError(405,'Método no permitido.');sameOrigin(req);if(!req.headers['content-type']?.startsWith('application/json'))throw new HttpError(415,'Se requiere JSON.');const actor=await authenticate(req.headers);requireAdmin(actor);const {db}=firebase();await rateLimit(db,actor.uid,'photos',10);return json(res,200,await uploadPhoto(db,actor,await readBody(req,2100000)));}catch(e){failure(res,e);}}
