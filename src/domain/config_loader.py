#!/usr/bin/env python3
"""
config_loader.py - R1 Helper
Loads configuration from R0 config files
Validators use this to stay config-driven
"""

import json
from pathlib import Path


def load_r_layers():
    """Load R-layer definitions from config"""
    config_path = Path(__file__).parent.parent / 'config' / 'r-layers.json'
    with open(config_path) as f:
        config = json.load(f)
    return config['layers']


def get_valid_r_layer_ids():
    """Get list of valid R-layer IDs"""
    layers = load_r_layers()
    return list(layers.keys())


def load_f_tag_rules():
    """Load F-tag format and completeness rules"""
    config_path = Path(__file__).parent.parent / 'config' / 'f-tags.json'
    with open(config_path) as f:
        return json.load(f)


def load_c_codes():
    """Load C-code definitions"""
    config_path = Path(__file__).parent.parent / 'config' / 'changes.json'
    with open(config_path) as f:
        return json.load(f)


def get_valid_c_codes():
    """Get list of valid C-codes"""
    config = load_c_codes()
    return list(config['codes'].keys())


def load_o_rules():
    """Load O-rule definitions"""
    config_path = Path(__file__).parent.parent / 'config' / 'operations.json'
    with open(config_path) as f:
        return json.load(f)


def load_module_config():
    """Load module configuration"""
    config_path = Path(__file__).parent.parent / 'config' / 'modules.json'
    with open(config_path) as f:
        return json.load(f)


def get_module_from_filepath(filepath):
    """
    Extract module name from filepath using naming convention.
    Convention: {module}-{component}.ext
    
    Examples:
      auth-login.py → "M-auth"
      payment-process.py → "M-payment"
      user.py → None (no module prefix)
    
    Returns:
      str: Module name (e.g., "M-auth") or None if no convention used
    """
    # Check if module detection is enabled
    config = load_module_config()
    if not config.get('enabled', False):
        return None
    
    filename = Path(filepath).stem  # "auth-login.py" → "auth-login"
    
    if '-' in filename:
        module = filename.split('-')[0]
        return f"M-{module}"
    
    return None
