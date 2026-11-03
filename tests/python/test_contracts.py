"""Offline behavioral checks. Uses a new retained temporary directory; deletes nothing."""
from pathlib import Path
import sys,json,tempfile,copy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import cinema,visual,choose_camera

def rejects(fn):
    try:fn()
    except (ValueError,FileExistsError):return
    raise AssertionError('Unsafe/invalid operation was accepted')

def main():
    r=Path(tempfile.mkdtemp(prefix='h3_contracts_'));checks=[]
    s={'reviewed':True,'guide_reviewed':True,'subject':'A performer','camera':'Fixed lateral','camera_fixed':True,'objects':[{'name':'VISIBLE_MARKER','visibility':'visible','relation':'beside actor','evidence_frames':['f0000']},{'name':'EXCLUDED_MARKER','visibility':'out_of_frame','relation':'outside','evidence_frames':[]}],'acting':[{'start':0,'end':1,'action':'Raises right arm'}]}
    p,omitted=cinema.scene_prompt(s,1);assert 'VISIBLE_MARKER' in p and 'EXCLUDED_MARKER' not in p and omitted==['EXCLUDED_MARKER'];checks.append('Visibility controls prompt object ingredients')
    bad=copy.deepcopy(s);bad['guide_reviewed']=False;rejects(lambda:cinema.scene_prompt(bad,1));checks.append('Unreviewed guide rejected')
    bad=copy.deepcopy(s);bad['objects'][0]['evidence_frames']=[];rejects(lambda:cinema.scene_prompt(bad,1));checks.append('Visible object without evidence rejected')
    bad=copy.deepcopy(s);bad['acting'][0]['end']=2;rejects(lambda:cinema.scene_prompt(bad,1));checks.append('Out-of-clip action rejected')
    q=r/'preserve.json';cinema.write(q,{'original':1});rejects(lambda:cinema.write(q,{'replacement':2}));assert cinema.read(q)=={'original':1};checks.append('Overwrite refused; original bytes preserved')
    g=cinema.read(ROOT/'workflows/workflow.template.api.json');ui=visual.make_visual(g,cinema.read(ROOT/'workflows/workflow.visual.template.json'));assert visual.verify_visual(g,ui)==[]
    broken=copy.deepcopy(ui);n=next(n for n in broken['nodes'] if n['id']==105);next(x for x in n['inputs'] if x['name']=='ref_images.ref_image_0')['link']=None;assert visual.verify_visual(g,broken);checks.append('Missing dynamic reference detected')
    choices=cinema.read(ROOT/'configs/camera_choices.json');changed=choose_camera.select(s,'rear',choices);assert not changed['reviewed'] and not changed['guide_reviewed'] and all(o['visibility']=='unknown' for o in changed['objects']);checks.append('Camera change invalidates previous visibility/review')
    cinema.write(r/'results.json',{'passed':checks});print(json.dumps({'passed':checks,'retained_test_directory':str(r)},indent=2))
if __name__=='__main__':main()
