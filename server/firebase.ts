import {cert,getApps,initializeApp} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {getFirestore} from 'firebase-admin/firestore';
import {getMessaging} from 'firebase-admin/messaging';
import {getAppCheck} from 'firebase-admin/app-check';
import {HttpError} from './domain';
export function configured(){return !!(process.env.FIREBASE_PROJECT_ID&&process.env.FIREBASE_CLIENT_EMAIL&&process.env.FIREBASE_PRIVATE_KEY);}
export function firebase(){
 if(!getApps().length){
   if(process.env.FIRESTORE_EMULATOR_HOST&&process.env.FIREBASE_AUTH_EMULATOR_HOST){initializeApp({projectId:process.env.FIREBASE_PROJECT_ID||'demo-detailing-experts'});}
   else {if(!configured())throw new HttpError(503,'El portal está en preparación. La conexión segura aún no está configurada.');initializeApp({credential:cert({projectId:process.env.FIREBASE_PROJECT_ID,clientEmail:process.env.FIREBASE_CLIENT_EMAIL,privateKey:process.env.FIREBASE_PRIVATE_KEY!.replace(/\\n/g,'\n')})});}
 }
 return {db:getFirestore(),auth:getAuth(),messaging:getMessaging(),appCheck:getAppCheck()};
}
export async function authenticate(headers:Record<string,any>){
 const authorization=headers.authorization;
 if(typeof authorization!=='string'||!authorization.startsWith('Bearer '))throw new HttpError(401,'Ingresa con tu cuenta.');
 const f=firebase();let token;
 try{token=await f.auth.verifyIdToken(authorization.slice(7),true);}catch{throw new HttpError(401,'Tu sesión venció. Ingresa nuevamente.');}
 const provider=token.firebase?.sign_in_provider;
 if(!(['google.com','password'].includes(provider)&&token.email_verified)&&!(provider==='phone'&&token.phone_number))throw new HttpError(403,'Verifica tu correo electrónico antes de ingresar.');
 if(process.env.REQUIRE_APP_CHECK!=='false'){
   const check=headers['x-firebase-appcheck'];if(typeof check!=='string')throw new HttpError(403,'No se pudo verificar la aplicación.');
   try{await f.appCheck.verifyToken(check);}catch{throw new HttpError(403,'No se pudo verificar la aplicación.');}
 }
 return {uid:token.uid,admin:token.admin===true,email:token.email||'',phone:token.phone_number||'',name:token.name||'Cliente'};
}
