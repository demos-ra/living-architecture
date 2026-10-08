#!/usr/bin/env python3
# living-architecture: generate.py, writes a project from its MTSV grids
# Copyright (C) 2026 Demos Ra <demos_ra@hotmail.com>
# SPDX-License-Identifier: AGPL-3.0-only WITH AdditionRef-LA-generated-output-exception-1.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation, with the additional
# permission of the living-architecture Generated Output Exception,
# version 1.0 (EXCEPTION.md).
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Reference implementation of canon's 3-generation.

Writes a PROJECT from its .templates.mtsv and .spec.mtsv. It holds no truth of
its own: every name, character and layout comes from those two sources, read
as .canon.mtsv says. Rows cited are .canon.mtsv sheet and row.
"""
import os
import sys

# 2-sources 49, 52: an MTSV file of sheets; a form feed starts a sheet; cell escapes.
ESCAPES = {"n": "\n", "t": "\t", "f": "\f", "r": "\r", "\\": "\\", "s": " "}


def read_cell(raw):
    out = []
    i = 0
    while i < len(raw):
        if raw[i] == "\\":
            if i + 1 == len(raw) or raw[i + 1] not in ESCAPES:
                raise ValueError(f"a backslash outside an escape: {raw!r}")
            out.append(ESCAPES[raw[i + 1]])
            i += 2
        else:
            out.append(raw[i])
            i += 1
    return "".join(out)


def read_mtsv(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    chunks = text.split("\f")
    if chunks[0] != "":
        raise ValueError(f"{path}: characters before the first sheet")
    sheets = {}
    for chunk in chunks[1:]:
        lines = chunk.split("\n")
        if lines[-1] == "":
            lines.pop()
        name = read_cell(lines[0])
        header = [read_cell(c) for c in lines[1].split("\t")]
        rows = [dict(zip(header, (read_cell(c) for c in line.split("\t")))) for line in lines[2:]]
        sheets.setdefault(name, []).append((header, rows))
    return sheets


def sheet_rows(sheets, name):
    return sheets[name][0][1] if name in sheets else []


NONE = "—"  # 2-sources 53
TEMPLATE_SHEET = {"MODULE": "1-modules", "FILE": "2-files", "BODY": "3-bodies",
                  "STATEMENT": "4-statements", "EXPRESSION": "5-expressions"}  # 2-sources 62
SPEC_SHEET = {"FOLDER": "1-folders", "MODULE": "2-modules", "STATEMENT": "3-statements",
              "EXPRESSION": "4-expressions", "TEXT": "5-texts"}  # 2-sources 66


def parse_template(template):
    """2-sources 70: characters with {{placeholder}} placeholders, a literal { written as \\{ and } as \\}."""
    parts, text, i = [], [], 0
    while i < len(template):
        if template.startswith("\\{", i) or template.startswith("\\}", i):
            text.append(template[i + 1])
            i += 2
        elif template.startswith("{{", i):
            j = template.index("}}", i + 2)
            if text:
                parts.append((False, "".join(text)))
                text = []
            parts.append((True, template[i + 2:j]))
            i = j + 2
        else:
            text.append(template[i])
            i += 1
    if text:
        parts.append((False, "".join(text)))
    return parts


def cut(cell):
    return "" if cell == NONE else cell


class Spec:
    """A FOLDER's .spec.mtsv, its rows by address (2-sources 68, 69)."""

    def __init__(self, sheets):
        self.sheets = sheets
        self.at = {}
        self.children = {}
        for container in ("STATEMENT", "EXPRESSION", "TEXT"):
            for row in sheet_rows(sheets, SPEC_SHEET[container]):
                place = row["place"]
                self.at.setdefault((container, place), []).append(row)
                parent, _, last = place.rpartition("/")
                if last.isdigit():
                    self.children.setdefault((container, parent), []).append((int(last), row))
        self.used = set()

    def one(self, container, address):
        rows = self.at.get((container, address), [])
        if rows:
            self.used.add(id(rows[0]))
        return rows[0] if rows else None

    def positions(self, container, base):
        rows = sorted(self.children.get((container, base), []), key=lambda p: p[0])  # 3-generation 115
        for _, row in rows:
            self.used.add(id(row))
        return [row for _, row in rows]


