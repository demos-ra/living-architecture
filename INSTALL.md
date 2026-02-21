# Living Architecture v2.0 - Installation & Testing Guide

## Quick Start

### 1. Install Locally
```bash
# Extract the archive
tar -xzf living-architecture-v2.0.tar.gz
cd living-architecture-v2.0

# Run end-to-end tests
python3 test-la.py
```

### 2. Test in Your Project
```bash
# Copy LA into your project
cp -r living-architecture-v2.0/* /path/to/your/project/

# Or link the hooks
cd /path/to/your/project
ln -s /full/path/to/living-architecture-v2.0/src/contract/hooks/pre-commit .git/hooks/
```

### 3. Verify Installation
```bash
# Test that hooks work
git add .
git commit -m "[F-test/R1/C2] Test commit"
# Should show LA validation output
```

## End-to-End Tester

The `test-la.py` script validates LA methodically:

```bash
# Run all tests
python3 test-la.py

# Test hierarchy:
# ✓ R0 - Config layer (all JSON files valid)
# ✓ R1 - Domain validators (syntax correct)
# ✓ R2 - Workflow orchestration
# ✓ R3 - Contract interfaces (hooks, CLI)
# ✓ R4 - Execution I/O
# ✓ Integration (cross-layer imports work)
# ✓ Self-validation (LA follows its own rules)
# ✓ Config-driven (no hardcoded values)
```

## What Gets Tested

### Structure Tests
- All R0 config files exist and are valid JSON
- All R1 validators exist and have valid Python syntax
- R2 workflow can import R1 validators
- R3 hooks and CLI exist
- R4 I/O modules exist

### Integration Tests
- R1 can import from R0 (config_loader works)
- R2 can import from R1 (validators accessible)
- Cross-layer communication works

### Self-Validation Tests
- LA follows its own R-layer rules
- No files in wrong layers
- Module naming convention followed

### Config-Driven Tests
- Validators read from R0 configs
- No hardcoded R-layer IDs
- No hardcoded C-codes
- Module config controls behavior

## Push to GitHub

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "[F-la/R0/C2] Initial LA v2.0 release"

# Add GitHub remote
git remote add origin https://github.com/YOUR-USERNAME/living-architecture.git

# Push
git branch -M main
git push -u origin main
```

## Expected Test Output

```
Living Architecture v2.0 - End-to-End Test
Testing in hierarchical order: R0 → R1 → R2 → R3 → R4

============================================================
                    R0 - CONFIG LAYER                      
============================================================

  Testing: R0: r-layers.json... ✓
  Testing: R0: f-tags.json... ✓
  Testing: R0: execution.json... ✓
  Testing: R0: operations.json... ✓
  Testing: R0: changes.json... ✓
  Testing: R0: modules.json... ✓
  Testing: R0: SYSTEM.md... ✓

[... continues through all layers ...]

============================================================
                      TEST SUMMARY                         
============================================================

  Total tests: 8
  Passed: 8

✓ ALL TESTS PASSED
LA v2.0 is ready to ship!
```

## Troubleshooting

### Test fails with import errors
```bash
# Make sure you're in the repo root
cd living-architecture-v2.0
python3 test-la.py
```

### Hooks not executable
```bash
chmod +x src/contract/hooks/pre-commit
chmod +x src/contract/cli/network-scan.py
```

### Module detection not working
```bash
# Check modules.json has enabled: true
cat src/config/modules.json
```

## Next Steps

1. Run `python3 test-la.py` - verify all tests pass
2. Test in a sample project
3. Push to GitHub
4. Share with team

Perfect. Precise. Ready to ship.
