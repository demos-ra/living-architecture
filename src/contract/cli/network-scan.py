#!/usr/bin/env python3
"""
network-scan.py - R3 CLI Interface
Project health scanning with progressive zoom

Usage:
  network-scan.py                     # All features
  network-scan.py F-counter           # Feature detail
  network-scan.py F-counter R1        # Layer detail
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from domain import validate_f_tags, la_output
from app import validation_workflow
import re
import subprocess

# F-tags to exclude from feature scans (infrastructure, not features)
EXCLUDED_TAGS = {'F-la'}


def _git(args):
    """Run a git command, return stripped stdout or empty string."""
    try:
        r = subprocess.run(['git'] + args, capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return ''


def _get_commits_with_ftag_and_layer(f_tag, r_layer):
    pattern = f'\\[{f_tag}/{r_layer}/'
    out = _git(['log', '--all', '--pretty=format:%h %s', '--grep', pattern])
    return [l for l in out.split('\n') if l] if out else []


def _get_commits_with_ftag(f_tag):
    out = _git(['log', '--all', '--grep', f_tag, '--oneline'])
    return [l for l in out.split('\n') if l] if out else []


def _get_files_for_ftag_and_layer(f_tag, r_layer):
    pattern = f'\\[{f_tag}/{r_layer}/'
    out = _git(['log', '--all', '--pretty=format:', '--name-only', '--grep', pattern])
    if out:
        return sorted({l.strip() for l in out.split('\n') if l.strip()})
    return []


def get_all_ftags():
    try:
        result = subprocess.run(
            ['git', 'log', '--all', '--pretty=format:%s'],
            capture_output=True, text=True
        )
        f_tags = set()
        for line in result.stdout.split('\n'):
            match = re.search(r'\[F-([a-z][a-z0-9-]*)/R[0-4]/C[1-5]\]', line)
            if match:
                tag = f"F-{match.group(1)}"
                if tag not in EXCLUDED_TAGS:
                    f_tags.add(tag)
        return sorted(f_tags)
    except:
        return []


def scan_all_features():
    print(la_output.header('NETWORK SCAN'))

    f_tags = get_all_ftags()

    if not f_tags:
        print("  No features detected")
    else:
        for f_tag in f_tags:
            result = validate_f_tags.validate_ftag_completeness(f_tag)
            if result['complete']:
                print(f"  {f_tag:20}{la_output.ok('complete')}")
            else:
                missing = ', '.join(result['layers_missing'])
                print(f"  {f_tag:20}{la_output.warn(f'missing {missing}')}")

    print()
    print(f"  {len(f_tags)} feature{'s' if len(f_tags) != 1 else ''} detected")
    print()
    print(la_output.divider())


def scan_feature(f_tag):
    print(la_output.header(f'{f_tag.upper()} FEATURE'))

    result = validate_f_tags.validate_ftag_completeness(f_tag)

    # R-layers
    if result['complete']:
        print(f"  {'R-layers':14}{la_output.ok('complete')}")
    else:
        missing = ', '.join(result['layers_missing'])
        present = len(result['layers_present'])
        total   = len(result['layers_required'])
        print(f"  {'R-layers':14}{la_output.warn(f'{present}/{total} — missing {missing}')}")

    # Execution + QC — get real files for this feature, run validators via R2
    feature_files = []
    for layer in result['layers_present']:
        feature_files.extend(_get_files_for_ftag_and_layer(f_tag, layer))
    feature_files = sorted(set(feature_files))

    val = validation_workflow.validate_files(feature_files)
    exec_val = val['execution']
    qc_val   = val['qc']

    print(f"  {'Execution':14}{la_output.ok('') if exec_val['valid'] else la_output.err('')}")
    if qc_val['valid']:
        print(f"  {'QC':14}{la_output.ok('')}")
    else:
        violations = qc_val.get('violations', [])
        print(f"  {'QC':14}{la_output.err(violations[0] if violations else 'violation')}")

    # Activity
    total_commits = _get_commits_with_ftag(f_tag)
    n = len(total_commits)
    print(f"  {'Activity':14}{n} commit{'s' if n != 1 else ''}")

    print()

    # Layer drill-down hints
    for layer in sorted(result['layers_present']):
        commits = _get_commits_with_ftag_and_layer(f_tag, layer)
        print(f"  {layer:14}{len(commits)} commit{'s' if len(commits) != 1 else ''}"
              f"  →  network-scan.py {f_tag} {layer}")

    print()
    print(la_output.divider())
def get_layer_detail(f_tag, r_layer):
    """Get files and commits for a specific F-tag + R-layer."""
    commits = _get_commits_with_ftag_and_layer(f_tag, r_layer)
    files   = _get_files_for_ftag_and_layer(f_tag, r_layer)
    return {'f_tag': f_tag, 'r_layer': r_layer, 'commits': commits, 'files': files}


def scan_layer(f_tag, r_layer):
    print(la_output.header(f'{f_tag.upper()} / {r_layer}'))

    detail = get_layer_detail(f_tag, r_layer)

    # Files
    if detail['files']:
        print(f"  {'Files':14}")
        for f in detail['files']:
            print(f"    {f}")
    else:
        print(f"  {'Files':14}none found")

    print()

    # Commits
    if detail['commits']:
        print(f"  {'Commits':14}")
        for c in detail['commits']:
            print(f"    {c}")
    else:
        print(f"  {'Commits':14}none found")

    print()
    print(la_output.divider())


def main():
    if len(sys.argv) == 1:
        scan_all_features()
    elif len(sys.argv) == 2:
        f_tag = sys.argv[1]
        if not f_tag.startswith('F-'):
            f_tag = f'F-{f_tag}'
        scan_feature(f_tag)
    elif len(sys.argv) == 3:
        f_tag = sys.argv[1]
        r_layer = sys.argv[2].upper()
        if not f_tag.startswith('F-'):
            f_tag = f'F-{f_tag}'
        scan_layer(f_tag, r_layer)
    else:
        print("Usage:")
        print("  network-scan.py                  # All features")
        print("  network-scan.py F-counter        # Feature detail")
        print("  network-scan.py F-counter R1     # Layer detail")


if __name__ == "__main__":
    main()
