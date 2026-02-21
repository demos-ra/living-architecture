#!/usr/bin/env python3
"""
validate-changes.py - R1 C-code Validator
Validates C-code format in commit messages
Config-driven: reads valid codes from src/config/changes.json
"""

import re
import sys
from config_loader import get_valid_c_codes


def validate_c_code_format(commit_message):
    """
    Validate that commit message has valid C-code.
    Only checks format (C1-C5), not semantic correctness.
    """
    # Extract C-code from message
    match = re.search(r'/C([1-5])\]', commit_message)
    
    if not match:
        return {
            'valid': False,
            'error': 'No C-code found in format [F-*/R*/C#]'
        }
    
    c_code = f"C{match.group(1)}"
    
    # Check against config
    valid_codes = get_valid_c_codes()
    
    if c_code not in valid_codes:
        return {
            'valid': False,
            'error': f'Invalid C-code: {c_code}. Must be one of: {", ".join(valid_codes)}'
        }
    
    return {
        'valid': True,
        'c_code': c_code
    }


def validate(commit_message):
    """Main validation function (config-driven)"""
    return validate_c_code_format(commit_message)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
        result = validate(message)
        
        if result['valid']:
            print(f"✓ C-code valid: {result['c_code']}")
        else:
            print(f"✗ {result['error']}")
            sys.exit(1)
    else:
        print("Usage: validate-changes.py '<commit message>'")
