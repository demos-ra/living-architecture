#!/usr/bin/env python3
# living-architecture: check.py, proves a project's code equals its MTSV grids
# Copyright (C) 2026 Demos Ra <demos_ra@hotmail.com>
# SPDX-License-Identifier: AGPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Reference implementation of canon's 4-verification.

Regenerates the PROJECT in memory with generate.py and compares it with what is
on disk, less what .canonignore lists, read by git itself. Holds no truth of its
own. Rows cited are .canon.mtsv sheet and row. Every finding names the source
that owns it; the output is never changed (4-verification 162).
"""
import os
import subprocess
import sys

from generate import (NONE, SPEC_SHEET, TEMPLATE_SHEET, Generator, parse_template,
                      read_mtsv, sheet_rows)

RESERVED = (".canon.mtsv", ".templates.mtsv", ".canonignore", ".spec.mtsv")  # 2-sources 47
CANON_SHEETS = ("1-structure", "2-sources", "3-generation", "4-verification")  # 2-sources 57
CANON_HEADER = ["container", "part", "requirement", "rationale"]
TEMPLATE_HEADER = ["notation", "kind", "template", "encoding"]  # 2-sources 62
PLACEHOLDER_HEADER = ["container", "notation", "kind", "place", "holds", "holds_kind",
                      "qualifier", "prefix", "separator", "suffix", "offset"]  # 2-sources 63
SPEC_HEADER = ["kind", "place", "holds"]  # 2-sources 66


class Checker:
    def __init__(self, root, reference_canon):
        self.root = root
        self.reference = reference_canon
        self.findings = []

    def find(self, finding, where, what, row):  # 4-verification 161
        self.findings.append((finding, where, what, row))

    def run(self):
        for name in RESERVED[:3]:  # 4-verification 179
            if not os.path.isfile(os.path.join(self.root, name)):
                self.find("MISSING", name, "at the project root", "4-verification 179")
        if self.findings:
            return self.findings
        self.sources()
        generator = Generator(self.root, report=self.find).walk()  # 4-verification 160, 173
        self.spec_rows(generator)
        self.disk(generator)
        return self.findings

    # the sources: sheets, headers, cells

    def shape(self, path, sheets, names, header_of):
        for name, copies in sheets.items():
            if len(copies) > 1:
                self.find("EXTRA", path, f"sheet {name} {len(copies)} times", "4-verification 164")
        for name in names:
            if name not in sheets:
                self.find("MISSING", path, f"sheet {name}", "4-verification 165")
            elif sheets[name][0][0] != header_of(name):
                self.find("CHANGED", f"{path} {name}", "header", "4-verification 167")

    def sources(self):
        canon = os.path.join(self.root, ".canon.mtsv")
        self.shape(".canon.mtsv", read_mtsv(canon), CANON_SHEETS, lambda n: CANON_HEADER)
        with open(canon, "rb") as a, open(self.reference, "rb") as b:  # 4-verification 166
            if a.read() != b.read():
                self.find("CHANGED", ".canon.mtsv", "not identical to the canon this checker implements",
                          "4-verification 166")
        templates = read_mtsv(os.path.join(self.root, ".templates.mtsv"))
        self.shape(".templates.mtsv", templates, list(TEMPLATE_SHEET.values()) + ["6-placeholders"],
                   lambda n: PLACEHOLDER_HEADER if n == "6-placeholders" else TEMPLATE_HEADER)
        self.template_cells(templates)

    def template_cells(self, sheets):
        def must_be_none(where, row, columns):  # 4-verification 168
            for c in columns:
                if row.get(c) != NONE:
                    self.find("CHANGED", where, f"{c} is not —", "4-verification 168")

        rows = {c: sheet_rows(sheets, s) for c, s in TEMPLATE_SHEET.items()}
        for r in rows["MODULE"]:
            must_be_none(f"1-modules {r['kind']}", r, ("notation", "template", "encoding"))
        for r in rows["FILE"]:
            if r["notation"] == NONE:
                must_be_none(f"2-files {r['kind']}", r, ("template", "encoding"))
        for c in ("BODY", "STATEMENT", "EXPRESSION"):
            for r in rows[c]:
                must_be_none(f"{TEMPLATE_SHEET[c]} {r['notation']} {r['kind']}", r, ("encoding",))
        placeholders = sheet_rows(sheets, "6-placeholders")
        keyed = {(p["container"], p["notation"], p["kind"], p["place"]) for p in placeholders}
        for c in ("FILE", "BODY", "STATEMENT", "EXPRESSION"):  # 4-verification 172, both ways
            for r in rows[c]:
                if r["template"] == NONE:
                    continue
                for is_placeholder, place in parse_template(r["template"]):
                    if is_placeholder and (c, r["notation"], r["kind"], place) not in keyed:
                        self.find("MISSING", f"6-placeholders {c} {r['notation']} {r['kind']}",
                                  f"row for {{{{{place}}}}}", "4-verification 172")
        for p in placeholders:
            where = f"6-placeholders {p['container']} {p['notation']} {p['kind']} {p['place']}"
            if p["container"] != "MODULE":
                template = next((r["template"] for r in rows.get(p["container"], [])
                                 if (r["notation"], r["kind"]) == (p["notation"], p["kind"])), None)
                if template is None or p["place"] not in [v for t, v in parse_template(template) if t]:
                    self.find("EXTRA", where, "no placeholder of its template", "4-verification 172")
            else:
                must_be_none(where, p, ("prefix", "separator", "suffix", "offset"))
            if p["holds"] in ("FILE", "BODY") and p["qualifier"] != "one":  # 4-verification 174
                self.find("CHANGED", where, "qualifier is not one", "4-verification 174")
            if p["qualifier"] != "sequence":  # 2-sources 73
                must_be_none(where, p, ("separator",))
            if p["qualifier"] == "one":
                must_be_none(where, p, ("prefix", "suffix"))
            if p["holds"] == "TEXT":
                must_be_none(where, p, ("holds_kind",))

    # the spec: rows the walk did not reach, addresses, cells

    def spec_rows(self, generator):
        for folder, spec in generator.specs.items():
            where = os.path.normpath(os.path.join(folder, ".spec.mtsv"))
            self.shape(where, spec.sheets, list(SPEC_SHEET.values()), lambda n: SPEC_HEADER)
            places = {}
            for container, sheet in SPEC_SHEET.items():
                for r in sheet_rows(spec.sheets, sheet):
                    if r["place"] in RESERVED:  # 4-verification 163
                        self.find("EXTRA", f"{where} {sheet}", f"RESERVED name {r['place']}", "4-verification 163")
                    if r["place"] != NONE:  # 4-verification 171
                        if r["place"] in places:
                            self.find("EXTRA", f"{where} {sheet}", f"a second container at {r['place']}",
                                      "4-verification 171")
                        places[r["place"]] = sheet
                    if container in ("STATEMENT", "EXPRESSION", "TEXT") and id(r) not in spec.used:
                        self.find("EXTRA", f"{where} {sheet} {r['place']}",
                                  "no placeholder of its parent fills it here", "4-verification 199 203 207 172")
                    nones = {"FOLDER": ("kind", "holds"), "MODULE": ("holds",), "STATEMENT": ("holds",),
                             "EXPRESSION": ("holds",), "TEXT": ("kind",)}[container]
                    for c in nones:  # 4-verification 168
                        if r[c] != NONE:
                            self.find("CHANGED", f"{where} {sheet} {r['place']}", f"{c} is not —",
                                      "4-verification 168")
                    if container == "MODULE":  # 2-sources 85
                        if "{{name}}" in r["kind"] and r["place"] == NONE:
                            self.find("MISSING", f"{where} {sheet} {r['kind']}",
                                      "a name for {{name}}", "4-verification 168")
                        if "{{name}}" not in r["kind"] and r["place"] != NONE:
                            self.find("CHANGED", f"{where} {sheet} {r['kind']}",
                                      "place is not —: the KIND fixes the name", "4-verification 168")

    # the disk: what git lists, less .canonignore

    def git_files(self, *flags):
        out = subprocess.run(["git", "-C", self.root, "ls-files", "-z", *flags],
                             capture_output=True, check=True).stdout
        return {os.path.normpath(p) for p in out.decode("utf-8").split("\0") if p}

    def disk(self, generator):
        ignore = os.path.abspath(os.path.join(self.root, ".canonignore"))  # 4-verification 157
        on_disk = (self.git_files("-c", "-o")
                   - self.git_files("-c", "-o", "-i", f"--exclude-from={ignore}"))
        on_disk = {p for p in on_disk if os.path.exists(os.path.join(self.root, p))}
        expected = set(generator.files) | generator.assets
        for path, data in sorted(generator.files.items()):
            if path not in on_disk:
                self.find("MISSING", path, "GENERATED FILE", "4-verification 191")
            else:
                with open(os.path.join(self.root, path), "rb") as f:
                    if f.read() != data:  # 4-verification 175, 192, 208
                        self.find("CHANGED", path, "bytes differ from the regenerated output",
                                  "4-verification 192")
        for path in sorted(generator.assets - on_disk):
            self.find("MISSING", path, "ASSET FILE", "4-verification 191")
        for path in sorted(on_disk - expected):
            if os.path.basename(path) not in RESERVED:  # 4-verification 191
                self.find("EXTRA", path, "at no placeholder row's path", "4-verification 191")
        disk_dirs = {os.path.dirname(p) or "." for p in on_disk}
        for d in sorted(generator.dirs - {"."}):  # 4-verification 182
            if not os.path.isdir(os.path.join(self.root, d)):
                self.find("MISSING", d, "FOLDER directory", "4-verification 182")
        for d in sorted(disk_dirs - generator.dirs):
            self.find("EXTRA", d, "directory not named in 1-folders nor made by a placeholder row's path",
                      "4-verification 182")


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    here = os.path.dirname(os.path.abspath(__file__))
    reference = argv[2] if len(argv) > 2 else os.path.join(here, ".canon.mtsv")
    findings = Checker(root, reference).run()
    for finding, where, what, row in findings:
        print(f"{finding}\t{where}\t{what}\t{row}")
    print(f"{len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
