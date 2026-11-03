"""Collection refuses symlinks even when bytes match; retains all fixtures."""
from pathlib import Path
import sys,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import cinema
from test_resume_review import Regressions
class SymlinkTests(unittest.TestCase):
 def test_matching_symlink_is_rejected(self):
  root,run,out,history,args=Regressions().fixture();dst=run/'native_audio.mp4'
  try:dst.symlink_to(out/'first.mp4')
  except (OSError,NotImplementedError) as exc:self.skipTest('OS cannot create symlinks: '+str(exc))
  before=(out/'first.mp4').read_bytes()
  with patch.object(cinema,'api',return_value=history):
   with self.assertRaises(ValueError):cinema.collect(args)
  self.assertTrue(dst.is_symlink());self.assertEqual((out/'first.mp4').read_bytes(),before);self.assertFalse((run/'result.json').exists())
 def test_symlink_guard_before_digest(self):
  root,run,out,history,args=Regressions().fixture();dst=run/'native_audio.mp4'
  original=Path.is_symlink
  with patch.object(cinema,'api',return_value=history),patch.object(Path,'is_symlink',lambda p:p==dst or original(p)),patch.object(cinema,'digest',side_effect=AssertionError('Must reject before following link')):
   with self.assertRaises(ValueError):cinema.collect(args)
  self.assertFalse(dst.exists());self.assertFalse((run/'result.json').exists())
if __name__=='__main__':unittest.main(verbosity=2)
