---
name: ml-debug-audit
description: "Checks a finished or crashed run by reading its data: the whole log, sampled raw records, and the records behind the headline number, recomputed by hand. Use when a run or pueue job ends and its result matters, before you write that a result is good or bad, or when the user asks what a run actually showed (/auditlog). Replaces auditlog. Sub-skill of ml-debug."
---

# Audit a run by reading its data

<!-- PI/Claude, 2026-11-17, from wassname: "it's just about making it read the data, spot check it". Replaces the auditlog skill and the audit form in references/exercises.md. -->

> Read your data. Often, the quality of the data is a crucial driver of the results of your experiments. Often, it is quite bad. -- Nanda

A summary table can be wrong while every row in it looks plausible: the caption describes a different rule than the code, a broken reply scores as a success, the run used other code than you think. You find these only by reading the records the number came from. Read first, then say what the run showed.

## Steps

1. **The question.** Quote the job label, the `run.md` question or the plan: what this run was meant to decide, and what you predicted. If nothing was recorded, say so.
2. **The whole log.** Read `run.md` from the first line to the last, in chunks. Write the line ranges you read out of the total. Quote every warning, failed `SHOULD`, `FIXME`, NaN or error, each with its line number.
3. **Random records.** Run `python3 scripts/look.py <run directory>` from the `ml-debug` folder. It picks records at random and prints its seed. Read one record in full, as the model received it: template, special tokens, the reply.
4. **The records behind the headline.** Open the raw records that make the headline number: the best case, the worst case, and one near the middle. For each, read the input and the output in full and write one sentence: does the score match what the output does? A broken, cut-off, looping or off-task reply that scores well is a finding.
5. **Recompute the headline by hand.** From the raw records, compute the main number in the result table yourself, with a few lines of code. If it differs from the reported number, or the caption describes a different rule than the one that reproduces it, that is a finding.
6. **What ran.** Check that the command, the commit and the resolved config are the ones the question needs. A field that records the wrong commit, a default that was not overridden, or a file that changed during the run is a finding.
7. **Causes.** For each finding, and for the headline result, do the CAUSES step of `ml-debug`: three or more explanations with a %, one of them a bug in the code or the metric, with the strongest evidence for and against each, and the cheapest test that separates the top two.

## The report

Write it to `slop/audits/job_<id>.md` (or the project's audit folder) and put the first part in your reply:

```markdown
## Job <id>: <what it showed, in one line>

Question: "<quoted>". Prediction: "<quoted>" | none recorded.
Findings (most important first):
1. <what is wrong or surprising>. Evidence: "<quote>" (<file:line>). Effect on the result: <one line>.
Read: run.md lines <a-b> of <N>; look.py seed <s>, records <...>; headline records <...>.
Headline recomputed: <my number> against <reported number>.
Causes: <the CAUSES lines>.
Next: <the test or the fix, run or queued>.
```

"No findings" is a valid result when the Read line shows that you read the data. A report that lists only what the log says, with no record read and no number recomputed, is not an audit.

Do not change code or queue jobs during an audit unless the user asked for a fix.
