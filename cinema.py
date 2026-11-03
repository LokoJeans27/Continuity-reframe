"""Local H3 cinema pilot. No hosted generation, deletes or file replacement."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, time, urllib.request, urllib.parse, uuid
import cv2
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))

def read(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))

def write(p, value):
    with pathlib.Path(p).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)

def digest(p):
    h = hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def copy_new(a, b):
    with pathlib.Path(a).open('rb') as src, pathlib.Path(b).open('xb') as dst:
        shutil.copyfileobj(src, dst)

def command(args):
    subprocess.run(args, check=True)

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)], text=True))

def api(base, path, data=None):
    u = urllib.parse.urlparse(base)
    if u.scheme != 'http' or u.hostname not in ('localhost','127.0.0.1','::1'):
        raise ValueError('Only a local HTTP ComfyUI server is supported.')
    req = urllib.request.Request(base.rstrip('/')+path, data=None if data is None else json.dumps(data).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)

def newdir(p):
    p = pathlib.Path(p).resolve(); p.mkdir(parents=True, exist_ok=False); return p

def prepare(a):
    source = pathlib.Path(a.video).resolve()
    info = probe(source); vs = next(s for s in info['streams'] if s['codec_type']=='video')
    if not any(s['codec_type']=='audio' for s in info['streams']): raise ValueError('Source must contain audio; silent-source support is not implemented.')
    if a.frames < 5 or (a.frames-5)%17: raise ValueError('H3 length must be 17k+5.')
    if a.frames < 124 and not a.pilot_short: raise ValueError('Below recommended124 frames. Explicit --pilot-short is required for this experimental short pilot.')
    if a.frames > 362 or a.width%32 or a.height%32 or min(a.width,a.height)<32: raise ValueError('Use length<=362 and dimensions divisible by32.')
    duration = a.frames/24
    if a.start < 0 or a.start+duration > float(info['format']['duration'])+.001: raise ValueError('Selected interval exceeds source duration.')
    indices = [int(x) for x in a.frames_at.split(',')] if a.frames_at else sorted(set(round(j*(a.frames-1)/6) for j in range(7)))
    if any(i<0 or i>=a.frames for i in indices): raise ValueError('Selected frame outside clip.')
    p = newdir(a.out); (p/'frames').mkdir(); (p/'original_frames').mkdir()
    vf = f'scale={a.width}:{a.height}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad={a.width}:{a.height}:(ow-iw)/2:(oh-ih)/2,fps=24'
    command(['ffmpeg','-n','-v','error','-ss',str(a.start),'-i',str(source),'-t',str(duration),'-vf',vf,'-frames:v',str(a.frames),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',str(p/'source.mp4')])
    command(['ffmpeg','-n','-v','error','-i',str(p/'source.mp4'),'-vn','-t',str(duration),'-ar','44100','-ac','2','-c:a','pcm_s16le',str(p/'audio.wav')])
    c = cv2.VideoCapture(str(p/'source.mp4')); original = cv2.VideoCapture(str(source)); rate = float(original.get(cv2.CAP_PROP_FPS)); records=[]; tiles=[]
    try:
        for i in range(a.frames):
            ok,f = c.read()
            if not ok: raise RuntimeError(f'Prepared clip ended at frame{i}')
            if i not in indices: continue
            fn = f'f{i:04d}_{i/24:.6f}s.png'; assert cv2.imwrite(str(p/'frames'/fn),f)
            oi = round((a.start+i/24)*rate); original.set(cv2.CAP_PROP_POS_FRAMES,oi); ok,of = original.read()
            if not ok: raise RuntimeError('Cannot extract original reference frame')
            ofn = f'original_f{oi:06d}_{oi/rate:.6f}s.png'; assert cv2.imwrite(str(p/'original_frames'/ofn),of)
            records.append({'prepared_frame':i,'clip_seconds':i/24,'requested_source_seconds':a.start+i/24,'original_frame':oi,'original_seconds_cfr':oi/rate,'original_png':ofn,'prepared_png':fn})
            tile = np.zeros((216,320,3),np.uint8); tile[24:]=cv2.resize(f,(320,192)); cv2.putText(tile,f'f{i}  {i/24:.3f}s',(8,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,255,255),1); tiles.append(tile)
    finally: c.release(); original.release()
    while len(tiles)%3: tiles.append(np.zeros_like(tiles[0]))
    assert cv2.imwrite(str(p/'contact.jpg'),np.vstack([np.hstack(tiles[j:j+3]) for j in range(0,len(tiles),3)]))
    write(p/'project.json',{'source_original':str(source),'source_original_sha256':digest(source),'prepared_sha256':digest(p/'source.mp4'),'start':a.start,'frames':a.frames,'fps':24,'width':a.width,'height':a.height,'duration':duration,'pilot_short':a.pilot_short,'original_fps':rate,'time_limit':'Original frame/time labels assume CFR. For VFR normalize separately and retain provenance.','audio':'AAC reencoded from source; comparisons later packet-copy this prepared AAC.'})
    write(p/'frame_manifest.json',records)
    write(p/'scene.template.json',{'schema_version':1,'reviewed':False,'guide_reviewed':False,'subject':'Describe performer identity using visible evidence','camera':'Describe target position, direction and framing','camera_fixed':True,'objects':[{'name':'example object','visibility':'unknown','relation':'Describe observed location without moving it','evidence_frames':[],'uncertainty':'Not established'}],'acting':[{'start':0,'end':duration,'action':'Describe source action and anatomical arm, gaze and timing'}],'guide_uncertainties':['Hidden geometry is not verified'],'guide_review_notes':'Check posture, occlusions, frame margins and anatomy before accepting guide.'})
    print('PREPARED',p,flush=True)

def scene_prompt(scene, duration):
    if scene.get('reviewed') is not True or scene.get('guide_reviewed') is not True: raise ValueError('Complete manual scene and guide review in a NEW scene JSON first.')
    allowed={'visible','partial','occluded','out_of_frame','unknown'}
    visible=[]; omitted=[]
    for item in scene['objects']:
        if item['visibility'] not in allowed: raise ValueError('Unknown visibility state')
        if item['visibility'] in ('visible','partial'):
            if not item.get('evidence_frames'): raise ValueError('Visible objects require evidence frame IDs')
            visible.append(item['name']+': '+item['relation'])
        else: omitted.append(item['name'])
    actions=[]
    for event in scene['acting']:
        if not 0<=event['start']<event['end']<=duration+.001: raise ValueError('Action timing outside selected clip')
        actions.append(f"[{event['start']:.3f}s-{event['end']:.3f}s] {event['action']}")
    camera_rule='Keep camera fixed without pans, tilts, zooms, cuts or return to source view.' if scene['camera_fixed'] else 'Follow only the camera motion explicitly described above.'
    prompt='\n'.join(['subject_definitions:',scene['subject']+' Video 1 provides identity and acting; Picture 1 defines target camera and initial frame.','summary:',scene['camera'],'retention_analysis:',camera_rule,'Preserve visible spatial relations without moving objects to make them appear.','Visible scene: '+'; '.join(visible),'detailed_description:']+actions+['Translate anatomical gestures into this view with natural occlusion. Do not freeze the initial pose or invent new actions.','overall_soundscape:','Follow original speech timing without added dialogue or effects.','non_diegetic_music:','None.'])
    return prompt,omitted

def build(a):
    p=pathlib.Path(a.project).resolve(); info=read(p/'project.json'); scene=read(a.scene); prompt,omitted=scene_prompt(scene,info['duration'])
    image=cv2.imread(str(a.guide))
    if image is None: raise ValueError('Guide image cannot be decoded')
    if (a.width is None)!=(a.height is None): raise ValueError('Specify both output width and height, or neither.')
    ow,oh=(a.width,a.height) if a.width is not None else (info['width'],info['height'])
    if ow<32 or oh<32 or ow%32 or oh%32: raise ValueError('Output dimensions must be positive multiples of32.')
    input_root=pathlib.Path(a.comfy_input).resolve()
    if not input_root.is_dir(): raise ValueError('Existing ComfyUI input directory required')
    run=newdir(a.out); token='cinema_'+uuid.uuid4().hex; stage=input_root
    w,h=ow,oh; scale=min(w/image.shape[1],h/image.shape[0]); iw,ih=round(image.shape[1]*scale),round(image.shape[0]*scale); canvas=np.zeros((h,w,3),np.uint8); x,y=(w-iw)//2,(h-ih)//2; canvas[y:y+ih,x:x+iw]=cv2.resize(image,(iw,ih),interpolation=cv2.INTER_AREA)
    assert cv2.imwrite(str(run/'guide.png'),canvas)
    for name,src in [('source.mp4',p/'source.mp4'),('audio.wav',p/'audio.wav'),('guide.png',run/'guide.png'),('reference_original.png',pathlib.Path(a.guide))]: copy_new(src,stage/(token+'_'+name))
    copy_new(a.scene,run/'scene.json')
    with (run/'prompt.txt').open('x',encoding='utf8') as f:f.write(prompt)
    graph=read(ROOT/'workflow.template.api.json')
    graph['50']['inputs']['file']=token+'_source.mp4'; graph['220']['inputs']['audio']=token+'_audio.wav'; graph['201']['inputs']['image']=token+'_guide.png'
    graph['202']['inputs']['image']=token+'_reference_original.png'
    graph['105']['inputs'].update(prompt=prompt,width=w,height=h,length=info['frames'],ref_image_size=a.ref_image_size); graph['15']['inputs']['noise_seed']=a.seed; graph['9']['inputs']['steps']=a.steps
    for node,label in [('92','native_audio'),('95','original_audio')]: graph[node]['inputs']['filename_prefix']=token+'/'+label
    write(run/'workflow.api.json',graph)
    from visual import make_visual
    write(run/'workflow.visual.json',make_visual(graph,read(ROOT/'workflow.visual.template.json')))
    write(run/'run.json',{'project':str(p),'stage':str(stage),'prefix':token,'server':a.server,'guide_original_sha256':digest(a.guide),'source_prepared_sha256':digest(p/'source.mp4'),'seed':a.seed,'steps':a.steps,'objects_omitted_from_prompt':omitted,'status':'built_not_submitted','manual_image_step':True,'output_width':w,'output_height':h,'ref_image_size':a.ref_image_size,'original_reference_separate':True})
    print('BUILT',run,flush=True)

def doctor(a):
    graph=read(ROOT/'workflow.template.api.json'); nodes=api(a.server,'/object_info'); missing=sorted({n['class_type'] for n in graph.values()}-set(nodes))
    models=[]
    for node,field in [('6','unet_name'),('11','vae_name'),('13','clip_name'),('24','vae_name')]:
        item=graph[node]; options=nodes.get(item['class_type'],{}).get('input',{}).get('required',{}).get(field,[[]])[0]; name=item['inputs'][field]
        models.append({'file':name,'listed':name in options})
    report={'missing_nodes':missing,'models':models,'ffmpeg':shutil.which('ffmpeg'),'ffprobe':shutil.which('ffprobe'),'python':sys.version,'opencv':cv2.__version__,'numpy':np.__version__,'server':a.server,'system_stats':api(a.server,'/system_stats')}
    write(a.out,report); print(json.dumps({'missing_nodes':missing,'models':models},indent=2))
    if missing or not all(x['listed'] for x in models) or not report['ffmpeg'] or not report['ffprobe']: raise RuntimeError('Dependencies missing; see doctor report. Nothing downloaded or installed.')

def submit(a):
    r=pathlib.Path(a.run).resolve(); info=read(r/'run.json'); server=info['server']
    if (r/'submission.json').exists() or (r/'submission_intent.json').exists(): raise ValueError('Submission already attempted. Use collect; do not resubmit an uncertain job.')
    q=api(server,'/queue')
    if q['queue_running'] or q['queue_pending']: raise RuntimeError('ComfyUI queue busy; no submission performed.')
    client=str(uuid.uuid4()); write(r/'submission_intent.json',{'client_id':client,'time':time.time(),'warning':'If connection is lost, inspect server queue/history before any new submission.'})
    response=api(server,'/prompt',{'prompt':read(r/'workflow.api.json'),'client_id':client})
    write(r/'submission.json',response); print('SUBMITTED',response.get('prompt_id'),flush=True)
    if 'prompt_id' not in response: raise RuntimeError(str(response))

def collect(a):
    r=pathlib.Path(a.run).resolve(); info=read(r/'run.json'); pid=read(r/'submission.json')['prompt_id']; start=time.monotonic()
    if (r/'result.json').exists(): raise ValueError('Result already collected; nothing replaced.')
    while True:
        h=api(info['server'],'/history/'+pid)
        if pid in h: break
        if time.monotonic()-start>=a.wait: print('PENDING',pid,flush=True); return
        time.sleep(min(5,a.wait-(time.monotonic()-start)))
    result=h[pid]
    if result['status']['status_str']!='success': write(r/'result.json',result); raise RuntimeError('ComfyUI reported failure; history preserved.')
    outroot=pathlib.Path(a.comfy_output).resolve(); copied=[]
    for node in ['92','95']:
        found=[]
        for values in result['outputs'][node].values():
            if isinstance(values,list): found += [v for v in values if isinstance(v,dict) and 'filename' in v]
        if len(found)!=1: raise RuntimeError('Ambiguous SaveVideo outputs; inspect history without resubmitting.')
        v=found[0]; src=(outroot/v.get('subfolder','')/v['filename']).resolve()
        if not src.is_relative_to(outroot): raise ValueError('Output path leaves selected ComfyUI output root')
        dst=r/('native_audio.mp4' if node=='92' else 'original_audio.mp4')
        if dst.is_symlink():
            raise ValueError(f'Symlink destination refused; no files changed: {dst}')
        source_hash=digest(src)
        if dst.exists():
            if not dst.is_file() or digest(dst)!=source_hash:
                raise FileExistsError(f'Existing collected file differs from server output; preserved without changes: {dst}')
        else:
            copy_new(src,dst)
            if digest(dst)!=source_hash:
                raise RuntimeError(f'Collected copy failed integrity check; retained for inspection: {dst}')
        copied.append({'node':node,'file':dst.name,'sha256':source_hash})
    write(r/'result.json',{'history':result,'files':copied}); print('COLLECTED',r,flush=True)

def compare(a):
    r=pathlib.Path(a.run).resolve(); run=read(r/'run.json'); p=pathlib.Path(run['project']); info=read(p/'project.json'); n=info['frames']
    if not (r/'result.json').is_file(): raise ValueError('Collection not complete. Repeat collect until COLLECTED before compare; no comparison folder created.')
    result=read(r/'result.json')
    if result.get('history',{}).get('status',{}).get('status_str')!='success': raise ValueError('No successful collected result; comparison not started.')
    recorded={x['file']:x['sha256'] for x in result.get('files',[])}
    for name in ['native_audio.mp4','original_audio.mp4']:
        f=r/name
        if not f.is_file() or name not in recorded or digest(f)!=recorded[name]: raise ValueError('Collected video missing or hash differs: '+name+'; no comparison folder created.')
        check=cv2.VideoCapture(str(f))
        try:
            ok,_=check.read()
            if not check.isOpened() or not ok: raise ValueError('Collected video cannot be decoded: '+name)
        finally: check.release()
    source=p/'source.mp4'; guide=cv2.imread(str(r/'guide.png')); caps=[cv2.VideoCapture(str(x)) for x in [source,r/'original_audio.mp4']]
    if guide is None or any(not c.isOpened() for c in caps):
        for c in caps:c.release()
        raise ValueError('Source video or guide cannot be opened; no comparison folder created.')
    try: o=newdir(r/'comparison')
    except Exception:
        for c in caps:c.release()
        raise
    raw=o/'silent_preserved.mp4'; writer=cv2.VideoWriter(str(raw),cv2.VideoWriter_fourcc(*'mp4v'),24,(1920,420)); assert writer.isOpened(); tiles=[]
    try:
        for i in range(n):
            ims=[]
            for c in caps:
                ok,f=c.read()
                if not ok: raise RuntimeError('Frame count mismatch')
                ims.append(f)
            row=np.zeros((420,1920,3),np.uint8)
            for j,(f,label) in enumerate(zip([ims[0],guide,ims[1]],['SOURCE','MANUAL GUIDE','H3 RESULT'])):
                row[36:,j*640:(j+1)*640]=cv2.resize(f,(640,384));cv2.putText(row,f'{label} | f{i} {i/24:.3f}s',(j*640+10,25),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),1)
            writer.write(row)
            tile=cv2.resize(row,(960,210)); tiles.append(tile)
            if len(tiles)==6 or i==n-1:
                assert cv2.imwrite(str(o/f'frames_ending_{i:04d}.jpg'),np.vstack(tiles)); tiles=[]
        if any(c.read()[0] for c in caps): raise RuntimeError('Unexpected extra frames')
    finally:
        writer.release()
        for c in caps:c.release()
    dst=o/'comparison.mp4'; command(['ffmpeg','-n','-v','error','-i',str(raw),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-shortest',str(dst)])
    hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(x),'-map','0:a:0','-c','copy','-f','hash','-'],text=True).strip() for x in [source,dst]]
    write(o/'verification.json',{'frames':n,'fps':24,'audio_hashes':hashes,'audio_packets_identical_to_prepared':hashes[0]==hashes[1],'visual_review':'MANUAL_NOT_YET_PERFORMED','limits':'Audio identity here is to prepared AAC, not original complete file; not lipsync validation.'})
    if hashes[0]!=hashes[1]: raise RuntimeError('Audio packet hash mismatch')
    print('COMPARISON_READY',dst,flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    x=sub.add_parser('prepare');x.add_argument('--video',required=True);x.add_argument('--out',required=True);x.add_argument('--start',type=float,default=0);x.add_argument('--frames',type=int,default=124);x.add_argument('--width',type=int,default=640);x.add_argument('--height',type=int,default=384);x.add_argument('--frames-at');x.add_argument('--pilot-short',action='store_true');x.set_defaults(fn=prepare)
    x=sub.add_parser('build');x.add_argument('--project',required=True);x.add_argument('--scene',required=True);x.add_argument('--guide',required=True);x.add_argument('--comfy-input',required=True);x.add_argument('--out',required=True);x.add_argument('--server',default='http://127.0.0.1:8188');x.add_argument('--seed',type=int,default=18840101);x.add_argument('--steps',type=int,default=20);x.add_argument('--width',type=int);x.add_argument('--height',type=int);x.add_argument('--ref-image-size',choices=['match','max'],default='max');x.set_defaults(fn=build)
    x=sub.add_parser('doctor');x.add_argument('--server',default='http://127.0.0.1:8188');x.add_argument('--out',required=True);x.set_defaults(fn=doctor)
    x=sub.add_parser('submit');x.add_argument('--run',required=True);x.set_defaults(fn=submit)
    x=sub.add_parser('collect');x.add_argument('--run',required=True);x.add_argument('--comfy-output',required=True);x.add_argument('--wait',type=int,default=50,choices=range(0,56));x.set_defaults(fn=collect)
    x=sub.add_parser('compare');x.add_argument('--run',required=True);x.set_defaults(fn=compare)
    a=p.parse_args();a.fn(a)

if __name__=='__main__': main()
