const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/../../ui/camera_picker.html','utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
assert(!/[\u00c2\u00c3\ufffd]/.test(html),'No broken UTF-8 text');
assert(html.includes('Regenerar instrucci\u00f3n'));assert(html.includes('\u00bfReemplazar'));
const e={};for(const id of ['az','el','dist','shot','notes','preview','azout','elout','distout','cam','ray','sidecam','side','file','save','status','regenerate'])e[id]={value:'',attributes:{},handlers:{},addEventListener(n,f){this.handlers[n]=f},setAttribute(n,v){this.attributes[n]=v}};
e.az.value='0';e.el.value='0';e.dist.value='1';e.shot.value='front';let saved,confirmation=false;
function mockElement(){return {value:'',attributes:{},handlers:{},addEventListener(n,f){this.handlers[n]=f},setAttribute(n,v){this.attributes[n]=v},removeAttribute(n){delete this.attributes[n]},appendChild(x){e[x.id]=x},click(){}};}
const ctx={document:{getElementById:id=>e[id]||(e[id]=mockElement()),createElement:()=>mockElement()},window:{confirm:()=>confirmation},Blob:class{constructor(parts){this.parts=parts}},URL:{createObjectURL(b){saved=JSON.parse(b.parts[0]);return'blob:test'},revokeObjectURL(){}},setTimeout(){}};
vm.createContext(ctx);vm.runInContext(js,ctx);vm.runInContext('scene={objects:[],acting:[]}',ctx);

function evaluate(s){return vm.runInContext(s,ctx)}
confirmation=true;
evaluate("loadScene({objects:[],acting:[],camera:'Exact loaded instruction',camera_choice:'rear',camera_parameters:{azimuth:180,elevation:20,distance:1.5},camera_notes:'Keep hands'})");
assert.equal(e.az.value,180);assert.equal(e.el.value,20);assert.equal(e.notes.value,'Keep hands');assert.equal(e.preview.value,'Exact loaded instruction');assert.equal(e.shot.value,'custom');
evaluate('loadScene({objects:[],acting:[]})');assert.equal(e.notes.value,'');assert.equal(e.az.value,0);assert.equal(e.dist.value,1);
e.shot.value='overhead';e.shot.handlers.change();e.save.handlers.click();assert(saved.camera.includes('do not tilt the head'));
e.el.value=10;e.el.handlers.input();assert.equal(e.shot.value,'custom');assert(!e.preview.value.includes('True overhead'));
e.notes.value='round trip note';e.notes.handlers.input();e.save.handlers.click();ctx.roundTrip=saved;evaluate('loadScene(roundTrip)');assert.equal(e.notes.value,'round trip note');assert.equal(e.preview.value,saved.camera);
e.preview.value='manual text';e.preview.handlers.input();confirmation=false;assert.equal(evaluate('loadScene({objects:[],acting:[]})'),false);assert.equal(e.preview.value,'manual text');
confirmation=true;assert.throws(()=>evaluate("loadScene({objects:[],acting:[],camera_parameters:{azimuth:'90',elevation:0,distance:1}})"));assert.equal(e.preview.value,'manual text');
console.log('PASS restore/reset, preset specifics, custom label, JSON round trip, cancelled load, invalid-load preservation.');
