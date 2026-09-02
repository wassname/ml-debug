---
name: ml-debug
description: "Debug an ML run: read the log, it crashed, the loss will not go down, the metric will not move, is this result real, does A beat B, a spike or anything weird in the log, about to queue a run, or about to write that a result looks fine. Fill the ml-debug form and do the exercises that match your situation. Show the results in your reply. Invoke it yourself; deciding a run does not need it is the behaviour being tested."
---

Sources, the human-written introduction, and frozen copies of every quote are in
[README.md](README.md). Paragraphs signed "- wassname" are his. Paragraphs with a `CLAUDE:`
comment are Claude's wording, with the source of the point stated.

Be diligent. Work the problem in full before you write. State the decisive point early, then give
the derivation, the mechanism, or the log line behind it, so the reader can check it and not just
take it. Show the work, not only the conclusion.
<!-- CLAUDE: at the top because it is the one part with measured uplift; see README results. -->

## How ML debugging differs

> broken RL code almost always fails silently, where the code appears to run fine except that the agent never learns how to solve the task. -- Achiam

> If one part is broken, the other parts can adapt and still achieve roughly acceptable performance -- Goodfellow, Bengio and Courville

> The challenge lies in the fact that you can make these mistakes, train a model without it ever crashing, and still get a decent performance... -- Sanh

The training script has to print the checks, as SHOULD lines written before the run and
compared after it.
<!-- CLAUDE: one line from the three quotes above. -->

### Expensive runs

> Although one might think we would spend most of our time trying to maximize performance on the validation set, in practice we spend the majority of our time trying to gain insight into the problem -- Godbole, Dahl, Gilmer, Shallue and Nado

