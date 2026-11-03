const fs=require('fs'),vm=require('vm'),assert=require('assert');
function load(path){
 const html=fs.readFileSync(path,'utf8'),js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
 const elements={};for(const id of ['az','el','dist','shot','notes','preview','azout','elout','distout','cam','ray','sidecam','side','file','save','status','regenerate'])elements[id]={value:'',attributes:{},handlers:{},addEventListener(n,f){this.handlers[n]=f},setAttribute(n,v){this.attributes[n]=v}};
 Object.assign(elements.az,{value:'0'});elements.el.value='0';elements.dist.value='1';elements.shot.value='front';
 let answer=false,confirms=0,saved;
 const ctx={document:{getElementById:id=>elements[id],createElement:()=>({click(){}})},window:{confirm(){confirms++;return answer}},URL:{createObjectURL(blob){saved=JSON.parse(blob.parts[0]);return 'blob:test'},revokeObjectURL(){}},Blob:class{constructor(parts){this.parts=parts}},setTimeout(){},console};
 vm.createContext(ctx);vm.runInContext(js,ctx);
 return {ctx,e:elements,setAnswer:x=>answer=x,confirms:()=>confirms,saved:()=>saved};
}
const original=load(__dirname+'/fixtures/camera_picker_before_fix.html');
original.e.preview.value='MI TEXTO MANUAL';original.e.az.value='35';original.e.az.handlers.input();
assert.notEqual(original.e.preview.value,'MI TEXTO MANUAL');console.log('REPRODUCED: prior version silently loses manual text.');
const path=process.argv[2]||__dirname+'/../../ui/camera_picker.html',t=load(path),e=t.e;
e.az.value='35';e.az.handlers.input();assert(e.preview.value.includes('azimuth 35'));
const manual='Mi instrucción: mantener la mano visible.\nTexto propio con acentos.';e.preview.value=manual;
for(const [id,value] of [['az','52'],['el','25'],['dist','1.8'],['notes','Nuevas notas']]){e[id].value=value;e[id].handlers.input();assert.equal(e.preview.value,manual,id);}
e.shot.value='rear';e.shot.handlers.change();assert.equal(e.preview.value,manual);assert(e.status.textContent.includes('se conserva'));
e.regenerate.handlers.click();assert.equal(t.confirms(),1);assert.equal(e.preview.value,manual,'cancel keeps text');
vm.runInContext('scene={objects:[{visibility:"visible"}],acting:[],reviewed:true,guide_reviewed:true}',t.ctx);
e.save.handlers.click();assert.equal(t.saved().camera,manual);assert.equal(t.saved().camera_instruction_source,'manual');assert.equal(t.saved().camera_controls_match_instruction,false);assert.equal(t.saved().reviewed,false);
t.setAnswer(true);e.regenerate.handlers.click();assert.equal(t.confirms(),2);assert(e.preview.value.includes('azimuth 180'));assert(e.preview.value.includes('Nuevas notas'));
e.az.value='20';e.az.handlers.input();assert(e.preview.value.includes('azimuth 20'),'automatic updates resume after explicit regeneration');
e.save.handlers.click();assert.equal(t.saved().camera_instruction_source,'generated');assert.equal(t.saved().camera_controls_match_instruction,true);
for(const preset of ['front','three_quarter','lateral','wide','overhead','floor','rear']){e.shot.value=preset;e.shot.handlers.change();assert(Number.isFinite(Number(e.cam.attributes.cx)));}
console.log('PASS: sliders, notes and presets preserve manual text; cancel/confirm regeneration; exported text and provenance; automatic mode and seven presets. DOM harness; browser visual acceptance pending.');
