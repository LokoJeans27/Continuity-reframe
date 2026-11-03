"""Regression checks for root CLI compatibility and relocated resources."""
from pathlib import Path
import subprocess,sys,tempfile,json,unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import cinema,visual,choose_camera,attach_camera
class LayoutTests(unittest.TestCase):
 def test_legacy_imports_resolve_to_implementations(self):
  for module in [cinema,visual,choose_camera,attach_camera]:
   self.assertTrue(Path(module.__file__).resolve().is_relative_to(ROOT/'src/continuity_reframe'))
 def test_cli_from_different_working_directory(self):
  cwd=Path(tempfile.mkdtemp(prefix='continuity_layout_'))
  for entry,args in [('cinema.py',['--help']),('choose_camera.py',['--list']),('attach_camera.py',['--help'])]:
   result=subprocess.run([sys.executable,'-B',str(ROOT/entry),*args],cwd=cwd,capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
  choices=json.loads(subprocess.check_output([sys.executable,'-B',str(ROOT/'choose_camera.py'),'--list'],cwd=cwd,text=True))
  self.assertEqual(choices,json.loads((ROOT/'configs/camera_choices.json').read_text()))
 def test_selector_legacy_link(self):
  html=(ROOT/'camera_picker.html').read_text()
  self.assertIn('url=ui/camera_picker.html',html)
  self.assertIn('href="ui/camera_picker.html"',html)
  self.assertTrue((ROOT/'ui/camera_picker.html').is_file())
if __name__=='__main__':unittest.main(verbosity=2)
