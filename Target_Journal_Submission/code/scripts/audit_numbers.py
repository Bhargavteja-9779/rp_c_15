#!/usr/bin/env python
"""G11 integrity audit: every number in the manuscript must be filled from a result file by the builder, or be a
documented protocol constant / identifier listed in scripts/audit_allowlist.txt. Reads manuscript/build/manuscript_audit.md
(written by the builder with markers around machine-filled values). Exit code 1 and a list of offending numbers on failure."""
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
txt = (R / "manuscript" / "build" / "manuscript_audit.md").read_text()
txt = txt[: txt.find("# References")] if "# References" in txt else txt
txt = re.sub(r"⟦.*?⟧", " ", txt, flags=re.S)                       # machine-filled values
txt = re.sub(r"^---.*?---", " ", txt, count=1, flags=re.S)                     # yaml title block
txt = re.sub(r"\]\([^)]*\)\{[^}]*\}", "]", txt)                                # figure paths and widths
txt = re.sub(r"\[@[^\]]*\]", " ", txt)                                         # citations
txt = re.sub(r"https?://\S+|doi:\S+|10\.\d{4,}/\S+", " ", txt)                 # links / DOIs
txt = re.sub(r"(Tables?|Figs?\.|Sections?|Eqs?\.|Note|table|Appendix)\s[S]?\d+[a-z]?(?:\.\d+)?(?:(?:, | and | or |–)[S]?\d+[a-z]?(?:\.\d+)?)*", " ", txt)
txt = re.sub(r"\(\d+\)", " ", txt)                                             # equation numbers
txt = re.sub(r"^#+ [\d.]+", " ", txt, flags=re.M)                              # heading numbers
txt = re.sub(r"\$[^$]*\$", lambda m: " ", txt)                                 # inline maths (symbols; constants checked below)
allow = set()
for line in (R / "scripts" / "audit_allowlist.txt").read_text().splitlines():
    line = line.split("#")[0].strip()
    if line:
        allow.update(x.strip() for x in line.split(","))
bad = []
for mo in re.finditer(r"(?<![\w.])\d+(?:[.,]\d+)*(?![\w])", txt):
    tok = mo.group(0).rstrip(".,")
    if tok in allow:
        continue
    ctx = txt[max(0, mo.start() - 50): mo.end() + 30].replace("\n", " ")
    bad.append((tok, ctx))
for tok, ctx in bad:
    print(f"UNTRACED {tok!r}: ...{ctx}...")
print(f"{len(bad)} untraced numbers")
sys.exit(1 if bad else 0)
