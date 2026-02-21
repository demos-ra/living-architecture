#!/usr/bin/env python3
"""
validate-execution.py - R1 Execution Pattern Validator
Validates I/O ownership, state machines, flow paths.
Pure functions — content passed in by R2, no file I/O here.
"""

import sys
import re
import json


def check_io_ownership(filepath, content):
    """Check for I/O operations and ownership."""
    io_patterns = {
        'stdout':  [r'print\(', r'console\.log', r'echo\s'],
        'stderr':  [r'console\.error', r'sys\.stderr'],
        'file':    [r'open\(', r'fs\.', r'File\('],
        'network': [r'fetch\(', r'axios', r'requests\.'],
    }
    operations = []
    for io_type, patterns in io_patterns.items():
        for pattern in patterns:
            if re.findall(pattern, content):
                operations.append({'type': io_type})
    return {
        'has_io':     len(operations) > 0,
        'operations': operations,
        'valid':      len(operations) <= 2
    }


def check_state_machines(filepath, content):
    """Check for state machine completeness."""
    has_state       = bool(re.search(r'state\s*=|setState|this\.state', content))
    has_transitions = bool(re.search(r'switch|if.*state|case\s', content))
    if has_state:
        return {
            'has_state_machine': True,
            'has_transitions':   has_transitions,
            'valid':             has_transitions
        }
    return {'has_state_machine': False, 'valid': True}


def check_flow_paths(filepath, content):
    """Check for deep relative imports (circular risk)."""
    imports = []
    for line in content.split('\n'):
        match = re.search(r'(?:from|import)\s+([^\s]+)', line)
        if match:
            imports.append(match.group(1))
    bad_imports = [imp for imp in imports if imp.count('..') > 2]
    return {
        'imports':       imports,
        'circular_risk': len(bad_imports) > 0,
        'valid':         len(bad_imports) == 0
    }


def validate(filepath, content):
    """
    Main validation function.
    R2 reads the file via file-io and passes content here.
    """
    io_result    = check_io_ownership(filepath, content)
    state_result = check_state_machines(filepath, content)
    flow_result  = check_flow_paths(filepath, content)
    all_valid = io_result['valid'] and state_result['valid'] and flow_result['valid']
    return {
        'valid':          all_valid,
        'filepath':       filepath,
        'io_ownership':   io_result,
        'state_machines': state_result,
        'flow_paths':     flow_result
    }


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath) as f:
                content = f.read()
        except Exception as e:
            print(f'Cannot read file: {e}')
            sys.exit(1)
        result = validate(filepath, content)
        print(json.dumps(result, indent=2))
    else:
        print('Usage: validate-execution.py <filepath>')
