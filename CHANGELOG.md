# Changelog

All notable changes to Living Architecture will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-02-15

### Changed

- **BREAKING:** Migrated from R1-R4 to R0-R5 pluggable framework
- Updated all documentation to use R0-R5 naming consistently
- Moved detailed documentation to `docs/` directory for better organization
- Restructured examples with clearer naming: `minimal-r3-r4/`, `standard-r1-r4/`, `full-r0-r5/`
- Renamed `starter-template/` to `starter/` for clarity
- Consolidated template files to eliminate duplication

### Added

- **R0 • CONFIG** layer (optional) - Environment and deployment configuration
- **R2 • APPLICATION** layer (optional) - Workflows and use cases
- **R5 • PRESENTATION** layer (optional) - UI and rendering
- `CONTRIBUTING.md` - Contribution guidelines for developers
- `CHANGELOG.md` - Version history tracking
- `.gitignore` - Proper ignore patterns for OS, Python, and Node files
- `docs/README.md` - Documentation navigation guide
- `examples/README.md` - Example catalog with descriptions
- Migration guide in README for users familiar with R1-R4 system

### Removed

- `TEST-OUTCOME-TRACKER.md` - Internal testing artifact
- `TEST-OUTCOME-AUTO.md` - Temporary test results
- `TESTING-GUIDE.md` - Internal testing documentation
- Duplicate template files in `packages/.../templates/starter-template/`
- Redundant ARCHITECTURE.md files (consolidated into `docs/ARCHITECTURE.md`)

### Fixed

- Version mismatch between README.md (was 1.0.0) and package.json (1.0.8)
- Template duplication in npm package structure
- Inconsistent layer naming across documentation
- Broken documentation hierarchy (truth was buried in specs/)
- Examples using outdated R1-R4 nomenclature

---

## [1.0.8] - 2025-XX-XX

### Added
- Improved validation scripts
- Enhanced error detection

### Fixed
- Minor bug fixes in dependency validators

---

## [1.0.0] - 2025-02-08

### Added
- Initial release with R1-R4 architecture system
- Git hook validators for dependency flow
- Pre-commit, commit-msg, and post-commit hooks
- Commit format enforcement
- `npx create-living-architecture` scaffolding tool
- Basic documentation and examples
- Dependency validation tools
- Error structure validation
- Change classification system

### Features
- Four-layer architecture (R1-R4)
- Automatic dependency validation
- Git commit format enforcement
- Project scaffolding via npm

---

## Migration Notes

### From 1.0.x to 1.1.0

If you have an existing project using the old R1-R4 system:

**Layer Mapping:**
- R1 (Domain) → R1 (DOMAIN) ✓ Same
- R2 (Database) → R4 (INFRASTRUCTURE) ⚠️ Renamed
- R3 (API) → R3 (INTERFACE) ⚠️ Renamed
- R4 (Integrations) → R4 (INFRASTRUCTURE) ⚠️ Merged

**New Layers Available:**
- R0 (CONFIG) - Optional root layer for configuration
- R2 (APPLICATION) - Optional layer for workflows
- R5 (PRESENTATION) - Optional layer for UI

**Action Required:**
1. Review your layer organization
2. Update import paths if renaming layers
3. Update commit messages to use new layer names
4. Re-run validators: `bash tools/validate-all.sh`

The core principles remain unchanged: dependency gravity, unidirectional flow, and automatic validation.
