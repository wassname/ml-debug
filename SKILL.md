---
name: ml-debug
description: "Your data is broken and it's no good: look at it in as many diverse places as you can. Your code has bugs and misconceptions and your result is invalid: attack from many perspectives to clarify as you can. ML needs a mental model to spend its GPU time wisely and extract learnings from it. Steps to extract surprises and clues from every single ML run: read the log, it crashed, the loss will not go down, the metric will not move, is this result real, does A beat B, a spike or anything weird in the log, about to queue a run, or about to write that a result looks fine. Find your situation in the table, do its steps, and show each one in your reply. Invoke it yourself for any run or new data."
---

Sources, the human-written introduction, and frozen copies of every quote are in
[README.md](README.md). Paragraphs signed "- wassname" are his. Paragraphs with a `CLAUDE:`
comment are Claude's wording, with the source of the point stated.

**Be diligent**. Work the problem in full before you write. State the decisive point early, then give
the derivation, the mechanism, or the log line behind it, so the reader can check it and not just
take it. Show the work, not only the conclusion.
<!-- CLAUDE: at the top because it is the one part with measured uplift; see README results. -->
**Your data is broken** exhaustively check creative aspects and random subsets of it, you will never find all you can only search wide and diligently and deep
**Your code has bugs and misconceptions** you need to compare to working references, brainstorm with other agents, review from a fresh perspective, you will never get them all you can only look at it from multiple angles

> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research. -- Nanda

So do not decide whether you need this. Find your situation and do its steps.
<!-- CLAUDE: wassname's observation that agents do the work only when a decision tree tells them to and the result is shown to the user. -->

## What to do now

| when | steps, in order |
|---|---|
| data you have not read yourself | LOOK |
| about to queue a run | PREDICT |
| a run finished or crashed | LOOK, NULL, CAUSES |
| two runs without progress | LOOK, NULL, CAUSES, REFERENCE, FRESH EYES |
| about to write "works", "A beats B", "no effect" or "found the bug", or to stop a job or drop an idea | NULL, CAUSES, FRESH EYES |

