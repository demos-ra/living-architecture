"""R1 Domain package — auto-discovers .py modules
Bootstrap exception: imports module_loader from R4 (exec) to load hyphenated filenames.
This is a package-init-only exception; no other R1 file may import from R4.
"""
import sys
from pathlib import Path
from exec import module_loader

_dir = Path(__file__).parent

if str(_dir) not in sys.path:
    sys.path.insert(0, str(_dir))

# Auto-discover all .py files (except __init__)
for _f in sorted(_dir.glob('*.py')):
    if _f.stem == '__init__':
        continue
    _name = _f.stem.replace('-', '_')
    _mod = module_loader.load_module(f'domain.{_name}', _f)
    globals()[_name] = _mod
