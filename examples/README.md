# Examples

Living Architecture examples organized by complexity.

---

## Working Code Examples

### starter/

Full working template with R1-R4 layers (Domain, Application, Interface, Infrastructure).

```bash
cd examples/starter
ls src/
# domain/ application/ interface/ infrastructure/
```

**Use this as:**
- Starting point for new projects
- Reference implementation
- Template for custom scaffolding

**Active layers:** R1, R2, R3, R4  
**Files:** ~30 files  
**Complexity:** Medium

---

## Conceptual Examples

These explain architecture patterns without full implementations. Each contains a detailed README explaining when and why to use the pattern.

### minimal-r3-r4/

**Smallest possible system:** INTERFACE + INFRASTRUCTURE only

**When to use:**
- MVP / Week 1 prototypes
- Simple CRUD applications
- Microservices with thin logic

**Active layers:** R3, R4  
**Example:** Startup building first prototype

See: [minimal-r3-r4/README.md](minimal-r3-r4/README.md)

---

### standard-r1-r4/

**Typical system:** Add DOMAIN + APPLICATION layers

**When to use:**
- Business rules emerge (>10 rules)
- Workflows become complex (>3 workflows)
- Need clear separation of concerns

**Active layers:** R1, R2, R3, R4  
**Example:** Business rules extracted, clear structure

See: [standard-r1-r4/README.md](standard-r1-r4/README.md)

---

### full-r0-r5/

**Enterprise system:** All 6 layers active

**When to use:**
- Complex configuration needs (>5 concerns)
- Multiple frontends (web + mobile + admin)
- Multi-tenant systems
- Feature flagging required

**Active layers:** R0, R1, R2, R3, R4, R5  
**Example:** Enterprise multi-tenant application

See: [full-r0-r5/README.md](full-r0-r5/README.md)

---

## Choosing the Right Pattern

| Scenario | Example | Layers |
|----------|---------|--------|
| Weekend hackathon | minimal-r3-r4 | R3, R4 |
| Standard web app | standard-r1-r4 | R1-R4 |
| SaaS product | full-r0-r5 | R0-R5 |

Start minimal. Add layers as complexity grows.

---

## Evolution Path

```
minimal-r3-r4 (Week 1)
     ↓
     Add business rules
     ↓
standard-r1-r4 (6 months)
     ↓
     Add second frontend
     ↓
full-r0-r5 (2+ years)
```

---

## Using Examples

### Study the Patterns

```bash
# Read conceptual examples
cat examples/minimal-r3-r4/README.md
cat examples/standard-r1-r4/README.md
cat examples/full-r0-r5/README.md
```

### Copy the Starter

```bash
# Use npx (recommended)
npx create-living-architecture my-project

# Or copy manually
cp -r examples/starter my-project
cd my-project
git init
```

### Test Validators

```bash
cd examples/starter
python3 ../../tools/validate-dependencies.py --root .
# Should pass: ✅ No dependency violations found
```

---

## Contributing Examples

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for how to add new examples.

New examples should:
1. Demonstrate a specific pattern or scale
2. Include detailed README
3. Pass all validators
4. Be tested with actual code (if not conceptual)