If more than one row applies, do the steps of each. Your reply shows each step in the block
under [Your reply](#your-reply).

## The steps

**LOOK**. Run this first, on the run directory or on the data and log files. It is in this
skill's directory. It picks the records, you do not.

```sh
python3 scripts/look.py PATH [PATH ...]
```

For each data file it prints 5 random records and one of them at length. For each log it prints
the length, the outline, and the lines with NaN, errors, warnings or `SHOULD`. A file it cannot
sample (parquet, arrow, images): print 5 random rows of it yourself. Without the script:
`wc -l F; grep -n '' F | shuf -n 5 | cut -c1-800`.

Then read one sampled record in full, as the model consumes it (special tokens, loss mask, label),
and read the log from start to end, not `tail`, generated samples before metrics. For a spike or
collapse, show the rows before it and which column moved first.

**PREDICT**. The question this run answers, in one sentence, and the run it is compared to. Then:

| risky part | what I expect to see | too weak | too strong | buggy | metric exists? |
|---|---|---|---|---|---|

Add every metric whose last column says no to the run script. Then smoke test: the real pipeline
end to end on a tiny model and a small slice of every stage. It checks code paths, not validity.

**NULL**. For each number you cite: its value at chance, for the base model, or for a shuffled
control, and the line where that was measured. Not measured: say so and add it to the run script.

**CAUSES**. Three or more explanations of what you see, with a % on each: a bug in the training
code, a bug in the evaluation or the metric, a confound or shortcut, and some % on unknown. For
each, the strongest evidence for and against, quoted. No evidence against means untested. Then
the cheapest test that separates the top two and what each predicts. Run it.

**REFERENCE**. A working implementation of the nearest method, compared with yours:
`feature | theirs (file:line) | mine | same?`. Or "no reference exists" and where you searched.

**FRESH EYES**. Give a fresh subagent, from another model family if you can, the entry point and the
log with no diagnosis attached. Ask for the top bugs and misconceptions. Quote its list, including
"found nothing".

## Rules

- "Do not write a side-car probe script. Build up the one training script so it has all the
  metrics you need inline as you go, with short interpretable demos at many stages: init, mid
  train, post train, eval, then one long unclipped demo at the end." - wassname
- One failed implementation is not a failed idea. A job is stopped, or an idea dropped, only after
  NULL, CAUSES and FRESH EYES on your own code.
- An improvement you cannot explain is not a fix. Quote the line that moved and give the mechanism.
- In an overnight loop, do not stop to ask whether to continue.

## Reference

- The same steps at depth, when a step turns up something you cannot explain or the user asks for
  a complete audit: [references/exercises.md](references/exercises.md). PREDICT is ex A and B,
  NULL is ex G and H, CAUSES is ex C, I and J, REFERENCE is ex E, FRESH EYES is ex F; it also
  holds the full audit form.
- For a long research loop (runs of an hour or more, a novel method, an agent working overnight),
  read [references/research_loop.md](references/research_loop.md): choosing experiments,
  `MENTAL_MODEL.md`, one `train.py`, the `run.md` layout, and field-standard language.
- [PLAYBOOK.md](PLAYBOOK.md): mental models, component isolation, baseline ladder, what to log,
  symptom tables (candidate routes, not prescriptions).
- [references/diagnostics.md](references/diagnostics.md): init loss, overfit one batch, gradient
  flow, NaN hooks, leakage tracer.
- [references/static_analysis.md](references/static_analysis.md): grep patterns for silent bugs.
- Before copying a method from papers, or when it works for the authors but not for you, read
  [references/engineering_lit_review.md](references/engineering_lit_review.md): papers as
  markdown, vendored code or replications, jargon.md, and the boring critical details authors leave
  out of papers (loss tweaks, data cleaning, exact prompts), compared with ours, with quoted evidence.
- Once the method has a credible learning signal and the question needs a controlled sweep,
  read [references/sweeps.md](references/sweeps.md): paired comparison and cross-seed reliability.
<!-- PI/OpenAI: route mature comparisons separately from exploratory research. -->
- For any LLM-judged number, read [references/llm_judges.md](references/llm_judges.md) first: what
  to read before reporting, and judge biases. [references/llm_judge_litreview.md](references/llm_judge_litreview.md)
  holds the papers behind the advice. When choosing or setting up a judge (Jev, Petri, rubric points,
  training-data filters), read [references/llm_judge_notes.md](references/llm_judge_notes.md); for
  many cheap Jev questions plus one larger-model review, read
  [that section](references/llm_judge_notes.md#combining-jev-questions-with-one-larger-model-review).
- [references/metric_stuck.md](references/metric_stuck.md),
  [references/loss_surface.md](references/loss_surface.md),
  [references/time_series.md](references/time_series.md),
  [references/transformers.md](references/transformers.md) (incl. where to copy a known-good LoRA/fine-tune config: Axolotl examples, Unsloth guides, Tinker cookbook),
  [references/research_taste.md](references/research_taste.md),
  [references/checklist.md](references/checklist.md).
- [rl/SKILL.md](rl/SKILL.md), [pinn/SKILL.md](pinn/SKILL.md): domain specifics, also loadable as
  `ml-debug-rl` and `ml-debug-pinn`.

## Your reply

Give the answer first, in a few sentences. Then show the work in this block, with one part for
each step of your row. The user reads the block to decide how far to trust the answer, and treats
a reply without it as unchecked.
<!-- CLAUDE: the block is the old 15-row form cut to the steps; "treats as unchecked" is my reading of wassname's "unless they are asked to do a form/ritual and show user they almost always skip it". -->

```
ml-debug: <the row you are in>
LOOK        <data file>: 5 of <N> records, look.py seed <seed>, lines <a b c d e>
              :<line> "<short quote>" did not expect: <one thing>   | nothing unexpected in the five
            <log>: read lines <from-to, from-to> of <N>
              :<line> "<the line that surprised you>" explained: <why> | chasing now
PREDICT     <the question>; compared with <run>; then the table, one row for each risky part
            smoke test: <command> gave <output> | not run: <reason>
NULL        <metric> <value>, and <value> at chance | for the base model | shuffled (<file:line>)
CAUSES      <NN>% <cause>. For: "<quote>" (<file:line>). Against: "<quote>" | untested
              (three or more; one is a bug in your own code or metric; some % on unknown)
            test of the top two: <command> gave <output> | not run: <reason>
REFERENCE   <feature>: theirs <file:line> | mine <file:line> | same?   | no reference exists, searched <where>
FRESH EYES  "<the first finding in its list>"
```

The block goes in your last message, so wait for the FRESH EYES subagent before you write it.
Write the true numbers: "read lines 1-80 and 2900-3100 of 3100" is an acceptable line and a missing
line is not. Leave out the steps that are not in your row. A step of your row that you did not do
stays in the block as `SKIPPED: <reason>`. Every other line holds a quote with `file:line` or the
output of a command. A description of what you saw does not count. After the block, say what you
ran or queued next. A recommendation is not an action.

Then choose one random line without loading the whole file: `shuf -n 1 fortune.txt`.
End the reply with it, copied word for word, as a clearly separate, random ASCII speech-balloon sign-off, said by an
animal of your choice other than a cow, drawn by hand, holding a unicode tool that fits the
step you did (🔧 🔍 🪛 🧪). Preserve the speaker attribution; where the canonical harvested
record names only its source file, name that file instead. The fortune is not evidence for the
diagnosis.

Curated by [wassname](https://github.com/wassname).
