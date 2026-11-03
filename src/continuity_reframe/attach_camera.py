"""Create a NEW run with the optional camera text node. No execution or installation."""
from pathlib import Path
import argparse,json,uuid,shutil
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):
    with p.open('x',encoding='utf8') as f:json.dump(x,f,indent=2)
def attach(api,ui,controls):
    api=json.loads(json.dumps(api));ui=json.loads(json.dumps(ui));key=str(max(int(x) for x in api)+1)
    if isinstance(api['105']['inputs']['prompt'],list):raise ValueError('Prompt already linked; inspect it instead of replacing it')
    params={'base_prompt':api['105']['inputs']['prompt'],**controls};api[key]={'class_type':'H3ManualCameraBrief','inputs':params};api['105']['inputs']['prompt']=[key,0]
    target=next(n for n in ui['nodes'] if n['id']==105);lid=max(l[0] for l in ui['links'])+1
    if any(x['name']=='prompt' for x in target['inputs']):raise ValueError('Prompt already has a visual input')
    slot=len(target['inputs']);target['inputs'].append({'name':'prompt','type':'STRING','link':lid,'widget':{'name':'prompt'}})
    ui['nodes'].append({'id':int(key),'type':'H3ManualCameraBrief','pos':[750,1300],'size':[700,650],'flags':{},'order':0,'mode':0,'inputs':[],'outputs':[{'name':'camera_prompt','type':'STRING','links':[lid],'slot_index':0}],'properties':{'Node name for S&R':'H3ManualCameraBrief'},'widgets_values':list(params.values()),'widgets_values_named':params,'title':'MANUAL CAMERA BRIEF - guide image remains external'})
    ui['links'].append([lid,int(key),0,105,slot,'STRING']);ui['last_node_id']=int(key);ui['last_link_id']=lid
    return api,ui
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',required=True);p.add_argument('--out',required=True);p.add_argument('--use-angle-brief',action='store_true');p.add_argument('--guide-reviewed',action='store_true');p.add_argument('--preset',default='custom',choices=['custom','frontal','three_quarter','lateral','overhead','low','rear','wide']);p.add_argument('--azimuth',type=float,default=45);p.add_argument('--elevation',type=float,default=0);p.add_argument('--distance',type=float,default=1);p.add_argument('--notes',default='');a=p.parse_args()
    if a.use_angle_brief and not a.guide_reviewed:p.error('Review a guide for these controls, then pass --guide-reviewed. This tool creates no image.')
    r=Path(a.run).resolve();o=Path(a.out).resolve();o.mkdir(parents=True,exist_ok=False)
    params={'use_angle_brief':a.use_angle_brief,'preset':a.preset,'azimuth':a.azimuth,'elevation':a.elevation,'distance':a.distance,'notes':a.notes,'guide_reviewed_for_this_camera':a.guide_reviewed}
    g,ui=attach(read(r/'workflow.api.json'),read(r/'workflow.visual.json'),params);prefix='camera_'+uuid.uuid4().hex
    for node,label in [('92','native_audio'),('95','original_audio')]:
        value=prefix+'/'+label;g[node]['inputs']['filename_prefix']=value;n=next(n for n in ui['nodes'] if n['id']==int(node));i=list(n['widgets_values_named']).index('filename_prefix');n['widgets_values_named']['filename_prefix']=value;n['widgets_values'][i]=value
    meta=read(r/'run.json');meta['prefix']=prefix;meta['status']='built_not_submitted';meta['camera_controls']=params
    save(o/'workflow.api.json',g);save(o/'workflow.visual.json',ui);save(o/'run.json',meta)
    for name in ['guide.png','scene.json','prompt.txt']:
        with (r/name).open('rb') as f,(o/name).open('xb') as h:shutil.copyfileobj(f,h)
    print(o)
if __name__=='__main__':main()
