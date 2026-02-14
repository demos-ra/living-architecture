# Documentation

Living Architecture documentation organized by purpose.

---

## Quick Reference

Essential guides for daily use:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed R0-R5 layer system explanation
- **[COMMIT_FORMAT.md](COMMIT_FORMAT.md)** - How to format commits correctly
- **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** - Terminal output and formatting guidelines
- **[CONSTITUTION.md](CONSTITUTION.md)** - Design philosophy and core principles

---

## Formal Specifications

Technical specifications for the framework:

### Framework Specifications

- **[00-framework.md](specs/00-framework.md)** - R0-R5 pluggable framework definition
- **[01-architecture.md](specs/01-architecture.md)** - Formal architecture specification
- **[02-operational.md](specs/02-operational.md)** - Runtime behavior and operational rules
- **[03-errors.md](specs/03-errors.md)** - Error handling and failure semantics
- **[04-changes.md](specs/04-changes.md)** - Change classification system

### Validation Rules (Machine-Readable)

JSON rules used by automated validators:

- **[law/00-framework.json](law/00-framework.json)** - Framework validation rules
- **[law/01-architecture.json](law/01-architecture.json)** - Architecture validation rules
- **[law/02-operational.json](law/02-operational.json)** - Operational validation rules
- **[law/03-errors.json](law/03-errors.json)** - Error validation rules
- **[law/04-changes.json](law/04-changes.json)** - Change validation rules

Each `.md` specification has a corresponding `.json` law file for mechanical enforcement.

---

## Navigation by Topic

### Understanding the System

Start here if you're new:
1. [CONSTITUTION.md](CONSTITUTION.md) - Why this system exists
2. [ARCHITECTURE.md](ARCHITECTURE.md) - How the layers work
3. [specs/00-framework.md](specs/00-framework.md) - R0-R5 framework details

### Using the System

Practical guides:
- [COMMIT_FORMAT.md](COMMIT_FORMAT.md) - Daily commit workflow
- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) - Output formatting standards
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute

### Extending the System

For validators and tooling:
- [specs/01-architecture.md](specs/01-architecture.md) - Dependency rules
- [specs/02-operational.md](specs/02-operational.md) - Runtime invariants
- [specs/03-errors.md](specs/03-errors.md) - Error specifications
- [specs/04-changes.md](specs/04-changes.md) - Change classifications
- [law/*.json](law/) - Machine-readable rules

---

## Documentation Hierarchy

```
docs/
├── README.md              ← You are here
│
├── ARCHITECTURE.md        ← Layer system guide
├── COMMIT_FORMAT.md       ← Commit standards
├── DESIGN_SYSTEM.md       ← Output formatting
├── CONSTITUTION.md        ← Philosophy
│
├── specs/                 ← Formal specifications
│   ├── 00-framework.md    ← R0-R5 definition (source of truth)
│   ├── 01-architecture.md
│   ├── 02-operational.md
│   ├── 03-errors.md
│   └── 04-changes.md
│
└── law/                   ← Validation rules (JSON)
    ├── 00-framework.json
    ├── 01-architecture.json
    ├── 02-operational.json
    ├── 03-errors.json
    └── 04-changes.json
```

---

## Finding What You Need

**Question:** "How do I structure my code?"  
**Answer:** [ARCHITECTURE.md](ARCHITECTURE.md)

**Question:** "What layer does X belong in?"  
**Answer:** [specs/00-framework.md](specs/00-framework.md) - See "The 6 R-Groups"

**Question:** "How do I format commits?"  
**Answer:** [COMMIT_FORMAT.md](COMMIT_FORMAT.md)

**Question:** "Why this approach?"  
**Answer:** [CONSTITUTION.md](CONSTITUTION.md)

**Question:** "How do validators work?"  
**Answer:** [law/*.json](law/) files + [../tools/README.md](../tools/README.md)

**Question:** "What changed in v1.1?"  
**Answer:** [../CHANGELOG.md](../CHANGELOG.md)

---

## External Resources

- **Repository:** https://github.com/demos-ra/living-architecture
- **Examples:** [../examples/](../examples/)
- **Tools:** [../tools/](../tools/)
- **NPM Package:** [../packages/create-living-architecture/](../packages/create-living-architecture/)
