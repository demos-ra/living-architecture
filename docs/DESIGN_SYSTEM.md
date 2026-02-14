# Design System

Living Architecture design system for terminal output and documentation.

---

## Principles

1. **Comprehension first**
   Every element must increase clarity. Remove anything that doesn't inform.

2. **Minimal symbol set**
   10 approved symbols. No additions without removing one first.

3. **System colors only**
   Respect user's terminal theme. No custom colors.

4. **Flat structure**
   Maximum 2 levels. Deeper nesting is information overload.

5. **Natural language**
   Sentence case. Concise. No jargon.

---

## Approved Symbols

### Status (4 symbols)

```
● Solid dot    Complete, online, working
○ Hollow dot   Incomplete, offline, broken
✓ Check        Validation passed, ready
✗ Cross        Validation failed, error
```

### Structure (5 symbols)

```
• Bullet       Label separator (R1 • Domain)
├─ Branch      First item in list
└─ Terminal    Last item in list
│  Vertical    Continuation between items
─  Horizontal  Section separator (sparingly)
```

### Reserved (1 symbol)

```
∆ Delta        Reserved for future metrics
```

**Total: 10 symbols**

---

## Forbidden

Never use:

- Emoji (🎉 ⚡ 🚀 ✨)
- Decorative symbols (★ ► ■ ◆)
- Custom colors/formatting
- Bold/italic in terminal output
- Animations/spinners
- Progress bars with percentage
- ASCII art
- Box drawing beyond approved set

---

## Layout Rules

### Spacing

```
2-space indent (never tab, never 4-space)
1 blank line between sections
No trailing whitespace
No leading blank line
One trailing newline at end
```

### Alignment

Align on symbols:

```
R1 • Domain
R2 • Database
R3 • API
```

Not:

```
R1  • Domain
R2  • Database
R10 • Something
```

### Line Length

Maximum 80 characters.
Break long lines naturally:

Not:
```
"Creating project directory structure and installing git hooks"
```

Yes:
```
"Creating structure"
Then: "Installing validators"
```

---

## Typography

### Case

```
Sentence case (not Title Case)
Layer names: Domain, Database, API, Integrations
Status: ONLINE, OFFLINE (all caps for emphasis)
Files: exact case (user_verification.py)
```

### Language

**Concise:**
```
Yes: "Creating structure"
No:  "Now creating project structure..."
```

**Natural:**
```
Yes: "Fix tests before committing"
No:  "Test suite execution failed - remediation required"
```

**Direct:**
```
Yes: "Dependencies ✓ Flow correct"
No:  "Dependency validation has passed successfully"
```

---

## Applications

### 1. Post-Commit Status

Format:

```
COMMIT: <Layer>: <Description> [<hash>]

<blank line>
R<N> • <Layer>
  <filename> <status>

<blank line>
STATUS: <overall>
```

Example:

```
COMMIT: Domain: Add user verification [a3f891c]

R1 • Domain
  user_verification.py ● ONLINE

R3 • API
  verification_routes.py ● ONLINE

R4 • Integrations
  email_service.py ● ONLINE

STATUS: ● ALL ONLINE
```

With failure:

```
COMMIT: Integrations: Add Stripe webhook [b4e7f2a]

R1 • Domain
  payment.py ● ONLINE

R4 • Integrations
  stripe_gateway.py ○ OFFLINE

Failed tests:
  test_webhook_signature

STATUS: ○ PARTIAL
```

Rules:
- File indented 2 spaces
- Status follows filename with space
- Failed tests indented 2 spaces under label
- Overall status always present

---

### 2. NPX Install

Format:

```
Living Architecture

<blank line>
<Action>
  <symbol> <item>
  <symbol> <item>

<blank line>
<symbol> <completion>

<blank line>
<instructions>
```

Example:

```
Living Architecture

Creating structure
  ● domain
  ● database
  ● api
  ● integrations

Installing validators
  ● pre-commit
  ● commit-msg
  ● post-commit

✓ Ready

Commit format: Layer: Description [R#/C#]
```

Rules:
- Action in sentence case
- Items indented 2 spaces
- Completion message on own line
- Instructions concise

---

### 3. Pre-Commit Validation

Format:

```
Validating

<blank line>
<Check>
  <symbol> <result>

<blank line>
<instruction if fail>
```

Success:

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
  ✓ Flow correct

Tests
  ✗ 2 failures
    test_user_verification
    test_email_format

Fix tests before committing
```

Rules:
- Check name in sentence case
- Result indented 2 spaces
- Failed items indented 4 spaces (2 from result)
- Instruction on separate line, no indent

---

### 4. Error Messages

Format:

```
<Check>
  ✗ <Error type>
    <specifics>

