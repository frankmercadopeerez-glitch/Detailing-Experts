import {readFile,writeFile,readdir} from 'node:fs/promises';
async function walk(dir){for(const e of await readdir(dir,{withFileTypes:true})){if(e.name.startsWith('.')||['node_modules','dist','server','api','tests'].includes(e.name))continue;const p=`${dir}/${e.name}`;if(e.isDirectory())await walk(p);else if(/\.(html|xml|txt)$/.test(p)){const old=await readFile(p,'utf8');const updated=old.replaceAll('https://detailingexperts.com','https://detailing-experts.vercel.app');if(updated!==old)await writeFile(p,updated);}}}
await walk('.');
const path='js/components.js';let js=await readFile(path,'utf8');
if(!js.includes('Ingresar al portal')){
 js=js.replace('<div class="nav__actions">','<div class="nav__actions">\n      <a href="/portal/" class="nav__portal" aria-label="Ingresar al portal de clientes">Ingresar al portal</a>');
 js=js.replace('<div class="nav__mobile" id="mobile-nav" role="dialog" aria-modal="true" aria-label="Menú móvil">','<div class="nav__mobile" id="mobile-nav" role="dialog" aria-modal="true" aria-label="Menú móvil">\n  <a href="/portal/" class="nav__mobile-link">Ingresar al portal</a>');
 await writeFile(path,js);
 for(const file of ['css/style.css','css/style.min.css'])await writeFile(file,(await readFile(file,'utf8'))+'\n.nav__portal{color:#fff;text-decoration:none;border:1px solid #ffffff55;border-radius:5px;padding:10px 14px;font-size:12px;white-space:nowrap}.nav__portal:focus-visible{outline:3px solid #fff;outline-offset:3px}@media(max-width:1100px){.nav__actions .nav__portal{display:none}}\n');
}
console.log('Local links point to the verified Vercel domain. Public site remains informational.');
