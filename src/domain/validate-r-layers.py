#!/usr/bin/env python3
"""
Living Architecture - Dependency Direction Validator
Validates that code doesn't violate R-layer dependency rules.
NOW INCLUDES: Circular dependency detection within R-layers
"""

import sys
import re
from pathlib import Path
from collections import defaultdict, deque


def detect_circular_dependencies(files_with_imports):
    """
    Detect circular import dependencies.
    Returns list of cycles if found.
    """
    # Build dependency graph
    graph = defaultdict(set)
    for filepath, imports in files_with_imports.items():
        for imp in imports:
            graph[filepath].add(imp)
    
    # Detect cycles using DFS
    def has_cycle(node, visited, rec_stack, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack, path):
                    return True
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]
        
        path.pop()
        rec_stack.remove(node)
        return False
    
    visited = set()
    cycles = []
    
    for node in graph:
        if node not in visited:
            rec_stack = set()
            path = []
            cycle = has_cycle(node, visited, rec_stack, path)
            if cycle:
                cycles.append(cycle)
    
    return cycles


def _load_r_layer_rules():
    """
    Load dependency rules from R0 config (r-layers.json).
    Returns (forbidden_deps, r_group_patterns, r_group_names) keyed by directory name.
    """
    import json
    config_path = Path(__file__).parent.parent / 'config' / 'r-layers.json'
    with open(config_path) as f:
        config = json.load(f)

    layers = config['layers']        # e.g. {"R0": {"name": "Config", "directory": "config"}}
    deps   = config['dependencies']  # e.g. {"R0": {"forbidden": ["R1", ...]}}

    # Map directory name → list of forbidden directory names
    forbidden_deps = {}
    r_group_patterns = {}
    r_group_names = {}

    for r_id, layer in layers.items():
        dirname = layer['directory']
        forbidden_r_ids = deps.get(r_id, {}).get('forbidden', [])
        forbidden_dirs  = [layers[r]['directory'] for r in forbidden_r_ids if r in layers]

        forbidden_deps[dirname]    = forbidden_dirs
        r_group_patterns[dirname]  = [dirname]
        r_group_names[dirname]     = f"{r_id} {layer['name']}"

    return forbidden_deps, r_group_patterns, r_group_names


FORBIDDEN_DEPS, R_GROUP_PATTERNS, R_GROUP_NAMES = _load_r_layer_rules()

def detect_r_group(filepath):
    """Determine R-group from file path."""
    path_str = str(filepath).lower()

    for r_group, patterns in R_GROUP_PATTERNS.items():
        for pattern in patterns:
            if f'/{pattern}/' in path_str or f'\\{pattern}\\' in path_str:
                return r_group

    return None

def extract_import_target(line):
    """Extract the imported module/package path from an import statement."""
    patterns = [
        r'from\s+["\']?([^"\']+)["\']?\s+import',     # Python: from X import
        r'import\s+["\']?([^"\']+)["\']?',             # Python/JS: import X
        r'require\(["\']([^"\']+)["\']\)',              # JS: require('X')
        r'use\s+([^;]+);',                             # Rust: use X;
    ]

    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            return match.group(1)

    return None

def detect_import_r_group(import_path):
    """Determine which R-group an import is targeting."""
    import_lower = import_path.lower()

    for r_group, patterns in R_GROUP_PATTERNS.items():
        for pattern in patterns:
            if pattern in import_lower:
                return r_group

    return None

def check_file(filepath, content):
    """
    Check a single file for dependency violations.
    R2 reads the file via file-io and passes content here.
    """
    violations = []

    source_r_group = detect_r_group(filepath)
    if not source_r_group:
        return []

    for line_num, line in enumerate(content.split('\n'), 1):
        if line.strip().startswith(('#', '//', '/*', '*')):
            continue

        if any(keyword in line for keyword in ['import', 'from', 'require', 'use']):
            import_target = extract_import_target(line)
            if not import_target:
                continue

            target_r_group = detect_import_r_group(import_target)
            if not target_r_group:
                continue

            forbidden = FORBIDDEN_DEPS.get(source_r_group, [])
            if target_r_group in forbidden:
                violations.append({
                    'file':             str(filepath),
                    'line':             line_num,
                    'source_r_group':   source_r_group,
                    'target_r_group':   target_r_group,
                    'content':          line.strip()
                })

    return violations

def main():
    """Scan all source files for dependency violations."""
    print("Checking dependency direction (D2)")
    print()

    violations = []
    file_extensions = ['*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.rs', '*.go', '*.java']

    for ext in file_extensions:
        for filepath in Path('.').rglob(ext):
            if any(skip in str(filepath) for skip in ['node_modules', 'venv', '.venv', 'build', 'dist', '.git', '__init__.py', 'test-project']):
                continue
            violations.extend(check_file(filepath, filepath.read_text(encoding='utf-8', errors='ignore')))

    if violations:
        print("  ✗ Dependency Direction Violations Found (D2)")
        print()
        for v in violations:
            source_name = R_GROUP_NAMES.get(v['source_r_group'], v['source_r_group'])
            target_name = R_GROUP_NAMES.get(v['target_r_group'], v['target_r_group'])
            print(f"  {v['file']}:{v['line']}")
            print(f"    {source_name} cannot depend on {target_name}")
            print(f"    > {v['content']}")
            print()

        print("  Forbidden dependencies:")
        for source, targets in FORBIDDEN_DEPS.items():
            source_name = R_GROUP_NAMES.get(source, source)
            target_names = [R_GROUP_NAMES.get(t, t) for t in targets]
            print(f"    {source_name}: cannot import from {', '.join(target_names)}")
        print()

        sys.exit(1)
    else:
        print("  ✓ No dependency violations found")
        sys.exit(0)

if __name__ == '__main__':
    main()
