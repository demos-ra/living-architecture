# Contributing to Living Architecture

Thank you for your interest in contributing!

---

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/living-architecture.git
   cd living-architecture
   ```

3. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```

---

## Making Changes

### Code Changes

1. Follow the R0-R5 architecture
2. Run validators before committing:
   ```bash
   bash tools/validate-all.sh
   ```

3. Ensure all tests pass:
   ```bash
   python3 tools/test-runner.py
   ```

### Documentation Changes

- Update relevant `.md` files in `docs/`
- Ensure internal links work
- Keep language clear and concise

---

## Commit Format

All commits must follow the standard format:

```
Layer: Description [R#/C#]
```

Examples:
```bash
git commit -m "Tools: Add layer detection [R4/C2]"
git commit -m "Docs: Update architecture guide [R0/C1]"
git commit -m "Framework: Add R0 support [R0/C4]"
```

See [docs/COMMIT_FORMAT.md](docs/COMMIT_FORMAT.md) for details.

### Layer Codes

- R0 • Config
- R1 • Domain
- R2 • Application
- R3 • Interface
- R4 • Infrastructure
- R5 • Presentation

### Classification Codes

- C1 • Internal (refactoring)
- C2 • Feature (new functionality)
- C3 • Contract (API changes)
- C4 • Structure (architecture changes)
- C5 • Migration (data migrations)

---

## Validation

### Required Validators

Before committing, ensure these pass:

```bash
# Check dependency flow
python3 tools/validate-dependencies.py --root .

# Check error structure
python3 tools/validate-errors.py --root .

# Run all validators
bash tools/validate-all.sh
```

### Git Hooks

The pre-commit hook runs automatically. To bypass temporarily:

```bash
git commit --no-verify -m "Message [R#/C#]"
```

Use `--no-verify` sparingly and only for work-in-progress commits.

---

## Pull Request Process

1. Update documentation if needed
2. Ensure all validators pass
3. Update CHANGELOG.md under "Unreleased" section
4. Push to your fork
5. Open a pull request with clear description

### PR Title Format

Use the same format as commits:

```
Layer: Description [R#/C#]
```

Example:
```
Tools: Add Python 3.12 support [R4/C2]
```

---

## Testing

### Run Tests Locally

```bash
# Run all tests
python3 tools/test-runner.py

# Test specific example
python3 tools/validate-dependencies.py --root examples/starter
```

### Test the NPM Package

```bash
cd packages/create-living-architecture
npm link
create-living-architecture test-project
cd test-project
# Verify structure created correctly
```

---

## Code Style

### Python

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Shell Scripts

- Use `#!/usr/bin/env bash`
- Add comments for complex logic
- Test on Linux/macOS

### Markdown

- Use consistent header levels
- Keep line length reasonable
- Use code blocks with language tags

---

## Adding New Features

### New Validator

1. Create script in `tools/`
2. Add to `tools/validate-all.sh`
3. Update `tools/README.md`
4. Add tests to `tools/test-runner.py`

### New Layer (R-group)

Major change requiring:
1. Update `docs/specs/00-framework.md`
2. Update `docs/ARCHITECTURE.md`
3. Update validators
4. Update all examples
5. Bump version to next major

### New Example

1. Create directory in `examples/`
2. Add README.md explaining the pattern
3. Update `examples/README.md`
4. Add validator tests

---

## Documentation Structure

```
docs/
├── README.md           # Documentation index
├── ARCHITECTURE.md     # Detailed R0-R5 guide
├── COMMIT_FORMAT.md    # Commit standards
├── DESIGN_SYSTEM.md    # Terminal output guidelines
├── CONSTITUTION.md     # Design philosophy
├── specs/              # Formal specifications
│   ├── 00-framework.md
│   ├── 01-architecture.md
│   ├── 02-operational.md
│   ├── 03-errors.md
│   └── 04-changes.md
└── law/                # JSON validation rules
    └── *.json
```

---

## Release Process

Maintainers only:

1. Update version in:
   - `packages/create-living-architecture/package.json`
   - Root `README.md`
   - `CHANGELOG.md`

2. Create release commit:
   ```bash
   git commit -m "Release: v1.1.0 [R0/C5]"
   git tag v1.1.0
   ```

3. Publish npm package:
   ```bash
   cd packages/create-living-architecture
   npm publish
   ```

4. Push to GitHub:
   ```bash
   git push origin main --tags
   ```

---

## Questions?

- Open an issue for bugs or feature requests
- Use discussions for questions about architecture
- Reference relevant documentation in issues

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
