# Living Architecture

Code organized by dependency gravity.

```
npx create-living-architecture my-project
```

---

## Philosophy

Systems stabilize when dependency direction is consistent.

Dependencies create weight.

• Zero dependencies → core
• Maximum dependencies → periphery

Living Architecture formalizes this model using four layers (R1–R4).
Validators enforce unidirectional flow. Structure remains consistent
over time.

---

## Gravitational laws

### Law 1: Dependency weight

Components belong in layers proportional to dependency count.

• Zero dependencies → R1 • Domain
• Maximum dependencies → R4 • Integrations

Heavy components do not belong in the core.
Core logic does not depend outward.

---

### Law 2: Unidirectional flow

Dependencies flow toward the core.

Allowed:

```
R4 → R3 → R2 → R1
```

Forbidden:

```
R1 ↛ R2 ↛ R3 ↛ R4
```

Violations block commit.

---

### Law 3: Natural settling

Correct placement reduces refactoring pressure.
Incorrect placement increases friction.

Friction indicates structural misalignment.

---

## System design

Four fixed layers organized by dependency weight.
Layer boundaries are enforced automatically.

R1 • Domain
R2 • Database
R3 • API
R4 • Integrations

Layers are structural constraints, not conventions.

R1 contains interfaces and pure domain.
R2 contains implementations.
R3 contains orchestration.
R4 contains adapters.

### R1 • Domain

Core business logic.
Zero external dependencies.
Changes when business rules change.

### R2 • Database

Persistence layer.
Depends only on domain.
Changes when data model evolves.

### R3 • API

HTTP endpoints.
Orchestrates domain and database.
Changes when client needs change.

### R4 • Integrations

External systems and UI.
Adapts domain to outside world.
Changes when external systems change.

Full specification: `ARCHITECTURE.md`

---

## Performance

Gravitational alignment improves structural consistency and reduces
architectural drift over time.

Observed effects when dependency flow is enforced:

• Initial placement accuracy — Increased
• Reorganization cycles — Reduced
• AI collaboration — Increased structural predictability
• Architectural drift — Reduced
• Cognitive load — Reduced
• Developer onboarding — Faster
• Change impact analysis — More localized and traceable

When validators enforce flow:

• Core logic remains stable
• Integrations remain replaceable
• Refactors stay localized

---

## Install

### New project

```
npx create-living-architecture my-project
cd my-project
```

### Existing project

```
cd your-project
npx create-living-architecture .
```

Structure created. Validators installed.

---

## Workflow

Human prompts AI.
AI generates code in appropriate layers.
Validators enforce laws.

Example:

H:

"Add user email verification"

AI generates:

```
src/domain/user_verification.py
src/integrations/email_service.py
src/api/verification_routes.py
```

Commit:

```
Domain: Add user verification [R1/C2]
```

Validation:

```
Dependencies
  ✓ Flow correct

Tests
  ✓ All pass
```

Post-commit:

```
COMMIT: Domain: Add user verification [a3f891c]

R1 • Domain
  user_verification.py ● ONLINE

R3 • API
  verification_routes.py ● ONLINE

R4 • Integrations
  email_service.py ● ONLINE

STATUS: ● ALL ONLINE
```

---

## Commits

Required format:

```
Layer: Description [R#/C#]
```

Examples:

```
Domain: Add user entity [R1/C2]
Database: Add user persistence [R2/C2]
API: Add registration endpoint [R3/C2]
Integrations: Add email service [R4/C2]
Database: Add timestamps [R2/C5]
```

### Layer codes

R1 • Domain
R2 • Database
R3 • API
R4 • Integrations

### Classification codes

C1 • Internal
C2 • Feature
C3 • Contract
C4 • Structure
C5 • Migration

Commit format enforced via commit-msg hook.

---

## Validation

### Pre-commit

```
Validating

Dependencies
  ✓ Flow correct

Tests
  ✓ All pass
```

Failure:

```
Validating

Dependencies
  ✓ Flow correct

Tests
  ✗ 2 failures
    test_user_verification
    test_email_format

Fix tests before committing
```

---

### Error example

```
Dependencies
  ✗ Violation detected
    domain/user.py imports database/repository.py

Fix: Remove import or use dependency inversion
```

---

## Dashboard

View domain changes:

```
git log --oneline --grep="^Domain"
```

View structural or migration changes:

```
git log --oneline --grep="C[45]"
```

Filter by layer:

```
git log --oneline --grep="R1"
```

Git history becomes architectural view.

---

## Requirements

• Node.js 18+
• Git 2.0+
• Python 3.8+ (optional for test validation)

---

## Bypass

```
git commit --no-verify -m "Work in progress [R1/C2]"
```

Use sparingly.

---

## Configuration

```
.living-arch/
  law/
  tools/
```

Modify JSON rules.
Extend validators in `tools/`.

---

## Status

Version: 1.0.0
License: MIT
Repository: https://github.com/demos-ra/living-architecture

Gravitational rules enforced.
Structure remains consistent.
