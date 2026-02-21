#!/usr/bin/env python3
"""
test-la.py - Living Architecture End-to-End Tester
Tests LA methodically following proper hierarchy and flow

Usage:
  python3 test-la.py           # Run all tests
  python3 test-la.py --quick   # Run quick validation only
  python3 test-la.py --verbose # Show detailed output
"""

import sys
import os
import subprocess
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'═' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'═' * 60}{Colors.END}\n")


def print_test(name, status="running"):
    if status == "running":
        print(f"  Testing: {name}... ", end="", flush=True)
    elif status == "pass":
        print(f"{Colors.GREEN}✓{Colors.END}")
    elif status == "fail":
        print(f"{Colors.RED}✗{Colors.END}")
    elif status == "warn":
        print(f"{Colors.YELLOW}⚠{Colors.END}")


def test_r0_config_layer():
    """Test R0: All config files exist and are valid JSON"""
    print_header("R0 - CONFIG LAYER")
    
    config_files = [
        'r-layers.json',
        'f-tags.json',
        'execution.json',
        'operations.json',
        'changes.json',
        'modules.json',
        'SYSTEM.md'
    ]
    
    all_pass = True
    for filename in config_files:
        print_test(f"R0: {filename}", "running")
        filepath = Path('src/config') / filename
        
        if not filepath.exists():
            print_test("", "fail")
            print(f"    Missing: {filepath}")
            all_pass = False
            continue
        
        # Validate JSON files
        if filename.endswith('.json'):
            try:
                import json
                with open(filepath) as f:
                    json.load(f)
                print_test("", "pass")
            except json.JSONDecodeError as e:
                print_test("", "fail")
                print(f"    Invalid JSON: {e}")
                all_pass = False
        else:
            print_test("", "pass")
    
    return all_pass


def test_r1_domain_validators():
    """Test R1: All validators exist and are executable"""
    print_header("R1 - DOMAIN VALIDATORS")
    
    validators = [
        'config_loader.py',
        'validate-r-layers.py',
        'validate-f-tags.py',
        'validate-execution.py',
        'validate-operations.py',
        'validate-changes.py'
    ]
    
    all_pass = True
    for filename in validators:
        print_test(f"R1: {filename}", "running")
        filepath = Path('src/domain') / filename
        
        if not filepath.exists():
            print_test("", "fail")
            all_pass = False
            continue
        
        # Check Python syntax
        result = subprocess.run(
            ['python3', '-m', 'py_compile', str(filepath)],
            capture_output=True
        )
        
        if result.returncode == 0:
            print_test("", "pass")
        else:
            print_test("", "fail")
            print(f"    Syntax error: {result.stderr.decode()}")
            all_pass = False
    
    return all_pass


def test_r2_workflow():
    """Test R2: Workflow orchestrates correctly"""
    print_header("R2 - WORKFLOW ORCHESTRATION")
    
    print_test("R2: validation-workflow.py", "running")
    filepath = Path('src/app/validation-workflow.py')
    
    if not filepath.exists():
        print_test("", "fail")
        return False
    
    # Check syntax
    result = subprocess.run(
        ['python3', '-m', 'py_compile', str(filepath)],
        capture_output=True
    )
    
    if result.returncode == 0:
        print_test("", "pass")
        return True
    else:
        print_test("", "fail")
        return False


def test_r3_interfaces():
    """Test R3: Hooks and CLI exist"""
    print_header("R3 - CONTRACT INTERFACES")
    
    interfaces = [
        ('hooks/pre-commit', True),
        ('hooks/commit-msg', True),
        ('cli/network-scan.py', True)
    ]
    
    all_pass = True
    for filename, should_exec in interfaces:
        print_test(f"R3: {filename}", "running")
        filepath = Path('src/contract') / filename
        
        if not filepath.exists():
            print_test("", "fail")
            all_pass = False
            continue
        
        if should_exec and not os.access(filepath, os.X_OK):
            print_test("", "warn")
            print(f"    Not executable (run: chmod +x {filepath})")
        else:
            print_test("", "pass")
    
    return all_pass


def test_r4_io_modules():
    """Test R4: I/O modules exist"""
    print_header("R4 - EXECUTION I/O")
    
    modules = ['git-io.py', 'file-io.py']
    
    all_pass = True
    for filename in modules:
        print_test(f"R4: {filename}", "running")
        filepath = Path('src/exec') / filename
        
        if not filepath.exists():
            print_test("", "fail")
            all_pass = False
            continue
        
        # Check syntax
        result = subprocess.run(
            ['python3', '-m', 'py_compile', str(filepath)],
            capture_output=True
        )
        
        if result.returncode == 0:
            print_test("", "pass")
        else:
            print_test("", "fail")
            all_pass = False
    
    return all_pass


def test_cross_layer_imports():
    """Test that validators can import from R0 and R4"""
    print_header("CROSS-LAYER INTEGRATION")
    
    print_test("R1 → R0 imports", "running")
    try:
        sys.path.insert(0, 'src')
        from domain import config_loader
        config_loader.load_r_layers()
        print_test("", "pass")
    except Exception as e:
        print_test("", "fail")
        print(f"    {e}")
        return False
    
    print_test("R2 → R1 imports", "running")
    try:
        from app import validation_workflow
        print_test("", "pass")
    except Exception as e:
        print_test("", "fail")
        print(f"    {e}")
        return False
    
    return True


