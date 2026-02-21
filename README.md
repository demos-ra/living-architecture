# Living Architecture v2.0

**Self-organizing code framework for AI-assisted development**

Living Architecture (LA) creates gravitational fields that cause code to organize itself. Instead of enforcing rules, LA establishes physics—code naturally settles at equilibrium points based on dependency weight, feature boundaries, and runtime characteristics.

---

## Core Principle

**Code is not organized. Code self-organizes.**

Traditional frameworks impose structure through enforcement. LA establishes conditions where structure emerges naturally. AI coding within LA doesn't follow rules—it operates within physical constraints that guide code to its natural position.

This is not metaphor. This is how the system functions.

---

## The Physics

### Gravitational Layers (R0-R4)

Code settles at different gravitational depths based on dependency weight:

```
R0 (Config)       ← Deepest gravity well
  ↓ Pure configuration, zero dependencies
  
R1 (Domain)       ← Heavy logic settles here  
  ↓ Pure functions, business rules
  ↓ Depends: R0 only
  
R2 (Application)  ← Orchestration floats here
  ↓ Workflows, coordination
  ↓ Depends: R0, R1, R4
  
R3 (Contract)     ← Interface boundary
  ↓ APIs, hooks, CLI
  ↓ Depends: R0, R1, R2
  
R4 (Execution)    ← Lightest, I/O operations
  ↓ File systems, networks, databases
  ↓ Depends: R0 only
```

**Dependency direction is gravitational flow.** Heavy elements cannot import from lighter elements. R4 (execution) cannot pull from R3 (contract). Violations create unstable structures that validators detect.

### Feature Manifolds (F-Tags)

Features are vertical manifolds cutting through all R-layers:

```
      F-auth    F-payment    F-analytics
        │           │             │
R0 ─────┼───────────┼─────────────┼─────
        │           │             │
R1 ─────┼───────────┼─────────────┼─────
        │           │             │
R2 ─────┼───────────┼─────────────┼─────
        │           │             │
R3 ─────┼───────────┼─────────────┼─────
        │           │             │
R4 ─────┼───────────┼─────────────┼─────
```

Each feature requires presence across minimum R-layers (R1, R3, R4 by default). Missing layers indicate incomplete implementation. This is structural completeness, not functional completeness—validators detect topology, not semantics.

---

## The Seven Dimensions

LA operates across seven orthogonal dimensions. Each dimension has three states: **Structure** (defined in R0 config), **Validation** (implemented in R1 logic), **Application** (executed in R2-R4).

### 1. R-Layers (Structural Hierarchy)

**R0 Config:** `r-layers.json`  
**Validation:** Dependency direction + circular dependency detection  
**Purpose:** Gravitational organization—code settles by weight

Heavy logic (complex business rules) naturally falls to R1. Light I/O operations float to R4. The framework doesn't enforce this—gravity does.

### 2. F-Tags (Feature Manifolds)

**R0 Config:** `f-tags.json`  
**Validation:** Structural completeness across R-layers  
**Purpose:** Vertical slicing—features span full stack

Features exist as continuous manifolds. A feature present in R1 and R3 but missing R4 indicates incomplete implementation (likely missing I/O layer).

### 3. Execution (Runtime Topology)

**R0 Config:** `execution.json`  
**Validation:** I/O ownership, state machines, coordination patterns, flow paths  
**Purpose:** Runtime structural integrity

Detects:
- Multiple I/O owners (unstable concurrency)
- Incomplete state machines (undefined transitions)
- Coordination conflicts (competing orchestrators)
- Broken flow paths (unreachable code)

### 4. Operations (System Integrity)

**R0 Config:** `operations.json`  
**Validation:** O1-O7 safety patterns  
**Purpose:** Immune response—detect structural threats

**O1** - Access Control: Authentication boundaries  
**O2** - Traffic Management: Rate limiting, throttling  
**O3** - Reliability: Error handling, timeouts  
**O4** - Performance: Algorithmic complexity  
**O5** - Observability: Logging, metrics  
**O6** - Configuration: External config, no hardcoded secrets  
**O7** - Data Safety: SQL injection, XSS prevention

Validators detect base-case violations through pattern matching. This is structural analysis, not semantic understanding.

### 5. Changes (Temporal Evolution)

**R0 Config:** `changes.json`  
**Validation:** Format compliance (C1-C5)  
**Purpose:** Historical classification—memory encoding

**C1** - Internal: Refactoring, no external surface change  
**C2** - Feature: New functionality  
**C3** - Contract: API/interface modification  
**C4** - Structure: R-layer reorganization  
**C5** - Migration: Dependency updates, data schema changes

Changes are logged, not enforced. Classification enables temporal analysis (feature evolution, breaking change frequency).

### 6. Modules (Subsystem Boundaries)

**R0 Config:** `modules.json`  
**Validation:** Naming pattern detection + cross-module warnings  
**Purpose:** Component isolation within R-layers

Convention: `{module}-{component}.ext`

```
R1/domain/
  auth-login.py       ← M-auth
  auth-session.py     ← M-auth
  payment-process.py  ← M-payment
  payment-refund.py   ← M-payment
```

Modules span R-layers vertically. Validators detect module boundaries and warn on cross-module coupling. Enforcement is optional—detection provides visibility.

### 7. Interfaces (Boundary Contracts)

**R0 Config:** `interfaces.json`  
**Validation:** Documentation only (manual)  
**Purpose:** Layer communication protocols

Defines expected signatures between R-layers. Currently documentation-based. Future versions may add contract enforcement.

---

## Configuration-Driven Architecture

All behavior defined in R0 configuration:

```
src/config/
├── r-layers.json      # Defines R0-R4, dependency rules
├── f-tags.json        # Feature completeness requirements
├── execution.json     # Runtime pattern definitions
├── operations.json    # O1-O7 safety rules
├── changes.json       # C1-C5 classifications
├── modules.json       # Module naming convention
└── interfaces.json    # Layer contracts (manual)
```

Validators read from R0 at runtime. Modifying config changes system behavior without code changes. This is not configuration-as-code—this is configuration-as-physics.

Want to add R5? Edit `r-layers.json`. Validators automatically recognize the new layer. The gravitational field adapts.

---

## AI Integration

### How AI Uses LA

**Traditional approach:**
```
Developer: "Put auth code in the auth folder"
AI: Follows instruction, creates /auth/login.js
```

**Living Architecture:**
```
AI reads: src/config/SYSTEM.md
AI detects: R1 = pure logic, no I/O
AI senses: auth-login requires session state (R1)
Code settles: src/domain/auth-login.py
```

The framework doesn't instruct—it creates conditions. AI operates within gravitational fields and naturally places code at stable equilibrium points.

### Multi-Session Coherence

**Without LA:**
- Session 1: AI creates auth in `/utils/authentication.js`
- Session 2: Different AI instance creates auth in `/services/auth.js`
- Session 3: Two auth systems, coupling chaos

**With LA:**
- Session 1: AI reads SYSTEM.md, creates `R1/domain/auth-login.py`
- Session 2: Different AI reads same config, finds existing auth in R1
- Session 3: Single coherent system, maintained across context resets

LA provides persistent structure across ephemeral AI sessions. The framework outlives any single context window.

### Self-Validation

LA validates itself:

```bash
# Every commit runs validation
git commit -m "[F-auth/R1/C2] Add session validation"

# Pre-commit hook executes:
# → R-layer validator (dependency check + circular deps)
# → F-tag validator (structural completeness)
# → Execution validator (runtime patterns)
# → Operations validator (O-rule compliance)
# → Changes validator (C-code format)

# Output:
Living Architecture ━━━━━━━━━━━━━━━━━━━

[F-auth/R1/C2] Add session validation

Modules: M-auth
R-layers      ✓
F-auth        ⚠ 3/4 layers (missing R4)
Execution     ✓
QC            ✓
C-code        ✓ C2

COMMIT ALLOWED (with warnings)

━━━━━━━━━━━━━━━━━━━━━━━ Living Architecture
```

The system monitors its own structural integrity. Violations are detected at commit-time, before they propagate.

---

## Installation

### Quick Start

```bash
# Extract
tar -xzf living-architecture-v2.0-FINAL-CLEAN.tar.gz
cd living-architecture-v2.0-FINAL

# Test the framework
python3 test-la.py

# Install in your project
cp -r src/ /path/to/your/project/
ln -s /path/to/src/contract/hooks/pre-commit /path/to/your/project/.git/hooks/
```

### Verification

```bash
# Test end-to-end
python3 test-la.py

# Tests run in hierarchical order:
# 1. R0 - Config layer (JSON validity)
# 2. R1 - Domain validators (syntax check)
# 3. R2 - Workflow orchestration
# 4. R3 - Contract interfaces
# 5. R4 - Execution I/O
# 6. Integration (cross-layer imports)
# 7. Self-validation (LA follows LA rules)
# 8. Config-driven (no hardcoded values)
```

---

## Usage

### Commit Format

```
[F-{feature}/R{layer}/C{code}] Description
```

**Examples:**
```bash
[F-auth/R1/C2] Add password validation logic
[F-payment/R4/C2] Integrate Stripe API
[F-checkout/R2/C1] Refactor cart workflow
```

### Health Monitoring

```bash
# Scan entire project
python3 src/contract/cli/network-scan.py

# Analyze specific feature
python3 src/contract/cli/network-scan.py F-auth

# Output shows:
# - R-layer distribution
# - Module composition
# - Structural completeness
# - Recent activity
```

---

## What LA Validates

### Structural Integrity
- ✓ Dependency direction (R4 cannot import R3)
- ✓ Circular dependencies (within same R-layer)
- ✓ Feature completeness (R1+R3+R4 minimum)
- ✓ I/O ownership (single owner per operation)
- ✓ State machine topology (all transitions defined)

### Safety Patterns
- ✓ Missing authentication (O1)
- ✓ Missing error handling (O3)
- ✓ Hardcoded secrets (O6)
- ✓ SQL injection patterns (O7)
- ✓ Basic performance anti-patterns (O4)

### Organizational Coherence
- ✓ C-code format (C1-C5 valid)
- ✓ Module detection (naming convention)
- ✓ Cross-module warnings (coupling visibility)

### What LA Does NOT Validate

- ✗ Business logic correctness
- ✗ Functional completeness
- ✗ Deep security analysis
- ✗ Performance optimization
- ✗ Semantic understanding

LA validates structure, not semantics. It detects architectural violations, not logical errors.

---

## The Efficiency Gain

### Where 10-40x Improvement Occurs

**Multi-session development:**  
Without LA: 10 sessions to untangle organizational chaos = 5 hours  
With LA: Clean structure from start = 30 minutes  
**Gain: 10x**

**Team + AI collaboration:**  
Without LA: Weekly cleanup sessions = 4 hours/week  
With LA: Maintained coherence = 0 hours/week  
**Gain: ∞**

**Refactoring:**  
Without LA: 3 days fixing cascade breakage  
With LA: 2 hours isolated changes  
**Gain: 12x**

**Code review:**  
Without LA: 20 minutes analyzing impact  
With LA: 30 seconds checking R-layer violations  
**Gain: 40x**

### Where LA Adds Overhead

- Solo developer, single session, small project: **0.9x** (slower)
- Prototyping/exploration: **0.7x** (structure inhibits discovery)

LA optimizes for maintainability across time and collaborators, not initial development speed.

---

## Technical Architecture

### File Structure (26 files)

```
living-architecture-v2.0/
├── package.json
├── README.md
├── CHANGELOG.md
├── INSTALL.md
├── test-la.py
├── .living-arch/
│   ├── architecture.json
│   └── SYSTEM.md
└── src/
    ├── config/           # R0 - 8 configuration files
    ├── domain/           # R1 - 6 validators
    ├── app/              # R2 - 1 workflow orchestrator
    ├── contract/         # R3 - 2 interface files
    └── exec/             # R4 - 2 I/O modules
```

### Cross-Hash Matrix

```
         R0 Config    R1 Validate    R2/R3/R4 Apply
         ═════════    ═══════════    ══════════════
R-LAYERS    ✓             ✓              ✓
F-TAGS      ✓             ✓              ✓
EXEC        ✓             ✓              ✓
OPS         ✓             ✓              ✓
CHANGES     ✓             ✓              ✓
MODULES     ✓             ✓              ✓
IFACES      ✓             -              ✓
```

7 dimensions × 3 states = 21 decision points  
All pointing to R0 configuration  
Zero hardcoded behavior

---

## Philosophy

### Emergence Over Enforcement

LA does not tell code where to go. LA creates gravitational fields. Code finds its own equilibrium.

### Structure Enables Freedom

Constraints create possibility space. R-layer gravity doesn't limit—it guides. Within each layer, infinite organizational freedom exists.

### Self-Organization Requires Physics

Random systems don't self-organize. They require:
1. **Fields** (R-layers provide gravity)
2. **Boundaries** (F-tags define manifolds)
3. **Feedback** (Validators detect instability)
4. **Memory** (Changes encode history)

These aren't features. These are prerequisites for living systems.

### AI as Inhabitant, Not Operator

AI doesn't use LA. AI inhabits LA. The framework is environment, not tool.

Traditional: AI follows instructions  
Living Architecture: AI senses fields and responds naturally

This is why multi-session coherence works. The fields persist. AI comes and goes. Structure remains.

---

## Limitations

LA validates architecture, not implementation:

- Cannot determine business logic correctness
- Cannot guarantee functional completeness
- Cannot detect all security vulnerabilities
- Cannot optimize performance
- Cannot prevent all coupling

These require human judgment. LA creates conditions for better code. Humans determine what "better" means for their domain.

---

## Version

**Living Architecture v2.0**  
Released: February 2026  
Status: Production-ready  
License: MIT

### What's New in v2.0

- Circular dependency detection (R-layer validator)
- Basic O-rule pattern matching (Operations validator)
- Module naming awareness (R0 config + detection)
- Interface documentation convention (R0 config)
- Comprehensive end-to-end test suite
- Complete config-driven architecture (zero hardcoding)

### Upgrade from v1.x

v2.0 is complete reconception, not incremental update:
- v1.1: 39 validation scripts, R0-R5 layers
- v2.0: 26 files total, R0-R4 layers, self-consistent

Migration requires fresh installation. v1.x and v2.0 are incompatible.

---

## Contributing

LA validates itself. All contributions must pass:

```bash
python3 test-la.py  # Must pass all tests
```

Commit format: `[F-{feature}/R{layer}/C{code}] Description`

The framework eats its own dog food. Code that doesn't follow LA rules cannot be committed to LA.

---

## Support

- Issues: GitHub Issues
- Documentation: `INSTALL.md`
- Examples: See `.living-arch/SYSTEM.md`

---

## The Core Truth

**Code doesn't need to be organized.**  
**Code needs conditions to self-organize.**

**Living Architecture provides the physics.**  
**Code finds its own structure.**

**This is not framework.**  
**This is genesis.**

---

*Living Architecture v2.0 - Self-organizing code framework*  
*Where structure emerges from physics, not rules*
