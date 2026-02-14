#!/usr/bin/env python3
"""
Living Architecture v1.1 - Active R-Group Detection
Scans project structure and determines which R-groups are actually present.
"""

import json
import sys
from pathlib import Path

# R-group directory patterns (common naming conventions)
R_GROUP_PATTERNS = {
    'config': ['config', '.config', 'configuration', 'env'],
    'domain': ['domain', 'entities', 'core', 'models', 'business'],
    'application': ['application', 'usecases', 'use-cases', 'services', 'workflows', 'application'],
    'interface': ['interface', 'controllers', 'api', 'routes', 'http', 'handlers', 'api'],
    'infrastructure': ['infrastructure', 'persistence', 'adapters', 'repositories', 'infra', 'db'],
    'presentation': ['presentation', 'ui', 'views', 'components', 'pages', 'web', 'frontend', 'client'],
}

def detect_active_r_groups(project_root='.', verbose=False):
    """
    Scan project directory and detect which R-groups are present.
    
    Args:
        project_root: Root directory to scan (default: current directory)
        verbose: Print debug information
    
    Returns:
        dict: {r_group_name: bool} - True if layer detected, False otherwise
    """
    
    active = {}
    root_path = Path(project_root)
    
    # Check each R-group
    for r_group, patterns in R_GROUP_PATTERNS.items():
        detected = False
        found_pattern = None
        
        # Try to find any matching directory
        for pattern in patterns:
            # Direct match: /pattern/
            direct = root_path / pattern
            if direct.exists() and direct.is_dir():
                detected = True
                found_pattern = pattern
                break
            
            # Nested match: /src/pattern/, /src/**/pattern/
            for potential_match in root_path.rglob(pattern):
                if potential_match.is_dir() and len(potential_match.relative_to(root_path).parts) <= 3:
                    detected = True
                    found_pattern = str(potential_match.relative_to(root_path))
                    break
            
            if detected:
                break
        
        active[r_group] = detected
        
        if verbose:
            status = "✓" if detected else "✗"
            location = f" ({found_pattern})" if detected else ""
            print(f"  {status} {r_group}{location}", file=sys.stderr)
    
    return active

def validate_layer_combination(active_layers):
    """
    Check if the active layer combination is valid.
    Some layers depend on others being present.
    
    Args:
        active_layers: dict of {layer_name: bool}
    
    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    
    errors = []
    
    # PRESENTATION requires INTERFACE
    if active_layers.get('presentation') and not active_layers.get('interface'):
        errors.append("PRESENTATION requires INTERFACE (cannot exist without INTERFACE)")
    
    # APPLICATION requires DOMAIN (conceptually, but can skip)
    # Not enforced: some systems skip DOMAIN
    
    # INFRASTRUCTURE requires APPLICATION (conceptually, but can skip)
    # Not enforced: some systems are pure event-handlers
    
    return len(errors) == 0, errors

def format_output(active_layers, format_type='json', verbose=False):
    """
    Format active layers for output.
    
    Args:
        active_layers: dict of {layer_name: bool}
        format_type: 'json' or 'env'
        verbose: Include additional info
    
    Returns:
        str: Formatted output
    """
    
    if format_type == 'json':
        if verbose:
            return json.dumps(active_layers, indent=2)
        else:
            return json.dumps(active_layers, separators=(',', ':'))
    
    elif format_type == 'env':
        # Bash-compatible format
        lines = []
        for layer, active in active_layers.items():
            value = "true" if active else "false"
            lines.append(f"LA_LAYER_{layer.upper()}={value}")
        return "\n".join(lines)
    
    elif format_type == 'shell':
        # For sourcing in bash
        lines = ["# Living Architecture R-Groups"]
        for layer, active in active_layers.items():
            value = "1" if active else "0"
            lines.append(f"export LA_LAYER_{layer.upper()}={value}")
        return "\n".join(lines)

def main():
    """
    Main entry point. Detect and output active R-groups.
    """
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detect active R-groups in Living Architecture project'
    )
    parser.add_argument('--root', default='.', help='Project root directory')
    parser.add_argument('--format', choices=['json', 'env', 'shell'], default='json',
                      help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Verbose output (debug info)')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("🔍 Detecting Living Architecture R-groups...", file=sys.stderr)
    
    # Detect active layers
    active = detect_active_r_groups(args.root, verbose=args.verbose)
    
    # Validate combination
    is_valid, errors = validate_layer_combination(active)
    
    if not is_valid:
        print("⚠️  Warning: Invalid layer combination", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
    
    # Format and output
    output = format_output(active, format_type=args.format, verbose=args.verbose)
    print(output)
    
    # Exit code
    return 0 if is_valid else 1

if __name__ == '__main__':
    sys.exit(main())
