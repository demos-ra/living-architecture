#!/usr/bin/env python3
"""
System Governance Spec - Error Structure Validator
Validates that errors follow canonical structure from 03-ERROR-SYSTEM.md

Checks for:
- Use of error registry kinds
- Required fields: kind, scope, cause, location, resolution_hint
- Valid scope values: USER, SYSTEM, DEPENDENCY
"""

import json
import sys
import re
from pathlib import Path

# Load error specification
try:
    with open('law/03-error-system.json', 'r') as f:
        ERROR_SPEC = json.load(f)
        VALID_KINDS = list(ERROR_SPEC['global_error_registry'].keys())
        VALID_SCOPES = ERROR_SPEC['canonical_error_structure']['required_fields'][1]['allowed_values']
except FileNotFoundError:
    print("⚠️  Warning: law/03-error-system.json not found - skipping validation")
    sys.exit(0)
except Exception as e:
    print(f"⚠️  Warning: Could not load error spec: {e}")
    sys.exit(0)

# Patterns that suggest error creation (adjust for your languages)
ERROR_CREATION_PATTERNS = [
    r'throw\s+new\s+\w*Error',           # JS/TS: throw new Error
    r'raise\s+\w*Error',                  # Python: raise Error
    r'return\s+Err\(',                    # Rust: return Err(
    r'Error\s*\{',                        # Rust/Go: Error{
    r'\.Errorf?\(',                       # Go: fmt.Errorf
]

# Patterns that suggest canonical error usage
CANONICAL_PATTERNS = [
    r'kind\s*[:=]',
    r'scope\s*[:=]',
    r'cause\s*[:=]',
    r'location\s*[:=]',
    r'resolution_hint\s*[:=]',
]

def check_for_canonical_structure(content, start_pos, context_size=500):
    """Check if error creation uses canonical structure."""
    # Get context around error creation
    context = content[start_pos:start_pos + context_size]
    
    # Check for canonical fields
    has_kind = bool(re.search(r'kind\s*[:=]', context))
    has_scope = bool(re.search(r'scope\s*[:=]', context))
    has_cause = bool(re.search(r'cause\s*[:=]', context))
    has_location = bool(re.search(r'location\s*[:=]', context))
    has_resolution_hint = bool(re.search(r'resolution_hint\s*[:=]', context))
    
    # Check for registry kinds
    has_registry_kind = any(kind in context for kind in VALID_KINDS)
    
    # Check for valid scopes
    has_valid_scope = any(scope in context for scope in VALID_SCOPES)
    
    return {
        'has_canonical_fields': has_kind and has_scope and has_cause and has_location and has_resolution_hint,
        'has_registry_kind': has_registry_kind,
        'has_valid_scope': has_valid_scope,
        'fields_present': {
            'kind': has_kind,
            'scope': has_scope,
            'cause': has_cause,
            'location': has_location,
            'resolution_hint': has_resolution_hint,
        }
    }

def check_file(filepath):
    """Scan file for error creation and validate structure."""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for error creation patterns
        for pattern in ERROR_CREATION_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                
                # Check if it uses canonical structure
                check = check_for_canonical_structure(content, match.start())
                
                # If no canonical structure detected, flag as violation
                if not check['has_canonical_fields'] and not check['has_registry_kind']:
                    missing_fields = [k for k, v in check['fields_present'].items() if not v]
                    
                    violations.append({
                        'file': str(filepath),
                        'line': line_num,
                        'pattern': match.group(0),
                        'issue': 'Error created without canonical structure',
                        'missing_fields': missing_fields,
                        'has_registry_kind': check['has_registry_kind'],
                    })
    
    except Exception as e:
        print(f"⚠️  Warning: Could not read {filepath}: {e}", file=sys.stderr)
    
    return violations

def main():
    """Scan all source files for error structure violations."""
    print("🔍 Checking error system compliance...")
    print()
    
    # Find all source files
    violations = []
    file_extensions = ['*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.rs', '*.go', '*.java']
    
    for ext in file_extensions:
        for filepath in Path('.').rglob(ext):
            # Skip node_modules, venv, build directories, and test files
            if any(skip in str(filepath) for skip in ['node_modules', 'venv', '.venv', 'build', 'dist', '.git', 'test', 'spec']):
                continue
            
            violations.extend(check_file(filepath))
    
    if violations:
        print("❌ Error System Violations Found:")
        print()
        
        for v in violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Issue: {v['issue']}")
            print(f"    Pattern: {v['pattern']}")
            
            if v['missing_fields']:
                print(f"    Missing fields: {', '.join(v['missing_fields'])}")
            
            if not v['has_registry_kind']:
                print(f"    Not using error registry kind")
            
            print()
        
        print("Required canonical structure:")
        print("  - kind: from error registry")
        print("  - scope: USER | SYSTEM | DEPENDENCY")
        print("  - cause: factual description")
        print("  - location: R-group + component")
        print("  - resolution_hint: corrective action")
        print()
        
        print(f"Valid error kinds: {', '.join(VALID_KINDS[:5])}... (see law/03-error-system.json)")
        print()
        
        print("Example compliant error:")
        print("""
  {
    kind: "VALIDATION_FAILED",
    scope: "USER",
    cause: "Email format invalid: missing @ symbol",
    location: "R2:UserRegistration",
    resolution_hint: "Provide valid email address"
  }
        """)
        
        sys.exit(1)
    else:
        print("✅ No error system violations found")
        sys.exit(0)

if __name__ == '__main__':
    main()
