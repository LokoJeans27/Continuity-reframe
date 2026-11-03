"""Offline regressions; all fixtures are retained and no model is called."""
from pathlib import Path
import sys,tempfile,unittest,json,copy
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
if (ROOT/'cinema.py').exists():sys.path.insert(0,str(ROOT))
else:sys.path.insert(0,str(ROOT/'H3_CAMERA_KIT_REVIEW_22'))
import cinema
class Regressions(unittest.TestCase):
 def test_reviews_require_actual_true(self):
  scene={'reviewed':True,'guide_reviewed':True,'subject':'Actor','camera':'Front','camera_fixed':True,'objects':[],'acting':[]}
  cinema.scene_prompt(scene,1)
  for field in ['reviewed','guide_reviewed']:
   for value in ['false','true',1,0,None,False,[],{}]:
    with self.subTest(field=field,value=value):
     s=copy.deepcopy(scene);s[field]=value
     with self.assertRaises(ValueError):cinema.scene_prompt(s,1)
   s=copy.deepcopy(scene);del s[field]
   with self.assertRaises(ValueError):cinema.scene_prompt(s,1)
 def fixture(self):
  root=Path(tempfile.mkdtemp(prefix='h3_resume_review_'));run=root/'run';out=root/'server';run.mkdir();out.mkdir()
  cinema.write(run/'run.json',{'server':'offline-mock'});cinema.write(run/'submission.json',{'prompt_id':'completed'})
  history={'completed':{'status':{'status_str':'success'},'outputs':{'92':{'videos':[{'filename':'first.mp4'}]},'95':{'videos':[{'filename':'second.mp4'}]}}}}
  with (out/'first.mp4').open('xb') as f:f.write(b'FIRST_COMPLETE')
  return root,run,out,history,SimpleNamespace(run=str(run),comfy_output=str(out),wait=0)
 def test_resume_after_second_output_missing(self):
  root,run,out,history,args=self.fixture()
  with patch.object(cinema,'api',return_value=history):
   with self.assertRaises(FileNotFoundError):cinema.collect(args)
   first=run/'native_audio.mp4';before=first.read_bytes();mtime=first.stat().st_mtime_ns
   self.assertFalse((run/'result.json').exists())
   with (out/'second.mp4').open('xb') as f:f.write(b'SECOND_COMPLETE')
   cinema.collect(args)
   self.assertEqual(first.read_bytes(),before);self.assertEqual(first.stat().st_mtime_ns,mtime)
   self.assertEqual((run/'original_audio.mp4').read_bytes(),b'SECOND_COMPLETE')
   result=cinema.read(run/'result.json');self.assertEqual(len(result['files']),2)
   with self.assertRaises(ValueError):cinema.collect(args)
 def test_existing_different_file_is_preserved(self):
  root,run,out,history,args=self.fixture()
  existing=run/'native_audio.mp4'
  with existing.open('xb') as f:f.write(b'USER_FILE_MUST_SURVIVE')
  with patch.object(cinema,'api',return_value=history):
   with self.assertRaises(FileExistsError):cinema.collect(args)
  self.assertEqual(existing.read_bytes(),b'USER_FILE_MUST_SURVIVE');self.assertFalse((run/'result.json').exists())
if __name__=='__main__':unittest.main(verbosity=2)
