# System Governance Spec

**Constitutional constraints for AI-modified codebases**

## What This Is

A machine-readable specification that defines how software systems should be structured, operated, and evolved when AI is a continuous contributor to the codebase.

Instead of relying on tribal knowledge, code comments, or documentation that decays over time, this framework encodes architectural invariants as explicit rules that both humans and AI must follow.

## Philosophy: Infrastructure for Harmonious Timelines

Traditional software architecture assumes human-only contributors operating in linear time with tribal knowledge transfer. This framework assumes a different reality:

- **Continuous AI contribution** as a fundamental force, not an edge case
- **Multiple simultaneous constraint dimensions** that compose orthogonally, not hierarchical control structures  
- **Encoded intent** as the persistent substrate, replacing implicit assumptions that decay
- **Time as a first-class dimension** — systems evolve across sessions, contributors, and contexts

Think of this as **constitutional field mechanics for code**: each dimension exerts independent force, violations are detectable resonance failures, and coherence emerges from constraint composition rather than centralized control. The system self-stabilizes across AI iterations because the rules are present in every interaction, not stored in human memory.

As AI agents become economic actors querying tokenized knowledge and modifying codebases continuously, they need shared constitutional infrastructure. This spec is foundational for systems where humans and agents collaborate asynchronously at machine timescales, and intent must persist across infinite micro-decisions.

## Quick Start (Plug & Play)

### Installation (2 Minutes)

