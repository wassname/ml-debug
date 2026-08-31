---
name: ml-debug
description: "Debug an ML run: read the log, it crashed, the loss will not go down, the metric will not move, is this result real, does A beat B, a spike or anything weird in the log, about to queue a run, or about to write that a result looks fine. Machine learning debugging exercises, each under a quote from a practitioner. Do the exercise for your situation and show the result in your reply. Invoke it yourself."
---

In an attempt to upskill the machine learning debugging on AI coding assistants (and humans), I've collected high quality sources on how to debug machine learning projects, focusing on the mindset and the "taste". When I started ML I went searching for discussions on best practices, and started a few discussions of my own and they helped me a lot, over the years I've collected good ones. I hope they can help others, as well as help in auto research setups. This intro is human written, and the below is AI written with human guidance. - wassname

Be diligent. Work the problem in full before you write. State the decisive point early, then give
the derivation, the mechanism, or the log line behind it, so the reader can check it and not just
take it. Show the work, not only the conclusion.
<!-- CLAUDE: top of the file because it is the one part with measured uplift. See the results
table in README.md. Do not bury it. -->

## Task: The ml-debug form

Your task is to fill in the below form and show it in full to the user.

To do this, read the full log, and think about the architecture, training dynamics, bugs, etc and
show the user you have thought about it. Think step by step, be diligent, avoid overconfident or
narrow perspectives, in order to complete this critical thinking exercise. You will be evaluated on
the form. Write "unknown" in a row you cannot fill, and say what would fill it.

- 3+ hypothesis or diagnosis with % bet on each
- Q: Strange or unexpected observations from the log, quote the lines and explain why they are
  surprising
  - TODO Have blind subagent read log and fill out this form, quote it's answer too
- Is it:
  - Q: Overfitting, underfitting, **loss** blowing up.
  - You should use OneCycleLR, if so, at what **lr** does it start and stop learning (this can tell
    you ceiling and floor)?
  - Q: Is the **init** giving 0 change, or too much (incoherent / exploding change), and does it
    beat baseline?
    - Note that it should work at init, or else your data or architecture has a bug
  - Q: Does it beat **dummy** (persistance, null model, or simple heuristic) at each stage?
    - Note it should do this easily
  - Q: Does it beat **baseline models** at each stage?
    - Note you are not finished untill you do this in val and held out
  - Q: How long does each stage take, and how much GPU ram? Can we **speed up** the iteration cycle?
  - Q: Have you viewed one inference including **sample data**, model output, and reasoning to
    ensure it aligns with expectations? You should print one sample of input, output, and everything
    else each time to sanity check and bring sunlight. Q: Link or quote one full sample or plot of
    each type
  - Advanced: TODO There is always a bug: find the most likely one, and have a blind subagent find
    the most likely one and quote both here to user

Exercises #1, #3, #7 and #15 below are the long form of the rows above.

> It's normal to want to rush into training and evaluating models, but it's important to take the time to think about the goals of a project, to fully understand the data that will be used to support these goals, to consider any limitations of the data that need to be addressed, and to understand what's already been done in your field. -- Lones

> This *sounds* obvious, but in practice this requires constant active effort, and if you are not actively doing this you'll inevitably fall into traps. Always seek alternative explanations, seek and implement strong baselines, check for bugs, etc. -- Nanda

Then do the exercises for your situation and show the result in your reply. Each
exercise is marked (small) or (large). A small one takes less than a paragraph to answer; a large
one is a lot of work, such as searching for a reference repo and comparing against it.

Always do ex #1 and ex #3. Then walk the list and do every branch whose condition is true. Do all
the small ones you match, and one large one.

- always, whatever you are doing
  - ex #1 read the log end to end (small)
  - ex #3 read your data (small)
- before a run
  - if about to queue it: ex #5 list the options you have (small), ex #6 write down what you
    expect to see (small)
  - if about to change the design, or you cannot explain the last run: ex #13 pseudocode and
    external review (large)
- after a run
  - if it finished or crashed: ex #2 name a second cause for the same number (small), ex #4 chase
    the weird thing (small)
  - if the log looks weird, a spike or a flat line or an impossible value: ex #11 read the rows
    before the spike (small), then ex #10 localise the error (small)
- before you report
  - if about to set a pass gate or quote a threshold: ex #15 get the scale before the gate (large)
  - if about to quote a headline metric: ex #12 name what else could score well (small)
  - if about to say you found the cause: ex #7 multiple diagnoses with % bets (large)
  - if about to say A beats B: ex #8 three ways the result is false (large)
  - if about to call it negative: ex #14 one implementation is not the idea (small)
