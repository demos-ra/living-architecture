# living-architecture

**Stop managing code. Manage grids.**

AI agents lose track of large codebases, break files they weren't asked to touch, and run out of context. Here an agent never edits code: it edits a few small grids, and spec-driven, deterministic code generation writes the whole codebase from them.

You describe a project in a few spreadsheet-like grids. A generator writes every file of the codebase from them, byte for byte. A checker proves the code on disk is exactly what the grids say. The codebase is output, the way a compiled binary is output: you never edit it, you regenerate it.

| You are | What changes |
|---|---|
| **Vibe coder** | Vibe coding without the mess: you stop asking a model to edit a growing pile of files and hoping nothing else breaks. You change rows; the whole codebase follows. Nothing drifts, because nothing is written by hand. |
| **Developer** | Code becomes deterministic output. A pull request is a diff of grid rows. The checker turns "does the code match the design?" into a yes or a numbered list of exactly what differs and where to fix it. |
| **AI model or agent** | You no longer hold a codebase in your context. You read three small files with a closed vocabulary, write rows at exact addresses, run two commands, and stop at 0 findings. Every finding names the file and row that owns it. |

This is not a model writing code. It is a mechanical translation: the same grids always produce the same bytes, on any machine, by any implementation that follows the rules.

## Quick start

```sh
git clone https://github.com/demos-ra/living-architecture
cd living-architecture
python3 generate.py .    # writes example/ from the grids
python3 check.py .       # 0 findings: the code on disk is exactly the grids
```

Then open `example/util.ts`, and the rows in `example/.spec.mtsv` that it was written from. Change a row, run both commands again.

## What it is

Three files, each an MTSV file: tab-separated rows, grouped into sheets, a form feed starting each sheet. Each file owns one thing.

Any text editor opens them. Opening MTSV files in LibreOffice and Excel, one tab per sheet, is coming soon.

| File | Owns | Changes |
|---|---|---|
| `.canon.mtsv` | the rules: what a container is, where every fact lives, how code is written, how it is checked | never; identical in every project |
| `.templates.mtsv` | how each language writes each kind of thing: `if (…) {…}`, `model … {…}`, `a { … }` | only to add a language |
| `.spec.mtsv` | this project: its folders, modules, statements, expressions and text | this is what you edit |

`generate.py` and `check.py` are the reference implementation of `.canon.mtsv`. They hold no knowledge of their own: no language, file or project name, no default. Any implementation in any language that follows `.canon.mtsv` is equally valid.

## How it works

### Eight containers, outermost first

```
PROJECT → FOLDER → MODULE → FILE        the layout on disk
       → BODY → STATEMENT → EXPRESSION → TEXT   the syntax inside a file
```

Every container answers three questions, and nothing else: its **KIND** (what it is), its **PLACE** (where it sits), its **HOLDS** (what it holds).

### The descent: the parent decides, the spec fills only what is left open

Each parent hands its child exactly one slot, its kind where the parent fixes it, and the layout around it. A `.tsx` file always holds a `SourceFile`; a `FunctionDeclaration`'s body is always a `Block`. The spec never repeats what a parent already fixes. It names only what is open: which statement goes here, which expression, which text.

### Addresses

Every spec row sits at an address: the file's path, `#`, then one step per placeholder and one number per position in a list.

```
util.ts#/SourceFile/0/Body/0/Expression/Left/Text
```

reads: in `util.ts`, the first statement, its body's first statement, its expression's left side, its text.

### From rows to code

These rows from `example/.spec.mtsv` (abridged):

```
3-statements   FunctionDeclaration · Body   util.ts#/SourceFile/0
3-statements   ReturnStatement              util.ts#/SourceFile/0/Body/0
4-expressions  BinaryExpression             util.ts#/SourceFile/0/Body/0/Expression
5-texts        —                            util.ts#/SourceFile/0/name/Text   add
```

become `example/util.ts`:

```ts
export function add(a: number, b: number): number {
    return a + b;
}
```

Every character comes from a template, a placeholder row or a text cell. The spaces, line breaks and the 4-space indent come from TypeScript's own printer, written into `.templates.mtsv`.

## How to

### Start a project

1. Copy `.canon.mtsv` and `.templates.mtsv` into the project root, unchanged.
2. Write `.canonignore`: everything in the root that is not the project, in `.gitignore` syntax (this README, tool files, local folders).
3. Write `.spec.mtsv` in the root, and one in every folder: five sheets, `1-folders · 2-modules · 3-statements · 4-expressions · 5-texts`, each with the header `kind · place · holds`, header only when empty.
4. Run `python3 generate.py .` then `python3 check.py .`.

