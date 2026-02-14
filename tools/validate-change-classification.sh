#!/bin/bash
# System Governance Spec - Change Classification Validator
# Ensures commit messages include [C1], [C2], [C3], [C4], or [C5]

set -e

# Get the most recent commit message
COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null || echo "")

# If no git history (new repo), skip check
if [ -z "$COMMIT_MSG" ]; then
    echo "⚠️  No git history found - skipping change classification check"
    exit 0
fi

# Check for classification tag
if echo "$COMMIT_MSG" | grep -qE '^\[C[1-5]\]'; then
    CLASSIFICATION=$(echo "$COMMIT_MSG" | grep -oE '\[C[1-5]\]')
    echo "✅ Change classification found: $CLASSIFICATION"
    exit 0
else
    echo ""
    echo "❌ ERROR: Commit message must start with change classification"
    echo ""
    echo "Current commit message:"
    echo "  $COMMIT_MSG"
    echo ""
    echo "Required format: [C1-C5] Description"
    echo ""
    echo "Change Classifications:"
    echo "  [C1] Local Implementation Change (internal logic only)"
    echo "  [C2] Behavioral Change (observable effects, stable contracts)"
    echo "  [C3] Contract Change (API/schema modification)"
    echo "  [C4] Structural Change (architectural boundaries)"
    echo "  [C5] Data Evolution Change (schema migration)"
    echo ""
    echo "Examples:"
    echo "  [C1] Refactor user validation logic"
    echo "  [C2] Strengthen email validation rules"
    echo "  [C3] Add optional 'timezone' field to User API"
    echo "  [C4] Move authentication from R4 to R2"
    echo "  [C5] Add 'last_login' timestamp to users table"
    echo ""
    exit 1
fi
