// Maya-style gestures with explicit screen-space pan and independent dolly/FOV.
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
let targetOffset=[0,0,0],drag=null;
function currentCamera(){return cameraGeometry(+$('yaw').value,+$('pitch').value,+$('radius').value,DATA.target_depth,+$('zoom').value,targetOffset)}
function pose(y,p,r=+$('radius').value){$('yaw').value=clamp(y,-180,180);$('pitch').value=clamp(p,-90,90);$('radius').value=clamp(r,.2,5);render()}
function panPixels(dx,dy,c=currentCamera()){
 const units=c.orbit_radius/(canvas.clientWidth/640*c.projection.fx);
 targetOffset=targetOffset.map((v,i)=>v-(dx*c.right[i]+dy*c.down[i])*units);
 render();
}
function dolly(factor){$('radius').value=clamp(+$('radius').value*factor,.2,5);render()}
function resetView(){targetOffset=[0,0,0];$('zoom').value=1;pose(0,0,1)}
for(const id of ['yaw','pitch','radius','zoom','footprint'])$(id).addEventListener('input',render);
$('reset').onclick=resetView;$('near').onclick=()=>pose(15,8);$('extreme').onclick=()=>pose(70,10,1.3);
canvas.onpointerdown=e=>{
 if(e.pointerType==='mouse'&&e.button!==0&&e.button!==1&&e.button!==2)return;
 if(e.button===2&&!e.altKey)return;
 e.preventDefault();
 let mode=e.altKey&&e.button===2?'dolly':e.altKey&&e.button===0?'orbit':e.button===1||e.shiftKey?'pan':e.ctrlKey?'dolly':$('navigation-mode').value;
 drag={id:e.pointerId,x:e.clientX,y:e.clientY,mode};canvas.setPointerCapture(e.pointerId);
};
canvas.onpointermove=e=>{
 if(!drag||drag.id!==e.pointerId)return;
 const dx=e.clientX-drag.x,dy=e.clientY-drag.y;drag.x=e.clientX;drag.y=e.clientY;
 if(drag.mode==='pan')panPixels(dx,dy);
 else if(drag.mode==='dolly')dolly(Math.exp(-dx*.008));
 else orbitPixels(dx,dy);
};
canvas.onpointerup=canvas.onpointercancel=canvas.onlostpointercapture=()=>drag=null;
function orbitPixels(dx,dy){
 const sx=$('invert-orbit-x').checked?-1:1,sy=$('invert-orbit-y').checked?-1:1;
 pose(+$('yaw').value-dx*.2*sx,+$('pitch').value+dy*.2*sy);
}
canvas.oncontextmenu=e=>{if(e.altKey)e.preventDefault()};
canvas.addEventListener('wheel',e=>{
 e.preventDefault();const dy=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?canvas.clientHeight:1);
 if(e.shiftKey){$('zoom').value=clamp(+$('zoom').value*Math.exp(-dy*.001),.6,2);render()}
 else dolly(Math.exp(dy*.001));
},{passive:false});
canvas.onkeydown=e=>{
 const arrows={ArrowLeft:[-20,0],ArrowRight:[20,0],ArrowUp:[0,-20],ArrowDown:[0,20]};
 if(arrows[e.key]){e.preventDefault();if(e.shiftKey)panPixels(...arrows[e.key]);else orbitPixels(arrows[e.key][0]/2,arrows[e.key][1]/2)}
 else if(e.key==='+'||e.key==='='){e.preventDefault();dolly(.9)}
 else if(e.key==='-'){e.preventDefault();dolly(1/.9)}
 else if(e.key.toLowerCase()==='f'){e.preventDefault();resetView()}
};
$('pan-left').onclick=()=>panPixels(-30,0);$('pan-right').onclick=()=>panPixels(30,0);
$('pan-up').onclick=()=>panPixels(0,-30);$('pan-down').onclick=()=>panPixels(0,30);
$('dolly-in').onclick=()=>dolly(.9);$('dolly-out').onclick=()=>dolly(1/.9);
window.addEventListener('resize',render);