<blank line>
Fix: <instruction>
```

Example:

```
Dependencies
  ✗ Violation detected
    domain/user.py imports database/repository.py

Fix: Remove import or use dependency inversion
```

Rules:
- Error type concise
- Specifics indented 4 spaces
- Fix instruction clear and actionable
- No "please" or "you should"

---

### 5. README Examples

All code blocks showing terminal output must match formats above exactly.

Example in markdown:

````markdown
Post-commit displays status:

```
COMMIT: Domain: Add user verification [a3f891c]

R1 • Domain
  user_verification.py ● ONLINE

STATUS: ● ALL ONLINE
```
````

Rules:
- Use triple backticks
- No syntax highlighting (plain text)
- Exact spacing match terminal output
- No embellishment

---

## Anti-Patterns

### Too Verbose

❌ "Now beginning the process of creating your project structure..."
✓  "Creating structure"

❌ "Installation has completed successfully!"
✓  "✓ Ready"

### Symbol Abuse

❌ ★ ONLINE ★
✓  ● ONLINE

❌ ═══════════════
✓  ─────────────── (or omit)

❌ [✓] Pass
✓  ✓ Pass

### Deep Nesting

❌
```
R1 • Domain
├─ Models
│  ├─ user.py ● ONLINE
│  └─ payment.py ● ONLINE
└─ Services
   └─ auth.py ● ONLINE
```

✓
```
R1 • Domain
  user.py ● ONLINE
  payment.py ● ONLINE
  auth.py ● ONLINE
```

### Color/Formatting

❌ `\033[32m● ONLINE\033[0m`
✓  `● ONLINE`

❌ `**ONLINE**` (markdown bold)
✓  `ONLINE`

❌ `READY` (green background)
✓  `✓ Ready`

---

## Validation

### Self-Check

Before shipping any terminal output, verify:

```
□ Uses only approved symbols (10 total)
□ No custom colors
□ Maximum 2 levels indent
□ 2-space indent (not 4, not tab)
□ 1 blank line between sections
□ Sentence case
□ Concise language
□ No trailing whitespace
□ Matches README example
```

### Automated Check

```bash
# In pre-commit hook
# Flag unapproved symbols
grep -r "🎉\|★\|►\|■\|◆\|⚡\|🚀" output/ && exit 1

# Flag custom colors
grep -r "\\033\[" output/ && exit 1

# Flag 4-space indent
grep -r "^    " output/ && exit 1
```

---

## Rationale

### Why These Symbols?

```
● ○ - Universal (traffic lights, radio buttons, forms)
✓ ✗ - Instantly recognized (checkboxes, forms)
├ └ │ - Minimal tree structure (file explorers)
─ - Simple separator (dividers)
• - Neutral bullet (lists, labels)
```

Not: ★ ► ■ (decorative, not functional)

### Why System Colors?

Respects:
- User's theme preference (dark/light)
- Accessibility settings (high contrast)
- Terminal capabilities (some don't support 256-color)

Avoids:
- Color blindness issues
- Theme clashes
- Assuming terminal capabilities

### Why Flat Structure?

Cognitive load:
- 1 level = instant scan
- 2 levels = quick parse
- 3+ levels = mental stack overflow

Information density:
- More nesting ≠ more clarity
- Usually means poor grouping
- Flatten or split into sections

### Why 2-Space Indent?

Readability:
- Visible but not excessive
- Standard for many languages (JSON, YAML)
- Works in 80-column terminals

Not 4-space:
- Takes too much horizontal space
- Creates deep-looking trees quickly

Not tabs:
- Inconsistent rendering
- Alignment issues

---

## Evolution

### Adding New Symbols

Process:

1. Identify specific need (not general "might be useful")
2. Check if existing symbols can serve purpose
3. If new symbol required, remove one existing
4. Update this document
5. Update all examples

**Symbol budget: 10 maximum**
**Current: 10/10 used**

To add new: Must remove existing

### Changing Format

Process:

1. Propose change with rationale
2. Update DESIGN_SYSTEM.md
3. Update README examples
4. Update all terminal outputs
5. Test in multiple terminals

Never:
- Change without updating documentation
- Make "temporary" exceptions
- Deviate "just this once"

---

## Reference Implementation

All terminal outputs in Living Architecture follow this system:

```
Source of truth: README.md examples
Enforcement: This document
Validation: Pre-commit checks
```

If output doesn't match this spec = bug.

---

## Version

1.0.0

Minimal. Intuitive. Unwarpable.
