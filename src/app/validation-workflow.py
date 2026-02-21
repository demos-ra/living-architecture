#!/usr/bin/env python3
"""
validation-workflow.py - R2 Orchestration
Coordinates all R1 validators with R4 I/O.
R4 reads files, R1 validates content, R2 assembles results.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from exec import git_io, file_io
from domain import (
    validate_f_tags,
    validate_execution,
    validate_operations,
    validate_r_layers,
    validate_changes,
    la_output,
)
from domain.config_loader import get_module_from_filepath


def run_all_validators():
    commit_msg = git_io.get_commit_message()
    if not commit_msg:
        return {'error': 'No commit message found', 'overall_valid': False}

    staged_files = git_io.get_staged_files()

    results = {
        'commit_message': commit_msg,
        'staged_files':   staged_files,
        'validations':    {}
    }

    # R0-driven validators (commit message only)
    results['validations']['changes'] = validate_changes.validate(commit_msg)
    results['validations']['f_tags']  = validate_f_tags.validate(commit_msg)

    # Per-file validators — R4 reads, R1 checks
    exec_results   = []
    qc_results     = []
    layer_violations = []

    for filepath in staged_files:
        if not filepath.endswith(('.py', '.js')):
            continue

        content = file_io.read_file(filepath)
        if content is None:
            continue

        exec_results.append(validate_execution.validate(filepath, content))
        qc_results.append(validate_operations.validate(filepath, content))
        layer_violations.extend(validate_r_layers.check_file(filepath, content))

    results['validations']['execution'] = {
        'valid': all(r.get('valid', True) for r in exec_results),
        'files': exec_results
    }

    results['validations']['qc'] = {
        'valid':      all(r.get('valid', True) for r in qc_results),
        'files':      qc_results,
        'violations': [v for r in qc_results for v in r.get('violations', [])]
    }

    results['validations']['r_layers'] = {
        'valid':      len(layer_violations) == 0,
        'violations': layer_violations
    }

    # Module detection
    modules_touched = set()
    for filepath in staged_files:
        module = get_module_from_filepath(filepath)
        if module:
            modules_touched.add(module)
    results['modules_touched'] = sorted(modules_touched)

    results['overall_valid'] = all(
        v.get('valid', True) for v in results['validations'].values()
    )

    return results


def validate_files(filepaths):
    """
    Run execution + QC validators against a list of files.
    Used by network-scan (R3) to get real results for scan_feature.
    """
    exec_valid = True
    qc_valid   = True
    qc_violations = []

    for filepath in filepaths:
        content = file_io.read_file(filepath)
        if content is None:
            continue
        e = validate_execution.validate(filepath, content)
        q = validate_operations.validate(filepath, content)
        if not e.get('valid', True):
            exec_valid = False
        if not q.get('valid', True):
            qc_valid = False
            qc_violations.extend(q.get('violations', []))

    return {
        'execution': {'valid': exec_valid},
        'qc':        {'valid': qc_valid, 'violations': qc_violations}
    }


def format_output(results):
    lines = []
    lines.append(la_output.header('LIVING ARCHITECTURE'))
    lines.append(f"  {results['commit_message']}")
    lines.append('')

    if results.get('modules_touched'):
        lines.append(f"  Modules: {', '.join(results['modules_touched'])}")
        lines.append('')

    # R-layers
    r_val = results['validations']['r_layers']
    if r_val['valid']:
        lines.append(f"  {'R-layers':14}{la_output.ok('')}")
    else:
        n = len(r_val['violations'])
        suffix = 's' if n != 1 else ''
        lines.append(f"  {'R-layers':14}{la_output.err(f'{n} violation{suffix}')}") 

    # F-tag
    f_tag_val = results['validations']['f_tags']
    if f_tag_val.get('valid'):
        f_tag_name = f_tag_val.get('f_tag', 'F-unknown')
        if f_tag_val.get('complete'):
            lines.append(f"  {f_tag_name:14}{la_output.ok('')}")
        else:
            missing = ', '.join(f_tag_val.get('layers_missing', []))
            lines.append(f"  {f_tag_name:14}{la_output.warn(f'missing {missing}')}")
    else:
        lines.append(f"  {'F-tag':14}{la_output.err(f_tag_val.get('error', 'Invalid'))}")

    # Execution
    exec_val = results['validations']['execution']
    lines.append(f"  {'Execution':14}{la_output.ok('') if exec_val['valid'] else la_output.err('')}")

    # QC
    qc_val = results['validations']['qc']
    if qc_val['valid']:
        lines.append(f"  {'QC':14}{la_output.ok('')}")
    else:
        violations = qc_val.get('violations', [])
        lines.append(f"  {'QC':14}{la_output.err(violations[0] if violations else 'violation')}")

    # C-code
    c_val = results['validations']['changes']
    if c_val.get('valid'):
        lines.append(f"  {'C-code':14}{la_output.ok(c_val.get('c_code', ''))}")
    else:
        lines.append(f"  {'C-code':14}{la_output.err(c_val.get('error', 'Invalid'))}")

    lines.append('')
    if results['overall_valid']:
        lines.append(f"  {la_output.ok(la_output.bold('COMMIT ALLOWED'))}")
    else:
        lines.append(f"  {la_output.err(la_output.bold('BLOCKED: Fix errors to proceed'))}")
    lines.append('')
    lines.append(la_output.divider())

    return '\n'.join(lines)


if __name__ == '__main__':
    results = run_all_validators()

    if 'error' in results:
        sys.exit(0)

    print(format_output(results))
    sys.exit(0 if results['overall_valid'] else 1)
