# Architecture

This project uses [Living Architecture](https://github.com/demos-ra/living-architecture).

Code organized by dependency gravity - heavy (pure logic) sinks to bottom, light (adapters) floats to top.

## Layers

**R1 • Domain** (heaviest - zero dependencies)
- Core business logic
- Entities, value objects, domain services
- No framework dependencies

**R2 • Database** (depends on domain only)
- Data persistence
- Repositories, DAOs
- Database adapters

**R3 • API** (orchestrates domain + database)  
- Application services
- Use cases, workflows
- Business process coordination

**R4 • Integrations** (lightest - adapts everything)
- External system adapters
- UI/presentation layer
- Third-party services
- HTTP, GraphQL, message queues

## Dependency Rules

Dependencies flow down only:
```
R4 → R3 → R2 → R1
```

- R1 imports nothing
- R2 imports only R1
- R3 imports R1, R2
- R4 imports all

Violations caught by git hooks.

## Benefits

**Swap layers independently:**
- Change database? Only R2 affected
- Change UI framework? Only R4 affected  
- Core business logic never touched

**Git history = architecture:**
```bash
git log --oneline
```

Shows which layer each change affected.
