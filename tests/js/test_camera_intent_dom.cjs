const fs=require('fs'),vm=require('vm'),assert=require('assert');
const synthetic=process.argv.includes('--synthetic');
const html=fs.readFileSync(__dirname+(synthetic?'/../../examples/camera_intent/ready/studio.html':'/../../ui/camera_intent/studio.html.template'),'utf8');
for(const name of ['camera_math.js','navigation.js'])assert(html.includes(fs.readFileSync(__dirname+'/../../ui/camera_intent/'+name,'utf8').replaceAll('\r\n','\n').trim()),'Embedded module matches '+name);
if(!synthetic){assert(!/data:image\/\w+;base64,[A-Za-z0-9+/]{100}/.test(html));}
const values={yaw:'0',pitch:'0',radius:'1',zoom:'1',footprint:'1','navigation-mode':'orbit',notes:'',intent:''},elements={};let confirm=false,saved;
const gl=new Proxy({getShaderParameter:()=>true,getProgramParameter:()=>true,getError:()=>0},{get:(o,k)=>o[k]||(k===k.toUpperCase()?1:()=>({}))});
const el=id=>elements[id]||(elements[id]={value:values[id]||'',checked:false,textContent:'',clientWidth:640,clientHeight:360,handlers:{},addEventListener(n,f){this.handlers[n]=f},getContext:()=>gl,toDataURL:()=>'data:image/png;base64,TEST',setPointerCapture(){},click(){}});
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
const canvas=el('view'),event=(extra={})=>({pointerId:1,pointerType:'mouse',button:0,clientX:100,clientY:100,altKey:false,ctrlKey:false,shiftKey:false,preventDefault(){},...extra});
function drag(extra,dx,dy){canvas.onpointerdown(event(extra));canvas.onpointermove(event({clientX:100+dx,clientY:100+dy}));canvas.onpointerup();}
ev('resetView()');drag({altKey:true},50,20);assert.equal(+el('yaw').value,-10);assert.equal(+el('pitch').value,4);
el('invert-orbit-x').checked=true;ev('resetView()');drag({altKey:true},50,20);assert.equal(+el('yaw').value,10);assert.equal(+el('pitch').value,4);
el('invert-orbit-x').checked=false;el('invert-orbit-y').checked=true;ev('resetView()');drag({altKey:true},50,20);assert.equal(+el('yaw').value,-10);assert.equal(+el('pitch').value,-4);el('invert-orbit-y').checked=false;
for(const [yaw,pitch] of [[0,0],[90,0],[25,80],[0,90]]){
 ev(`resetView();pose(${yaw},${pitch})`);const before=ev('currentCamera()');drag({altKey:true,button:1},30,20);const after=ev('currentCamera()');
 for(let i=0;i<3;i++)assert(Math.abs((after.position[i]-before.position[i])-(after.target[i]-before.target[i]))<1e-9);
 const cam=after.world_to_camera.slice(0,3).map(row=>row.slice(0,3).reduce((s,n,i)=>s+n*before.target[i],row[3]));assert(Math.abs(cam[0]*after.projection.fx/cam[2]-30)<1e-8);assert(Math.abs(cam[1]*after.projection.fy/cam[2]-20)<1e-8);
}
ev('resetView()');const preDolly=ev('currentCamera()');drag({altKey:true,button:2},50,0);const postDolly=ev('currentCamera()');assert(postDolly.relative_distance<1);assert.equal(postDolly.projection.fx,preDolly.projection.fx);assert.deepEqual(postDolly.target,preDolly.target);
let radius=+el('radius').value;canvas.handlers.wheel(event({deltaY:100,deltaMode:0}));assert(+el('radius').value>radius);radius=+el('radius').value;canvas.handlers.wheel(event({deltaY:-100,deltaMode:0,shiftKey:true}));assert.equal(+el('radius').value,radius);assert(+el('zoom').value>1);
ev('resetView()');el('navigation-mode').value='pan';drag({},20,0);assert(ev('currentCamera().target_offset[0]')<0);el('navigation-mode').value='dolly';drag({},20,0);assert(+el('radius').value<1);el('navigation-mode').value='orbit';
canvas.onkeydown(event({key:'F'}));assert.equal(+el('radius').value,1);assert.equal(+el('zoom').value,1);assert.equal(ev('currentCamera().target_offset.join()'),'0,0,0');canvas.onkeydown(event({key:'ArrowRight',shiftKey:true}));assert(ev('currentCamera().target_offset[0]')<0);
el('save').onclick();const movedPack=JSON.parse(saved);assert.deepEqual(movedPack.camera.position,JSON.parse(JSON.stringify(ev('currentCamera().position'))));assert.deepEqual(movedPack.camera.target,JSON.parse(JSON.stringify(ev('currentCamera().target'))));assert.equal(movedPack.navigation_version,2);
ctx.devicePixelRatio=2;ev('render()');assert.equal(canvas.width,1280);assert.equal(canvas.height,720);assert.equal(ctx.viewerState.device_pixel_ratio,2);
console.log('PASS both orbit axes/inversion, Maya bindings, screen-following pan at 4 views, dolly vs zoom, trackpad, keyboard, export and DPR');
