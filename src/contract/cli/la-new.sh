#!/bin/bash
#
# la-new.sh - R3 Contract (local installer)
# Usage: ./la-new.sh <project-name>
#

LA_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"

BORDER="════════════════════════════════════════════════════════════"

if [ -z "$1" ]; then
    echo "Usage: ./la-new.sh <project-name>"
    echo "Example: ./la-new.sh my-app"
    exit 1
fi

PROJECT_NAME="$1"

if [ -d "$PROJECT_NAME" ]; then
    echo "✗ Directory '$PROJECT_NAME' already exists"
    exit 1
fi

echo ""
echo "$BORDER"
printf "%*s\n" $(( (${#BORDER} + 18) / 2 )) "LIVING ARCHITECTURE"
echo "$BORDER"
echo ""
echo "  Creating project: $PROJECT_NAME"

# Copy LA structure
mkdir -p "$PROJECT_NAME"
cp -r "$LA_DIR/src"          "$PROJECT_NAME/src"
cp -r "$LA_DIR/.living-arch" "$PROJECT_NAME/.living-arch"

# Init git
git init "$PROJECT_NAME" --quiet

# Hook up pre-commit and commit-msg
chmod +x "$PROJECT_NAME/src/contract/hooks/pre-commit"
chmod +x "$PROJECT_NAME/src/contract/hooks/commit-msg"

ln -sf "$(pwd)/$PROJECT_NAME/src/contract/hooks/pre-commit" \
       "$PROJECT_NAME/.git/hooks/pre-commit"

ln -sf "$(pwd)/$PROJECT_NAME/src/contract/hooks/commit-msg" \
       "$PROJECT_NAME/.git/hooks/commit-msg"

# Initial commit — skip validation, this is scaffolding not app code
cd "$PROJECT_NAME"
git add .
git commit --no-verify -m "LA v2.0 scaffold" --quiet
cd ..

echo ""
echo "  ✓ Project created: $PROJECT_NAME/"
echo "  ✓ Git initialized"
echo "  ✓ Hooks installed"
echo "  ✓ Initial commit done"
echo ""
echo "  Ready:  cd $PROJECT_NAME"
echo ""
echo "$BORDER"
echo ""
