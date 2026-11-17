# docs/results.md, organised by question

<!-- Moved from the repo-setup skill by PI/Claude, 2026-11-17; wassname's practices. -->


The journal is append-only and time-ordered. `docs/results.md` is the
orthogonal cut: organized by the question each run answers, curated, and
regenerated from a script (`just results`) on top. Keep both, since they serve
different reads ("what did I do on date X" vs "what is the current best answer
to question Y"). Two things carry the doc and must not be dropped: every
section is titled by the question it answers (the "why"), and every section
ends with a one-line **Answer** that states the conclusion. Everything else
(the table, the preamble, the provenance) exists to support that question ->
answer arc.

Read it like a short paper or lab report, not a dump: a "How to read this"
preamble defines the metrics and comparison rules once, and under each table a
few sentences of interpretation reason from the numbers to the answer. Define
jargon the first time it appears, and put the data provenance (logs, commit,
input version, run ids) in an HTML comment so any row can be re-created from the
comment alone. Clarity comes from the structure (question headings, the table,
one `**Answer:**` lead-in), so there is no need to shout: keep bold to about one
emphasis per section rather than a bold word in every line. The example below
is meant to make those properties self-evident.

The last column is `argv`. With tyro (and tyro subcommands) the CLI invocation
fully describes a variant, so logging it makes each row both self-describing
and copy-paste reproducible, and it replaces a hand-maintained "which parameter
differs" column.

### Example (`docs/results.md` excerpt)

````markdown
# Results, organized by the question each run answers

## How to read this

- Rates are the mean over the final five training steps (the converged regime),
  written as absolute fractions. Compare rows within a table by eye.
- "hack" is the fraction of student rollouts a detector flags as reward-hacks;
  "solve" is the fraction that pass the held-out ground-truth tests.
- A projection-vs-baseline difference is quoted only when the two runs share a
  seed (paired); a multi-seed mean is never compared against a single-seed point.
- Numbers are only compared within one `eval_version` (v3 here). A bump means
  the evaluation changed (judge, rubric, prompt, or metric), so pre-bump rows are
  measured on a different scale and never pooled with post-bump rows.
- "±std" is the spread across seeds; a blank means a single seed. Runs that did
  not log every training step are excluded.

## Q1. Does gradient projection reduce hacking relative to vanilla GRPO?

<!-- runs: logs/*_vanilla_s4{1,2,3}.log, logs/*_proj_s4{1,2,3}.log
     commit: a1b2c3d   pueue: 153,154,170,171
     v_hack: out/v21.safetensors (extracted at commit 9f8e7d6, 16 pairs) -->

Held fixed for this table: eval_version=v3, fast preset, mix=0.5, top-k=5, one_sided gate, 20 steps.

| method  |  hack |  ±std | solve |   n | argv                                              |
| :------ | ----: | ----: | ----: | --: | :------------------------------------------------ |
| vanilla | 0.719 | 0.120 | 0.306 |   3 | `run vanilla --mix 0.5`                           |
| proj    | 0.588 | 0.131 | 0.256 |   3 | `run projected --mix 0.5 --vhack v21.safetensors` |

**Answer: a consistent-in-sign reduction.** Projection lowers the hack rate by
about 13 points (0.719 to 0.588) while the solve rate falls about 5 points. The
reduction is negative on all three seeds once paired by seed, so its sign is
reliable. The across-seed spread (~0.13) is close to the effect itself, so the
magnitude is not yet pinned down and needs more seeds before any precise claim.
````

### Evaluation version

The evaluation is the measuring instrument. Change the judge model, the rubric, the prompt
template, the pass/fail threshold, or the metric definition, and every number
shifts for reasons unrelated to the method under test. Comparing across that change
has the same fault as comparing across seeds or across several changed
settings: you cannot separate the effect of the method from the effect of the evaluation.

Give the evaluation a version, so that the comparison cannot happen by accident:

```python
# mypackage/eval.py -- ONE canonical constant, next to the code it versions.
# Bump on ANY change to the eval DEFINITION: judge model/rubric, prompt
# template, metric formula, pass threshold, or the eval dataset. Do NOT bump
# for refactors that leave the numbers identical. One line of changelog per bump.
EVAL_VERSION = "v3"   # v3: switch judge to sonnet-4.5, add held-out test split
```

Rules:
- The version lives beside the eval code (single source of truth), gets stamped
  into `metadata.json` and every `results.tsv` row, and is a grouping/filter key
  in `just results` so pre- and post-bump rows never pool into one group.
- Bump on a *definition* change, not a code path change. A refactor that leaves
  the metric bit-identical keeps the version; a new judge or rubric bumps it.
- `results.md` compares only within a version; a cross-version delta is quoted
  only after re-running the older method under the current version.

### Two ways to feed it

Both end in the same polars-grouped markdown table; pick by whether you want a
durable cross-run ledger or just to re-parse logs on demand.

(a) **Shared `results.tsv`** -- every run appends one row; all worktrees append
to the same file, so parallel/branch runs accumulate into one ledger. A single
newline-terminated line append is atomic enough on POSIX for short rows.

```python
# at the END of each run (mypackage/run.py)
import sys, dataclasses
from mypackage.eval import EVAL_VERSION
row = {**dataclasses.asdict(cfg), "eval_version": EVAL_VERSION,
       "hack": hack_l5, "solve": solve_l5,
       "argv": " ".join(sys.argv[1:])}                 # argv captured here
with open(RESULTS_TSV, "a") as f:                      # shared across worktrees
    f.write("\t".join(str(row[c]) for c in COLS) + "\n")
```

(b) **Parse logs at read time** -- no ledger; `just results` globs `logs/*.log`
and pulls the one-line summary each run prints at the end (bottom-line-up-front,
the final metrics line). Slower but stateless.

Either source feeds one script, grouped into comparable sets of runs (same everything
except the parameter under test), argv last:

```python
# scripts/results.py  -- `just results` runs this
import polars as pl
from tabulate import tabulate

df = pl.read_csv("results.tsv", separator="\t")   # or build from parsed logs
# eval_version first: rows from different evaluation versions never pool into one group
GROUP = ["eval_version", "method", "mix", "gate", "k"]  # all-else-equal grouping keys
agg = (df.group_by(GROUP)
         .agg(pl.col("hack").mean().round(3),
              pl.col("hack").std().round(3).alias("hack_sd"),
              pl.col("solve").mean().round(3),
              pl.len().alias("n"),
              pl.col("seed").sort().str.join(",").alias("seeds"),
              pl.col("argv").first()))            # argv LAST: row is reproducible
print(tabulate(agg.to_pandas(), headers="keys", tablefmt="pipe", floatfmt="+.3f"))
```
