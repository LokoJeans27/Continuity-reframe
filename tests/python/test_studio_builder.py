import base64,importlib.util,json,os,struct,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('builder',root/'ui/camera_intent/build_studio.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
work=Path(os.environ.get('TEMP',os.environ.get('TMP','.')))/('continuity-builder-test-'+uuid.uuid4().hex);work.mkdir()
data={'count':1,'target_depth':2,'buffer':base64.b64encode(struct.pack('<8f',0,0,2,1,0,0,.02,1)).decode(),'ignored_private_path':'DO_NOT_EXPORT'}
(work/'proxy.json').write_text(json.dumps(data));(work/'frame.jpg').write_bytes(b'\xff\xd8\xff\xe0TEST\xff\xd9')
m.build(work/'proxy.json',work/'frame.jpg',work/'viewer.html');s=(work/'viewer.html').read_text(encoding='utf8');assert '__CAMERA_DATA__' not in s and 'DO_NOT_EXPORT' not in s
try:m.build(work/'proxy.json',work/'frame.jpg',work/'viewer.html');raise AssertionError('overwrote existing output')
except FileExistsError:pass
data['count']=2;(work/'bad.json').write_text(json.dumps(data))
try:m.build(work/'bad.json',work/'frame.jpg',work/'bad.html');raise AssertionError('accepted mismatched buffer')
except ValueError:pass
assert not (work/'bad.html').exists()
print('PASS builder validation, privacy field whitelist and no overwrite; test artifacts retained')
