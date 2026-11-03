from pathlib import Path
import tempfile,sys,unittest
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT if (ROOT/'cinema.py').exists() else ROOT/'H3_CAMERA_KIT_QUICKSTART_26'))
import cinema
class ComparePreflight(unittest.TestCase):
 def make(self):
  root=Path(tempfile.mkdtemp(prefix='h3_compare_preflight_'));run=root/'run';project=root/'project';run.mkdir();project.mkdir()
  cinema.write(run/'run.json',{'project':str(project)});cinema.write(project/'project.json',{'frames':90})
  return run,SimpleNamespace(run=str(run))
 def test_pending_does_not_create_folder_and_retry_stays_possible(self):
  r,a=self.make()
  for _ in range(2):
   with self.assertRaisesRegex(ValueError,'COLLECTED'):cinema.compare(a)
   self.assertFalse((r/'comparison').exists())
 def test_missing_second_video_does_not_create_folder(self):
  r,a=self.make()
  with (r/'native_audio.mp4').open('xb') as f:f.write(b'preserve')
  cinema.write(r/'result.json',{'history':{'status':{'status_str':'success'}},'files':[]})
  with self.assertRaises(ValueError):cinema.compare(a)
  self.assertFalse((r/'comparison').exists());self.assertEqual((r/'native_audio.mp4').read_bytes(),b'preserve')
 def test_matching_hash_but_undecodable_video_rejected(self):
  r,a=self.make();records=[]
  for name in ['native_audio.mp4','original_audio.mp4']:
   with (r/name).open('xb') as f:f.write(b'not a video')
   records.append({'file':name,'sha256':cinema.digest(r/name)})
  cinema.write(r/'result.json',{'history':{'status':{'status_str':'success'}},'files':records})
  with self.assertRaisesRegex(ValueError,'decoded'):cinema.compare(a)
  self.assertFalse((r/'comparison').exists())
if __name__=='__main__':unittest.main(verbosity=2)