class Generator:
    def __init__(self, root, report=None):
        self.root = root
        self.report = report or self.fail
        sheets = read_mtsv(os.path.join(root, ".templates.mtsv"))  # 3-generation 124: read once
        self.kinds = {c: {(r["notation"], r["kind"]): r for r in sheet_rows(sheets, s)}
                      for c, s in TEMPLATE_SHEET.items()}
        self.placeholders = {}
        self.module_files = {}
        for r in sheet_rows(sheets, "6-placeholders"):
            self.placeholders[(r["container"], r["notation"], r["kind"], r["place"])] = r
            if r["container"] == "MODULE":
                self.module_files.setdefault(r["kind"], []).append(r)
        self.files = {}      # path -> bytes of a GENERATED FILE
        self.assets = set()  # paths of ASSET FILEs, left as they are
        self.dirs = set()    # directories the walk reaches
        self.specs = {}      # FOLDER path -> Spec

    @staticmethod
    def fail(finding, where, what, row):
        raise SystemExit(f"{finding} {where}: {what} ({row})")

    # PROJECT · FOLDER · MODULE · FILE: LAYOUT

    def walk(self):
        self.folder(".")  # 3-generation 124, 128: the root FOLDER is the project root
        return self

    def folder(self, path):
        self.dirs.add(path)  # 3-generation 127
        spec_path = os.path.join(self.root, path, ".spec.mtsv")
        if not os.path.isfile(spec_path):
            return self.report("MISSING", path, "its .spec.mtsv", "4-verification 184")
        spec = Spec(read_mtsv(spec_path))  # 3-generation 129: read once
        self.specs[path] = spec
        for row in sheet_rows(spec.sheets, "1-folders"):
            self.folder(os.path.normpath(os.path.join(path, row["place"])))
        for row in sheet_rows(spec.sheets, "2-modules"):
            self.module(path, spec, row)

    def module(self, folder, spec, row):
        kind, name = row["kind"], row["place"]
        if (NONE, kind) not in self.kinds["MODULE"]:  # 3-generation 131
            return self.report("MISSING", folder, f"MODULE KIND {kind}", "4-verification 186")
        for p in self.module_files.get(kind, []):  # 3-generation 133
            path = p["place"]
            if "{{name}}" in path:  # 3-generation 132, 2-sources 89
                path = path.replace("{{name}}", name)
            self.file(folder, spec, os.path.normpath(os.path.join(folder, path)), path, p["holds_kind"])

    def file(self, folder, spec, path, name, kind):
        rows = [r for (_, k), r in self.kinds["FILE"].items() if k == kind]  # 3-generation 135
        if not rows:
            return self.report("MISSING", path, f"FILE KIND {kind}", "4-verification 190")
        row = rows[0]
        self.dirs.add(os.path.dirname(path) or ".")  # 3-generation 136
        if row["template"] == NONE:
            self.assets.add(path)  # 3-generation 136, 137: an ASSET FILE is left at its path
            return
        segments = self.render("FILE", row["notation"], kind, row["template"], name + "#", 0, spec)
        self.files[path] = layout(segments).encode(row["encoding"])  # 3-generation 137

    # BODY · STATEMENT · EXPRESSION · TEXT: SYNTAX

    def container(self, container, notation, kind, address, indent, spec):
        row = self.kinds[container].get((notation, kind))  # 3-generation 139, 143, 147
        if row is None:
            self.report("MISSING", address, f"{container} KIND {kind}, notation {notation}",
                        {"BODY": "4-verification 194", "STATEMENT": "4-verification 198",
                         "EXPRESSION": "4-verification 202"}[container])
            return []
        return self.render(container, notation, kind, row["template"], address, indent, spec)

    def render(self, container, notation, kind, template, address, indent, spec):
        segments = []  # 3-generation 117
        for is_placeholder, value in parse_template(template):
            if is_placeholder:
                segments += self.placeholder(container, notation, kind, value, address, indent, spec)
            else:
                segments.append((value, indent, False))
        return segments

    def placeholder(self, container, notation, kind, place, address, indent, spec):
        row = self.placeholders.get((container, notation, kind, place))
        if row is None:
            self.report("MISSING", address, f"placeholder {place} of {kind}", "4-verification 172")
            return []
        holds, holds_kind, qualifier = row["holds"], row["holds_kind"], row["qualifier"]
        base = address if container == "BODY" else f"{address}/{place}"  # 2-sources 68
        child_indent = indent + (int(row["offset"]) if row["offset"] != NONE else 0)  # 3-generation 120
        fills = []
        if holds == "TEXT":
            text = spec.one("TEXT", base)  # 2-sources 105, 106
            if text is not None:
                fills.append([(text["holds"], child_indent, True)])  # 3-generation 153: verbatim
        elif holds_kind != NONE and qualifier == "one":
            fills.append(self.container(holds, notation, holds_kind, base, child_indent, spec))  # 2-sources 70
        else:
            if container == "BODY" or qualifier == "sequence":
                rows = spec.positions(holds, base)  # 2-sources 68: /position
            else:
                one = spec.one(holds, base)
                rows = [one] if one is not None else []
            for r in rows:
                k = holds_kind if holds_kind != NONE else r["kind"]  # 2-sources 96, 100
                fills.append(self.container(holds, notation, k, r["place"], child_indent, spec))
        if qualifier == "one" and not fills:
            self.report("MISSING", base, f"a fill of {place}", "4-verification 174")
        if not fills:
            return []  # 3-generation 119
        segments = [(cut(row["prefix"]), indent, False)]  # 3-generation 120
        for n, fill in enumerate(fills):
            if n:
                segments.append((cut(row["separator"]), indent, False))
            segments += fill
        segments.append((cut(row["suffix"]), indent, False))
        return segments


def layout(segments):
    """3-generation 120: every line break written is followed by the indentation of the container
    that holds the next character, in spaces, and none on an empty line; a TEXT is verbatim."""
    out, pending = [], False
    for text, indent, verbatim in segments:
        for ch in text:
            if ch == "\n":
                out.append(ch)
                pending = not verbatim
            else:
                if pending:
                    out.append(" " * indent)
                    pending = False
                out.append(ch)
    return "".join(out)


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    generator = Generator(root).walk()
    for path in sorted(generator.dirs):  # 3-generation 127, 136
        os.makedirs(os.path.join(root, path), exist_ok=True)
    for path, data in sorted(generator.files.items()):  # 3-generation 111
        with open(os.path.join(root, path), "wb") as f:
            f.write(data)
    print(f"{len(generator.files)} files written, {len(generator.assets)} assets left")


if __name__ == "__main__":
    main(sys.argv)
