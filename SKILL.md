---
name: ml-debug
description: "Rituals for machine learning development and debugging: forms to fill and show the user at each trigger point, so evidence gets read instead of assumed. Use when framing an ML project's success evidence, before launching a run, after a run finishes or crashes, when stuck after two diagnostic cycles, and before reporting any result. Turns 'read your data', 'assume you have a bug', and 'compare to reference code' into artifacts the user can check."
---

# Rituals for ML development

The practitioner folklore behind every ritual here is in [README.md](README.md), written for humans.
Agents read that prose, agree with it, and then skip it: measured on ml-bench, loading the folklore
changed a model's score by +0.023 +/- 0.044, which is nothing.

So each principle below is a ritual instead: a trigger, a form, and an artifact you show the user.
A skipped ritual is then visible. The forms ask questions and never prescribe the fix, because the
judgement is yours and the system is probably not in your training data.

Fill the forms in the chat, in the audit file, or in the guide, as each ritual says. Write plain
english. Use these words for every credence, from the
[Kesselman list](https://gwern.net/doc/statistics/bayes/2008-kesselman.pdf#p71):

| Almost certain | Highly likely | Likely | Even | Unlikely | Highly unlikely | Remote |
|---|---|---|---|---|---|---|
| 86-99% | 71-85% | 56-70% | 46-55% | 31-45% | 16-30% | 1-15% |

## 1. Frame the project, once, before the first real run

Write this into the project's `AGENTS.md` and keep it there. Without it, a null result later gets
explained away, because nobody wrote down what a null would mean.

```markdown
GOAL: one paragraph, plain english. What is learned, and what is the contribution.
OPTIMISING: one sentence, no jargon, no symbols. What the loss actually rewards.
PERVERSE SATISFACTIONS: 2-3 plain-english ways to score well while doing nothing
  interesting (copy the input, learn the class prior, exploit the judge). Give each
  the metric or control arm that would expose it.
EVIDENCE A, qualitative: a full trace, out of sample, long enough to see it break.
  Name the arms: bare, treatment, reversed treatment, and a placebo that should not move.
EVIDENCE B, quantitative: beats a named baseline on a named metric, not chance.
ELSE: if A and B disagree, or either fails, say now what that means about the method.
```

## 2. Keep a training guide, under 400 lines, living

`TRAINING_GUIDE.md` in the project. The worker maintains it. It holds the current model of the
system, not a run history, so it stays small by replacing claims that went stale.

Frontmatter carries only what a program can check:

```yaml
---
last_reviewed_job: 21
stages: {init: uncertain, posterior: working, writer: failing, generation: failing}
---
```

One markdown entry per stage, and each entry says what should become observable, in order:

```markdown
## Writer
Purpose: use the inferred user state to change decoder behavior.
Theory of change: state difference -> write difference -> logit difference -> behavior difference.
Expected sequence: 1. write leaves its initial scale. 2. write beats zero-write.
  3. swapping the state changes the logits. 4. generations differ. 5. they differ in the
  intended direction. 6. the effect survives out of sample.
Required observations: writer loss curve, update norm, zero-write arm, shuffled-state arm,
  first-token logits, long free generations.
Current evidence: quote a job and a number for each link you claim.
Status: partial, likely, 60%.
Earliest unsupported link: step 5. Swaps move the logits, the direction is not established.
Main question: ...
```

Do not put a failure-mode list in this file. A list of possible causes gives an agent thirty
excuses. The expected sequence gives it one question: which link should be visible by now, and is it?

## 3. Before a run

Show the user this form. Queue nothing until it is filled.

| risky part | what I expect to see | what would falsify it | metric exists? |
|---|---|---|---|

If the metric that would show the effect does not exist yet, add it and then run. A run that cannot
distinguish success from failure is not worth the GPU time.

Also state which stage of the training guide this run advances, and paste the loss from overfitting
about 20 samples. Near zero, or something is wrong before the real run starts.

## 4. After every run, including a crash

Run `/auditlog`, which owns the full procedure. It requires the whole log, the resolved config, the
actual data, complete raw outputs from every arm, a stage table, and hypotheses that each carry a
quote, a credence, contrary evidence, and a discriminating test.

Three things this skill adds to that audit:

1. A quote-centered narrative. For each technically risky part, write what you expected to see, then
   quote the log line, metric row, or sample that shows what you did see. A summary without a quote
   does not show that you opened the log. A needed metric that is missing is a valid outcome: add it
   and run again.
2. A prediction check against the form from ritual 3, row by row, marked supported, contradicted, or
   unresolved.
3. The earliest unsupported link in the training guide, updated. Then edit the affected stage entry.
   If the guide grew, you appended run history instead of replacing a stale claim.

Anything weird gets a line in the audit, and every line ends explained or being investigated. An
anomaly you found without looking for it is a large problem, so chase it rather than hoping it goes
away.

## 5. When stuck, after two diagnostic cycles or a metric that will not move

Both of these, not one:

Reference diff. Find the most-adopted implementation of the nearest method, ranking candidates by
community adoption, then papers citing it, then code that runs. Then fill a table, one row per
feature, with their file and line in every row.

| feature | theirs (file:line) | mine | same? |
|---|---|---|---|

Cover the algorithm tweaks, the engineering tricks, the hyperparameters, and which metrics they
log, because the tricks are usually in the code and not in the paper. "No reference exists" is a
finding you must state out loud, never one you imply by skipping the table.

Subagent bug hunt. Send a fresh-eyes subagent at the module or the diff with the instruction: find
at least one bug, we all have at least one. Report what it found, including nothing. You cannot see
your own typos because you know what the code was supposed to say.

## 6. Before reporting any result

Three artifacts, every time, for a positive result as much as a negative one:

1. Three or more diagnoses with credences, including a code bug and an invalid evaluation whenever
   they are plausible. Leave probability on an unknown cause. Do not pad the list to reach three.
2. The five most likely ways this result is invalid, each with the check that would settle it.
3. Complete raw samples, chosen at random, quoted. Say how you chose them. Samples picked because
   they look clean prove nothing.

Start from a substantial probability that a surprising result is invalid, and lower it only as
checks rule out bugs, leakage, and broken evaluation. Excitement is evidence of a bug.

## Reference

Open the one the situation calls for. These widen a hypothesis space. They are not authoritative
for your system:

- [PLAYBOOK.md](PLAYBOOK.md) -- mental models, component isolation, baseline ladder, what to log, symptom tables, triage, anti-patterns.
- [refs/checklist.md](refs/checklist.md) -- Lones's 36 do/don'ts across data, training, evaluation, comparison, reporting.
- [refs/diagnostics.md](refs/diagnostics.md) -- copy-paste snippets: init loss, overfit one batch, gradient flow, NaN hooks, leakage tracer, backprop-to-input dependency check.
- [refs/static_analysis.md](refs/static_analysis.md) -- grep patterns for silent bugs.
- [refs/loss_surface.md](refs/loss_surface.md) -- visualize a custom loss and its gradient field with synthetic tensors.
- [refs/metric_stuck.md](refs/metric_stuck.md) -- why a metric will not move, plus the structural ceiling check.
- [refs/sweeps.md](refs/sweeps.md) -- paired comparison and cross-seed reliability, before claiming A beats B.
- [refs/llm_judges.md](refs/llm_judges.md) -- judge biases, repeat draws, paired differences, when an LLM-judged eval looks too good.
- [refs/time_series.md](refs/time_series.md) -- deployment-faithful temporal evaluation and causal missing values.
- [refs/research_taste.md](refs/research_taste.md) -- patience, choosing what to try, information gain, de-risking.
- [refs/transformers.md](refs/transformers.md) -- full traces, warmup and learning rate, train-deploy parity, scale priors, steering.
- [rl/SKILL.md](rl/SKILL.md) -- probe environments, reward engineering, defaults, reference implementations.
- [pinn/SKILL.md](pinn/SKILL.md) -- nondimensionalization, gradient pathologies, curriculum.

Curated by [wassname](https://github.com/wassname).
