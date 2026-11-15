---
name: ml-debug-logging
description: "Write the run log of an ML training or evaluation script: one Markdown file, run.md, that states the question, shows each metric beside the expectation written for it, and ends with the result table. Use when you write or change logging code, when a log cannot be understood from its last 40 lines, when a table does not render, or when you write SHOULD, TODO validate or FIXME statements. Sub-skill of ml-debug."
---

# The run log

<!-- CLAUDE (PI, Fable) with wassname, 2026-11-15. The practices are wassname's, from his logging skill; the wording and the examples are Claude's unless quoted. Example values are illustrative, not measurements. -->

The training script writes `run.md`. It is the log and the result page, so it must be valid
Markdown. Full example: [example_run.md](example_run.md).

- First lines: the question, the run it is compared with, and what resolves it; then `argv` and
  the resolved config as a `setting | value` table.
- One heading per stage, with the path from its parent: `## train -> step 0`.
- A blank line before and after every heading, table and code fence. A table with no blank line
  before it renders as plain text. Two blank lines before a stage heading.
- Metrics as a table decimated to 30 to 60 rows, not one line per step. Arrows on the headers
  (`↑`, `↓`). The best value in bold, baselines and floors in italics, one number per cell.
- Each diagnostic statement directly under the metric it interprets.
- One full demo per LLM-facing stage, as the model receives it: special tokens visible, not
  truncated. Use the same prompt at each evaluation, so that a change in behaviour is visible.
- Final 40 lines: status, the question again, the complete result table, a link to the raw
  records, and the path of `run.md` as the last line. Nothing prints after it.

```markdown
| run | exact match ↑ | answer loss ↓ |
|:---|---:|---:|
| answer-only mask (this run) | **0.470** | 0.41 |
| *full-sequence loss (stored run)* | *0.445* | 0.48 |
| *base model (floor)* | *0.215* | 2.41 |
```

## Sinks, progress and failure

- One message, written once. INFO goes to stdout and to `run.md`; DEBUG goes to `run.md` only.
  Keep stdout sparse: an agent reads it through `tail`.
- Plain Markdown in both: no emojis, level icons, ANSI colours or timestamp prefixes. Do not
  strip Unicode from model outputs or data.
- Open `run.md` before the work starts, and keep it when the run fails. On failure, print the
  failed stage and the error, link the full traceback, and exit with a nonzero status.
- Progress bars go to stderr, outside both sinks: ASCII `tqdm` with `mininterval=120` and
  `maxinterval=120`. Do not print one line per step.
- Close each stage with its elapsed time, and its peak GPU memory when relevant.
- Compose one section as one f-string. Build tables with `tabulate(rows, headers, tablefmt="pipe")`.
  Show a symmetric uncertainty as `value ±half-width`.

```python
import shlex
import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{message}\n", colorize=False)
logger.add(run_dir / "run.md", level="DEBUG", format="{message}\n", colorize=False)

logger.info(f"# train: {name}\n\nQuestion: {question}\n\nargv: `{shlex.join(sys.argv)}`")
logger.debug(f"\n\n## train -> step {step}\n\n{table}\n\n{statement}")   # run.md only
```

## The raw records are the source of truth

- Write every prompt, reply, special token, judge input and error verbatim to an append-only
  JSONL file (or an Inspect `.eval` log). `run.md` is a compressed view of it.
- Every view links to its source with a path relative to the project root, with a line number
  where possible. A summary without a link removes the reader's means to check the data.
- Do not paraphrase an output in a way that changes its meaning. Do not omit a failed, truncated,
  incoherent, refusing or saturated output from a summary.
- When the user says "show me", reproduce the text. Do not describe it.

## Diagnostic statements

A diagnostic statement is a prediction, written before the observation, placed beside the metric
it concerns. It makes a later mismatch visible and states what the mismatch would indicate. Full
rules and harmful examples: [diagnostic_statements.md](diagnostic_statements.md).

Models state expectations with more confidence than their record supports, and a later reader
debugs around a wrong `SHOULD`. So the default is `TODO validate:`.

| keyword | use it when | example |
|---|---|---|
| `SHOULD [basis]: ... ELSE ...` | The expectation follows from a mechanism, a derivation, a paper, or a run that validated it. Name the basis. | `SHOULD [mechanism: LoRA B is zero at initialisation]: step-0 score equals the base model's. ELSE the adapter path is not an identity.` |
| `TODO validate: ...` | Every other expectation. Add a credence if you have one. | `TODO validate (60%): exact match is higher with the answer-only mask; compare with job 37 at equal steps.` |
| `FIXME: ...` | A fault that was observed. | `FIXME: 14 of 200 held-out prompts are also in the training set.` |

- Predict a direction, an ordering, a relation to a control, or an invariant. Do not predict a
  number. `SHOULD: accuracy > 0.7` with no derivation is an invented threshold.
- Do not write the diagnosis for a violation unless the causal link has been validated. State what
  the violation distinguishes.
- After the run, mark each statement as held or violated in the lab report (the journal entry for the run), and state which
  belief changed.
