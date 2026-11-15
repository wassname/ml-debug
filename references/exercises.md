# The full audit form and exercises A to J

The steps in [SKILL.md](../SKILL.md) are what you do every time. This file is the same work at
depth: the full form for a complete audit of a run, the routing that says which exercise applies,
and the exercises.

## The ml-debug form

Read the whole log first. Save the complete form in the run's audit. Show the decision and
supporting evidence in the reply as described in
[research_loop.md](research_loop.md#turn-evidence-into-a-research-decision); when the user requests the full form
in chat, include all rows there too. Do not substitute "audit complete" or a file path for
the findings.

Ground each answer in quoted log evidence. If evidence is missing, write "unknown"
and say what would fill the gap.

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

Some rows are an exercise below at less depth. The form is for a complete audit; the exercise is
done at depth when the routing says so.

## Routing

Before a run, after a run, before you report. At each, do every small item that applies and one
large item. A small item is under a paragraph. A large one is real work.

Before a run:
- always: options table (ex A, small), predictions (ex B, small), smoke test
- if about to change the design, or the last run cannot be explained: pseudocode and external
  review (ex F, small; the review is delegated)

After a run (finished or crashed):
- for a complete audit: the form
- always: second cause for the same number (ex C, small)
- if it failed: reproduce it, same seed then a different seed, before diagnosing. A failure
  that does not reproduce is a different problem; write that down
- if the log has a spike, a flat line, or an impossible value: rows before the spike (ex D, small)
- if two cycles have passed with no progress: reference implementation (ex E, large), and
  redo `MENTAL_MODEL.md` steps 2 to 4 before the next run

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

| option | metric it should affect | direction and order | possible outcomes and model updates | GPU / elapsed time |
|---|---|---|---|---|
<!-- PI/OpenAI: compare expected learning and cost, not only score improvement. -->

Consider architecture and loss changes where they are live choices for this problem, alongside
data, regularisation, and optimiser. Say which options change in this run and why. Several can
change in one run if each has its own metric (see Expensive runs in [research_loop.md](research_loop.md#expensive-runs)). Show the config diff against
the run you will compare to.

### ex B: predictions (small)

> Before acting plan by writing multiple competing hypotheses: consider the most likely failure but also some of: a subtle failure, a perverse failure, a possible bug, and an unknown. Put a rough credence on each. Finally write down what you expect to see differently for success vs each possibility and brainstorm the cheapest tests that may narrow them down. -- wassname

Write down the question this run answers in one sentence, the result that would change the
current explanation, and which parts change versus the comparison run. For an
exploratory run, name the behaviour or unknown you will inspect and how it could guide the next
change; do not invent a precise hypothesis merely to fill the table. Then:
<!-- PI/OpenAI: distinguish exploration from testing an established explanation. -->

| component | origin | expected if it works | if too weak | if too strong | if it has a bug | metric logged? |
|---|---|---|---|---|---|---|

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
