"""Select a MANUAL camera brief; this does not generate an image or change a video."""
import argparse,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
def select(scene,choice,choices):
    result=json.loads(json.dumps(scene));result['camera']=choices[choice]
    result['reviewed']=False;result['guide_reviewed']=False
    result['camera_choice']=choice
    for obj in result['objects']:
        obj['visibility']='unknown'
        obj['uncertainty']='Re-evaluate visibility from this newly selected camera.'
    result['guide_review_notes']='Generate a new guide manually, inspect pose/background/occlusions/gesture margins, then review this sheet.'
    return result
def main():
    choices=json.loads((ROOT/'configs/camera_choices.json').read_text(encoding='utf8'))
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--list',action='store_true');p.add_argument('--scene');p.add_argument('--choice',choices=list(choices));p.add_argument('--out');a=p.parse_args()
    if a.list:print(json.dumps(choices,indent=2));return
    if not all([a.scene,a.choice,a.out]):p.error('--scene, --choice and --out are required unless --list is used')
    scene=json.loads(pathlib.Path(a.scene).read_text(encoding='utf8'))
    with pathlib.Path(a.out).open('x',encoding='utf8') as f:json.dump(select(scene,a.choice,choices),f,indent=2)
if __name__=='__main__':main()
