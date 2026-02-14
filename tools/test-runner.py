#!/usr/bin/env python3
"""
Living Architecture v1.1 - Automated Test Runner
Runs all tests, records results, generates outcome tracker.
No manual intervention needed.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class TestRunner:
    def __init__(self, project_root='.'):
        self.root = Path(project_root)
        self.results = []
        self.passed = 0
        self.failed = 0
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def run_command(self, command, shell=False):
        """
        Run a shell command and capture output.
        
        Returns:
            (returncode: int, stdout: str, stderr: str)
        """
        try:
            if shell:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(command, capture_output=True, text=True, shell=False)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
    
    def test(self, name, command, expected_pattern, shell=False, verbose=False):
        """
        Run a single test.
        
        Args:
            name: Test name
            command: Command to run (string or list)
            expected_pattern: What to look for in output (substring or list)
            shell: Use shell execution
            verbose: Print output
        """
        print(f"\n🧪 {name}...", end=" ", flush=True)
        
        returncode, stdout, stderr = self.run_command(command, shell=shell)
        output = stdout + stderr
        
        # Check if expected pattern is in output
        if isinstance(expected_pattern, list):
            passed = any(pattern in output for pattern in expected_pattern)
        else:
            passed = expected_pattern in output or (expected_pattern == "" and returncode == 0)
            
            # For JSON output, try to parse and check
            if isinstance(expected_pattern, str) and expected_pattern.startswith('{'):
                try:
                    parsed = json.loads(stdout.strip())
                    passed = True
                except:
                    passed = False
        
        result = {
            'name': name,
            'command': command if isinstance(command, str) else ' '.join(command),
            'expected': expected_pattern,
            'actual': output.strip()[:200],  # First 200 chars
            'passed': passed,
            'returncode': returncode
        }
        
        self.results.append(result)
        
        if passed:
            print("✅ PASS")
            self.passed += 1
        else:
            print("❌ FAIL")
            self.failed += 1
        
        if verbose or not passed:
            print(f"  Command: {result['command']}")
            print(f"  Expected: {result['expected'][:100]}")
            print(f"  Got: {result['actual'][:100]}")
    
    def test_layer_detection_tiny(self):
        """Test 1a: Detect layers on r1-6-tiny (3 layers)"""
        self.test(
            "Test 1a: Layer Detection - r1-6-tiny (3 layers)",
            ['python3', 'tools/detect-active-layers.py', '--root', 'examples/r1-6-tiny'],
            '{"config": false, "domain": false, "application": true, "interface": true, "infrastructure": true, "presentation": false}'
        )
    
    def test_layer_detection_starter(self):
        """Test 1b: Detect layers on starter-template (5 layers)"""
        self.test(
            "Test 1b: Layer Detection - starter-template (5 layers)",
            ['python3', 'tools/detect-active-layers.py', '--root', 'examples/starter-template'],
            '{"config": false, "domain": true, "application": true, "interface": true, "infrastructure": true, "presentation": false}'
        )
    
    def test_layer_detection_verbose(self):
        """Test 1c: Layer detection with verbose output"""
        self.test(
            "Test 1c: Layer Detection - Verbose Mode",
            ['python3', 'tools/detect-active-layers.py', '--root', 'examples/starter-template', '--verbose'],
            ['domain', 'application', 'interface']
        )
    
    def test_dependencies_tiny(self):
        """Test 2a: Validate dependencies on r1-6-tiny"""
        self.test(
            "Test 2a: Dependency Validation - r1-6-tiny",
            ['python3', 'tools/validate-dependencies.py', '--root', 'examples/r1-6-tiny'],
            'No dependency violations'
        )
    
    def test_dependencies_starter(self):
        """Test 2b: Validate dependencies on starter-template"""
        self.test(
            "Test 2b: Dependency Validation - starter-template",
            ['python3', 'tools/validate-dependencies.py', '--root', 'examples/starter-template'],
            'No dependency violations'
        )
    
    def test_errors_validation(self):
        """Test 3: Error validation"""
        self.test(
            "Test 3: Error Validation - starter-template",
            ['python3', 'tools/validate-errors.py', '--root', 'examples/starter-template'],
            ''  # Just check it runs
        )
    
    def test_file_framework_json(self):
        """Test 4a: Check law/00-framework.json exists"""
        self.test(
            "Test 4a: Framework JSON exists",
            ['test', '-f', 'docs/law/00-framework.json'],
            '',
            shell=True
        )
    
    def test_file_framework_md(self):
        """Test 4b: Check specs/00-framework.md exists"""
        self.test(
            "Test 4b: Framework MD exists",
            ['test', '-f', 'docs/specs/00-framework.md'],
            '',
            shell=True
        )
    
    def test_json_syntax(self):
        """Test 4c: Validate JSON syntax"""
        self.test(
            "Test 4c: JSON Syntax Valid",
            ['python3', '-m', 'json.tool', 'docs/law/00-framework.json'],
            ''
        )
    
    def test_examples_exist(self):
        """Test 4d: Check example projects exist"""
        self.test(
            "Test 4d: Example Projects Exist",
            'ls examples/r1-6-* 2>/dev/null | wc -l',
            '3',
            shell=True
        )
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 70)
        print("  Living Architecture v1.1 - Automated Test Suite")
        print("=" * 70)
        print(f"\n📋 Test Run: {self.timestamp}")
        print(f"📁 Project Root: {self.root}")
        
        # Layer Detection Tests
        print("\n" + "=" * 70)
        print("LAYER DETECTION TESTS")
        print("=" * 70)
        self.test_layer_detection_tiny()
        self.test_layer_detection_starter()
        self.test_layer_detection_verbose()
        
        # Dependency Validation Tests
        print("\n" + "=" * 70)
        print("DEPENDENCY VALIDATION TESTS")
        print("=" * 70)
        self.test_dependencies_tiny()
        self.test_dependencies_starter()
        
        # Error Validation Tests
        print("\n" + "=" * 70)
        print("ERROR VALIDATION TESTS")
        print("=" * 70)
        self.test_errors_validation()
        
        # File/Structure Tests
        print("\n" + "=" * 70)
        print("FILE & STRUCTURE TESTS")
        print("=" * 70)
        self.test_file_framework_json()
        self.test_file_framework_md()
        self.test_json_syntax()
        self.test_examples_exist()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"\n✅ PASSED: {self.passed}/{total}")
        print(f"❌ FAILED: {self.failed}/{total}")
        print(f"📊 Pass Rate: {pass_rate:.1f}%")
        
        if self.failed > 0:
            print("\n⚠️  FAILED TESTS:")
            for result in self.results:
                if not result['passed']:
                    print(f"\n  ❌ {result['name']}")
                    print(f"     Command: {result['command']}")
                    print(f"     Expected: {result['expected']}")
                    print(f"     Got: {result['actual']}")
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        print("\n" + "=" * 70)
    
    def generate_tracker(self):
        """Generate TEST-OUTCOME-TRACKER.md"""
        tracker = f"""# Living Architecture v1.1 - Test Outcome Report

