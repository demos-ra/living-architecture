# Commit Format

Required format for all commits.

```
Layer: Description [R#/C#]
```

---

## Structure

**Layer:** Which architectural layer changed
**Description:** What changed (imperative mood, sentence case)
**[R#/C#]:** Layer code + Classification code

---

## Layer Codes

### R1 • Domain

Core business logic.
Zero dependencies.

Examples:
- `Domain: Add user entity [R1/C2]`
- `Domain: Add email validation [R1/C2]`
- `Domain: Refactor payment logic [R1/C1]`

### R2 • Database

Persistence layer.
Depends on domain.

Examples:
- `Database: Add user repository [R2/C2]`
- `Database: Add user table migration [R2/C5]`
- `Database: Optimize user query [R2/C1]`

### R3 • API

HTTP endpoints.
Orchestrates domain + database.

Examples:
- `API: Add registration endpoint [R3/C2]`
- `API: Change auth response format [R3/C3]`
- `API: Add rate limiting [R3/C2]`

### R4 • Integrations

External systems and UI.
Adapts to outside world.

Examples:
- `Integrations: Add Stripe payment [R4/C2]`
- `Integrations: Add SendGrid email [R4/C2]`
- `Integrations: Update Auth0 config [R4/C1]`

---

## Classification Codes

### C1 • Internal

Refactoring, optimization, code cleanup.
No external behavior change.

Examples:
- `Domain: Refactor user validation [R1/C1]`
- `Database: Optimize query performance [R2/C1]`
- `API: Rename handler functions [R3/C1]`

### C2 • Feature

New functionality, bug fixes.
External behavior changes.

Examples:
- `Domain: Add email verification [R1/C2]`
- `Database: Add user soft delete [R2/C2]`
- `API: Add password reset endpoint [R3/C2]`

### C3 • Contract

API modifications, interface changes.
Breaking changes.

Examples:
- `Domain: Change user interface [R1/C3]`
- `API: Change auth token format [R3/C3]`
- `Integrations: Update webhook signature [R4/C3]`

### C4 • Structure

Architecture changes, reorganization.
Layer boundary modifications.

Examples:
- `Structure: Move validation to domain [R1/C4]`
- `Structure: Split user module [R2/C4]`
- `Structure: Reorganize API routes [R3/C4]`

### C5 • Migration

Schema changes, data transformations.
Database migrations.

Examples:
- `Database: Add timestamps to users [R2/C5]`
- `Database: Migrate user emails to lowercase [R2/C5]`
- `Database: Split user_name into first_name and last_name [R2/C5]`

---

## Examples

### New Feature

```
Domain: Add user entity [R1/C2]
Database: Add user persistence [R2/C2]
API: Add registration endpoint [R3/C2]
Integrations: Add email verification service [R4/C2]
```

### Bug Fix

```
Domain: Fix email validation regex [R1/C2]
```

### Refactoring

```
Domain: Extract validation logic [R1/C1]
Database: Consolidate user queries [R2/C1]
```

### Breaking Change

```
API: Change user response format [R3/C3]
```

### Architecture Change

```
Structure: Move auth logic to domain [R1/C4]
```

### Data Migration

```
Database: Add user_status column [R2/C5]
Database: Migrate legacy user data [R2/C5]
```

---

## Multi-Layer Changes

When one feature touches multiple layers, create separate commits:

```
Domain: Add payment entity [R1/C2]
Database: Add payment repository [R2/C2]
API: Add payment endpoint [R3/C2]
Integrations: Add Stripe gateway [R4/C2]
```

**Why separate commits:**
- Clear architectural boundaries
- Easy to query by layer
- Simple to revert specific layers
- Atomic changes per layer

---

## Validation

Commit format is enforced automatically via commit-msg hook.

### Valid

```
Domain: Add user entity [R1/C2]
```

### Invalid

```
add user entity
```

Error:

```
❌ Invalid commit format

Expected: Layer: Description [R#/C#]

Examples:
  Domain: Add user entity [R1/C2]
  Database: Add user persistence [R2/C2]
  API: Add registration endpoint [R3/C2]
```

---

## Git Log Queries

Format enables architectural queries:

### View domain changes

```bash
git log --oneline --grep="^Domain"
```

### View all features

```bash
git log --oneline --grep="C2"
```

### View breaking changes

```bash
git log --oneline --grep="C3"
```

### View migrations

```bash
git log --oneline --grep="C5"
```

### View domain features

```bash
git log --oneline --grep="R1" --grep="C2" --all-match
```

### View recent structural changes

```bash
git log --oneline --grep="C4" --since="1 month ago"
```

---

## Best Practices

### Do

- Use imperative mood: "Add user" not "Added user"
- Be specific: "Add email validation" not "Add validation"
- One layer per commit
- Match layer code to actual files changed

### Don't

- Mix multiple layers in one commit
- Use vague descriptions: "Fix stuff"
- Omit classification code
- Use wrong layer code

---

## Bypass

Skip validation only when necessary:

```bash
git commit --no-verify -m "Work in progress [R1/C2]"
```

Creates audit trail.
Use sparingly.

---

## Version

1.0.0

Format enforced automatically.
Git log becomes architectural view.
