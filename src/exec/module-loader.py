#!/usr/bin/env python3
"""
module-loader.py - R4 Module I/O
Loads hyphenated Python modules from the filesystem.
Hyphenated filenames are valid paths but invalid Python identifiers;
this module bridges that gap at the I/O layer where it belongs.
"""

import importlib.util
import sys
from pathlib import Path


def load_module(name, filepath):
    """
    Load a Python module from a filepath, registering it in sys.modules.

    Args:
        name:     Dotted module name to register (e.g. 'domain.validate_f_tags')
        filepath: Absolute or relative path to the .py file

    Returns:
        The loaded module object.
    """
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod
