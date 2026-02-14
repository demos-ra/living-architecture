# Living Architecture R1-6: Pluggable Framework

**Version:** 1.1.0  
**Status:** Production Ready  
**Replaces:** R1-4 (v1.0.0) with backward compatibility

---

## What Is R1-6?

An evolution of Living Architecture that supports **pluggable R-groups** instead of requiring all 6 layers.

Projects start minimal (3 layers) and grow by adding layers as needed. Validators adapt to detect which layers exist and enforce rules only for active layers.

---

## The 6 R-Groups (Responsibility Groups)

### R0: CONFIG (Optional)
**When to add:** Configuration concerns > 5  
**Purpose:** Environment, feature flags, parameters, deployment config  
**Dependencies:** None (root layer)  
**Example:** Feature flags, multi-tenant config, deployment parameters

### R1: DOMAIN (Optional)
**When to add:** Business rules > 10  
**Purpose:** Business entities, invariants, value objects  
**Dependencies:** CONFIG (if exists)  
**Example:** User entity, Payment rules, Order business logic

### R2: APPLICATION (Optional)*
**When to add:** Workflows > 3 or state machines needed  
**Purpose:** Use cases, workflows, orchestration  
**Dependencies:** CONFIG, DOMAIN (if they exist)  
**Example:** CreateOrder workflow, UserRegistration process

### R3: INTERFACE (Required)
**When to add:** Always (every system has boundaries)  
**Purpose:** API contracts, controllers, DTO mapping  
**Dependencies:** CONFIG, DOMAIN, APPLICATION (if they exist)  
**Example:** REST endpoints, GraphQL resolvers, CLI handlers

### R4: INFRASTRUCTURE (Required)
**When to add:** Always (every system executes somewhere)  
**Purpose:** Persistence, external integrations, side effects  
**Dependencies:** CONFIG, DOMAIN, APPLICATION (if they exist)  
**Note:** Cannot depend on INTERFACE (abstraction inversion)  
**Example:** Database repositories, HTTP clients, message queues

### R5: PRESENTATION (Optional)
**When to add:** Frontends > 1  
**Purpose:** UI, views, rendering, client state  
**Dependencies:** CONFIG, INTERFACE only  
**Example:** React components, Vue pages, mobile app

*APPLICATION: Can be skipped in pure CQRS or event-sourced systems

---

## Skip Matrix: When to Include Each Layer

| Layer | Required? | Skip if... | Add when... |
|-------|-----------|-----------|-------------|
| CONFIG | No | Environment variables sufficient | >5 config concerns |
| DOMAIN | No | Rules embedded in APPLICATION | >10 business rules |
| APPLICATION | No* | Single handler or pure CQRS | >3 workflows or state machines |
| INTERFACE | **YES** | Never | Always present |
| INFRASTRUCTURE | **YES** | Never | Always present |
| PRESENTATION | No | Single web app in INTERFACE | 2+ frontends exist |

---

## How Projects Evolve

### Tiny (MVP, Week 1)
```
Active: APPLICATION, INTERFACE, INFRASTRUCTURE
Validation: Check 3-layer dependencies only
Example: Startup building first prototype
Files: ~50-100 total
```

### Small (6 months)
```
Active: DOMAIN, APPLICATION, INTERFACE, INFRASTRUCTURE
Validation: Check 4-layer dependencies
Example: Business rules extracted, clear structure
Files: ~200-300 total
```

### Growing (2 years)
```
Active: DOMAIN, APPLICATION, INTERFACE, INFRASTRUCTURE, PRESENTATION
Validation: Check 5-layer dependencies
Example: Multiple frontends (web + mobile)
Files: ~500-800 total
```

### Enterprise (5+ years)
```
Active: CONFIG, DOMAIN, APPLICATION, INTERFACE, INFRASTRUCTURE, PRESENTATION
Validation: Check all 6-layer dependencies
Example: Complex config, multiple deployment targets
Files: 1000+ total
```

---

## Dependency Rules (D2)

Each R-group can only depend on layers below it in the pyramid:

```
PRESENTATION
     ↓ (can depend on INTERFACE only)
INFRASTRUCTURE
     ↓ (can depend on APPLICATION only, not INTERFACE)
INTERFACE
     ↓ (can depend on APPLICATION only)
APPLICATION
     ↓ (can depend on DOMAIN only)
DOMAIN
     ↓ (can depend on CONFIG only)
CONFIG
     ↓ (depends on nothing)
```

### Forbidden Dependencies
- PRESENTATION cannot import INFRASTRUCTURE or APPLICATION
- INFRASTRUCTURE cannot import INTERFACE or PRESENTATION
- INTERFACE cannot import INFRASTRUCTURE or PRESENTATION
- APPLICATION cannot import INTERFACE, INFRASTRUCTURE, or PRESENTATION
- DOMAIN cannot import anything except CONFIG
- CONFIG cannot import anything

---

## Validator Behavior

### How Detection Works
1. Scan project directory for R-group patterns
2. Determine which layers are actively used
3. Load dependency rules for active layers only
4. Validate imports against filtered rules

### What Gets Validated
- ✅ Dependency direction (D2)
- ✅ Change classification (C1-C5)
- ✅ Error structure (canonical form)
- ✅ Operational constraints (O1-O7)

### What Gets Skipped
- Layers not detected are not validated
- No errors for "missing" layers
- All layer combinations are valid

---

## Migration from R1-4

### For v1.0 Projects
No changes required. v1.0 projects continue to work with v1.0 validators.

### To Adopt v1.1
1. Update submodule to v1.1.0
2. No code changes needed
3. Validators automatically detect your 5 R-groups
4. All v1.0 rules still apply

### Benefits of v1.1
- Same structure, better tooling
- Clearer evolution path
- Support for minimal projects
- Cleaner validation rules

---

## Example: Tiny Project Skip Matrix

```json
{
  "config": false,
  "domain": false,
  "application": true,
  "interface": true,
  "infrastructure": true,
  "presentation": false
}
```

**Validation:** Only check APPLICATION → INTERFACE, APPLICATION → INFRASTRUCTURE, INTERFACE → INFRASTRUCTURE

**Invalid:** PRESENTATION, CONFIG, DOMAIN are not validated (don't exist)

**Result:** Tight, focused validation for small team

---

## First Principles

R1-6 is built on three principles:

1. **Minimal Required Structure**
   - Not all projects need all layers
   - Start with what's needed
   - Add as complexity grows

2. **Explicit Evolution Path**
   - Clear trigger for when to add each layer
   - Documented at each phase
   - No surprise requirements

3. **Same Guarantees**
   - Dependency direction still enforced
   - Error structure still canonical
   - Change classification still required
   - Nothing weakened, only more flexible

---

## Backward Compatibility

✅ **v1.0 projects work unchanged**
- All 5 R-groups detected automatically
- All v1.0 rules enforced
- v1.0 examples still work
- Migration is zero-effort

✅ **v1.0 validators compatible with v1.1**
- Can use v1.0 validators on v1.1 code
- v1.1 validators backward-compatible with v1.0 projects
- Both versions coexist

✅ **Safe to upgrade or stay**
- Stay on v1.0 if you prefer (git tag v1.0.0)
- Upgrade to v1.1 when ready
- No breaking changes

---

## Questions

**Q: What if my project doesn't fit these 6 layers?**  
A: It will. These layers represent fundamental responsibilities (config, rules, flows, boundaries, execution, presentation). If you think you need a 7th, you likely need a 2nd system.

**Q: Can I use a different layer naming?**  
A: The names are conventional. What matters is the responsibility. Rename internally, but map to these 6 for validation.

**Q: What about microservices?**  
A: Each service is its own system with its own R-groups. The LA framework applies within each service, not across services.

**Q: Do I have to start with R1-6?**  
A: No. Start with v1.0 (R1-4). When you're ready to skip layers or add CONFIG, upgrade to v1.1 (R1-6).

---

**See also:**
- `docs/law/00-framework.json` — Machine-readable skip rules
- `docs/law/01-architecture.json` — Updated dependency graph
- `MIGRATION-R1-4-TO-R1-6.md` — Upgrade guide
- `examples/r1-6-*` — Example projects at each scale
