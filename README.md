# Living Architecture

Pluggable dependency architecture. Start minimal, grow as needed.

```bash
npx create-living-architecture my-project
```

---

## Philosophy

Systems stabilize when dependency direction is consistent.

Dependencies create weight.

• Zero dependencies → core  
• Maximum dependencies → periphery

Living Architecture formalizes this using a pluggable R0-R5 framework. Start with 2 required layers, add optional layers as complexity grows. Validators enforce unidirectional flow automatically.

---

## The R0-R5 System

Six responsibility groups. Two required, four optional.

### Required Layers (Always Present)

**R3 • INTERFACE**  
API boundaries and contracts  
• REST endpoints, GraphQL resolvers  
• Input/output translation  
• Cannot depend on R4 or R5

**R4 • INFRASTRUCTURE**  
External world interactions  
• Database repositories  
• Message queues, caches  
• Third-party API clients  
• Cannot depend on R3 or R5

### Optional Layers (Add When Needed)

**R0 • CONFIG** (when: >5 config concerns)  
Environment and deployment  
• Feature flags  
• Multi-tenant configuration  
• Deployment parameters

**R1 • DOMAIN** (when: >10 business rules)  
Business entities and invariants  
• User, Order, Payment entities  
• Business rule validation  
• Pure domain logic

**R2 • APPLICATION** (when: >3 workflows)  
Use cases and orchestration  
• CreateOrder workflow  
• UserRegistration process  
• State machines

**R5 • PRESENTATION** (when: >1 frontend)  
UI and rendering  
• React components  
• Mobile app  
• Admin dashboard

---

## Dependency Flow

Dependencies flow toward the core.

```
R5 → R3 → R2 → R1 → R0
     ↓         ↓    ↓
     R4 -------+----+
```

Rules:
- R0 depends on nothing
- R1 depends on R0 only
- R2 depends on R0, R1
- R3 depends on R0, R1, R2
- R4 depends on R0, R1, R2 (never R3 or R5)
- R5 depends on R0, R3 only

Violations block commit.

---

## Project Evolution

### Tiny (MVP, Week 1)

```
Active: R3, R4
Validators: Check 2-layer dependencies only
Example: Startup prototype
Files: ~50-100
```

Start with just INTERFACE + INFRASTRUCTURE.

### Small (6 months)

```
Active: R1, R2, R3, R4
Validators: Check 4-layer dependencies
Example: Business rules extracted
Files: ~200-300
```

Add DOMAIN + APPLICATION when rules and workflows emerge.

### Growing (2 years)

```
Active: R1, R2, R3, R4, R5
Validators: Check 5-layer dependencies
Example: Multiple frontends
Files: ~500-800
```

Add PRESENTATION when second frontend appears.

### Enterprise (5+ years)

```
Active: R0, R1, R2, R3, R4, R5
Validators: Check all 6 layers
Example: Complex multi-tenant system
Files: ~1000+
```

Add CONFIG when deployment complexity warrants.

---

## Quick Start

### New Project

```bash
npx create-living-architecture my-project
cd my-project
```

Creates:
```
my-project/
  src/
    domain/         # R1 - Business entities
    application/    # R2 - Workflows
    interface/      # R3 - API boundaries
    infrastructure/ # R4 - External systems
  .git/hooks/       # Validators installed
  ARCHITECTURE.md   # Layer documentation
  README.md
  .gitignore
```

Git hooks validate on every commit.

### Existing Project

```bash
cd your-project
npx create-living-architecture .
```

Structure created. Validators installed.

---

## Workflow

Human prompts AI. AI generates code in appropriate layers. Validators enforce laws.

Example:

```
H: "Add user email verification"
```

AI generates:

```
src/domain/user_verification.py        # R1
src/application/verify_email_workflow.py  # R2
src/interface/verification_routes.py   # R3
src/infrastructure/email_service.py    # R4
```

Commit:

```bash
git commit -m "Domain: Add user verification [R1/C2]"
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

R2 • Application
  verify_email_workflow.py ● ONLINE

R3 • Interface
  verification_routes.py ● ONLINE

R4 • Infrastructure
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
Application: Add order workflow [R2/C2]
Interface: Add registration endpoint [R3/C2]
Infrastructure: Add email service [R4/C2]
Config: Add feature flags [R0/C2]
Presentation: Add mobile app [R5/C2]
```

### Layer Codes

- R0 • Config
- R1 • Domain
- R2 • Application
- R3 • Interface
- R4 • Infrastructure
- R5 • Presentation

### Classification Codes

- C1 • Internal (refactoring, no external impact)
- C2 • Feature (new functionality)
- C3 • Contract (API changes)
- C4 • Structure (architecture changes)
- C5 • Migration (data migrations)

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
  ✗ Violation detected
    domain/user.py imports infrastructure/repository.py

Fix: Remove import or use dependency inversion
```

---

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Detailed R0-R5 explanation
- [Commit Format](docs/COMMIT_FORMAT.md) - Commit standards
- [Design System](docs/DESIGN_SYSTEM.md) - Terminal output guidelines
- [Constitution](docs/CONSTITUTION.md) - Design philosophy
- [Examples](examples/) - Example projects

---

## Examples

Working examples in `examples/`:

- `starter/` - Standard R1-R4 setup (working code)
- `minimal-r3-r4/` - Smallest system (conceptual)
- `standard-r1-r4/` - Typical system (conceptual)
- `full-r0-r5/` - Enterprise system (conceptual)

---

## Performance Benefits

Gravitational alignment improves structural consistency and reduces architectural drift.

Observed effects:

• Initial placement accuracy — Increased  
• Reorganization cycles — Reduced  
• AI collaboration — Increased structural predictability  
• Architectural drift — Reduced  
• Cognitive load — Reduced  
• Developer onboarding — Faster  
• Change impact analysis — More localized

When validators enforce flow:

• Core logic remains stable  
• Integrations remain replaceable  
• Refactors stay localized

---

## Git History as Dashboard

View domain changes:

```bash
git log --oneline --grep="^Domain"
```

View structural changes:

```bash
git log --oneline --grep="C4"
```

Filter by layer:

```bash
git log --oneline --grep="R1"
```

Git history becomes architectural view.

---

## Requirements

• Node.js 18+  
• Git 2.0+  
• Python 3.8+ (optional for test validation)

---

## Bypass Validation

```bash
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

Modify JSON rules. Extend validators in `tools/`.

---

## Status

**Version:** 1.1.0  
**License:** MIT  
**Repository:** https://github.com/demos-ra/living-architecture

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

---

## Migration from R1-4

If you're familiar with the old R1-R4 system:

**Old R1-4 Mapping:**
- Old R1 (Domain) → New R1 (DOMAIN)
- Old R2 (Database) → New R4 (INFRASTRUCTURE)
- Old R3 (API) → New R3 (INTERFACE)
- Old R4 (Integrations) → New R4 (INFRASTRUCTURE)

**New Additions:**
- R0 (CONFIG) - Optional root layer
- R2 (APPLICATION) - Workflows and use cases
- R5 (PRESENTATION) - UI layer

The core principles remain: dependency gravity, unidirectional flow, and automatic validation.

---

Gravitational rules enforced. Structure remains consistent.