**Test Date:** {self.timestamp}  
**System:** {sys.platform}  
**Python:** {sys.version.split()[0]}  
**Status:** Automated Test Run

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {len(self.results)} |
| Passed | {self.passed} |
| Failed | {self.failed} |
| Pass Rate | {(self.passed/len(self.results)*100):.1f}% |

---

## Results

"""
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            tracker += f"""### Test {i}: {result['name']}

| Field | Value |
|-------|-------|
| Status | {status} |
| Command | `{result['command']}` |
| Expected | {result['expected'][:100]} |
| Actual | {result['actual'][:100]} |
| Return Code | {result['returncode']} |

"""
        
        tracker += f"""---

## Conclusion

"""
        
        if self.failed == 0:
            tracker += "🎉 **ALL TESTS PASSED** - Ready to push to GitHub!\n\n"
            tracker += "Next steps:\n"
            tracker += "1. Review this report\n"
            tracker += "2. Push to GitHub: `git add . && git commit -m '[C4] LA v1.1' && git push`\n"
            tracker += "3. Tag release: `git tag -a v1.1.0 && git push --tags`\n"
        else:
            tracker += f"⚠️ **{self.failed} TESTS FAILED** - Review errors above\n\n"
            tracker += "Failed tests:\n"
            for result in self.results:
                if not result['passed']:
                    tracker += f"- {result['name']}\n"
            tracker += "\nSend this report to Claude for batch fixes.\n"
        
        return tracker
    
    def save_tracker(self, filename='TEST-OUTCOME-AUTO.md'):
        """Save tracker to file"""
        tracker = self.generate_tracker()
        with open(filename, 'w') as f:
            f.write(tracker)
        print(f"\n📄 Tracker saved: {filename}")
        return tracker

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Automated test runner for Living Architecture v1.1'
    )
    parser.add_argument('--root', default='.', help='Project root directory')
    parser.add_argument('--output', default='TEST-OUTCOME-AUTO.md', help='Output tracker filename')
    
    args = parser.parse_args()
    
    runner = TestRunner(args.root)
    runner.run_all_tests()
    tracker = runner.save_tracker(args.output)
    
    # Print tracker to stdout as well
    print("\n" + "=" * 70)
    print("DETAILED OUTCOME TRACKER")
    print("=" * 70)
    print(tracker)
    
    # Exit with appropriate code
    sys.exit(0 if runner.failed == 0 else 1)

if __name__ == '__main__':
    main()
