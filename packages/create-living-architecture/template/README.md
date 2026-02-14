# Starter Template

Example Living Architecture project structure.

## Structure

```
src/
  domain/         R1 - Zero dependencies
  database/       R2 - Depends on domain
  api/            R3 - Orchestrates
  integrations/   R4 - External systems + UI
```

## Usage

```bash
npx create-living-architecture my-project
```

## Commit Examples

```
Domain: Add user entity [R1/C2]
Database: Add user repository [R2/C2]
API: Add registration endpoint [R3/C2]
Integrations: Add SendGrid email [R4/C2]
```
