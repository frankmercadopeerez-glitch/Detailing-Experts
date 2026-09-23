import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {initializeApp,cert} from 'firebase-admin/app';
import {getFirestore} from 'firebase-admin/firestore';
import {createHash} from 'node:crypto';
const restore=process.argv[2]==='restore-emulator';
if(restore&&process.env.FIRESTORE_EMULATOR_HOST!=='127.0.0.1:8087')throw Error('La restauración solo está permitida en el emulador local 127.0.0.1:8087.');
if(!restore&&process.env.FIRESTORE_EMULATOR_HOST)throw Error('Elimina FIRESTORE_EMULATOR_HOST para generar una copia de producción.');
const app=restore?initializeApp({projectId:'demo-detailing-experts'}):initializeApp({credential:cert(JSON.parse(readFileSync('credentials/firebase-admin.json','utf8')))});
const db=getFirestore(app);
try{
 if(restore){const file=process.argv[3];if(!file)throw Error('Indica el archivo de copia.');const backup=JSON.parse(readFileSync(file,'utf8'));if(backup.format!==1)throw Error('Formato inválido');let count=0;for(const [collection,docs] of Object.entries(backup.collections) as [string,any[]][]){if(!/^[a-zA-Z_]+$/.test(collection))throw Error('Colección inválida');for(let i=0;i<docs.length;i+=400){const batch=db.batch();for(const d of docs.slice(i,i+400)){if(typeof d.id!=='string'||d.id.includes('/'))throw Error('ID inválido');batch.set(db.collection(collection).doc(d.id),d.data);count++;}await batch.commit();}}console.log(`Restauración verificada en emulador: ${count} documentos.`);
 }else{const backup:any={format:1,createdAt:new Date().toISOString(),collections:{},limits:'No incluye Firebase Authentication ni los archivos binarios de ImageKit.'};for(const collection of await db.listCollections()){const snap=await collection.get();backup.collections[collection.id]=snap.docs.map(d=>({id:d.id,data:d.data()}));}mkdirSync('credentials/backups',{recursive:true});const path=`credentials/backups/portal-${Date.now()}.json`,content=JSON.stringify(backup,null,2);writeFileSync(path,content,{mode:0o600});writeFileSync(path+'.sha256',createHash('sha256').update(content).digest('hex'));console.log(`Copia privada guardada: ${path}. Colecciones: ${Object.keys(backup.collections).length}.`);}
}finally{await db.terminate();}
