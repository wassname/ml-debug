# Running: order of work, timing pilot, job label, lab report

The run-time practices that the `ml-debug` steps use. Each section has the rule and a short example.
<!-- CLAUDE (PI, Fable) with wassname, 2026-11-15. The practices are wassname's, from his queueing and journal skill; the wording and the examples are Claude's unless quoted. Example values are illustrative, not measurements. -->

## Order of work in exploring mode

Do not run 3 seeds. Do not run an ablation. Do not rerun the baseline. Do these only after the
method works on an evaluation that you have checked.

1. Check the evaluation: the unmodified model completes the task, a null scores at the floor, and
   you have read sampled outputs.
2. Make the method work on that evaluation. Change several things per run. Choose changes whose
   effects are distinguishable in the logged metrics, or in a follow-up run if the method works.
3. Then the baseline, matched to the working method.
4. Then seeds, ablations and sweeps ([sweeps.md](sweeps.md)).

> If it takes 5 hours to run, we might only get 4 runs a day, so we need to make them as
> informative as possible. We can't schedule a sweep or ablation of 100+ runs, so we make multiple
> changes that will have separate and distinguishable effects on the metrics. - wassname

A model's default is the reverse order: baseline, seeds and ablations of a method that does not
work yet. That measures failures with high precision.

## Timing pilot

Before a long job, run 50 real steps at the real batch size on the real data path. Put the
measured seconds per step and the projected total in the job label. A data-loading bottleneck
shows in about one minute.

```text
timing: 50 steps in 5.5 s = 0.11 s/step; 5,000 steps = 9.2 min; evaluation 12 min; total 22 min
```

## Job label

The label states the uncertainty that the run reduces and the decision that each outcome enables.
It is the only record of the purpose of the job, so write it for a reader who has not seen this
session. Give the same text to the run, so that `run.md` starts with it.

```sh
pueue add -l "why: unsure whether the answer-only loss mask raises exact match vs job 37; resolve: adopt the mask if exact match is higher and replies are complete; 0.11 s/step, 22 min" -- just train --mask answer
```

| label | fault |
|---|---|
| `train run 4` | No uncertainty, no decision. |
| `why: test the mask` | States an action, not the uncertainty or what each outcome changes. |
| `why: mask should fix it; resolve: confirm` | Only one outcome is considered. |

`pueue` is recommended: one GPU job at a time, a label and a persistent log per job
(`pueue status`, `pueue log <id>`, `pueue follow <id>`). `pueue clean` deletes the labels of
finished jobs; copy them into the journal first. Any queue with labels and persistent logs is
sufficient.

## Lab report

One entry in `RESEARCH_JOURNAL.md` per run that changes a belief, written as a lab report: a
reader with no memory of the session must be able to evaluate it. Append at the end; never edit
an earlier entry; a correction is a new entry. Full example:
[examples/toolkit/lab_report.md](../examples/toolkit/lab_report.md).

```markdown
### 2026-03-01 12:05 -- answer-only loss mask: small gain, not separable from seed variance

Context. Commit, job id, command, model, evaluation size, mode.
Prediction, written before the run: "<claim>: 60%. If higher, 75%; if not, 35%."
Evidence: the table copied from the run log. Source: `outputs/<run>/run.md`, section "Result".
Interpretation (mine): what I conclude, with a credence, and the credence I move to.
Alternative: a second explanation, and the test that separates the two.
Next: the queued job, with its label.
```

- Evidence is copied from the log with its `path:line` or section, not retyped from memory.
- Interpretation is in the first person and is labelled. Use one calibrated word or a %.
- Do not set a numeric pass threshold in advance without a derivation. State the prediction and
  the credence you would move to for each outcome.
- No words that claim a quality: "striking", "promising", "interesting".
