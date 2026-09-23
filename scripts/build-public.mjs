import {mkdir,cp,readFile,writeFile,readdir,rm} from 'node:fs/promises';
import {resolve} from 'node:path';
const out=resolve('dist');
if(out!==resolve(process.cwd(),'dist'))throw new Error('Invalid build target');
await rm(out,{recursive:true,force:true}); await mkdir(out,{recursive:true});
for(const name of await readdir('.')) {
 if(/\.(html|xml|txt)$/.test(name) || ['images','css','js','servicios','blog','manifest.json','favicon.png'].includes(name)) await cp(name,`${out}/${name}`,{recursive:true});
}
await mkdir(`${out}/portal`,{recursive:true});
for(const name of ['manifest.webmanifest','sw.js','offline.html','icon.svg','privacidad.html'])await cp(`portal/${name}`,`${out}/portal/${name}`);
// Only public assets enter dist; server code, rules and credentials are never copied.
console.log('Public site and portal assets prepared. No deployment performed.');
