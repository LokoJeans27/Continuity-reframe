"""Offline build contract tests with synthetic fixtures; no inference or deletion."""
from pathlib import Path
import sys,tempfile,json,cv2,numpy as np
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import cinema,visual
def main():
    root=Path(tempfile.mkdtemp(prefix='h3_final_options_'));project=root/'project';project.mkdir();inputs=root/'input';inputs.mkdir()
    (project/'source.mp4').write_bytes(b'SYNTHETIC COPY FIXTURE - not a decodable video');(project/'audio.wav').write_bytes(b'SYNTHETIC COPY FIXTURE - not decodable audio')
    cinema.write(project/'project.json',{'frames':90,'duration':3.75,'width':64,'height':64})
    scene={'reviewed':True,'guide_reviewed':True,'subject':'Test subject','camera':'Test camera','camera_fixed':True,'objects':[],'acting':[{'start':0,'end':3.75,'action':'Test movement'}]};cinema.write(root/'scene.json',scene)
    guide=root/'original.png';assert cv2.imwrite(str(guide),np.arange(91*137*3,dtype=np.uint8).reshape(91,137,3))
    args=SimpleNamespace(project=str(project),scene=str(root/'scene.json'),guide=str(guide),comfy_input=str(inputs),out=str(root/'run'),server='http://127.0.0.1:8188',seed=1,steps=20,width=96,height=64,ref_image_size='max')
    cinema.build(args);g=cinema.read(root/'run/workflow.api.json');u=cinema.read(root/'run/workflow.visual.json')
    assert not visual.verify_visual(g,u)
    assert cinema.digest(inputs/g['202']['inputs']['image'])==cinema.digest(guide)
    assert cv2.imread(str(inputs/g['201']['inputs']['image'])).shape[:2]==(64,96)
    assert g['105']['inputs']['ref_image_size']=='max' and g['105']['inputs']['ref_images.ref_image_1']==['202',0]
    assert (inputs/g['50']['inputs']['file']).read_bytes()==(project/'source.mp4').read_bytes()
    before=(root/'run/workflow.api.json').read_bytes()
    try:cinema.build(args)
    except FileExistsError:pass
    else:raise AssertionError('Existing run was overwritten')
    assert (root/'run/workflow.api.json').read_bytes()==before
    args.out=str(root/'bad');args.height=None
    try:cinema.build(args)
    except ValueError:pass
    else:raise AssertionError('Incomplete size accepted')
    assert not (root/'bad').exists()
    print('PASS: original reference bytes, separate resized anchor, independent output dimensions, source copy, visual links, overwrite refusal, incomplete-size guard. Synthetic structural test; no media inference. Retained:',root)
if __name__=='__main__':main()
