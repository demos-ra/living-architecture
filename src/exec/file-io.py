#!/usr/bin/env python3
"""
file-io.py - R4 File I/O Operations
Handles file reading and code analysis
"""

import re
from pathlib import Path


def read_file(filepath):
    """Read file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None


def analyze_imports(filepath, language='auto'):
    """Analyze import statements in a file."""
    content = read_file(filepath)
    if not content:
        return []
    
    # Auto-detect language
    if language == 'auto':
        ext = Path(filepath).suffix
        if ext == '.py':
            language = 'python'
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            language = 'javascript'
        else:
            return []
    
    imports = []
    
    if language == 'python':
        # Match: import X, from X import Y
        for line in content.split('\n'):
            match = re.match(r'^(?:from\s+(\S+)|import\s+(\S+))', line.strip())
            if match:
                imports.append(match.group(1) or match.group(2))
    
    elif language == 'javascript':
        # Match: import X from 'path', const X = require('path')
        patterns = [
            r"import\s+.+\s+from\s+['\"](.+)['\"]",
            r"require\(['\"](.+)['\"]\)"
        ]
        for line in content.split('\n'):
            for pattern in patterns:
                matches = re.findall(pattern, line)
                imports.extend(matches)
    
    return imports


def detect_io_operations(filepath):
    """Detect I/O operations in code."""
    content = read_file(filepath)
    if not content:
        return []
    
    io_patterns = [
        r'open\(',
        r'read\(',
        r'write\(',
        r'fetch\(',
        r'axios\.',
        r'fs\.',
        r'console\.log',
        r'print\(',
        r'document\.',
        r'window\.',
    ]
    
    operations = []
    for i, line in enumerate(content.split('\n'), 1):
        for pattern in io_patterns:
            if re.search(pattern, line):
                operations.append({
                    'line': i,
                    'type': pattern.strip('\\()'),
                    'code': line.strip()
                })
    
    return operations


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(f"Analyzing: {filepath}")
        print(f"Imports: {analyze_imports(filepath)}")
        print(f"I/O ops: {len(detect_io_operations(filepath))}")
    else:
        print("Usage: file-io.py <filepath>")