**Option 1: Use as Git Submodule**
```bash
# Add to your project
git submodule add https://github.com/demos-ra/system-governance-spec .governance

# Run validation
.governance/tools/validate-all.sh


Option 2: Copy Tools Directly

# Clone the repo
git clone https://github.com/demos-ra/system-governance-spec.git

# Copy tools to your project
cp -r system-governance-spec/tools ./tools
cp -r system-governance-spec/law ./law

# Run validation
./tools/validate-all.sh


Setup Pre-Commit Hook (1 Minute)

# Automatic validation before every commit
cp tools/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit


Now your commits are automatically checked for:
	∙	✅ Change classification ([C1-C5] in commit message)
	∙	✅ Dependency direction violations (D2)
	∙	✅ Error structure compliance
Setup CI/CD (GitHub Actions)
Create .github/workflows/governance.yml:

name: Governance Check

on: [pull_request, push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-python: '3.x'
      
      - name: Run governance checks
        run: ./tools/validate-all.sh


That’s it. Pull requests now auto-validate against the spec.
Usage Examples
Check your latest commit:

./tools/validate-all.sh


Check specific rules:

./tools/validate-change-classification.sh  # Commit message format
python3 tools/validate-dependencies.py     # Architecture compliance
python3 tools/validate-errors.py           # Error structure


Example compliant commit:

git commit -m "[C1] Refactor user validation logic"
# ✅ Passes - has classification, no violations


Example violation:

git commit -m "fix stuff"
# ❌ Fails - missing [C1-C5] classification


What Gets Validated



|Check                      |Rule                                                                 |Enforcement|
|---------------------------|---------------------------------------------------------------------|-----------|
|**Change Classification**  |Commit must start with `[C1]`, `[C2]`, `[C3]`, `[C4]`, or `[C5]`     |Blocking   |
|**Dependency Direction**   |R-groups must follow D2 rules (e.g., Domain can’t import Application)|Blocking   |
|**Error Structure**        |Errors must have: kind, scope, cause, location, resolution_hint      |Blocking   |
|**Operational Constraints**|Manual review (O1-O7 checklist in tools/README.md)                   |Advisory   |

Immediate ROI
Without tools: “Remember to add rate limiting” (decays over time)
With tools: AI cannot generate code that violates constraints (enforced mechanically)
Example:

# AI tries to generate this:
throw new Error("Invalid email")

# ❌ Validator blocks it:
# "Error created without canonical structure"
# "Missing fields: kind, scope, cause, location, resolution_hint"

# AI regenerates compliant version:
throw {
  kind: "VALIDATION_FAILED",
  scope: "USER", 
  cause: "Email format invalid: missing @ symbol",
  location: "R3:UserController",
  resolution_hint: "Provide email in format: user@domain.com"
}


See tools/README.md for detailed documentation.
Why This Exists
The Problem:
	∙	AI coding assistants generate code at machine speed
	∙	“Remember to add rate limiting” decays across sessions
	∙	Implicit architectural assumptions don’t survive AI iteration
	∙	Each new AI session starts with zero context
	∙	Technical debt compounds automatically
The Solution:
A constitutional framework that:
	∙	Persists across all coding sessions (human and AI)
	∙	Makes architectural rules machine-readable
	∙	Enforces invariants mechanically instead of manually
	∙	Prevents entropy in AI-modified systems
The Four Specifications
01-ARCHITECTURE.md
Multidimensional structural framework
Defines 5 orthogonal dimensions that every artifact must satisfy:
	∙	D1: Responsibility (Domain, Application, Interface, Infrastructure, Presentation)
	∙	D2: Dependency Direction (strict allowed/forbidden graph)
	∙	D3: Runtime (browser, server, pure computation boundaries)
	∙	D4: Language (boundaries aligned with responsibilities)
	∙	D5: Stability (change propagation rules)
02-OPERATIONAL.md
Runtime behavior constraints
Defines 7 operational dimensions that cut across all layers:
	∙	O1: Access Control & Abuse Prevention
	∙	O2: Traffic Management (rate limiting, quotas)
	∙	O3: Reliability & Fault Tolerance (retries, timeouts, circuit breakers)
	∙	O4: Performance & Resource Control
	∙	O5: Observability (logging, metrics, tracing)
	∙	O6: Configuration & Environment
	∙	O7: Data Safety & Lifecycle
03-ERROR-SYSTEM.md
Canonical failure handling
Defines a single, global error model:
	∙	Canonical structure (kind, scope, cause, location, resolution_hint)
	∙	Global error registry (15 error kinds defined)
	∙	Propagation rules (no re-wrapping, no semantic mutation)
	∙	Boundary translation constraints
04-CHANGE-GOVERNANCE.md
Evolution control
Defines how systems are allowed to change over time:
	∙	C1: Local Implementation Change (internal logic only)
	∙	C2: Behavioral Change (observable effects, stable contracts)
	∙	C3: Contract Change (versioned, backward-compatible)
	∙	C4: Structural Change (architectural boundaries)
	∙	C5: Data Evolution Change (schema migrations, highest risk)
Design Philosophy
This framework is built on three principles:
	1.	Explicit over implicit
	∙	Structure must be machine-legible
	∙	Constraints are enforced, not suggested
	∙	No tribal knowledge or unstated assumptions
	2.	Invariants over procedures
	∙	Define what must not break, not how to build
	∙	Freedom exists within constraints
	∙	Rules apply equally to humans and AI
	3.	Orthogonal concerns
	∙	Each dimension is independent
	∙	Violations in one dimension don’t excuse violations in others
	∙	No dimensional shortcuts allowed
How To Use This
For New Projects
	1.	Reference in system prompts:

This codebase follows the System Governance Spec:
https://github.com/demos-ra/system-governance-spec

Before generating code, review the architectural and operational
constraints defined in the specifications.


	2.	Add to your repository:
	∙	Link to this repo in your README
	∙	Reference specific specs in PR templates
	∙	Include in AI tool configurations (Cursor, Claude Code, etc.)

Follow System Governance Spec (github.com/demos-ra/system-governance-spec):
- Classify all changes as C1-C5
- Validate against architectural dimensions D1-D5
- Ensure operational compliance O1-O7
- Use canonical error structure


For code review:

Review this PR against System Governance Spec:
1. Which R-group (Responsibility layer)?
2. Dependencies valid? (D2)
3. Runtime aligned? (D3)
4. Language aligned? (D4)
5. Stability impact? (D5)
6. Change classification? (C1-C5)
7. Operational compliance? (O1-O7)


Who This Is For
	∙	Teams using AI coding assistants (Cursor, Claude Code, GitHub Copilot, etc.)
	∙	Solo developers building with AI at scale
	∙	Open source maintainers accepting AI-generated contributions
	∙	Anyone building systems where AI is a continuous contributor
Status
Version: 1.0.0Status: Normative (stable, production-ready)License: MIT (see LICENSE)
Contributing
This is foundational infrastructure for the agent economy. Contributions welcome via:
	∙	Issue discussions for clarifications
	∙	PRs for typo fixes or clarity improvements
	∙	Fork for domain-specific adaptations
Critical rule: Proposed changes must not violate the governance spec itself.
Author
Demos Ra - System Designer
Acknowledgments
This framework synthesizes decades of software architecture patterns (Clean Architecture, Hexagonal Architecture, Domain-Driven Design) into a minimal, AI-compatible form optimized for continuous machine modification.

Quick Reference
Dependency Flow:

R5 (Presentation) → R3 (Interface) → R2 (Application) → R1 (Domain)
R4 (Infrastructure) → R2 (Application) → R1 (Domain)

R1 depends on nothing
R2 never depends on R3, R4, or R5


Change Classification:
	∙	C1: Internal logic (cheap, common)
	∙	C2: Observable behavior (stable contracts)
	∙	C3: Contracts (versioned, migration path)
	∙	C4: Structure (rare, reviewed)
	∙	C5: Data (highest risk, rollback plan)
Operational Checklist:
	∙	Rate limiting implemented? (O2)
	∙	Timeouts defined? (O3)
	∙	Error handling bounded? (O3)
	∙	Inputs validated? (O7)
	∙	Logs structured? (O5)
	∙	Secrets externalized? (O6)
