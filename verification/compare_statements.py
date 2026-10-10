#!/usr/bin/env python3
"""compare_statements.py -- check that the Lean theorems proved here are the Clay (C) and (D)
statements of Formal Conjectures.

Usage: python3 compare_statements.py FORMAL_CONJECTURES_FILE [REPO_ROOT]

FORMAL_CONJECTURES_FILE is FormalConjectures/Millenium/NavierStokes.lean from
google-deepmind/formal-conjectures, at the commit the challenge names
(8bf45ed70d48b2b2a501de9c00b26bfa38c573ee).  The script strips comments, attributes and
whitespace, splits each file into its declarations and compares them by name:

  1. every declaration of ComparatorChallenges/NavierStokes.lean (the challenge) is
     identical to the declaration of the same name in Formal Conjectures, and the only
     Formal Conjectures declarations missing from the challenge are (A) and (B);
  2. NavierStokes/ComparatorDefinitions.lean, which the proof imports, has the same
     declarations as the challenge except the two challenge theorems;
  3. the statements of navier_stokes_breakdown_R3 and navier_stokes_breakdown_periodic in
     NavierStokes/ComparatorSolution.lean are identical to those of the challenge.

Prints ALL OK on success, otherwise the differing declarations, and exits with status 1.
"""
import re
import sys
from pathlib import Path

DECL = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+)*"
                  r"(def|theorem|lemma|abbrev|structure|instance|class)\s+([^\s:({\[]+)")
STOP = re.compile(r"^(end\b|namespace\b|section\b|open\b|variable\b|local notation\b|notation\b|"
                  r"public section|@\[expose\]|import\b|public import\b)")


def strip_comments(text):
    out, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            i += 1
        elif text.startswith("--", i):
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def strip_attributes(text):
    # remove @[...] blocks, which may span lines and nest brackets
    out, i = [], 0
    while i < len(text):
        if text.startswith("@[", i):
            depth, i = 1, i + 2
            while i < len(text) and depth:
                depth += {"[": 1, "]": -1}.get(text[i], 0)
                i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def declarations(path):
    text = strip_attributes(strip_comments(Path(path).read_text()))
    decls, name, buf = {}, None, []
    pending = ""
    for line in text.splitlines():
        s = line.strip()
        if s == "noncomputable":
            pending = "noncomputable "
            continue
        m = DECL.match(pending + s) if s else None
        if m or (s and STOP.match(s) and not line.startswith((" ", "\t"))):
            if name:
                decls[name] = " ".join(" ".join(buf).split())
            name, buf = (m.group(2), [pending + s]) if m else (None, [])
            pending = ""
            continue
        pending = ""
        if name:
            buf.append(s)
    if name:
        decls[name] = " ".join(" ".join(buf).split())
    return decls


def statement(decl):
    return decl.split(":= by", 1)[0].split(":=", 1)[0].strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    fc = declarations(sys.argv[1])
    root = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent)
    ch = declarations(root / "ComparatorChallenges/NavierStokes.lean")
    df = declarations(root / "NavierStokes/ComparatorDefinitions.lean")
    so = declarations(root / "NavierStokes/ComparatorSolution.lean")
    failed = []

    def check(name, ok, detail=""):
        print(("ok    " if ok else "FAIL  ") + name + (f"  ({detail})" if detail else ""))
        if not ok:
            failed.append(name)

    targets = ["navier_stokes_breakdown_R3", "navier_stokes_breakdown_periodic"]
    diff = [n for n in ch if fc.get(n) != ch[n]]
    check(f"challenge: {len(ch)} declarations, each identical to Formal Conjectures", not diff,
          ", ".join(diff))
    extra = sorted(set(fc) - set(ch))
    check("Formal Conjectures declarations missing from the challenge are (A) and (B) only",
          extra == ["navier_stokes_existence_and_smoothness_R3",
                    "navier_stokes_existence_and_smoothness_periodic"], ", ".join(extra))
    for t in targets:
        check(f"challenge contains {t}", t in ch)
    diff = [n for n in df if ch.get(n) != df[n]]
    missing = sorted(set(ch) - set(df))
    check(f"definitions used by the proof: {len(df)} declarations, each identical to the challenge",
          not diff, ", ".join(diff))
    check("the definitions module leaves out exactly the two challenge theorems",
          missing == sorted(targets), ", ".join(missing))
    for t in targets:
        ok = t in so and t in ch and statement(so[t]) == statement(ch[t])
        check(f"proved statement of {t} is the challenge statement", ok)
    if failed:
        print("FAILED:", ", ".join(failed))
        sys.exit(1)
    print("ALL OK")


if __name__ == "__main__":
    main()
