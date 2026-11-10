#!/usr/bin/env python3
"""Print records you did not choose from each data file, and the outline and warnings of each log.

usage: python3 look.py PATH [PATH ...]   (files or directories)
"""
import random
import re
import sys
from pathlib import Path

DATA = {".jsonl", ".ndjson", ".csv", ".tsv"}
LOG = {".md", ".log", ".txt", ".out", ".err"}
FLAG = re.compile(r"\b(nan|NaN|inf)\b|WARN|ERROR|\w+(Error|Warning)\b|Traceback|SHOULD|TODO|FIXME")

seed = random.randrange(10**6)
random.seed(seed)
files = [f for p in map(Path, sys.argv[1:]) for f in (sorted(p.iterdir()) if p.is_dir() else [p])]
for f in files:
    if f.suffix not in DATA | LOG:
        print(f"\n## {f.name}: not sampled. If it holds data, print 5 random rows of it yourself.")
        continue
    lines = f.read_text(errors="replace").splitlines()
    if f.suffix in DATA:
        picked = sorted(random.sample(range(1, len(lines) + 1), min(5, len(lines))))
        print(f"\n## ml-debug look seed={seed}: {f.name}, {len(lines)} records, sampled lines {picked}")
        for n in picked:
            print(f"{f.name}:{n}: {lines[n - 1][:800]}")
        n = random.choice(picked)
        print(f"\n{f.name}:{n}, first 6000 of {len(lines[n - 1])} characters:\n{lines[n - 1][:6000]}")
    else:
        flagged = [(n, t) for n, t in enumerate(lines, 1) if FLAG.search(t)]
        print(f"\n## ml-debug look: {f.name}, {len(lines)} lines, {len(flagged)} with nan, inf, ERROR, WARN, Traceback, SHOULD or TODO")
        for n, t in [(n, t) for n, t in enumerate(lines, 1) if t.startswith("#")][:40] + flagged[:20]:
            print(f"{f.name}:{n}: {t[:200]}")

print("""
Now show under LOOK in your reply:
- for each data file: the seed and the sampled line numbers, then each record that surprised you
  with its file:line, a short quote, and the one thing you did not expect. The script picked the
  records, so do not swap them for better examples. If none surprised you, say so.
- for each log: the line ranges you read out of the total, and each line that surprised you,
  quoted with its number and ending "explained: ..." or "chasing now". The lines above are an
  outline, not the log.""")
