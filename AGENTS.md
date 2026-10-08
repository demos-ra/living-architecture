# Instructions for agents

You do not write code in this repository. You write rows. `generate.py` writes every code file from the rows; `check.py` proves the files on disk equal the rows. A code file you edit by hand is a finding, not a fix.

`.canon.mtsv` is the only authority. Where this file and `.canon.mtsv` differ, `.canon.mtsv` wins.

## Files

| File | You may | Holds |
|---|---|---|
| `.canon.mtsv` | read only | the rules: sheets 1-structure (what), 2-sources (where), 3-generation (how written), 4-verification (how checked) |
| `.templates.mtsv` | read; add rows only to add a language | how each notation writes each kind |
| `.spec.mtsv`, one per folder | read and write | this project's rows |
| `generate.py`, `check.py` | run only | the reference implementation of `.canon.mtsv` |
| every generated file | never edit | output |

## Workflow, in order

1. Read `.canon.mtsv`, then `.templates.mtsv`, then each `.spec.mtsv`.
2. Change only `.spec.mtsv` rows; change `.templates.mtsv` only to add a language.
3. Run `python3 generate.py .`
4. Run `python3 check.py .`
5. At `0 findings`, stop: the work is done.
6. Otherwise, for each finding, fix the source it names, then go to step 3.

## Format

- MTSV: a form feed starts each sheet; the first line is the sheet name, the second the header, then one row per line; cells are separated by tabs.
- Cell escapes: `\n` line break, `\t` tab, `\f` form feed, `\r` carriage return, `\\` backslash, `\s` a space at either edge of a cell. No other backslash.
- `—` (U+2014) is a cell that does not apply.
- In a template, `{{name}}` is a placeholder; a literal `{` or `}` is written `\{` or `\}`, which in a cell is `\\{` or `\\}`.

## Spec rows

- Sheets: `1-folders`, `2-modules`, `3-statements`, `4-expressions`, `5-texts`; header `kind · place · holds` in every sheet; all five present, header only when empty.
- `1-folders`: kind `—`, place the folder's name, holds `—`.
- `2-modules`: kind a `1-modules` kind; place the module's name where the kind holds `{{name}}`, else `—`; holds `—`.
- `3-statements`, `4-expressions`: kind a kind of `4-statements` or `5-expressions` in the parent's notation, or `—` where the parent's placeholder fixes it; place the address; holds `—`.
- `5-texts`: kind `—`; place the address; holds the characters exactly as written in the output.
- Write no row where the parent's placeholder fixes the kind and its qualifier is `one`; the parent writes that container itself.
- Address: the file's path from its folder, `#`, then `/placeholder` for each step and `/position` (0, 1, 2, …) where a placeholder holds a sequence. The statements of a body are numbered directly after the placeholder that holds the body: `page.tsx#/SourceFile/0/Body/0`.

## Always

1. Write one row per container, at its address.
2. Take every kind from `.templates.mtsv`, in the parent's notation.
3. Write `—` in every cell that does not apply.
4. Write parentheses in the spec wherever the language needs them for precedence: `+(+x)`, `(1).toString()`.
5. Fix every finding in the source that owns it.

## Never

1. Edit `.canon.mtsv`.
2. Edit a generated file.
3. Add logic, defaults or special cases to `generate.py` or `check.py`.
4. Add a template form for style. Add a form only where the forms mean different things.
5. Invent a kind or a name. Kinds come from each notation's grammar, as `.templates.mtsv` lists them.
6. Rely on row order. Order comes only from the position in an address.
7. Name `.canon.mtsv`, `.templates.mtsv`, `.canonignore` or `.spec.mtsv` in a spec.
8. Name a kind in a spec row where the parent already fixes it.

## Findings

`MISSING` a source says it and it is not there · `EXTRA` it is there and no source says it · `CHANGED` it is there and differs. The last column names the `.canon.mtsv` row that requires it.

## If stuck

If the generator or checker seems to need a change, the sources are wrong, not the tools. Stop and ask the person you work for. Do not work around it.