- if two cycles have passed with no progress
  - ex #9 compare against a reference implementation (large)

Each exercise says what to show. Show it in full: the table, the quoted log line, the quoted
code, the pasted sample. Write "unknown" in a cell you cannot fill, and say what would fill it.
Give the source of each number.

Never stop a job or give up on an idea without doing all of these. One at a time, not all at once.

> **NEVER STOP**: Once the experiment loop has begun (after the initial setup), do NOT pause to ask the human if you should continue. Do NOT ask 'should I keep going?' or 'is this a good stopping point?'. The human might be asleep, or gone from a computer and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — read papers referenced in the code, re-read the in-scope files for new angles, try combining previous near-misses, try more radical architectural changes. The loop runs until the human interrupts you, period. -- Karpathy, [autoresearch/program.md](https://github.com/karpathy/autoresearch/blob/master/program.md)
<!-- annoy-less: [#9 negative framing + clipped fragment] "One at a time, not all at once." is an
X-not-Y closer in the AI register. Written by CLAUDE, your call. -->


## Common mistakes

Everyone makes these, and I have made most of them myself. They come up so often with AI agents in
long autoresearch runs that they are worth naming, so you can catch yourself early rather than after
a week of work. Reading the log and hunting for your own bug are the two that do most of the damage,
so start there when you are not sure where to start. - wassname
<!-- annoy-less: [MOST IMPORTANT - confidence changed] this whole paragraph is signed wassname but
was written by CLAUDE from your chat message. Your original last clause was:
"reading the log and looking for bugs are the most comomn I guess"
CLAUDE dropped "I guess" and changed "most common" to "do most of the damage", which is a different
and stronger claim. Restore your hedge if you want your own confidence level back. -->
<!-- annoy-less: [invented detail] "I have made most of them myself" and "rather than after a week
of work" are CLAUDE's, not from your message. First person claims about you that you did not make. -->


> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research. -- Nanda

> The challenge lies in the fact that you can make these mistakes, train a model without it ever crashing, and still get a decent performance... -- Sanh

Be careful about being overconfident. It is easy to write a diagnosis in the tone of a fact. Before
you commit to one, ask what you saw that a competing explanation could not also explain. If nothing,
then "I do not know, and here is what would tell me" is a good answer and not a failure.
Ex #7 multiple diagnoses with % bets.
<!-- annoy-less: [#9 negative framing] "is a good answer and not a failure" is the X-and-not-Y
closer. Say the positive claim only. Written by CLAUDE. -->


Do not quit after the first change and call the negative real. One failed attempt is much more
likely to be a bug in your implementation than a refutation of the idea. This is the expensive
mistake, because the idea gets thrown away and nobody goes back to it. Look for the bug first.
Ex #14 one implementation is not the idea.
<!-- annoy-less: [confidence changed + significance narration] your original was "quit after the
first change to misdiagnose a negative". CLAUDE added "much more likely to be a bug" (a probability
you did not state) and "This is the expensive mistake", which tells the reader how to rate it. -->


Try not to stop at the first idea you come up with. It arrives with no competition, so it wins by
default rather than on merit. Write down two more, and say what observation would separate them. If
you cannot name a test that distinguishes them, you have a preference and not a hypothesis.
Ex #6 write down what you expect to see, ex #7 multiple diagnoses with % bets.
<!-- annoy-less: [#9 negative framing] "you have a preference and not a hypothesis" is again the
X-and-not-Y closer. Two of these in one section reads as a formula. Written by CLAUDE. -->
<!-- annoy-less: [aphorism] "It arrives with no competition, so it wins by default rather than on
merit." is CLAUDE's epigram, not in your message. Cut or say it plainly. -->


> If it doesn't work, assume there's a bug. Spend a lot of effort searching for bugs before you resort to tweaking hyperparameters: usually it's a bug. Bad hyperparameters can significantly degrade RL performance, but if you're using hyperparameters similar to the ones in papers and standard implementations, those will probably not be the issue. -- Achiam

Watch out for getting obsessed with the legible hyperparameters. Learning rate, batch size and
warmup are easy to name and easy to change, so they attract more attention than they deserve. More
often the cause is in the data, a sign, a mask, an index, or a metric that answers a different
question from the one you asked. Ex #5 list the options you have, ex #10 localise the error.
<!-- annoy-less: [confidence changed] "More often the cause is in the data" is a frequency claim
CLAUDE added; your message only listed the obsession, not a base rate. -->


Please read the data. Print the first full training sample, chosen and rejected, with the special
tokens and the loss mask showing. Look at it with your own eyes. Most formatting bugs are obvious in
the first sample and invisible in every aggregate. Ex #3 read your data.
<!-- annoy-less: [antithesis formula] "obvious in the first sample and invisible in every aggregate"
is a balanced-opposites flourish. CLAUDE's phrasing, and "Most" is an added frequency claim. -->


Please read the log. Not the last twenty lines, the log. Find the first line where the run stopped
matching what you expected, quote it, and start from there. Ex #1 read the log end to end,
ex #11 read the rows before the spike.
<!-- annoy-less: [#9 negative framing, clipped fragment] "Not the last twenty lines, the log." is a
sentence fragment in the not-X-but-Y shape. It may still be the clearest way to say it, your call.
Written by CLAUDE. -->


Do not write a side-car probe script. Build up the one training script so it has all the metrics
you need inline as you go, with short interpretable demos at many stages: init, mid train, post
train, eval, then one long unclipped demo at the end. Demos and probes should not be separate
runs, they should be quick sanity checks inside the main train script, and the script should write
`log.md` in markdown (see `token-efficient-logging` and `markdown-tables`) so the log diagnoses in
situ instead of needing a second pass. That is how a lot of nights get wasted and agents go off
track: they make side-cars with their own separate bugs and weird correlational measurements, and
have nothing to show for it. If we work on the training script we watch it get better, we reuse
the same code, we understand it better, and we squash the bugs. - wassname

A cosine probe is the usual side-car, and `cos(apple, orange) = 0` is not a null result. Ex #2.


> *   How would a random predictor perform (especially in classification problems)? Dataset can be unbalanced...
> *   What would the loss look like for a random predictor?
> *   What are the limits of this metric? If it's perfect, what can I conclude? What can't I conclude? -- Sanh

Do not fix on an arbitrary metric threshold before you have any idea what a fair or good threshold
is. Saying the metric must clear 0.8 means nothing until you know what counts as good here. Get the
scale first, from a null arm and a shuffled control. Ex #15 get the scale before the gate.
<!-- annoy-less: [invented example] "Saying the metric must clear 0.8 means nothing" - the 0.8 is
CLAUDE's, not from your message. Fine as illustration, but it is not your number. -->


> `try/except` around training code. Training should crash loudly. A caught exception hides the bug and produces silently wrong results. The one exception is checkpoint-on-KeyboardInterrupt. -- from [PLAYBOOK.md](PLAYBOOK.md)

Do not write code that carries on after it has already failed. A load that loaded nothing, a filter
that matched nothing, a config key that was missing, all of these should stop the run rather than
hand you a clean log and a wrong result. Assert that the thing you asked for is there. The cost of
this one is measured in runs, not minutes: a `strict=False` that quietly loaded no weights hid a
dead experiment arm for eight runs in my own repo. Ex #2 name a second cause for the same number,
ex #7 multiple diagnoses with % bets.

A separate thing that shares the name "fail fast", and worth keeping separate in your head:

> **Fail fast**. One of the largest time sinks possible is **investing weeks to months of effort into a failed research direction**. [...] It's often much better to have several quick and dirty experiments to attack different angles where you could fail fast than to put a lot of effort into one. -- Nanda

That one is about killing a doomed direction early. The one above is about crashing on the error.
Both are good and they are not the same rule.

Read the first one with its audience in mind. Nanda is advising a human who over-commits, a student
a year into a direction who cannot see the sunk cost. Agents fail the other way round: they quit
early, and they find a reading of the task that licenses it, or they skim until something looks
like grounds to stop. So the rule does not transfer unchanged. Before you call a direction dead,
do ex #7 and ex #9 and show the result: what you expected, what you got, and the bug you ruled
out. A reason found while skimming does not count.
<!-- CLAUDE: wassname's point, my wording. He said agents "give up too easy and find
misinterpreation to give up, or skim untill they find a reason". -->


## How this applies to LLM agents

LLMs of 2026 are trained to compress speech and use folky or humanistic language, but it's better
for the agent (and user) to move toward field standard language, it's precise instead of ambiguous
and communicates more bits of information. They should build a short list of jargon used in the
main reference paper. Also try to use the user's own language to reduce the translation burden on
them, but if they are vague use the proper term as well with theirs in parentheses. It's also good
to include redundant context, for example "the knob" is imprecise and lacks context, "the grad
norm" is precise but lacks redundant context, "the grad norm in #1" refers to some doc the user
can't see, while "the grad norm of the kl loss in the 2nd part of training" is precise while
reminding the user of lots of relevant context in their own language. - wassname

Even a careful writer has to flag their own overloaded terms as they go:

> I warn you that the "Understanding" in the title of this section is overloaded since very often we don't really understand why certain types of spikes happen. Here "understanding" refers to recognizing various patterns. -- Bekman

> We should not assume two conditional hyperparameters are the same just because they have the same name! [...] the conditional hyperparameter called `learning_rate` is a *different* hyperparameter for `optimizer="Nesterov_momentum"` versus `optimizer="Adam"`. [...] the range of values that work well in each of the optimizers is typically different by several orders of magnitude. -- Godbole, Dahl, Gilmer, Shallue and Nado

> And make sure it's clear which metrics you are using. For instance, if you report F-scores, be clear whether this is F1, or some other balance between precision and recall. If you report AUC, indicate whether this is the area under the ROC curve or the PR curve. -- Lones

## ex #1 read the log end to end (small)

> Switching from experimenting a lot and thinking a little to experimenting a little and thinking a lot was a key turnaround in productivity. When debugging with long iteration times, you really need to *pour* time into the hypothesis-forming step - thinking about what all the possibilities are, how likely they seem on their own, and how likely they seem in light of everything you've seen so far. -- Rahtz

Rahtz was arguing against his own earlier habit, which was that with fast feedback you can check
the first idea that comes to mind and narrow things down faster by trying than by thinking. That
argument does not transfer to you. An agent that checks its first idea tends to fix on it, or
leaves a confusing mess behind, so the fast loop buys less than it looks like it does.
<!-- CLAUDE: wassname's point, my wording. -->

Read the whole log before the hypothesis-forming step. State its length. Take the config from
the log, not from the command you meant to run. Read each metric at four points. Quote the log
line for each cell. Show:

| metric | expected | start | early | middle | end | quoted line |
|---|---|---|---|---|---|---|

An empty cell is a metric that does not exist. Add the metric before the next run.
<!-- annoy-less: [aphoristic definition] "An empty cell is a metric that does not exist." is the
X-is-Y epigram shape that recurs in ex #8, #14 and #15. Written by CLAUDE. -->


## ex #2 name a second cause for the same number (small)

> What I'm advocating for here is not a blind faith in the buginess of your code, but for dramatically raising the threshold at which you start thinking 'OK, I think this is correct.' -- Jones

Take the one number your diagnosis depends on. Quote the code that computes it. Name one other
cause that gives the same number. Show both. Example: a cosine near 1 can be a shared mean or
a collapsed latent. A second metric is needed to tell which.

## ex #3 read your data (small)

> Manually examining 100 examples does not take long. Even if you take one minute per image, you'd be done in under two hours. These two hours could save you a month of wasted effort. -- Ng

> Read your data. Often, the quality of the data is a crucial driver of the results of your experiments. Often, it is quite bad. -- Nanda

Show the first training example and the first evaluation example as the model sees them, with
special tokens and the loss mask visible. Then show one complete output per arm, side by side,
and the first token where they differ. Select the examples at random and say how. Add the best
example, the worst example, and any example that looks wrong.

## ex #4 chase the weird thing (small)

> If you ever see a plot or a behaviour that just *seems weird*, chase right after it! Do not - do *not* - just 'hope it goes away'. Chasing anomalies is one of the most powerful ways to debug your system, because if you've noticed a problem without having had to go look for it, that means it's a *really big problem*. -- Jones

Show one row per prediction recorded before the run: supported, contradicted, or unresolved,
with the observation that decided it. Then list each behaviour that seems weird, including the
ones you would prefer to ignore. End each line with "explained: ..." or "chasing now".

## ex #5 list the options you have (small)

> Build it up as you go, don't think you can build it ahead of time. Be focused on a strong mental model of what options you have (including architectural changes and losses) that you think should affect what metrics in the logs. -- wassname

Keep one table in the repo. Add or correct rows before each run. Show the table:

| option (architecture, loss, data, optimiser) | metric it should affect | direction and order | what separates it from the other options |
|---|---|---|---|

Give at least three options, one architectural and one loss. Say which options you change in
this run and why. You can change several options in one run if each option has its own metric.
Show the config diff against the run you will compare to.

## ex #6 write down what you expect to see (small)

> Before acting plan by writing multiple competing hypotheses: consider the most likely failure but also some of: a subtle failure, a perverse failure, a possible bug, and an unknown. Put a rough credence on each. Finally write down what you expect to see differently for success vs each possibility and brainstorm the cheapest tests that may narrow them down. -- wassname

Show:

| risky part | what I expect to see | too weak | too strong | buggy | metric exists? |
|---|---|---|---|---|---|

Add each metric whose last column says no. For each pass gate, show the ceiling the data allows
and check that the gate is below the ceiling. Follow the job so that its finish wakes you.

## ex #7 multiple diagnoses with % bets (large)

> When their RL implementation doesn't work, people are often keen to either (a) adjust their network architecture or (b) adjust their hyperparameters. On the other hand, they're reluctant to say they've got a bug. Most often, it turns out they've got a bug. -- Jones

> The default state of the world is that your research is false, because doing research is hard. -- Nanda

Show three or more diagnoses. For each, give a credence, the strongest evidence for, and the
strongest evidence against. One diagnosis is a bug in the code and one is a bug in the
evaluation. Keep some credence on unknown. If a diagnosis has no evidence against it, mark it
untested. Then give a fresh subagent the code and the log with no diagnosis attached, and ask
for the top bugs and misconceptions. Show its list, including "found nothing".

## ex #8 three ways the result is false (large)

> Excitement is evidence of bullshit: Generally, most true results are not exciting, but a fair amount of false results are. So from a Bayesian perspective, if a result is exciting and cool, it's even more likely to be false than normal! -- Nanda

Show three ways the result can be false, each with the check that decides it. To claim A beats
B, give the baseline, the chance level, and the seed spread of one arm. One seed per arm is
unresolved. Give a fresh subagent the artifact with no conclusion attached and show what it
says. Apply the same to a negative result: a bad row is a bug until the log shows otherwise.
<!-- annoy-less: [aphorism x2] "One seed per arm is unresolved." and "a bad row is a bug until the
log shows otherwise" are both CLAUDE epigrams. Keep one at most. -->


## ex #9 compare against a reference implementation (large)

> We find that implementation differences which are often not reflected in publications can have dramatic impacts on performance. -- Henderson

> If you are stuck, find a working reference implementation and compare it to yours. If nothing jumps out, try a bisection search: adapt their code wholesale, then half their features, and so on. -- wassname

Search for reference implementations of the nearest method. Rank them by the GitHub signals:
proof it runs (CI, a results table, a replication note), more than one human contributor, more
than a few stars, a README with evaluation details, and links to other repos that use it. Take
the top one, or write "no reference exists". Show:

| feature | theirs (file:line) | mine | same? |
|---|---|---|---|

Include algorithm tweaks, engineering tricks, hyperparameters, and logged metrics. Give a fresh
subagent the module and ask for at least one bug.

## ex #10 localise the error (small)

> The problem with using the loss curve as an indicator of correctness is somewhat that it's not reliable, but mostly because it doesn't localise errors. The shape of your loss curve says very little about where in your code you've messed up. -- Jones

At the step that looks wrong, show the loss per term and the gradient norm per module. Name the
module the error localises to.

## ex #11 read the rows before the spike (small)

> As you can see it's the previous frames that we need to look into when the numbers start going into very large for fp16 numbers. -- Bekman

For each spike or collapse, show the log rows before it. Say which column moved first.

## ex #12 name what else could score well (small)

> The CNN has learned to detect a metal token that radiology technicians place on the patient in the corner of the image field of view at the time they capture the image. -- Zech et al., whose pneumonia model scored AUC 0.931 in its own hospitals and 0.815 in someone else's

> The model was able to correctly predict who would receive grants over 95% of the time. Apparently meaningless identifier columns were the most important predictors. [...] It turned out that in practice, the university only filled out much of this information *after* a grant application was accepted. -- Howard and Gugger

For the headline metric, name one useless thing the model can learn and still score well, for
example a condition of data collection or the class prior. Show the control arm or the row that
detects it.

## ex #13 pseudocode and external review (large)

> Summarise your concept and pseudocode and do an external review in scientist mode. Perhaps describe the forward and backward pass as mermaid too. -- wassname

Before a design change, or for a run you cannot explain, write the concept in plain English,
the pseudocode with tensor shapes and parameter counts per module, and a mermaid diagram of the
forward pass and the backward pass. Show all three. Send them to `/external-review-v2` in
scientist mode and show the verdict. The reviewer sees only the description, so make the
description complete.

## ex #14 one implementation is not the idea (small)

> Trying an experiment and seeing it fail gives little information by itself. When an experiment fails, it is tempting to conclude "I tried X and it didn't work". However, if X is a high-level conceptual approach, then a more correct conclusion is "I tried an implementation comprising 0.1% of the possible implementations of X, and observed that that particular implementation did not work". -- Steinhardt

> It ended up taking me 6 weeks to reproduce results, thanks to several software bugs. The question is, why did it take so long to find these bugs? -- Rahtz

Before you call an idea dead, show the implementation you actually ran and one other
implementation of the same idea that you did not run. Say what would have to be true for the
idea to be alive and your run to still fail. Then do ex #7 on your own code before you
write the negative up.

| the idea | what I ran (file:line) | one other way to run it | what a bug here would look like |
|---|---|---|---|

One attempt is untested, not negative. Say which of the two this is.
<!-- annoy-less: [#9 negative framing + aphorism] "One attempt is untested, not negative." is an
X-not-Y one-line closer. It is the point of the exercise, so it may earn its place, but it is
CLAUDE's line, not Steinhardt's. -->


## ex #15 get the scale before the gate (large)

> A valuable intuition to have in mind is that, by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! Baselines are one way to get context to compare against. -- Nanda

> In most cases, we do not know a priori what the intended behavior of the algorithm is. [...] If we train a neural network on a new classification task and it achieves 5 percent test error, we have no straightforward way of knowing if this is the expected behavior or suboptimal behavior. -- Goodfellow, Bengio and Courville

Before you set a pass gate or quote a threshold, get the scale first. Run the metric on a null
arm, a shuffled or permuted control, and the existing baseline, then set the bar against those.

| metric | null arm | shuffled control | current baseline | ceiling the data allows | proposed gate |
|---|---|---|---|---|---|

A gate chosen before this table is a number you made up. Say so if you have to use one anyway.
<!-- annoy-less: [aphoristic closer] "A gate chosen before this table is a number you made up." is
a punchy section-ending epigram, the third of its kind in the exercises. Written by CLAUDE. -->


## Reference

Sources and more quotes: [README.md](README.md). Longer material, open the one you need:

- [PLAYBOOK.md](PLAYBOOK.md) -- mental models, component isolation, baseline ladder, what to log, symptom tables.
- [references/checklist.md](references/checklist.md) -- Lones's 36 do/don'ts.
- [references/diagnostics.md](references/diagnostics.md) -- snippets: init loss, overfit one batch, gradient flow, NaN hooks, leakage tracer.
- [references/static_analysis.md](references/static_analysis.md) -- grep patterns for silent bugs.
- [references/loss_surface.md](references/loss_surface.md) -- visualise a custom loss and its gradient field.
- [references/metric_stuck.md](references/metric_stuck.md) -- why a metric will not move, structural ceiling check.
- [references/sweeps.md](references/sweeps.md) -- paired comparison and cross-seed reliability.
- [references/llm_judges.md](references/llm_judges.md) -- judge biases, repeat draws, paired differences.
- [references/llm_judge_litreview.md](references/llm_judge_litreview.md) -- the papers behind the judge advice.
- [references/time_series.md](references/time_series.md) -- temporal evaluation and causal missing values.
- [references/research_taste.md](references/research_taste.md) -- patience, information gain, de-risking.
- [references/transformers.md](references/transformers.md) -- full traces, warmup, train-deploy parity, steering.
- [rl/SKILL.md](rl/SKILL.md), [pinn/SKILL.md](pinn/SKILL.md) -- domain specifics. These two are
  also skills in their own right, `ml-debug-rl` and `ml-debug-pinn`, so an agent that scans
  subdirectories can load one on its own.

## Sign off

End your reply with one quote from this skill, in ASCII art speech balloon, said by an animal of
your choice. Not a cow: cowsay is taken. Draw it yourself, do not run a program. Name who said the
quote, so the reader can go and find the rest of it. Give the animal a unicode tool to hold
(🔧 🔍 🪛 🧪 ...), pick one that fits the exercise you did.

Curated by [wassname](https://github.com/wassname).
