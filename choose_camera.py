"""Compatibility entry point; implementation lives in src/continuity_reframe."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/"src"))
from continuity_reframe import choose_camera as _impl
if __name__=="__main__":
    _impl.main()
else:
    sys.modules[__name__]=_impl
