import {initializeApp} from 'firebase/app';
import {getAuth,GoogleAuthProvider,signInWithPopup,signOut,onAuthStateChanged,browserSessionPersistence,setPersistence,User,createUserWithEmailAndPassword,signInWithEmailAndPassword,sendEmailVerification,sendPasswordResetEmail,RecaptchaVerifier,signInWithPhoneNumber,ConfirmationResult,updateProfile} from 'firebase/auth';
import {initializeAppCheck,ReCaptchaEnterpriseProvider,getToken as appCheckToken,AppCheck} from 'firebase/app-check';
const env=import.meta.env;
export const config={apiKey:env.VITE_FIREBASE_API_KEY,authDomain:env.VITE_FIREBASE_AUTH_DOMAIN,projectId:env.VITE_FIREBASE_PROJECT_ID,appId:env.VITE_FIREBASE_APP_ID,messagingSenderId:env.VITE_FIREBASE_MESSAGING_SENDER_ID};
export const ready=Object.values(config).every(Boolean);
let auth:ReturnType<typeof getAuth>|undefined,check:AppCheck|undefined;
export function setup(callback:(user:User|null)=>void){if(!ready){callback(null);return;}const app=initializeApp(config);auth=getAuth(app);if(env.VITE_FIREBASE_APPCHECK_SITE_KEY)check=initializeAppCheck(app,{provider:new ReCaptchaEnterpriseProvider(env.VITE_FIREBASE_APPCHECK_SITE_KEY),isTokenAutoRefreshEnabled:true});onAuthStateChanged(auth,callback);}
export async function login(){if(!auth)throw new Error('El acceso está en preparación.');await setPersistence(auth,browserSessionPersistence);const provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});await signInWithPopup(auth,provider);}
let deviceToken='';
export const phoneEnabled=env.VITE_PHONE_AUTH_ENABLED==='true';
export async function emailLogin(email:string,password:string,register=false,details?:{name:string;plate:string}){
 if(!auth)throw new Error('El acceso está en preparación.');
 await setPersistence(auth,browserSessionPersistence);
 if(register){if(!details||details.name.length<3||! /^[A-Z0-9-]{4,10}$/.test(details.plate))throw new Error('Revisa el nombre y la placa.');sessionStorage.setItem('portal-registration',JSON.stringify({email:email.trim().toLowerCase(),...details}));const result=await createUserWithEmailAndPassword(auth,email,password);await updateProfile(result.user,{displayName:details.name});await sendEmailVerification(result.user);}
 else await signInWithEmailAndPassword(auth,email,password);
}
export async function resetPassword(email:string){if(!auth)throw new Error('El acceso está en preparación.');await sendPasswordResetEmail(auth,email);}
export async function refreshVerification(){if(!auth?.currentUser)return;await auth.currentUser.reload();await auth.currentUser.getIdToken(true);return auth.currentUser.emailVerified;}
export async function resendVerification(){if(auth?.currentUser)await sendEmailVerification(auth.currentUser);}
let verifier:RecaptchaVerifier|undefined,confirmation:ConfirmationResult|undefined;
export async function phoneCode(phone:string){
 if(!auth||!phoneEnabled)throw new Error('El acceso por SMS aún no está habilitado.');
 if(!/^\+[1-9]\d{7,14}$/.test(phone))throw new Error('Incluye el indicativo, por ejemplo +573001234567.');
 await setPersistence(auth,browserSessionPersistence);verifier?.clear();verifier=new RecaptchaVerifier(auth,'phone-recaptcha',{size:'normal'});
 confirmation=await signInWithPhoneNumber(auth,phone,verifier);
}
export async function confirmPhone(code:string){if(!confirmation)throw new Error('Solicita primero un código.');await confirmation.confirm(code);confirmation=undefined;verifier?.clear();verifier=undefined;}
export async function logout(){if(deviceToken){try{await api('device',{token:deviceToken,remove:true});}catch{/* session still closes */}try{const {getMessaging,deleteToken}=await import('firebase/messaging');await deleteToken(getMessaging());}catch{}deviceToken='';}if(auth)await signOut(auth);}
export async function api(action:string,body?:unknown,params:Record<string,string>={},path='/api/portal'){
 const headers:Record<string,string>={};if(auth?.currentUser)headers.Authorization=`Bearer ${await auth.currentUser.getIdToken()}`;
 if(check)headers['X-Firebase-AppCheck']=(await appCheckToken(check)).token;
 if(body!==undefined)headers['Content-Type']='application/json';
 const url=path===' /api/photo'?path:`${path}?${new URLSearchParams({action,...params})}`;
 const res=await fetch(url,{method:body===undefined?'GET':'POST',headers,body:body===undefined?undefined:JSON.stringify(body),cache:'no-store',signal:AbortSignal.timeout(40000)});
 const data=await res.json();if(!res.ok)throw new Error(data.error||'No se pudo completar la operación.');return data;
}
export async function notifications(){
 if(!env.VITE_FIREBASE_VAPID_KEY)throw new Error('Los avisos push aún están en preparación.');
 const {getMessaging,getToken,isSupported}=await import('firebase/messaging');if(!await isSupported())throw new Error('Este navegador no permite avisos. En iPhone, instala primero la app en la pantalla de inicio.');
 if(await Notification.requestPermission()!=='granted')throw new Error('No se concedió permiso. Puedes cambiarlo en los ajustes del navegador.');
 const registration=await navigator.serviceWorker.register('/portal/sw.js',{scope:'/portal/'});await navigator.serviceWorker.ready;
 deviceToken=await getToken(getMessaging(),{vapidKey:env.VITE_FIREBASE_VAPID_KEY,serviceWorkerRegistration:registration});await api('device',{token:deviceToken});await api('preferences',{notifications:true});
}
export async function compressPhoto(file:File){
 if(!['image/jpeg','image/png','image/webp'].includes(file.type))throw new Error('Selecciona una foto JPG, PNG o WebP. Si usas HEIC, expórtala como JPG.');
 if(file.size>20000000)throw new Error('La foto original debe pesar menos de 20 MB.');
 const bitmap=await createImageBitmap(file);try{if(bitmap.width*bitmap.height>80000000)throw new Error('La resolución de la foto es demasiado alta.');const scale=Math.min(1,1600/Math.max(bitmap.width,bitmap.height));const canvas=document.createElement('canvas');canvas.width=Math.round(bitmap.width*scale);canvas.height=Math.round(bitmap.height*scale);canvas.getContext('2d')!.drawImage(bitmap,0,0,canvas.width,canvas.height);
  let quality=.78;let blob:Blob|null=null;do{blob=await new Promise<Blob|null>(resolve=>canvas.toBlob(resolve,'image/webp',quality));quality-=.1;}while(blob&&blob.size>1000000&&quality>=.38);
  if(!blob||blob.size>1000000)throw new Error('No se pudo reducir la foto a menos de 1 MB.');
  const base64=await new Promise<string>((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.onerror=reject;reader.readAsDataURL(blob!);});return {base64,bytes:blob.size,original:file.size};
 }finally{bitmap.close();}
}

export function registrationDraft():{name:string;plate:string}|null{try{const d=JSON.parse(sessionStorage.getItem('portal-registration')||'null');return d?.email===auth?.currentUser?.email?.toLowerCase()?d:null;}catch{return null;}}
export function clearRegistrationDraft(){sessionStorage.removeItem('portal-registration');}
