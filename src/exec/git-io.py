#!/usr/bin/env python3
"""
git-io.py - R4 Git I/O Operations
Handles git operations needed by R2 validation-workflow.
"""

import subprocess
import sys
import os


def run_git_command(args):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f'Git error: {e.stderr}', file=sys.stderr)
        return None


def get_staged_files():
    """Get list of staged files."""
    output = run_git_command(['diff', '--staged', '--name-only'])
    if output:
        return [f for f in output.split('\n') if f]
    return []


def get_commit_message():
    """
    Get the commit message.
    commit-msg hook passes file path via LA_COMMIT_MSG_FILE env var.
    Falls back to COMMIT_EDITMSG for other contexts.
    """
    msg_file = os.environ.get('LA_COMMIT_MSG_FILE')
    if msg_file and os.path.exists(msg_file):
        try:
            with open(msg_file, 'r') as f:
                return f.read().strip()
        except IOError:
            pass

    try:
        with open('.git/COMMIT_EDITMSG', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


if __name__ == '__main__':
    print('Git I/O Operations')
    print(f'Staged files: {get_staged_files()}')
    print(f'Commit message: {get_commit_message()}')
