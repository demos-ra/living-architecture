#!/usr/bin/env python3
"""
validate-operations.py - R1 O-rule (QC) Validator
Checks O1, O3, O6, O7 safety rules via pattern matching.
Pure functions — content passed in by R2, no file I/O here.
"""

import re
import sys
import json
from config_loader import load_o_rules


def check_o1_access_control(filepath, content):
    """O1: API endpoints must have authentication."""
    violations = []
    if '@app.route' in content or '@api.route' in content:
        if '@auth.require' not in content and '@login_required' not in content:
            violations.append('O1: API endpoint missing authentication decorator')
    return violations


def check_o3_reliability(filepath, content):
    """O3: Network calls must have error handling."""
    violations = []
    network_patterns = [r'requests\.(get|post|put|delete)', r'fetch\(', r'axios\.']
    for pattern in network_patterns:
        if re.search(pattern, content):
            if 'try:' not in content and 'except' not in content:
                violations.append('O3: Network call without error handling')
            break
    return violations


def check_o6_configuration(filepath, content):
    """O6: No hardcoded secrets."""
    violations = []
    secret_patterns = [
        r'API_KEY\s*=\s*["\']sk-',
        r'PASSWORD\s*=\s*["\'].+["\']',
        r'SECRET\s*=\s*["\'].+["\']',
    ]
    for pattern in secret_patterns:
        if re.search(pattern, content):
            violations.append('O6: Hardcoded secret detected (use environment variables)')
            break
    return violations


def check_o7_data_safety(filepath, content):
    """O7: No SQL injection risk."""
    violations = []
    sql_patterns = [
        r'execute\(f["\'].*{.*}.*["\']',
        r'execute\(["\'].*%s.*["\'].*%',
        r'execute\(.*\+.*\)',
    ]
    for pattern in sql_patterns:
        if re.search(pattern, content):
            violations.append('O7: Possible SQL injection (use parameterized queries)')
            break
    return violations


def validate(filepath, content):
    """
    Main validation function.
    R2 reads the file via file-io and passes content here.
    """
    violations = []
    violations.extend(check_o1_access_control(filepath, content))
    violations.extend(check_o3_reliability(filepath, content))
    violations.extend(check_o6_configuration(filepath, content))
    violations.extend(check_o7_data_safety(filepath, content))
    return {
        'valid':      len(violations) == 0,
        'filepath':   filepath,
        'violations': violations
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
        if result['valid']:
            print('✓ No O-rule violations')
        else:
            print('✗ O-rule violations:')
            for v in result['violations']:
                print(f'  - {v}')
            sys.exit(1)
    else:
        print('Usage: validate-operations.py <filepath>')
