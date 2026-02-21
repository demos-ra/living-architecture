# Living Architecture - Development Guide

When working on LA itself, follow gravitational principles:

## R-Layers
- **R0** `src/config/` - Configuration JSON files
- **R1** `src/domain/` - Pure validation logic
- **R2** `src/app/` - Workflow orchestration
- **R3** `src/contract/` - Hooks and CLI
- **R4** `src/exec/` - Git and file I/O

## Commit Format
`[F-feature/R#/C#] Description`

Examples:
- `[F-r-layers/R1/C2] Add dependency validator`
- `[F-network-scan/R3/C2] Add CLI interface`

## The 5 F-Tags
- F-r-layers - R-layer validation
- F-f-tags - F-tag validation  
- F-execution - Runtime pattern validation
- F-operations - O-rule validation
- F-changes - Change tracking

LA validates itself using these same rules.
