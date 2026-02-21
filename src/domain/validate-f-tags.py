#!/usr/bin/env python3
"""
validate-f-tags.py - R1 F-tag Completeness Validator
Validates that F-tags are complete across R-layers
Config-driven: reads rules from src/config/f-tags.json
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from config_loader import load_f_tag_rules, load_r_layers


def extract_ftag_from_message(message):
    """Extract F-tag and R-layer from commit message [F-name/R#/C#]."""
    match = re.search(r'\[F-([a-z][a-z0-9-]*)/R([0-4])/C[1-5]\]', message)
    if match:
        return f"F-{match.group(1)}", f"R{match.group(2)}"
    return None, None


def get_layers_from_history(f_tag):
    """Get R-layers already committed for this F-tag from git history."""
    try:
        result = subprocess.run(
            ['git', 'log', '--all', '--pretty=format:%s'],
            capture_output=True, text=True
        )
        layers = set()
        for line in result.stdout.split('\n'):
            match = re.search(rf'\[{re.escape(f_tag)}/R([0-4])/C[1-5]\]', line)
            if match:
                layers.add(f"R{match.group(1)}")
        return layers
    except:
        return set()


def validate_ftag_completeness(f_tag):
    """Validate that F-tag has required R-layers (config-driven)."""
    config = load_f_tag_rules()
    required = set(config['completeness']['required_layers'])

    layers_present = get_layers_from_history(f_tag)
    missing = required - layers_present

    return {
        'complete': len(missing) == 0,
        'f_tag': f_tag,
        'layers_present': sorted(layers_present),
        'layers_required': sorted(required),
        'layers_missing': sorted(missing),
    }


def validate(commit_message):
    """Main validation function (config-driven)."""
    config = load_f_tag_rules()
    f_tag, current_layer = extract_ftag_from_message(commit_message)

    if not f_tag:
        return {'valid': False, 'error': 'No F-tag found in commit message'}

    if not re.match(config['format']['pattern'], f_tag):
        return {'valid': False, 'error': f'Invalid F-tag format: {f_tag}'}

    # Include current commit's layer in completeness check
    result = validate_ftag_completeness(f_tag)
    layers_present = set(result['layers_present'])
    if current_layer:
        layers_present.add(current_layer)

    required = set(config['completeness']['required_layers'])
    missing = sorted(required - layers_present)

    return {
        'valid': True,
        'complete': len(missing) == 0,
        'f_tag': f_tag,
        'layers_present': sorted(layers_present),
        'layers_missing': missing
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = validate(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: validate-f-tags.py '<commit message>'")

