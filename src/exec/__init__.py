"""R4 Execution package — auto-discovers .py modules, explicit .js"""
import sys
from pathlib import Path
import importlib.util as _ilu

_dir = Path(__file__).parent

# Bootstrap module-loader first
_spec = _ilu.spec_from_file_location('exec.module_loader', _dir / 'module-loader.py')
_ml = _ilu.module_from_spec(_spec)
sys.modules['exec.module_loader'] = _ml
_spec.loader.exec_module(_ml)
module_loader = _ml

# Auto-discover all .py files (except __init__ and module-loader)
for _f in sorted(_dir.glob('*.py')):
    if _f.stem in ('__init__', 'module-loader'):
        continue
    _name = _f.stem.replace('-', '_')
    _mod = _ml.load_module(f'exec.{_name}', _f)
    globals()[_name] = _mod
