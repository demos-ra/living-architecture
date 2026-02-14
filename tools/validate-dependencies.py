#!/usr/bin/env python3
"""
System Governance Spec - Dependency Direction Validator
Validates that code doesn't violate D2 (dependency direction rules).

Checks import/require statements to ensure:
- R1 (domain) depends on nothing
- R2 (application) only depends on R1
- R3 (interface) only depends on R2, R1
- R4 (infrastructure) only depends on R2, R1
- R5 (presentation) only depends on R3, R2, R1
"""

import sys
import re
from pathlib import Path

# Forbidden dependency patterns (from law/01-architecture.json)
FORBIDDEN_DEPS = {
    'domain': ['application', 'interface', 'infrastructure', 'presentation'],
    'application': ['interface', 'infrastructure', 'presentation'],
    'interface': ['infrastructure', 'presentation'],
    'infrastructure': ['interface', 'presentation'],
    'presentation': ['infrastructure'],
}

# R-group identifiers (common directory/namespace patterns)
R_GROUP_PATTERNS = {
    'domain': ['domain', 'entities', 'core', 'models'],
    'application': ['application', 'use-cases', 'usecases', 'services'],
    'interface': ['interface', 'controllers', 'api', 'routes', 'handlers'],
    'infrastructure': ['infrastructure', 'persistence', 'repositories', 'adapters'],
    'presentation': ['presentation', 'ui', 'views', 'components', 'pages'],
}

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
    # Match common import patterns across languages
    patterns = [
        r'from\s+["\']?([^"\']+)["\']?\s+import',     # Python: from X import
        r'import\s+["\']?([^"\']+)["\']?',             # Python/JS: import X
        r'require\(["\']([^"\']+)["\']\)',             # JS: require('X')
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

def check_file(filepath):
    """Check a single file for dependency violations."""
    violations = []
    
    # Determine source R-group
    source_r_group = detect_r_group(filepath)
    if not source_r_group:
        return []  # File not in governed directory
    
    # Check each line for imports
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Skip comments
                if line.strip().startswith(('#', '//', '/*', '*')):
                    continue
                
                # Check if line contains import-like keywords
                if any(keyword in line for keyword in ['import', 'from', 'require', 'use']):
                    import_target = extract_import_target(line)
                    if not import_target:
                        continue
                    
                    target_r_group = detect_import_r_group(import_target)
                    if not target_r_group:
                        continue
                    
                    # Check if this dependency is forbidden
                    forbidden = FORBIDDEN_DEPS.get(source_r_group, [])
                    if target_r_group in forbidden:
                        violations.append({
                            'file': str(filepath),
                            'line': line_num,
                            'source_r_group': source_r_group,
                            'target_r_group': target_r_group,
                            'content': line.strip()
                        })
    except Exception as e:
        print(f"⚠️  Warning: Could not read {filepath}: {e}", file=sys.stderr)
    
    return violations

def main():
    """Scan all source files for dependency violations."""
    print("🔍 Checking dependency direction (D2)...")
    print()
    
    # Find all source files
    violations = []
    file_extensions = ['*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.rs', '*.go', '*.java']
    
    for ext in file_extensions:
        for filepath in Path('.').rglob(ext):
            # Skip node_modules, venv, build directories
            if any(skip in str(filepath) for skip in ['node_modules', 'venv', '.venv', 'build', 'dist', '.git']):
                continue
            
            violations.extend(check_file(filepath))
    
    if violations:
        print("❌ Dependency Direction Violations Found (D2):")
        print()
        for v in violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    R-group '{v['source_r_group']}' cannot depend on '{v['target_r_group']}'")
            print(f"    > {v['content']}")
            print()
        
        print("Forbidden dependencies:")
        for source, targets in FORBIDDEN_DEPS.items():
            print(f"  {source}: cannot import from {', '.join(targets)}")
        print()
        
        sys.exit(1)
    else:
        print("✅ No dependency violations found")
        sys.exit(0)

if __name__ == '__main__':
    main()