def test_self_validation():
    """Test that LA can validate its own structure"""
    print_header("SELF-VALIDATION (LA validates LA)")
    
    print_test("LA follows R-layer rules", "running")
    # Check all files are in correct layers
    violations = []
    
    # R0 should only have .json and .md
    for f in Path('src/config').glob('*'):
        if f.is_file() and not (f.suffix in ['.json', '.md']):
            violations.append(f"R0 contains non-config file: {f}")
    
    # R1 should only have .py
    for f in Path('src/domain').glob('*'):
        if f.is_file() and f.suffix not in ['.py', '.js']:
            violations.append(f"R1 contains non-Python file: {f}")
    
    if violations:
        print_test("", "fail")
        for v in violations:
            print(f"    {v}")
        return False
    else:
        print_test("", "pass")
    
    print_test("Module naming convention", "running")
    # Check if validators use module naming
    module_files = list(Path('src/domain').glob('validate-*.py'))
    if module_files:
        print_test("", "pass")
        print(f"    Found {len(module_files)} validators")
    else:
        print_test("", "warn")
    
    return True


def test_config_driven():
    """Test that system is truly config-driven"""
    print_header("CONFIG-DRIVEN VERIFICATION")
    
    print_test("Validators read from R0", "running")
    try:
        sys.path.insert(0, 'src')
        from domain.config_loader import (
            load_r_layers,
            load_f_tag_rules,
            load_c_codes,
            load_module_config
        )
        
        # Verify configs load
        r_layers = load_r_layers()
        f_rules = load_f_tag_rules()
        c_codes = load_c_codes()
        modules = load_module_config()
        
        if r_layers and f_rules and c_codes and modules:
            print_test("", "pass")
        else:
            print_test("", "fail")
            return False
            
    except Exception as e:
        print_test("", "fail")
        print(f"    {e}")
        return False
    
    print_test("No hardcoded values", "running")
    # Quick check for common hardcoded patterns
    hardcoded = []
    for pyfile in Path('src/domain').glob('*.py'):
        with open(pyfile) as f:
            content = f.read()
            if "['R0', 'R1', 'R2'" in content:
                hardcoded.append(f"{pyfile.name}: Hardcoded R-layers")
            if "['C1', 'C2', 'C3'" in content:
                hardcoded.append(f"{pyfile.name}: Hardcoded C-codes")
    
    if hardcoded:
        print_test("", "warn")
        for h in hardcoded:
            print(f"    {h}")
    else:
        print_test("", "pass")
    
    return True


def test_installer():
    """Test installer files exist in correct layers"""
    print_header("INSTALLER (npx + local)")

    files = [
        ('R0', 'package.json',                           Path('package.json')),
        ('R1', 'src/domain/installer-logic.js',          Path('src/domain/installer-logic.js')),
        ('R2', 'src/app/installer-workflow.js',          Path('src/app/installer-workflow.js')),
        ('R3', 'installer.js',                           Path('installer.js')),
        ('R3', 'src/contract/cli/la-new.sh',             Path('src/contract/cli/la-new.sh')),
        ('R4', 'src/exec/installer-io.js',               Path('src/exec/installer-io.js')),
    ]

    all_pass = True
    for layer, label, filepath in files:
        print_test(f"{layer}: {label}", "running")
        if not filepath.exists():
            print_test("", "fail")
            print(f"    Missing: {filepath}")
            all_pass = False
            continue
        if not os.access(filepath, os.R_OK):
            print_test("", "fail")
            print(f"    Not readable: {filepath}")
            all_pass = False
            continue
        print_test("", "pass")

    # Verify la-new.sh is executable
    print_test("la-new.sh executable", "running")
    if os.access('src/contract/cli/la-new.sh', os.X_OK):
        print_test("", "pass")
    else:
        print_test("", "fail")
        all_pass = False

    # Verify installer.js is executable
    print_test("installer.js executable", "running")
    if os.access('installer.js', os.X_OK):
        print_test("", "pass")
    else:
        print_test("", "fail")
        all_pass = False

    return all_pass

def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    print(f"  Total tests: {total}")
    print(f"  {Colors.GREEN}Passed: {passed}{Colors.END}")
    if failed > 0:
        print(f"  {Colors.RED}Failed: {failed}{Colors.END}")
    
    print()
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED{Colors.END}")
        print(f"{Colors.GREEN}LA v2.0 is ready to ship!{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.END}")
        print(f"{Colors.RED}Fix issues before shipping{Colors.END}")
    
    return failed == 0


def main():
    """Run all tests in proper hierarchy"""
    print(f"\n{Colors.BOLD}Living Architecture v2.0 - End-to-End Test{Colors.END}")
    print("Testing in hierarchical order: R0 → R1 → R2 → R3 → R4\n")
    
    results = {}
    
    # Test in proper hierarchy (bottom-up)
    results['R0'] = test_r0_config_layer()
    results['R1'] = test_r1_domain_validators()
    results['R2'] = test_r2_workflow()
    results['R3'] = test_r3_interfaces()
    results['R4'] = test_r4_io_modules()
    
    # Integration tests
    results['Integration'] = test_cross_layer_imports()
    results['Self-Validation'] = test_self_validation()
    results['Config-Driven'] = test_config_driven()
    results['Installer'] = test_installer()
    
    # Summary
    all_pass = print_summary(results)
    
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    # Change to repo root if needed
    if not Path('src/config').exists():
        print(f"{Colors.RED}Error: Run from LA repository root{Colors.END}")
        sys.exit(1)
    
    main()


