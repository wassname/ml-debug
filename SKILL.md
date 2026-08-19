---
name: ml-debug
description: "Procedure for machine learning development and debugging. Execute the numbered steps and paste the filled templates into your reply. Use before queueing a run, after a run finishes or crashes, when stuck, before reporting any result, and before writing that a result looks fine. Makes 'read your data', 'assume you have a bug' and 'compare to reference code' produce artifacts the user can check."
---

# ML procedure: execute, do not summarise

If you are writing a description of what this file contains, you have already failed. Pick your
entry below, then do its steps in order, writing each output into your reply as you go.

- a run finished or crashed, go to P1
- you are about to queue or launch a run, go to P2
- you are about to report a result, or to write that something looks fine, go to P3
- two diagnostic cycles with no progress, or a metric will not move, go to P4
- no written evidence criteria for this project yet, go to P5

Write plain english. Give every credence a word and a number from the
[Kesselman list](https://gwern.net/doc/statistics/bayes/2008-kesselman.pdf#p71): almost certain
86-99, highly likely 71-85, likely 56-70, even 46-55, unlikely 31-45, highly unlikely 16-30, remote
1-15.

Nothing here tells you what to fix. The steps make you look before you decide, and the decision
stays yours, because this system is probably not in your training data.

## P1. A run finished or crashed

Steps 1 to 4 are what reading a run means, so do them even when you were asked only to read a log.
They write nothing except your reply. Steps 5 to 7 change files, so they wait for a task that asks
you to audit, decide, or act.

1. Open the log and read it end to end. State its length and confirm you read all of it. A tail
   once made three audits call a working method broken.
2. Write the measurement table. Fill it before you write one word of diagnosis.

   | risky part | expected | start | early | middle | end | quoted line |
   |---|---|---|---|---|---|---|

   Read each curve at four points, because the shape carries the diagnosis and the last number does
   not. If a metric that would settle a row does not exist, say which one, and add it to the code
   before the next run. STOP here if any cell is empty.
3. List every anomaly, including ones you would rather ignore. Each line ends explained, or being
   investigated now. An anomaly you found without looking for it is a big problem.
4. Write the prediction check against the P2 table from before this run, one row per prediction,
   marked supported, contradicted, or unresolved. Write "no predictions were recorded" if there
   were none, and then record them next time.
5. Run `/auditlog`. It owns the full audit and writes the audit file.
6. Open `TRAINING_GUIDE.md`, edit the stage this run touched, and write the earliest step of that
   stage's expected sequence that evidence does not yet support. If the file got longer, you
   appended history instead of replacing a stale claim.
7. Say what to run next and why it beats finishing, repeating, or cancelling work already queued.
   Cancel the queued work that no longer answers the question. Never stop applies to the research
   goal, never to one experiment, sweep or hypothesis.

A crash is a run and gets this procedure too. Then use judgement: a typo or a missing import gets
fixed and rerun at once, and a broken idea earns no more compute until you have read the papers and
the reference code.

## P2. You are about to queue or launch a run

1. Write which stage of `TRAINING_GUIDE.md` this run advances.
2. Fill this table. Do not queue anything until it is filled.

   | risky part | what I expect to see | what would falsify it | metric exists? |
   |---|---|---|---|

3. Add any metric whose row says no. A run that cannot separate success from failure is not worth
   the GPU time.
4. Overfit about 20 samples and paste the final loss. Near zero, or stop and fix that first.

## P3. You are about to report a result, or to say it looks fine

Do this for a positive result, a negative result, and an all-clear alike. "Everything checks out",
"nothing looks unresolved", "no open questions" and "the metrics look fine" are claims, and they are
the claims least likely to have been checked.

1. Write three or more diagnoses. Each one gets a credence, the strongest evidence for it, and the
   strongest evidence against it. Include a code bug and an invalid evaluation whenever they are
   plausible, and leave probability on an unknown cause. Do not pad the list to reach three.
2. For any diagnosis where you cannot find evidence against, write that you have not tested it and
   lower its credence.
3. Write the five most likely ways this result is invalid, each with the check that would settle it.
4. Quote complete raw samples chosen at random, and say how you chose them. Samples picked because
   they look clean prove nothing.
5. Only now write your conclusion.

Start from a substantial probability that a surprising result is invalid, and lower it as checks
rule out bugs, leakage and broken evaluation. An exciting result is more likely false than a boring
one. A machine learning system has many adaptive parts, so a broken one is often hidden by the
others compensating while the output still looks reasonable.

## P4. Stuck, after two cycles or a metric that will not move

Do both, not one.

1. Find the most-adopted implementation of the nearest method. Rank candidates by community
   adoption, then papers citing it, then code that runs. Write "no reference exists" out loud if
   that is the answer, rather than implying it by skipping this.
2. Fill one row per feature, with their file and line in every row.

   | feature | theirs (file:line) | mine | same? |
   |---|---|---|---|

   Cover algorithm tweaks, engineering tricks, hyperparameters, and which metrics they log. The
   tricks are usually in the code and not in the paper.
3. Send a fresh-eyes subagent at the module or the diff with this instruction: find at least one
   bug, we all have at least one. Report what it found, including nothing. You cannot see your own
   typos, because you know what the code was supposed to say.

## P5. No written evidence criteria yet

Write this into the project's `AGENTS.md`. Write the first draft while you still know almost
nothing, and expect it to be wrong. Its job then is to stop a null result from being explained away
later, because nobody wrote down what a null would mean.

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

Revise it whenever evidence changes what you believe, and say in the audit what you changed and why.
A frame you never revised is a frame you never tested. A frame you revised after seeing the result,
without saying so, is how a null becomes a success.

Then create `TRAINING_GUIDE.md`, under 180 lines, with the stages you can already name, every one
marked unknown. Grow it one observation at a time. It holds your current model of the system, not a
run history. Frontmatter carries only what a program can check:

```yaml
---
last_reviewed_job: 21
stages: {init: uncertain, posterior: working, writer: failing, generation: failing}
---
```

One entry per stage, saying what should become observable, in order:

```markdown
## Writer
Purpose: use the inferred user state to change decoder behavior.
Trained: writer. Frozen: decoder, encoder. Input: state at t. Loss: reply NLL.
Theory of change: state difference -> write difference -> logit difference -> behavior difference.
Expected sequence: 1. write leaves its initial scale. 2. write beats zero-write.
  3. swapping the state changes the logits. 4. generations differ. 5. they differ in the
  intended direction. 6. the effect survives out of sample.
Required observations: writer loss curve, update norm, zero-write arm, shuffled-state arm,
  first-token logits, long free generations.
Current evidence: quote a job and a number for each link you claim.
Missing evidence: the observations nobody has made yet.
Status: partial, likely, 60%.
Earliest unsupported link: step 5. Swaps move the logits, the direction is not established.
Main question: ...
```

Never put a list of possible failure causes in this file. Such a list gives an agent thirty excuses.
The expected sequence gives it one question: which link should be visible by now, and is it?

## Reference

Open the one the situation calls for. These widen a hypothesis space and are not authoritative for
your system. The practitioner folklore behind this procedure is in [README.md](README.md).

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
