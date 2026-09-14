import { defineConfig, loadEnv } from 'vite';
import { resolve } from 'node:path';
export default defineConfig(({mode}) => ({
  publicDir: false,
  build: {outDir:'dist',emptyOutDir:false,rollupOptions:{input:resolve('portal/index.html')}},
  plugins:[{name:'local-api',configureServer(server){
    Object.assign(process.env,loadEnv(mode,process.cwd(),''));
    server.middlewares.use('/api',async(req,res,next)=>{
      const endpoint=(req.url||'').split('?')[0];
      if(!['/portal','/photo','/wompi','/reminders'].includes(endpoint)){next();return;}
      try { const {default:handler}=await server.ssrLoadModule(`/api${endpoint}.ts`); await handler(req,res); }
      catch {res.statusCode=500;res.setHeader('Content-Type','application/json');res.end(JSON.stringify({error:'No se pudo procesar la solicitud.'}));}
    });
  }}]
}));
