---
name: ml-debug
description: "Your data is broken and it's no good: look at it in as many diverse places as you can. Your code has bugs and misconceptions and your result is invalid: attack from many perspectives to clarify as you can. ML needs a mental model to spend its GPU time wisely and extract learnings from it. Steps to extract surprises and clues from every single ML run: read the log, it crashed, the loss will not go down, the metric will not move, is this result real, does A beat B, a spike or anything weird in the log, about to queue a run, or about to write that a result looks fine. Find your situation in the table, do its steps, and show each one in your reply. Invoke it yourself for any run or new data."
---

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
| about to queue the first run of a new design | PREDICT, FRESH EYES |
| a run finished or crashed | LOOK, NULL, CAUSES |
| two consecutive runs without improvement | LOOK, NULL, CAUSES, REFERENCE, FRESH EYES |
| about to write "works", "A beats B", "no effect" or "found the bug", or to stop a job or discard a method | NULL, CAUSES, FRESH EYES |

If more than one row applies, do the steps of each. Report each step in the block under
[Your reply](#your-reply). The steps use the practices in [The toolkit](#the-toolkit).

## The steps

### LOOK

> The first step to training a neural net is to not touch any neural net code at all and instead begin by thoroughly inspecting your data. -- Karpathy

Run `scripts/look.py` (in this skill's directory) on the run directory, or on the data and log
files, before any other step. It draws the records at random and prints the seed, so the sample is
not your selection.

```sh
python3 scripts/look.py PATH [PATH ...]
```

For each data file it prints 5 random records, and one of them at length. For each log it prints
the line count, the heading outline, and every line with NaN, an error, a warning, `SHOULD`,
`TODO` or `FIXME`. For a file type it cannot sample (parquet, arrow, images), print 5 random rows
yourself. Without the script: `wc -l F; grep -n '' F | shuf -n 5 | cut -c1-800`.

Then read one sampled record in full, in the form the model receives: special tokens, loss mask,
label. Read the log from its first line to its last, not with `tail`. Read the generated samples
before the metrics. For a spike or a collapse, quote the rows before it and state which column
changed first.

### PREDICT

> Reserve experiments for once you've fleshed out the hypothesis space as thoroughly as possible and know which pieces of evidence would allow you to best distinguish between the different possibilities. -- Rahtz

Write these before the run.

1. Mode. Exploring: no variant has shown the target effect on an evaluation that you have checked.
   Do not run 3 seeds. Do not run an ablation. Do not rerun the baseline. Change several things per
   run, with effects that the logged metrics can distinguish; keep the run under 30 minutes.
   Confirming: a variant shows the effect. Now run the matched baseline, then seeds and ablations,
   one change per run.
2. Question. The question this run answers, in one sentence, and the run it is compared with. Put
   the sentence in the job label and in `run.md`.
3. Belief. Your credence in the claim now, as a %. For each possible outcome, the credence you
   would move to. If no outcome changes the credence, choose a different run. A small or noisy
   evaluation still moves it: a few points is a valid update, and many such updates decide.
4. Target and proxy. The target quantity (for example: the fraction of replayed plans that reach
   the edited goal). The metric used as its proxy (LLM-judge score, relative error, fraction of
   variance explained). One confound: a mechanism that changes the metric without changing the
   target (an LLM-judge score for topic relevance increases when the reply repeats the topic
   word). The control or table row that separates the two. If this proxy and the target have both
   been measured before in this project, state how often they ordered two models the same way. A
   proxy with no such record selects what to test on the target; it does not decide.
5. Decision rule. For each possible outcome, the action: continue with the method, discard it, or
   run a specified diagnostic. Define each outcome as an observation in the run report, not as a
   numeric threshold without a derivation.
6. Risk table, one row per component that can fail:

   | component | origin | expected if it works | if too weak | if too strong | if it has a bug | metric logged? |
   |---|---|---|---|---|---|---|

   Origin: copied (`file:line` of working code, or the section of the paper); changed from that
   reference (state the difference); or new and untested. Instrument in proportion to novelty. A
   copied component gets one row. A new component gets one row per silent failure mode (a failure
   that raises no error), each with a logged metric: its parameters do not move from
   initialisation; ablating it leaves the metric unchanged; its output has low effective rank or
   variance; it reduces to a trivial function, such as a copy of one input.
7. Add every metric whose last column is "no" to the run script. Write each expectation beside its
   metric as a diagnostic statement. `scripts/parts.py` computes three metrics for any component:
   parameter movement, each loss term's gradient-norm share and cosine, and the metric with each
   named input permuted across the batch.
8. Run the smoke test, then the timing pilot.
<!-- CLAUDE (PI, Fable) with wassname, 2026-11-15. Item 4 is construct validity without the term:
in one session three inferences had this fault (keyword frequency taken as behaviour change; the
goal stated in a reply taken as the executed plan; fraction of variance explained taken as
steering efficacy). Item 6: one run's faults were found in about one minute because each new
component already had its ablation metric, chosen before the run. -->

### NULL

> The default state of the world is that your research is false, because doing research is hard. -- Nanda

For each number you cite, give its value under a null: chance level, the base model, or a shuffled
control. Cite the `file:line` where the null was measured. If it was not measured, state that and
add the measurement to the run script.

For a claim that compares A with B ("beats", "equal to", "worse than"), also state:

1. Measured against. For each of the two numbers: the target or label it is an error against, its
   denominator, and the evaluation rows. This is the construct-validity question of PREDICT item
   4, asked of a comparison. When the three differ, the numbers do not rank the two models
   (an error against an easier target is lower for that reason alone), with one exception: when
   you know which side the difference favours, a result against that side still holds. Say which
   side is the conservative one.
2. Noise, as far as the mode needs it. Exploring: do not build a larger evaluation to measure
   it. A noisy evaluation is weak evidence: move your credence a little, say by how much, and
   continue. The variation between the evaluation's own items (a paired bootstrap of A minus B)
   costs no run and is usually enough. For the next run, a small variation of what worked is
   often worth more than the same thing with another seed: if the variations all work, that is
   evidence about the whole class, and the differences between them are noisy evidence about
   each. Spend the repeats on the best one later. Confirming: also quote the spread between
   repeated runs where they exist; it is often smaller than a formal interval. Rerun with
   another seed only for a source that all items share (training seed, one checkpoint, one
   evaluation-wide random draw) and only when the claim depends on it. In both modes, say what
   the evidence excludes and what it does not, not "significant" or "noise".
<!-- CLAUDE (PI, Fable), 2026-11-19, from a review of two days of use with wassname. Item 1: errors
against different labels were read as a ranking. Item 2 is wassname's: "can't we often estimate by
looking at intra sample var"; "when you measure noise you end up over engineering a quick dev test
to take 3h or not thinking bayesian and not updating your model on weak evidence ... we can use
noisy eval to get weak evidence to update"; "a slight expected change, a variation of one that
worked well, is often better than another seed. if a whole class works well, that's evidence about
the class, and within the class you have noisy evidence about the variations. more info same runs.
and you can always spend more time on the best later"; and on item 1: "sometimes you know one is
the conservative case and compare in one dir". -->

### CAUSES

> On the other hand, they're reluctant to say they've got a bug. Most often, it turns out they've got a bug. -- Jones

List three or more explanations of the observation, each with a %. Include a bug in the training
code, a bug in the evaluation or the metric, and a confound or shortcut. Assign a % to an unknown
cause. For each explanation, quote the strongest evidence for it and against it. An explanation
with no evidence against it is untested. State the cheapest test that separates the two most
probable explanations, and the result that each predicts. Run that test before you reply. If it
needs a GPU job or paid API calls, queue it or state its cost.

### REFERENCE

> We find that implementation differences which are often not reflected in publications can have dramatic impacts on performance. -- Henderson et al.

Find a working implementation of the nearest method. Compare it with yours feature by feature:
`feature | theirs (file:line) | mine | same?`. If none exists, write "no reference exists" and
list where you searched.

### FRESH EYES

> Get others (especially mentors) to red team your plans before you run them. Actively try to break your hypothesis. -- Nanda

Give a new subagent the entry point and the log, without your diagnosis. Use a different model
family if one is available. Ask for the most probable bugs and misconceptions. Quote its list,
including "found nothing". Before the first run of a new design there is no log: give it the
design document. Ask for the conditions under which the run is uninformative (no outcome changes
the belief), and for confounds that could produce a positive or a negative result independent of
the tested mechanism. Add a logged metric for each point you accept.

## The toolkit

Five skills in this repository, for five different times. `./install.sh <skills directory>`
links all of them.

| when | skill | what it holds |
|---|---|---|
| you set up or audit a repository | [setup/SKILL.md](setup/SKILL.md) (`ml-debug-setup`) | Smoke test on a tiny random model with `jaxtyping` and `beartype`; one training script that reads like pseudocode; `AGENTS.md` with the goal, the names and the mental model; `docs/papers/` and `docs/vendor/`; folders for throwaway work. |
| you write logging code | [logging/SKILL.md](logging/SKILL.md) (`ml-debug-logging`) | The layout of `run.md` with a full example; result tables; `SHOULD`, `TODO validate` and `FIXME` statements. |
| you queue, run and report | this skill, with [references/running.md](references/running.md) | Order of work, timing pilot, job label, lab report. |
| a run ended and its result matters | [audit/SKILL.md](audit/SKILL.md) (`ml-debug-audit`) | Read the data behind the result: the whole log, sampled records, the records behind the headline number, recomputed by hand. |
| a run or an analysis changes a belief | [journal/SKILL.md](journal/SKILL.md) (`ml-debug-journal`) | The journal entry: evidence with its source, nulls, competing explanations with a credence each, the prediction from before the run. |

The run-time practices, each with one example:

- Timing pilot, in the job label: `50 steps in 5.5 s = 0.11 s/step; 5,000 steps = 9.2 min`.
- Job label: `why: unsure whether the answer-only loss mask raises exact match vs job 37; resolve:
  adopt the mask if exact match is higher and replies are complete`. `pueue` is recommended:
  `pueue add -l "<label>" -- <command>`.
- Diagnostic statement, beside its metric in `run.md`. With a basis:
  `SHOULD [mechanism: LoRA B is zero at initialisation]: step-0 score equals the base model's. ELSE the adapter path is not an identity.`
  Without one, which is the usual case:
  `TODO validate (60%): exact match is higher with the answer-only mask`. Your stated expectations are wrong more often than you estimate, so
  do not write `SHOULD` without a basis and do not predict a number without a derivation.
- Lab report: one journal entry per run that changes a belief, in the format of
  [journal/SKILL.md](journal/SKILL.md) (`ml-debug-journal`). [Example](examples/toolkit/lab_report.md).

## Rules

- "Do not write a side-car probe script. Build up the one training script so it has all the
  metrics you need inline as you go, with short interpretable demos at many stages: init, mid
  train, post train, eval, then one long unclipped demo at the end." - wassname
- A failed implementation does not show that the method fails. Stop a job or discard a method only
  after NULL, CAUSES and FRESH EYES on your own code.
- An improvement without a mechanism is not a fix. Quote the log line that changed and state the
  mechanism that changed it.
- In an overnight loop, do not stop to ask whether to continue.

## Reference

| read | when |
|---|---|
| [references/exercises.md](references/exercises.md) | A step gives a result you cannot explain. For a complete audit, use [audit/SKILL.md](audit/SKILL.md). PREDICT is ex A and B, NULL is G and H, CAUSES is C, I and J, REFERENCE is E, FRESH EYES is F. |
| [references/research_loop.md](references/research_loop.md) | Runs of an hour or more, a novel method, or an overnight agent: the two modes, choosing experiments, turning evidence into a decision, `MENTAL_MODEL.md`. |
| [PLAYBOOK.md](PLAYBOOK.md) | Mental models, component isolation, baseline ladder, what to log, symptom tables. |
| [references/diagnostics.md](references/diagnostics.md), [references/static_analysis.md](references/static_analysis.md) | Initial loss, overfit one batch, gradient flow, NaN hooks, leakage tracer; grep patterns for silent bugs. |
| [references/engineering_lit_review.md](references/engineering_lit_review.md) | Before you copy a method from a paper, or when it works for the authors and not for you: papers as markdown, vendored code, `jargon.md`, and the implementation details that papers omit. |
| [references/sweeps.md](references/sweeps.md) | Confirming mode: paired comparison and cross-seed reliability. |
| [references/llm_judges.md](references/llm_judges.md) | Before you report any LLM-judged number. Papers: [llm_judge_litreview.md](references/llm_judge_litreview.md). Choosing or configuring a judge: [llm_judge_notes.md](references/llm_judge_notes.md), including [many cheap questions plus one larger-model review](references/llm_judge_notes.md#combining-jev-questions-with-one-larger-model-review). |
| [metric_stuck.md](references/metric_stuck.md), [loss_surface.md](references/loss_surface.md), [time_series.md](references/time_series.md), [transformers.md](references/transformers.md), [research_taste.md](references/research_taste.md), [checklist.md](references/checklist.md) | By symptom or domain. `transformers.md` lists known-good LoRA and fine-tune configs (Axolotl, Unsloth, Tinker). |
| [rl/SKILL.md](rl/SKILL.md), [pinn/SKILL.md](pinn/SKILL.md) | Domain skills `ml-debug-rl` and `ml-debug-pinn`. |

## Your reply

State the answer first, in a few sentences. Before the first number of a quantity, define the
quantity: its name, what it is computed from, and the axis that each mean or sum runs over (batch,
token, layer, item, seed). "The averaged label" can mean six things; "the mean of the labels of
this token and the 31 tokens before it" means one. Then report the work in the block below, one part per
step of your row. The user uses the block to decide how much to trust the answer. A reply without
the block is treated as unchecked.
<!-- CLAUDE: the block is the old 15-row form cut to the steps; "treated as unchecked" is my reading of wassname's "unless they are asked to do a form/ritual and show user they almost always skip it". -->

```
ml-debug: <the row you are in>
LOOK        <data file>: 5 of <N> records, look.py seed <seed>, lines <a b c d e>
              :<line> "<short quote>" unexpected: <one thing>   | nothing unexpected in the five
            <log>: read lines <from-to, from-to> of <N>
              :<line> "<the unexpected line>" explained: <mechanism> | under investigation
PREDICT     mode: exploring | confirming; <the question>; compared with <run>
            belief: <claim> <NN>% now; <outcome A> -> <NN>%, <outcome B> -> <NN>%
            target/proxy: <metric> is a proxy for <target quantity>; confound: <mechanism>; control: <row or control>
            decision: continue if <observation>; discard if <observation>; run <diagnostic> if <observation>
            risk table: <n> rows; new components: <n> rows, metrics <names>
            question recorded in the job label and run.md: "<the line>" | not yet: <reason>
            smoke test: <command> gave <output> | not run: <reason>
            timing: 50 steps gave <s per step>, projected <total> | not run: <reason>
NULL        <metric> <value>, and <value> at chance | for the base model | shuffled (<file:line>)
            (for "A beats B", "equal", "worse":)
            measured against: A and B both <target>, <denominator>, <rows> | differs in <what>; conservative side: <A or B> | not comparable
            B is: <run, same code and commit as A> | a stored run that differs in <what>
            noise: A - B = <value> over <n> items [<low>, <high>]; credence <NN>% -> <NN>%; excludes <what>, does not exclude <what>
CAUSES      <NN>% <cause>. For: "<quote>" (<file:line>). Against: "<quote>" | untested
              (three or more; one is a bug in your own code or metric; a % on unknown)
            test of the top two: <command> gave <output> | queued as <job> | not run: needs <GPU hours or $>
REFERENCE   <feature>: theirs <file:line> | mine <file:line> | same?   | no reference exists, searched <where>
FRESH EYES  "<the first finding in its list>"
```

Put the block in your final message; wait for the FRESH EYES subagent first. Report exactly what
you did: "read lines 1-80 and 2900-3100 of 3100" is acceptable, an omitted line is not. Omit the
steps that are not in your row. For a step in your row that you did not do, write
`SKIPPED: <reason>`. Every other line contains a quotation with `file:line`, or the output of a
command. A description of what you saw is not sufficient. After the block, state what you ran or
queued next. A recommendation is not an action.

End every `ml-debug` reply with a hand-drawn `cowsay -f cat` balloon. Make up the cat and its
lines; don't run `cowsay` or draw a random fortune. The cat is a sock puppet with an outside view.
Step back from the whole reply and ask: what are we trying to learn or decide, and what might
we have misunderstood? In the cat's voice, make a short, specific joke about the most likely
misconception. The cat can question the goal, the metric, or the agent's framing of the problem.
If no mistake stands out, joke about what's still untested. The cat is not evidence.

```text
 _________________________________________
/ They spent all night making the bot say \
| "I checked." Did anyone ask what the    |
\ customer needed it to check?            /
 -----------------------------------------
        \  /\_/\
         \( o.o )
           > ^ <
```
<!-- PI/OpenAI: wassname asked for the cat to step back fully and voice the likely misconception or misunderstanding. -->

Sources and frozen copies of every quotation: [README.md](README.md). Paragraphs signed
"- wassname" are his. Text with a `CLAUDE:` comment is Claude's wording, with the source of the
point stated. Curated by [wassname](https://github.com/wassname).
