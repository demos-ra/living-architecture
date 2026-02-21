# Living Architecture - Project Guide

## R-Layer Gravity

- **R0** `src/config/` - Pure configuration
- **R1** `src/domain/` - Pure business logic
- **R2** `src/app/` - Orchestration & workflows
- **R3** `src/contract/` - API boundaries & interfaces
- **R4** `src/exec/` - I/O operations

## Commit Format

```
[F-feature-name/R#/C#] Description
```

**Examples:**
- `[F-login/R1/C2] Add password validation logic`
- `[F-payments/R4/C2] Add Stripe API integration`
- `[F-checkout/R2/C1] Refactor cart workflow`

## Change Codes (C#)

- **C1** - Internal refactoring
- **C2** - New feature
- **C3** - API/contract change
- **C4** - R-layer restructure
- **C5** - Migration

## Module Naming Convention (Optional)

Group related code across ALL R-layers using module prefixes:

**Format:** `{module}-{component}.ext`

**Example - Auth module:**
```
R0/config/auth-rules.json
R1/domain/auth-login.py
R2/app/auth-workflow.py
R3/contract/auth-api.js
R4/exec/auth-db.py
```

**Benefits:**
- Visual grouping across layers
- Easy searching: `find . -name "auth-*"`
- Validators display module info
- **Entirely optional** - use if helpful

## Commands

```bash
network-scan              # See all features
network-scan F-login      # Analyze one feature
```

Let code settle at its natural gravity level.