### Add a module

1. Pick its kind from `.templates.mtsv` sheet `1-modules`, for example `{{name}} · .ts` or `page · .tsx`.
2. Add a `2-modules` row to its folder's `.spec.mtsv`: the kind, and its name in `place` where the kind holds `{{name}}`, else `—`.
3. Add its statements, expressions and texts at their addresses.
4. Generate, then check.

### Add a language

1. Every kind comes from the language's own grammar: one row per kind in `2-files` to `5-expressions`, named as the grammar names it.
2. Every space, line break and indent comes from the language's own serializer or formatter. Where it is silent, write the minimum the grammar needs.
3. One kind per form only where the forms mean different things. Never a form for style.
4. One `6-placeholders` row per `{{placeholder}}` of every template.

### Read a finding

```
CHANGED   util.ts   bytes differ from the regenerated output   4-verification 192
```

`MISSING`: a source says it, it is not there. `EXTRA`: it is there, no source says it. `CHANGED`: it is there and differs. The last column is the `.canon.mtsv` row that requires it. Fix the source that owns it, never the generated file.

## Rules

The same rules as [AGENTS.md](AGENTS.md), for people. Each comes from `.canon.mtsv`.

**Always**

- Edit only `.spec.mtsv`, and `.templates.mtsv` to add a language.
- Write one row per container, at its address.
- In `3-statements` and `4-expressions`, name a kind only where the parent's `holds_kind` is `—`; elsewhere the kind cell is `—`. Write no row at all where the parent fixes the kind and holds exactly one.
- Take every kind from the templates of the parent's notation.
- Write `—` in every cell that does not apply.
- Write cell escapes `\n \t \f \r \\ \s`, and a literal brace in a template as `\\{` and `\\}`.
- Write parentheses in the spec wherever the language needs them for precedence.
- Fix every finding in the source that owns it, then generate and check again.

**Never**

- Edit `.canon.mtsv`.
- Edit a generated file by hand.
- Add logic, defaults or special cases to `generate.py` or `check.py`. If the tools seem to need one, the sources are wrong.
- Add a template form for style.
- Invent a kind or a name.
- Rely on row order. Order comes only from the position in an address.
- Name `.canon.mtsv`, `.templates.mtsv`, `.canonignore` or `.spec.mtsv` in a spec.

## What canon does not do

- **Style.** Where a language's formatter varies layout by content with the same meaning (`{}` or `{ }`, `x =>` or `(x) =>`, column alignment in Prisma), canon writes one form. Canon is universal for function; it does not cater to style.
- **Validate your program.** The generator writes exactly what the spec says. A spec that describes something the language does not allow writes code the language does not allow.
- **Reorder.** Code is written in the order of the addresses.

## Languages

| Notation | Kinds from | Layout from |
|---|---|---|
| `css` | CSS Syntax Module Level 3 | CSSOM |
| `json` | RFC 8259 | ECMA-262 `JSON.stringify` |
| `prisma` | Prisma `datamodel.pest` (prisma-engines) | `prisma format` |
| `typescript`, `typescriptreact` (React) | TypeScript's parser (typescript-go) | TypeScript's printer |

Module kinds follow Next.js file conventions. Generated files are UTF-8 and end with a line break. Asset files (`.ico`, `.png`, `.svg`, `.mtsv`, …) are left as they are.

## Requirements

- Python 3, standard library only.
- git, for `check.py`: it reads `.canonignore` through git, so the project must be a git repository.

## Versioning

The tools carry no truth of their own, so they follow the version of `.canon.mtsv`. This release is `v3.0.0`.

## Author

living-architecture is created and maintained by Demos Ra: canon, its templates, the spec format and the reference implementation. It is built on [MTSV](https://github.com/demos-ra/mtsv-spec), also created by Demos Ra and registered as an [IETF Internet-Draft](https://datatracker.ietf.org/doc/draft-demosra-mtsv/). See [NOTICE](NOTICE).

## Commercial license and support

living-architecture is free under the AGPL. For use under other terms, for example inside a closed product, and for support contracts, email demos_ra@hotmail.com.

## Contributing

Pull requests are welcome. Before your first one is merged, you sign the [Contributor License Agreement](CLA.md); CLA assistant asks on your pull request, and you sign with your GitHub account. Report a vulnerability as [SECURITY.md](SECURITY.md) says.

## License

[AGPL-3.0-only](LICENSE) from `v3.0.0`, with the [Generated Output Exception](EXCEPTION.md): the code you generate from your own spec is yours, under any terms you choose. Earlier tags remain under the MIT license.
