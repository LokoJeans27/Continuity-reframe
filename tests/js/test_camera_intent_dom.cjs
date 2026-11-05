const fs=require('fs'),vm=require('vm'),assert=require('assert');
const synthetic=process.argv.includes('--synthetic');
const html=fs.readFileSync(__dirname+(synthetic?'/../../examples/camera_intent/ready/studio.html':'/../../ui/camera_intent/studio.html.template'),'utf8');
if(!synthetic){assert(!html.includes('57600'));assert(!/data:image\/\w+;base64,[A-Za-z0-9+/]{100}/.test(html));}
const values={yaw:'0',pitch:'0',radius:'1',zoom:'1',notes:'',intent:''},elements={};let confirm=false,saved;
const gl=new Proxy({getShaderParameter:()=>true,getProgramParameter:()=>true,getError:()=>0},{get:(o,k)=>o[k]||(k===k.toUpperCase()?1:()=>({}))});
const el=id=>elements[id]||(elements[id]={value:values[id]||'',checked:false,textContent:'',clientWidth:640,clientHeight:360,addEventListener(){},getContext:()=>gl,toDataURL:()=>'data:image/png;base64,TEST',setPointerCapture(){},click(){}});
const data={count:1,target_depth:2,buffer:Buffer.from(new Float32Array([0,0,2,1,0,0,.02,1]).buffer).toString('base64'),source:'TEST'};
const ctx={document:{getElementById:el,createElement:()=>({click(){}})},console,performance:{now:()=>1},atob:s=>Buffer.from(s,'base64').toString('binary'),Uint8Array,Float32Array,Blob:class{constructor(parts){saved=parts.join('')}},URL:{createObjectURL:()=>'',revokeObjectURL(){}},setTimeout(){},confirm:()=>confirm,addEventListener(){}};ctx.window=ctx;
vm.createContext(ctx);vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1].replace('__CAMERA_DATA__',JSON.stringify(data)),ctx);
const ev=s=>vm.runInContext(s,ctx);
for(const [yaw,pitch] of [[0,0],[-90,0],[90,0],[0,90],[25,15]]){ev(`pose(${yaw},${pitch})`);assert.equal(ev('getPackage().camera.elevation_degrees'),pitch);assert(ev('getPackage().prompt_matches_current_controls'));}
const prior=el('intent').value;el('intent').value='My preserved prompt';el('intent').oninput();ev('pose(0,90)');assert.equal(el('intent').value,'My preserved prompt');assert(!ev('getPackage().prompt_matches_current_controls'));
el('regenerate').onclick();assert.equal(el('intent').value,'My preserved prompt');confirm=true;el('regenerate').onclick();assert(ev('getPackage().prompt_matches_current_controls'));
el('intent').value=prior;el('intent').oninput();assert(!ev('getPackage().prompt_matches_current_controls'));
assert.equal(ev('getPackage().proxy'),null);el('include-proxy').checked=true;assert(ev('getPackage().proxy.data_url'));
el('save').onclick();const pack=JSON.parse(saved);assert.equal(pack.reviewed,false);assert.equal(pack.guide_reviewed,false);assert.equal(pack.automatically_sent,false);assert.equal(pack.prompt,'My preserved prompt'===el('intent').value?'My preserved prompt':prior);
console.log('PASS camera intent controls, manual edits, regeneration, optional proxy and export');
