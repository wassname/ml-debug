---
name: ml-debug-setup
description: "Set up or audit an ML research repository so that every run is cheap to check. A smoke test on a tiny random model with shape checks, one training script that reads like pseudocode, an AGENTS.md with the goal, the names and the mental model, reference papers and code in the repository, and folders for throwaway work. Use when starting a repository, adding a smoke test, or when agents lose the goal, coin their own names, or find runtime errors only inside queued jobs. Sub-skill of ml-debug."
---

# Repository setup for ML research

Do these once per repository. Each section has the rule and a short example to copy.
<!-- CLAUDE (PI, Fable) with wassname, 2026-11-15. The practices are wassname's, from his repository-setup skill; the wording and the examples are Claude's unless quoted. Example values are illustrative, not measurements. -->

## Smoke test

One command runs the real pipeline end to end at the smallest scale. Change only the scale: the
model, the number of batches, the number of updates, the number of generated tokens. Use the real
data loaders, the real evaluation and real disk I/O; no stubs. The scores are meaningless. It
detects runtime errors, shape errors and dtype errors.

- Model: a tiny random model of the same architecture, for example
  [wassname/qwen3-5lyr-tiny-random](https://huggingface.co/wassname/qwen3-5lyr-tiny-random).
- Size: 2 batches and 2 updates for every stage (train, extract, evaluate).
- Device: the GPU, in the foreground, so that the real dtype (for example bf16) is tested. A tiny
  model uses a small fraction of the GPU, so it can run beside a queued job. Do not put it in
  the queue.
- Harness: the same entry point and the same code as the real run, with a smaller config (a
  `--fast-dev-run` flag or preset on the dataclass config). Do not write a second, "lite" harness.
- Coverage: enough steps to trigger each periodic action (checkpoint save, scheduler step,
  evaluation). If the pipeline has a disk cache, run it twice, so that the cache-read path executes.
- Time: under 3 minutes. Read its last 40 lines.
- Shape checks: [jaxtyping](https://docs.kidger.site/jaxtyping/) annotations on function inputs
  and outputs, checked by [beartype](https://beartype.readthedocs.io/) in this run only.

```just
# justfile
smoke:
    BEARTYPE=1 uv run python train.py --model wassname/qwen3-5lyr-tiny-random --batches 2 --steps 2 --eval-items 2
```

If the smoke test does not execute a code path, treat that path as untested: extend the smoke
test. Do not use a real model to find a syntax error.

A second size is useful: a small development run on a small real model (for example
`Qwen/Qwen3-0.6B`) and a small evaluation, under 30 minutes. Its scores are real and have high
variance; use it in exploring mode.

```python
# mypackage/__init__.py: runtime shape and dtype checks, enabled by the smoke test only
import os
if os.environ.get("BEARTYPE"):
    from beartype.claw import beartype_this_package
    beartype_this_package()
```

## The training script reads like pseudocode

One file. The new logic (forward pass, loss, update) is linear, top to bottom, with shapes in the
signatures. Diagnostics are inline, not in a second script.

```python
from jaxtyping import Float, Int
from torch import Tensor

def answer_loss(logits: Float[Tensor, "b s v"], labels: Int[Tensor, "b s"],
                mask: Float[Tensor, "b s"]) -> Float[Tensor, ""]:
    nll = cross_entropy(logits.flatten(0, 1), labels.flatten(), reduction="none")  # (b*s,)
    return (nll * mask.flatten()).sum() / mask.sum()

for step, batch in enumerate(loader):
    loss = answer_loss(model(batch.ids).logits, batch.labels, batch.mask)
    loss.backward(); opt.step(); opt.zero_grad()
    if step % eval_every == 0:
        log_metrics(step, loss, exact_match(model, heldout))   # one row of the table in run.md
        log_demo(model, heldout[0])                            # the same prompt at every evaluation
```

## Config and command line

One dataclass holds the config; the command line is generated from it (`tyro.cli(Cfg)`). The
`argv` then describes a variant completely, so log it and put it in every result row. Defaults
are the current best settings, so that a run with no flags is the current best method.

```python
@dataclass
class Cfg:
    model: str = "wassname/qwen3-5lyr-tiny-random"   # the smoke default; the real model by flag
    steps: int = 5000
    fast_dev_run: bool = False                       # 2 batches, 2 updates, same code path

if __name__ == "__main__":
    main(tyro.cli(Cfg))
```

## One directory per run

Each run writes `outputs/<date>_<name>_<seed>/`. A reader must be able to reconstruct and check
the run from that directory alone.

```text
outputs/20260301T1140_answer_mask_s0/
  metadata.json          # commit, argv, resolved config, start and end time, host
  run.md                 # the run log and result page (the ml-debug-logging skill)
  metrics_train.csv      # rectangular metrics, one row per step
  records.jsonl          # every prompt and reply, verbatim
  ckpt_0600.safetensors  # zero-padded step, so that files sort in order
```

Name files so that the path states the purpose: `docs/specs/20260301_answer_mask.md`, not
`SPEC_4.md`; `scripts/data/01_fetch.py`, not `get_data_monday.py`. Agents do not edit a path that
contains `human`.

## Results across runs

`docs/results.md` is organised by question, not by date; the journal is the record by date. Each
section has the question as its heading, one table, and one line that starts with `Answer:`. The
provenance (logs, commit, job ids) goes in an HTML comment, so that any row can be regenerated.

The evaluation is the measuring instrument. Keep one constant beside the evaluation code and
store it with every result. Increase it when the judge, the prompt, the metric, the pass rule or
the evaluation data changes. Compare numbers only within one version; to compare across a change,
rerun the older method under the current version.

```python
EVAL_VERSION = "v3"   # v3: new judge model, held-out split added
```

```markdown
## Q1. Does the answer-only loss mask raise exact match?
<!-- runs: outputs/20260301T1140_answer_mask_s0, outputs/20260301T1010_full_seq_s0; commit 3f2a91c; jobs 37, 41 -->

| run | exact match ↑ | n | argv |
|:---|---:|---:|:---|
| answer-only mask | **0.470** | 200 | `train.py --mask answer` |
| *full-sequence loss* | *0.445* | 200 | `train.py --mask none` |

Answer: higher by 5 problems of 200 on one seed; not yet separable from seed variance.
```

## Mental model and names in AGENTS.md

`AGENTS.md` is read at the start of every session; other files are not. Put in it the names in
daily use and the current mental model, each under 20 lines ([template](AGENTS.template.md)).
The full name list is `docs/JARGON.md`. Take names from the latest one or two reference papers
and their code. A coined name is unique and long enough to signpost: "token-edit pair", not
"twin". Enforce banned terms with a lint on the files that agents write; agents do not open
`JARGON.md` before they coin a term.

```markdown
### Names

| say | not | what it is | from |
|---|---|---|---|
| token-edit pair | twin | a conversation and its copy with one word changed | user, 2026-03-01 |

### Mental model (updated 2026-03-01)

- The answer-only mask raises exact match: likely (65%). For: 0.470 against 0.445, one seed.
  Against: gradient norm is twice as large, so learning rate may be the cause. Test: job 42.
- Unexplained: exact match is still rising at step 600 in both runs.
```

## Reference sources in the repository (optional)

- `docs/papers/`: the papers the work builds on, as Markdown, so that an agent can grep and quote
  them with a line number.
- `docs/vendor/`: the reference implementation, as a pinned submodule, for the REFERENCE step of
  `ml-debug`: compare `feature | theirs (file:line) | mine`.

## Outlets for throwaway work

`slop/` for agent drafts, reviews and audits; `scripts/scratch/` for one-off scripts;
`tests/tdd/` for one-off tests. All are ignored by git. Promote a file only when a maintained
entry point needs it.
