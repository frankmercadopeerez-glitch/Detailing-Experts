import type {IncomingMessage,ServerResponse} from 'node:http';
import {authenticate,firebase} from '../server/firebase.js';
import {requireAdmin,HttpError} from '../server/domain.js';
import {rateLimit} from '../server/service.js';
import {readBody,json,failure,sameOrigin} from './portal.js';
import {uploadPhoto} from '../server/photos.js';
export default async function handler(req:IncomingMessage,res:ServerResponse){try{if(req.method!=='POST')throw new HttpError(405,'Método no permitido.');sameOrigin(req);if(!req.headers['content-type']?.startsWith('application/json'))throw new HttpError(415,'Se requiere JSON.');const actor=await authenticate(req.headers);requireAdmin(actor);const {db}=firebase();await rateLimit(db,actor.uid,'photos',10);return json(res,200,await uploadPhoto(db,actor,await readBody(req,2100000)));}catch(e){failure(res,e);}}
