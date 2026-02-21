#!/usr/bin/env python3
"""
la-output.py - R1 Domain
Standard output formatting for all LA interfaces.
Single source of truth for borders, colors, width.
"""

WIDTH = 60
BORDER = '═' * WIDTH

# ANSI colors
PURPLE = '\033[94m'
BOLD   = '\033[1m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m'
RESET  = '\033[0m'


def header(text):
    """Centered header with double-line borders."""
    return (
        f"\n{PURPLE}{BOLD}{BORDER}{RESET}\n"
        f"{PURPLE}{BOLD}{text:^{WIDTH}}{RESET}\n"
        f"{PURPLE}{BOLD}{BORDER}{RESET}\n"
    )


def divider():
    return f"{PURPLE}{BORDER}{RESET}"


def ok(text):
    return f"{GREEN}✓{RESET} {text}"


def warn(text):
    return f"{YELLOW}⚠{RESET} {text}"


def err(text):
    return f"{RED}✗{RESET} {text}"


def bold(text):
    return f"{BOLD}{text}{RESET}"