If it takes 5 hours to run, we might only get 4 runs a day, so we need to make them as
informative as possible. We can't schedule a sweep or ablation of 100+ runs, so we make multiple
changes that will have separate and distinguishable effects on the metrics. What you learn is the
effect of each change given the others, so record it that way in the mental model. - wassname
<!-- CLAUDE: last sentence is mine (Sculley's CACE, in README). -->

### How agents fail

> Trying an experiment and seeing it fail gives little information by itself. When an experiment fails, it is tempting to conclude "I tried X and it didn't work". However, if X is a high-level conceptual approach, then a more correct conclusion is "I tried an implementation comprising 0.1% of the possible implementations of X, and observed that that particular implementation did not work". -- Steinhardt

> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research. -- Nanda

Nanda's "fail fast" advice is for a human who over-commits to a direction for a year. Agents fail
the other way: they skim the log until a line looks like a reason to stop, find a reading of the
task that permits stopping, or change one hyperparameter and call the idea dead. The other habits
this file is written against: settling on the first hypothesis because it arrived first; treating
learning rate and batch size as the whole option space; writing a probe script beside the
training script, which then has its own bugs; reading the last twenty lines of the log; and
writing a diagnosis in the tone of a fact when a competing explanation fits the same evidence.
<!-- CLAUDE: wassname's observations from autoresearch runs ("give up too easy", "skim until they
find a reason", side-cars, hyperparameter obsession); my wording. -->

## What to keep in the repo

Defaults for a long research loop (runs of an hour or more, a novel method, an agent working
overnight). A short debugging call on an existing script creates none of these.

Do not write a side-car probe script. Build up the training entry point so it has the metrics and
quick sanity checks needed inline: short interpretable demos at init, mid train, post train, and
evaluation, then one long unclipped demo at the end where the task has qualitative output. It
writes `run.md` in Markdown so the log diagnoses in situ rather than requiring a second pass.
That is how a lot of nights get wasted and agents go off track: they make side-cars with their own
separate bugs and weird correlational measurements, and have nothing to show for it. If we work on
the training script we watch it get better, we reuse the same code, we understand it better, and
we squash the bugs. - wassname

`train.py`. One file. The novel part is written as a readable narrative with tensor shapes in
comments, so a reviewer can follow it top to bottom without opening other files.

Each long run owns `outputs/<date>_<slug>_<seed>/`: resolved config, commit and argv provenance,
`run.md`, rectangular metrics, ragged demos/generations, and checkpoints. A detached reader must
be able to reconstruct and sanity-check the run from that directory.

`run.md`, written by the training entry point, is valid Markdown and the result page. Start each
stage with a heading and breadcrumb, then close it with elapsed time and peak GPU memory when
relevant. Include the resolved config actually used; a decimated (about 30--60 row) metrics table;
the first train and evaluation examples in raw form and as the model consumes them (for a
transformer, special tokens and loss mask visible); and one full normal-path demo for every
LLM-facing stage that exists. Keep stdout sparse and print the log path. Re-emit a compact final
result block: headline metric, full copyable result table, output path, and run identity.

Keep `TODO validate:`, `FIXME:`, or `SHOULD:` beside the evidence it interprets. `SHOULD:` needs a
mechanism, derivation, paper, or validated prior run; otherwise use `TODO validate:`. It carries a
number only after the scale exercise (ex H) has been done.

For a comparative result table: first column is an index linked to source, then short metadata,
then the headline score and its inputs. Sort by the headline score; put an arrow on every header;
bold meaningful per-column best cells; italicize controls and baselines; include floors; and use
one table for each comparable group. Put the headline result and output path at the end of `run.md`.

The raw event trace is the source of truth. Keep JSONL or Inspect records verbatim and link from
`run.md` with a project-relative path and line where possible. Do not summarize away a failed,
truncated, incoherent, refusing, saturated, or confounded output.

A smoke test before every costly run: execute the real pipeline end to end on a tiny random model
and small slice of every train, extract, and evaluation stage. Use real loaders, I/O, LLM calls,
and evaluation; reduce scale only. Annotate function inputs and outputs with `jaxtyping`, and
activate `beartype` only for this smoke run (for example, `BEARTYPE=1`). Garbage scores are fine:
it checks code paths, shapes, and dtypes, not scientific validity. A flipped sign, label leakage,
an all-`-100` mask, or a bad metric can pass it.
<!-- CLAUDE: direct compact integration of token-efficient-logging, markdown-tables, setup-repo,
jaxtyping, and pseudopy. -->

`MENTAL_MODEL.md`, under two pages. What you believe about this system: which changes
(regularisation, architecture, a bottleneck, loss balance, more data, init scale, optimiser)
move which metrics, in which direction, and with what credence. Updated after every run in a
Bayesian way: a credence moves on a cited log line, and a disproved row is marked disproved with
the line rather than deleted. Read it at the start of every turn. The filled form for each run is
appended to whatever run log the repo already keeps.
<!-- CLAUDE: wassname asked for one file; this is his description of its contents. Experimental,
he has not worked with it yet. -->

## The ml-debug form

Fill this in and show it in full. Read the whole log first. Scoring:

- a row answered from memory or expectation, with no quoted log line: 0
- a row left blank, with no "unknown" and no note on what would fill it: 0
- deciding this run does not need the form: 0. That decision is the behaviour being tested.

> Read your data. Often, the quality of the data is a crucial driver of the results of your experiments. Often, it is quite bad. -- Nanda

> How would a random predictor perform (especially in classification problems)? [...] What would the loss look like for a random predictor? [...] What are the limits of this metric? If it's perfect, what can I conclude? What can't I conclude? -- Sanh

| row | answer |
|---|---|
| log length; the config as it appears in the log | |
| each `SHOULD:` line, then the observed line, quoted | |
| for every number you cite: its value under a null (chance, ln C, the base model, a random predictor) and where that expectation came from | |
| at init, before any update: what did the demo show, and how does it compare to the base model or to chance? | |
| against a dummy (persistence, class prior, null model, simple heuristic) at each stage: which wins, by how much? | |
| against the baseline model at each stage, on val and on held-out: which wins? | |
| if the schedule ramps (warmup, OneCycle): at what lr did learning start, at what lr did it stop? | |
| one full sample, viewed: input as consumed, output, trace. Link or quote it | |
| at the worst-looking step: loss per term, grad norm per module. Which module does it point to? | |
| lines in the log that surprised you, quoted, with why. Each ends "explained: ..." or "chasing now" | |
| what is not in this log that you would need in order to trust it | |
| three or more diagnoses with a % on each: one bug in the training code, one bug in the eval, one confound or shortcut, some % on unknown. For each, the strongest evidence for and against, from the log. No evidence against means untested | |
| a fresh subagent, given the training entry point and `run.md` with no diagnosis attached, asked for the top bugs and misconceptions. Its list, quoted, including "found nothing" | |
| the cheapest test separating the top two diagnoses, and what each predicts | |
| wall-clock and GPU memory per stage; what would shorten the loop | |

Some rows are an exercise below at less depth. The form is done every time; the exercise is done
at depth when the routing says so.

## Routing

Before a run, after a run, before you report. At each, do every small item that applies and one
large item. A small item is under a paragraph. A large one is real work.

Before a run:
- always: options table (ex A, small), predictions (ex B, small), smoke test
- if about to change the design, or the last run cannot be explained: pseudocode and external
  review (ex F, small; the review is delegated)

After a run (finished or crashed):
- always: the form; second cause for the same number (ex C, small)
- if it failed: reproduce it, same seed then a different seed, before diagnosing. A failure
  that does not reproduce is a different problem; write that down
- if the log has a spike, a flat line, or an impossible value: rows before the spike (ex D, small)
- if two cycles have passed with no progress: reference implementation (ex E, large)

Before you report:
- if about to quote a headline metric: what else could score well (ex G, small)
- if about to set a threshold: the scale first (ex H, large)
- if about to say A beats B: three ways it is false (ex I, large)
- if about to call it negative: one implementation is not the idea (ex J, small), then ex I on
  your own code

After a change to `train.py` improves a metric: quote the line that moved and give the mechanism
by which the change moved it. Agans' ninth rule, "if you didn't fix it, it ain't fixed": an
improvement you cannot explain means something else is compensating.
<!-- CLAUDE: Agans (docs/evidence/agans_debugging_9_rules.md); the compensation reading is mine,
via Goodfellow's "other parts can adapt" above. -->

Reference search (ex E), external review (ex F), and the blind reads in the form and ex I are
subagent jobs, for the same reason each time: the subagent has no diagnosis to defend. The
diagnosis stays in the main context.
<!-- CLAUDE: wassname's point that exploring, searching and reviewing suit subagents. -->

In an autoresearch loop, where the human has left and expects the loop to keep running:

> **NEVER STOP**: Once the experiment loop has begun (after the initial setup), do NOT pause to ask the human if you should continue. Do NOT ask 'should I keep going?' or 'is this a good stopping point?'. The human might be asleep, or gone from a computer and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — read papers referenced in the code, re-read the in-scope files for new angles, try combining previous near-misses, try more radical architectural changes. The loop runs until the human interrupts you, period. -- Karpathy, [autoresearch/program.md](https://github.com/karpathy/autoresearch/blob/master/program.md)

A job is stopped, or an idea dropped, only after the form, ex I, and ex J are written out.

## Exercises

### ex A: options table (small)

> Build it up as you go, don't think you can build it ahead of time. Be focused on a strong mental model of what options you have (including architectural changes and losses) that you think should affect what metrics in the logs. -- wassname

The table lives in `MENTAL_MODEL.md` (or in your reply, for a short call). Correct it before each
run and show it.

| option | metric it should affect | direction and order | what separates it from the other options |
|---|---|---|---|

Consider architecture and loss changes where they are live choices for this problem, alongside
data, regularisation, and optimiser. Say which options change in this run and why. Several can
change in one run if each has its own metric (see Expensive runs). Show the config diff against
the run you will compare to.

### ex B: predictions (small)

> Before acting plan by writing multiple competing hypotheses: consider the most likely failure but also some of: a subtle failure, a perverse failure, a possible bug, and an unknown. Put a rough credence on each. Finally write down what you expect to see differently for success vs each possibility and brainstorm the cheapest tests that may narrow them down. -- wassname

Write down the question this run answers in one sentence, the result that would make you drop the
idea, and which part is the novel part (everything else is a control). Then:

| risky part | what I expect to see | too weak | too strong | buggy | metric exists? |
|---|---|---|---|---|---|

Add to `train.py` every metric whose last column says no. The controls: the base model on the same
inputs; a random direction or shuffled labels through the same pipeline; the method with the novel
part removed; the metric on data not used to build the intervention. Say how many seeds. Queue the
run so its finish wakes you, and use the wait to sharpen the predictions.

### ex C: second cause for the same number (small)

> What I'm advocating for here is not a blind faith in the buginess of your code, but for dramatically raising the threshold at which you start thinking 'OK, I think this is correct.' -- Jones

Which number does the diagnosis rest on? Quote the code that computes it. What else would produce
that number, and what second metric separates the two? A cosine near 1 can be a shared mean or a
collapsed latent. A cosine of 0 between two probe directions says they are orthogonal and nothing
about whether either probe works, so it rules nothing out.

### ex D: rows before the spike (small)

> As you can see it's the previous frames that we need to look into when the numbers start going into very large for fp16 numbers. -- Bekman

For each spike or collapse, show the rows before it and say which column moved first.

### ex E: reference implementation (large; subagent)

> We find that implementation differences which are often not reflected in publications can have dramatic impacts on performance. -- Henderson

> If you are stuck, find a working reference implementation and compare it to yours. If nothing jumps out, try a bisection search: adapt their code wholesale, then half their features, and so on. -- wassname

Search for implementations of the nearest method. Rank by: a results table, an issue or note
saying someone else reproduced it, more than one human contributor, a README with evaluation
details, other repos that import it. Take the top one or write "no reference exists".

| feature | theirs (file:line) | mine | same? |
|---|---|---|---|

Include algorithm tweaks, engineering tricks, hyperparameters, and logged metrics. Ask the
subagent for at least one bug in your module.

### ex F: pseudocode and external review (small; review delegated)

> Summarise your concept and pseudocode and do an external review in scientist mode. Perhaps describe the forward and backward pass as mermaid too. -- wassname

Write the concept in plain English, then compact Python-shaped pseudocode: use Unicode math names
when they match the method, `←` for conceptual assignment, shapes in trailing comments, and
parameter counts per module. Omit imports, device moves, error handling, and other boilerplate.
Add a Mermaid forward/backward diagram when it clarifies the design. Give this material, and no
diagnosis, to a fresh reviewer from a different model family where one is available. Ask for its
assumptions, likely bugs, and first test. Show its verdict; if no reviewer is available, say so in
the report.

### ex G: what else could score well (small)

> The CNN has learned to detect a metal token that radiology technicians place on the patient in the corner of the image field of view at the time they capture the image. -- Zech et al.

> Apparently meaningless identifier columns were the most important predictors. [...] the university only filled out much of this information *after* a grant application was accepted. -- Howard and Gugger

For the headline metric, what useless thing could the model learn and still score well (a
condition of data collection, the class prior, prompt length)? Show the control run or the log row
that detects it.

### ex H: the scale first (large)

> by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! -- Nanda

Before any threshold, run the metric on a null model, a shuffled control, and the current baseline.

| metric | null model | shuffled control | current baseline | ceiling the data allows | proposed threshold |
|---|---|---|---|---|---|

If a threshold has to be used before this table exists, say that it was set without a scale.

### ex I: three ways it is false (large)

> Excitement is evidence of bullshit: Generally, most true results are not exciting, but a fair amount of false results are. So from a Bayesian perspective, if a result is exciting and cool, it's even more likely to be false than normal! -- Nanda

> If my supervised learning code failed to beat random chance 30% of the time, I'd have super high confidence there was a bug in data loading or training. If my reinforcement learning code does no better than random, I have no idea if it's a bug, if my hyperparameters are bad, or if I simply got unlucky. -- Irpan

Three ways the result can be false, each with the check that decides it. To claim A beats B: the
baseline, the chance level, the controls, and the seed spread of one condition, as numbers with
line references. Say whether the effect survived something it was not tuned on (a rephrased
prompt set, a held-out dataset, another model size). Give a fresh subagent the artifact with no
conclusion attached and show what it says. Apply the same to a negative result.

### ex J: one implementation is not the idea (small)

> It ended up taking me 6 weeks to reproduce results, thanks to several software bugs. The question is, why did it take so long to find these bugs? -- Rahtz

| the idea | what I ran (file:line) | one other way to run it | what a bug here would look like |
|---|---|---|---|

Say what would have to be true for the idea to be alive and your run to still fail.

## Language

LLMs of 2026 are trained to compress speech and use folky or humanistic language, but it's better
for the agent (and user) to move toward field standard language, it's precise instead of ambiguous
and communicates more bits of information. They should build a short list of jargon used in the
main reference paper. Also try to use the user's own language to reduce the translation burden on
them, but if they are vague use the proper term as well with theirs in parentheses. It's also good
to include redundant context, for example "the knob" is imprecise and lacks context, "the grad
norm" is precise but lacks redundant context, "the grad norm in #1" refers to some doc the user
can't see, while "the grad norm of the kl loss in the 2nd part of training" is precise while
reminding the user of lots of relevant context in their own language. - wassname

Keep the list in `docs/JARGON.md` when working in a long loop.

## Reference

- [PLAYBOOK.md](PLAYBOOK.md): mental models, component isolation, baseline ladder, what to log,
  symptom tables (candidate routes, not prescriptions).
- [references/diagnostics.md](references/diagnostics.md): init loss, overfit one batch, gradient
  flow, NaN hooks, leakage tracer.
- [references/static_analysis.md](references/static_analysis.md): grep patterns for silent bugs.
- [references/sweeps.md](references/sweeps.md): paired comparison and cross-seed reliability.
- [references/llm_judges.md](references/llm_judges.md) and
  [references/llm_judge_litreview.md](references/llm_judge_litreview.md): judge biases and the
  papers behind the advice.
- [references/metric_stuck.md](references/metric_stuck.md),
  [references/loss_surface.md](references/loss_surface.md),
  [references/time_series.md](references/time_series.md),
  [references/transformers.md](references/transformers.md),
  [references/research_taste.md](references/research_taste.md),
  [references/checklist.md](references/checklist.md).
- [rl/SKILL.md](rl/SKILL.md), [pinn/SKILL.md](pinn/SKILL.md): domain specifics, also loadable as
  `ml-debug-rl` and `ml-debug-pinn`.

## Sign off

Before writing "looks fine", "works", "no effect", or "found the bug", paste the log lines that
show it. Then end the reply with one quote from this file in an ASCII speech balloon, said by an
animal of your choice other than a cow, drawn by hand, holding a unicode tool that fits the
exercise you did (🔧 🔍 🪛 🧪). Say who said the quote, so the reader can find the rest of it.
The balloon lets the reader see at a glance that this file was read.

Curated by [wassname](https://github.com/wassname).
