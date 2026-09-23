import {readdir,readFile,stat,writeFile,mkdir} from 'node:fs/promises';
import {resolve,relative,dirname} from 'node:path';
const base=resolve('dist'),issues=[];let pages=0,links=0,schemas=0;
async function exists(p){try{return (await stat(p)).isFile();}catch{return false;}}
async function walk(dir){for(const name of await readdir(dir)){const file=resolve(dir,name);if((await stat(file)).isDirectory()){await walk(file);continue;}if(!name.endsWith('.html'))continue;pages++;const html=await readFile(file,'utf8'),route=relative(base,file).replaceAll('\\','/');
 const report=message=>issues.push({route,message});
 if(!route.startsWith('portal/')){if((html.match(/<h1\b/gi)||[]).length!==1)report('Expected one H1');if(!/<title>[^<]+<\/title>/i.test(html))report('Missing title');if(!/<meta[^>]+name=["']description["']/i.test(html))report('Missing description');if(route!=='404.html'&&!/rel=["']canonical["']/i.test(html))report('Missing canonical');}
 for(const m of html.matchAll(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)){schemas++;try{JSON.parse(m[1]);}catch{report('Invalid JSON-LD');}}
 for(const m of html.matchAll(/\b(?:href|src)=["']([^"']+)["']/gi)){let value=m[1].split('?')[0].split('#')[0];if(!value||/^(?:[a-z]+:|\/\/)/i.test(value))continue;links++;try{value=decodeURIComponent(value);}catch{report('Invalid URL '+value);continue;}let target=value.startsWith('/')?resolve(base,'.'+value):resolve(dirname(file),value);if(await exists(target)||await exists(resolve(target,'index.html')))continue;if(value==='/portal'||value==='/portal/admin')continue;report('Missing local target '+value);}
 }}
await walk(base);await mkdir('test-results',{recursive:true});const result={pages,links,schemas,issues};await writeFile('test-results/public-audit.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));if(issues.length)process.exitCode=1;
