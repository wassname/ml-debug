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

`pueue` is recommended; any queue with labels and persistent logs is sufficient.

- One GPU lane with one job at a time. Two GPU jobs that start together compete for memory.
  API-only jobs go in a separate group. A smoke test does not go in the queue.
- Run `pueue add -w "$PWD"` from the worktree that holds the code you mean to run.
- A command with a redirect or a pipe goes after `--` as one quoted string.
- `pueue clean` and `pueue reset` delete the labels of finished jobs. Copy the labels into the
  journal first.

## Follow the job

> - agents are lazy and don't read the log
> - agents forget to monitor long jobs and need some way to be woken up. sleep is token
>   inefficient. wait is ok but doesn't show log. follow does all
> -- wassname

Start one background follower per job at the moment you queue it, so that its end wakes you:

```sh
pueue follow <id> | tail -n 40      # for a job that is still queued: pueue wait <id> first
```

The wake-up means that the job ended, not that it succeeded: the pipe returns the exit status of
`tail`. Read the 40 lines, and check the result with `pueue status`. Do not poll with `sleep`.
Then read the whole of `run.md`, not its tail, before you report (the LOOK step).

## Lab report

One entry in `RESEARCH_JOURNAL.md` per run that changes a belief, appended at the end; a
correction is a new entry. The format, with the competing explanations and the prediction
written before the run, is the [ml-debug-journal](../journal/SKILL.md) skill. Full example:
[examples/toolkit/lab_report.md](../examples/toolkit/lab_report.md).
