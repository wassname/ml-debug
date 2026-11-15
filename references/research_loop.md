# Long research loops

Read for runs of an hour or more, a novel method, or an agent working overnight. The steps in
[SKILL.md](../SKILL.md) come first. Exercises (ex A to J) are in [exercises.md](exercises.md).

Contents: choosing experiments, turning evidence into a decision, how ML debugging differs and how
agents fail, what to keep in the repo (`train.py`, `run.md`, `MENTAL_MODEL.md`), language.

## The toolkit on one page

Each row is one practice and the artifact that records it, so that a later session can read it.
The sections below give the detail. Nothing here depends on a skill outside this repository or on
a particular job queue. It contains the subset of wassname's logging, queueing and
repository-setup practices that his projects use.

| when | do | recorded in | detail |
|---|---|---|---|
| once per project | the goal in the user's words, what is not the goal, the names, the key concepts quoted from the papers, the lessons | `AGENTS.md` ([template](../templates/AGENTS.md), under 150 lines) | the template's comments |
| before code | take names from the latest one or two reference papers and their code; where you must coin one, make it unique, informative and long enough to signpost | `docs/JARGON.md` | [Language](#language) |
| before a run | state the mode: exploring (no variant has shown the target effect) or confirming (a variant shows it) | the job's label | [Two modes](#two-modes-exploring-and-confirming) |
| before a run | state which components are new, the expected result with a %, and the observation that the opposite result would produce | `MENTAL_MODEL.md`, the spec | [SKILL.md](../SKILL.md) PREDICT; [Choose experiments](#choose-experiments-that-improve-the-mental-model) |
| before a run | for every new component, log one metric per silent failure mode (a failure that raises no error) | the one training script; [scripts/parts.py](../scripts/parts.py) computes three that need no design choice: parameter movement from initialisation, each loss term's gradient-norm share and cosine per component, and the metric with each named input permuted across the batch | [What to keep in the repo](#what-to-keep-in-the-repo) |
| before queueing | smoke test: tiny random model, 2 batches, 2 updates, every stage, type and shape checks on, in the foreground | one command, e.g. `just smoke` | same section |
| before queueing | timing pilot: 50 real steps at the real batch size; seconds per step and projected total | the job's label | same section |
| queueing | the question the run answers and what would resolve it | the job's label and the top of `run.md` | same section |
| during | each metric beside its `TODO validate:` or `SHOULD` statement; the final lines repeat the question | `run.md` | same section; [diagnostic_statements.md](diagnostic_statements.md) |
| after | LOOK, NULL, CAUSES, FRESH EYES; which belief changed and the evidence for the change | the journal, `MENTAL_MODEL.md` | [SKILL.md](../SKILL.md); [Turn evidence into a research decision](#turn-evidence-into-a-research-decision) |

> Before you run anything, write down what you expect to happen and why. **Then design the
> experiment so that the opposite result would also have been visible if it were true.** A clean
> answer to a question designed only to confirm your initial expectation is worth less than a
> messy, honest answer to a question you set up fairly.
> -- CS 2881 AI Safety, Homework Zero, Fall 2026 (Barak et al.), [course page](https://boazbk.github.io/mltheoryseminar/hw0-2026/) ([cache](../docs/evidence/cs2881_hw0_2026.md))

<!-- CLAUDE (PI, Fable), with wassname 2026-11-15: an index of what this file already held, plus
the timing pilot and the question in run.md. Written after a session where the faults of a run were
found in about one minute because each new component already had its ablation metric, and where
three setup faults and a 1-second training step were found late because the two rows "before
queueing" were not done. -->

## Two modes: exploring and confirming

> Don't just run more seeds. In blue-sky research we need to try multiple things at once, and only
> go back and do the baseline or multiple seeds once it's working and our setup is clear. And we
> need fast iterations (smoke test under 3 minutes, run under 30 minutes) even if this means a
> small noisy dev eval. - wassname, 2026-11-15 (spelling corrected)

| | exploring: no variant has shown the target effect | confirming: a variant shows it and the setup is fixed |
|---|---|---|
| one run | the complete candidate method, several changes together, each new component instrumented | one change against a matched baseline |
| size | smoke test under 3 minutes; run with its evaluation under 30 minutes; a small evaluation with high variance is accepted | the sample size that the claim requires |
| baseline | the stored one; rerun it only if a shared reference row (a null, the standard method) no longer matches | rerun beside the candidate |
| seeds, sweeps, ablations | none | yes ([sweeps.md](sweeps.md)) |
| evidence read | per-component diagnostics and sampled outputs first; the headline metric is weak evidence at this sample size | the headline metric with its interval |
| ends with | a variant that shows the target effect, or an identified cause of failure | a claim with its uncertainty |

Agents tend to apply the confirming column in both modes: matched baselines, additional seeds and a
larger evaluation before any variant has shown the effect. The compute then measures non-working
variants with high precision. In the exploring mode, the safeguard against discarding a method on
one high-variance metric is the per-component diagnostics and the sampled outputs, not additional
seeds.
<!-- CLAUDE (PI, Fable): from a session where I reran a known baseline and asked for a larger
evaluation before the first model had trained. The table is my wording of wassname's rule above
and of "Choose experiments" below; the last paragraph is my reading. -->

## Choose experiments that improve the mental model

Use this skill before choosing research runs, architecture changes, sweeps, ablations, or probes,
not only after failures. Research alternates between exploration and testing explanations.
Observations can precede theory: when you do not know which variables matter, use a small real
experiment to discover behaviour rather than invent a confident hypothesis.

Your mental model includes plausible mechanisms, confidence in them (priors), and their predicted
observations. Choose runs by the useful model updates their possible outcomes would support,
relative to GPU time and elapsed time. Include promising architecture changes; do not restrict
the search to optimiser settings. Use rough judgments, not invented information-gain scores.

Before a costly sweep or ablation, establish a credible learning signal through the real pipeline.
An earlier targeted comparison is useful when it distinguishes a specific failure or mechanism;
name that distinction. Otherwise, sweeping a method that does not work mostly compares failures.
For a probe, state which decision or unknown its outcomes could clarify and why existing inline
metrics cannot answer it. Prefer adding the check to the real pipeline over a separate script.

A speculative ("Hail Mary") run can be worth its cost even with low confidence of success.
Use the real run to collect inline probes, sanity checks, and examples at several stages, so
failure still reveals where the mental model diverges from observed behaviour. Several promising
changes can be tried together; distinguish learning about the combination from attributing an
effect to one change. Judge the run by useful learning as well as task improvement.
<!-- PI/OpenAI: wassname's clarification that instrumented speculative runs can be valuable. -->

Use exercises A/B ([exercises.md](exercises.md)) for the choice and predictions. After the run, update `MENTAL_MODEL.md` with
the observation, which belief changed and why, and the next useful action. Useful learning can
come without a score improvement; model-building must still advance the user's research goal.
For the source reasoning, read [Bayesian experimental design](research_taste.md#bayesian-experimental-design).
<!-- PI/OpenAI: from wassname's research-stage and GPU-budget guidance, with sources in the linked reference. -->

## Turn evidence into a research decision

The purpose is to advance the user's research goal. Completing a report is supporting work.
In the reply, show the decisive observations with their controls and denominators, explain
what they change about the diagnosis, and identify the next experiment or repair and its
expected distinguishing result. Separate observations from suspected causes. State what
you actually executed or queued; a recommendation is not an action. Link the complete
audit for inspection, but a path alone does not satisfy "show the results".

Report progress against research questions, not just completed runs. A buggy or insufficiently
investigated run leaves the question inconclusive. Work through the data, logs, and code over
successive debugging iterations: fix bugs, improve misleading metrics, inspect actual examples,
and rerun. Show what each iteration changed in the explanation and what remains unchecked.
A negative conclusion needs a stated scope and evidence against plausible alternatives; a count
of debugging rounds alone is not enough. For a brief update, use `busy`'s research-question states.
<!-- PI/OpenAI: align research conclusions with wassname's question-led busy framing. -->

Missing evidence blocks the next experiment only when it could invalidate that experiment,
make it uninterpretable, or create an unacceptable cost or risk. Explain that connection.
Otherwise investigate it alongside useful authorized work. Reporting defects are not
automatic training gates. Keep the full checks below; use them to choose what to do next.
<!-- Codex: addresses audits that listed checks but hid decisive evidence and delayed experiments. -->

## How ML debugging differs

> broken RL code almost always fails silently, where the code appears to run fine except that the agent never learns how to solve the task. -- Achiam

> If one part is broken, the other parts can adapt and still achieve roughly acceptable performance -- Goodfellow, Bengio and Courville

> The challenge lies in the fact that you can make these mistakes, train a model without it ever crashing, and still get a decent performance... -- Sanh

Write inline diagnostic expectations in `run.md`, beside the metrics and examples they interpret.
State expectations before the run; quote important expected-versus-observed divergences afterward
and say which belief they change. [diagnostic_statements.md](diagnostic_statements.md) distinguishes
supported `SHOULD:` predictions from `TODO validate:` hypotheses.
<!-- PI/OpenAI: route inline predictions to their canonical definition; CLAUDE 2026-11-15: that definition now lives in this repository. -->

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

Do not write a side-car probe script. Build up the one training script so it has all the metrics
you need inline as you go, with short interpretable demos at many stages: init, mid train, post
train, eval, then one long unclipped demo at the end. Demos and probes should not be separate
runs, they should be quick sanity checks inside the main train script, and the script should write
`run.md` in Markdown so the log diagnoses in situ instead of needing a second pass. That is how a
lot of nights get wasted and agents go off track: they make side-cars with their own separate bugs
and weird correlational measurements, and have nothing to show for it. If we work on the training
script we watch it get better, we reuse the same code, we understand it better, and we squash the
bugs. - wassname

`train.py`. One file. The novel part is written as a readable narrative with tensor shapes in
comments, so a reviewer can follow it top to bottom without opening other files.

Each long run owns `outputs/<date>_<slug>_<seed>/`: resolved config, commit and argv provenance,
`run.md`, rectangular metrics, ragged demos/generations, and checkpoints. A detached reader must
be able to reconstruct and sanity-check the run from that directory.

`run.md`, written by the training entry point, is valid Markdown and the result page. Start each
stage with a heading and breadcrumb, then close it with elapsed time and peak GPU memory when
relevant. Include the resolved config actually used; a decimated (about 30 to 60 row) metrics table;
the first train and evaluation examples in raw form and as the model consumes them (for a
transformer, special tokens and loss mask visible); and one full normal-path demo for every
LLM-facing stage that exists. Each demo starts with its full setup (task, input as the model reads it,
intervention, judge question, column meanings), then the results; read the demos before the metrics, as
the first sanity check (wassname 2026-10-04: "the most important part"). Keep stdout sparse and print the log path. Re-emit a compact final
result block: headline metric, full copyable result table, output path, and run identity.

Keep `TODO validate:`, `FIXME:`, or `SHOULD:` beside the evidence it interprets. `SHOULD:` needs a
mechanism, derivation, paper, or validated prior run; otherwise use `TODO validate:`
([diagnostic_statements.md](diagnostic_statements.md) has the forms and examples). It carries a
number only after the scale exercise (ex H) has been done.

For a comparative result table: first column is an index linked to source, then short metadata,
then the headline score and its inputs. Sort by the headline score; put an arrow on every header;
bold meaningful per-column best cells; italicize controls and baselines; include floors; and use
one table for each comparable group. Put the headline result and output path at the end of `run.md`.

The raw event trace is the source of truth. Keep JSONL or Inspect records verbatim and link from
`run.md` with a project-relative path and line where possible. Do not summarize away a failed,
truncated, incoherent, refusing, saturated, or confounded output.

A smoke test before every costly run: execute the real pipeline end to end on a tiny random model
and small slice of every train, extract, and evaluation stage (2 batches, 2 updates). It is one
command, takes a minute or two, and runs in the foreground; do not queue it behind real jobs. Use real loaders, I/O, LLM calls,
and evaluation; reduce scale only. Annotate function inputs and outputs with `jaxtyping`, and
activate `beartype` only for this smoke run (for example, `BEARTYPE=1`). Garbage scores are fine:
it checks code paths, shapes, and dtypes, not scientific validity. A flipped sign, label leakage,
an all-`-100` mask, or a bad metric can pass it.
<!-- CLAUDE: direct compact integration of token-efficient-logging, markdown-tables, setup-repo,
and jaxtyping. -->

A timing pilot before every long job: 50 real steps at the real batch size on the real data path.
Put the measured seconds per step and the projected total in the job's label. This detects a
data-loading bottleneck in about one minute.

Record the run's question in the job label and in `run.md`. With any job queue, label the job with
the reason for the run and the result that would resolve it (`why: unsure whether X improves Y against baseline; resolve: switch
the default only if both improve`). Give the same text to the run, so `run.md` opens with it and
its final lines repeat it above the relevant metrics. The script does not print a conclusion that
it cannot compute.
<!-- CLAUDE (PI, Fable): from wassname's queue-label habit, 2026-11-15; agents forgot the point of
a job between queueing it and reading it. -->

`MENTAL_MODEL.md`, under one page, with two sections:

- **Current model:** the best explanation so far, uncertainties, and predictions. A wrong model
  is better than an unfalsifiable one; record unknowns without forcing a finished theory.
- **Dated clues:** short observations not yet accounted for by the current model. Use shared
  jargon, enough context to identify the stage or condition, and a source log or journal link.
  Keep observations separate from suspected causes.

As clues accumulate, revise the current model to account for them, cite the dated evidence,
and state which belief changed and why. Remove an absorbed clue from the pending section only
when its original observation remains in the linked log or journal. Preserve unresolved
contradictions; do not rewrite observations to fit the explanation.
<!-- PI/OpenAI: wassname's dated clues proposal; keep the model short and the evidence recoverable. -->

- Retrodict: for the last several results, would the model have predicted them? For each miss,
  which belief caused it? Revise that belief and cite the log or journal line.
- Ceiling: for each part of the method, what is the best it could do (the target it imitates, a
  reference, an oracle)? Has that been measured on the current evaluation? If not, say so.
- Predict before each run (ex B). The model's quality is its record of predictions, not its length.

Read it at the start of every turn. The filled form for each run is appended to whatever run log
the repo already keeps. For the source of these steps, see
[research_taste.md](research_taste.md#predictive-models-jiao).
<!-- CLAUDE: LUCID3 backtests (2026-10-14, local slop/research/20261014_mental_model_backtest.md):
18 runs, 3 versions of this instruction. Forecast accuracy did not differ; this text is kept only
because it is shorter. Untested: giving the agent the project's own prediction record. -->

## Language

For explaining findings from the reader's existing knowledge, use `annoy-less`.
<!-- PI/OpenAI -->

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

Take the names from the latest one or two papers the work builds on, and from their code, before
any name of your own. A name you must coin is unique in the project, says what the thing is, and
is long enough to signpost: "token-edit pair", not "twin"; "latent classes", not "classes"; "the
state-dependent part of the slope", not "the gates" on first use. A coined short term requires every
later reader to look up its definition. Agents do not open `JARGON.md` before they coin a term, so
enforce the banned terms with a lint on the files that agents write.
<!-- CLAUDE (PI, Fable), 2026-11-15: wassname had to correct "code", "slot" and "twin" in one
session although the project's JARGON.md existed; a regex hook on written files did catch a
banned word the same day. -->
