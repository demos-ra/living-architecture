#!/bin/bash
# System Governance Spec - Master Validator
# Runs all governance checks in sequence

set -e  # Exit on first failure

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SYSTEM GOVERNANCE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Track overall status
FAILED=0

# Change Classification Check
echo "1️⃣  Change Classification (C1-C5)"
echo "────────────────────────────────────────────────────────"
if ./tools/validate-change-classification.sh; then
    echo ""
else
    FAILED=1
fi

# Dependency Direction Check
echo "2️⃣  Dependency Direction (D2)"
echo "────────────────────────────────────────────────────────"
if python3 tools/validate-dependencies.py; then
    echo ""
else
    FAILED=1
fi

# Error Structure Check
echo "3️⃣  Error System Compliance"
echo "────────────────────────────────────────────────────────"
if python3 tools/validate-errors.py; then
    echo ""
else
    FAILED=1
fi

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    echo "✅ ALL GOVERNANCE CHECKS PASSED"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    exit 0
else
    echo "❌ GOVERNANCE VIOLATIONS DETECTED"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Please fix violations before merging."
    echo "See errors above for details."
    echo ""
    exit 1
fi
