---
name: ml-debug
description: "Machine learning debugging exercises, each under a quote from a practitioner. If this loaded, do the exercise for your situation and show the result in your reply. Invoke it yourself. Triggers: read the log, the run finished, it crashed, queue a run, the loss is not going down, the metric will not move, is this result real, does A beat B, a spike or anything weird in the log, and any moment you are about to write that a result looks fine."
---

In an attempt to upskill the machine learning debugging on AI coding assistants (and humans), I've collected high quality sources on how to debug machine learning projects, focusing on the mindset and the "taste". When I started ML I went searching for discussions on best practices, and started a few discussions of my own and they helped me a lot, over the years I've collected good ones. I hope they can help others, as well as help in auto research setups. This intro is human written, and the below is AI written with human guidance. - wassname

If this skill loaded, do at least one exercise below and show the result in your reply. Each
exercise is marked (small) or (large). A small one takes less than a paragraph to answer; a large
one is a lot of work, such as searching for a reference repo and comparing against it. Do all the
small ones that apply, and pick one large one. Exercises 1 and 3 are always in scope.
<!-- CLAUDE: 7 was mandatory but is large under the new small/large rule. Left as a pickable large one. wassname to confirm. -->
Then select by situation:

- a run finished or crashed: 1, 2, 3, 4
- something weird in the log (a spike, a flat line, an impossible value): 10, 11
- about to queue a run: 5, 6
- about to change the design, or a run you cannot explain: 13
- about to report a result, or to call it negative: 7, 8, 12, 14
- about to set a pass gate or quote a threshold: 15
- two cycles with no progress: 9

Each exercise says what to show. Show it in full: the table, the quoted log line, the quoted
code, the pasted sample. Write "unknown" in a cell you cannot fill, and say what would fill it.
Give the source of each number.

Never stop a job or give up on an idea without doing all of these. One at a time, not all at once.

## Common mistakes

Everyone makes these, and I have made most of them myself. They come up so often with AI agents in
long autoresearch runs that they are worth naming, so you can catch yourself early rather than after
a week of work. Reading the log and hunting for your own bug are the two that do most of the damage,
so start there when you are not sure where to start. - wassname

> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research. -- Nanda

> The challenge lies in the fact that you can make these mistakes, train a model without it ever crashing, and still get a decent performance... -- Sanh

Be careful about being overconfident. It is easy to write a diagnosis in the tone of a fact. Before
you commit to one, ask what you saw that a competing explanation could not also explain. If nothing,
then "I do not know, and here is what would tell me" is a good answer and not a failure. Exercise 7.

Do not quit after the first change and call the negative real. One failed attempt is much more
likely to be a bug in your implementation than a refutation of the idea. This is the expensive
mistake, because the idea gets thrown away and nobody goes back to it. Look for the bug first.
Exercise 14.

Try not to stop at the first idea you come up with. It arrives with no competition, so it wins by
default rather than on merit. Write down two more, and say what observation would separate them. If
you cannot name a test that distinguishes them, you have a preference and not a hypothesis.
Exercises 6 and 7.

> If it doesn't work, assume there's a bug. Spend a lot of effort searching for bugs before you resort to tweaking hyperparameters: usually it's a bug. Bad hyperparameters can significantly degrade RL performance, but if you're using hyperparameters similar to the ones in papers and standard implementations, those will probably not be the issue. -- Achiam

Watch out for getting obsessed with the legible hyperparameters. Learning rate, batch size and
warmup are easy to name and easy to change, so they attract more attention than they deserve. More
often the cause is in the data, a sign, a mask, an index, or a metric that answers a different
question from the one you asked. Exercises 5 and 10.

Please read the data. Print the first full training sample, chosen and rejected, with the special
tokens and the loss mask showing. Look at it with your own eyes. Most formatting bugs are obvious in
the first sample and invisible in every aggregate. Exercise 3.

Please read the log. Not the last twenty lines, the log. Find the first line where the run stopped
matching what you expected, quote it, and start from there. Exercises 1 and 11.

Be wary of reaching for a cosine probe instead of building the training script with metrics. It is
easy to make a mistake with cosine. It is not causal, and two different subspaces score near zero
even when they are correlated, so `cos(apple, orange) = 0` is not a null result. Building the real
thing and running it takes longer and answers the question. Exercise 2.

> *   How would a random predictor perform (especially in classification problems)? Dataset can be unbalanced...
> *   What would the loss look like for a random predictor?
> *   What are the limits of this metric? If it's perfect, what can I conclude? What can't I conclude? -- Sanh

Do not fix on an arbitrary metric threshold before you have any idea what a fair or good threshold
is. Saying the metric must clear 0.8 means nothing until you know what counts as good here. Get the
scale first, from a null arm and a shuffled control. Exercise 15.

## How this applies to LLM agents

<!-- CLAUDE: wassname to write. This slot is for your comment on how the advice above lands
differently for an LLM agent than for a human. Left empty on purpose rather than filled with
my guess at your opinion. -->

## 1. "Experimenting a little and thinking a lot" (small)

> Switching from experimenting a lot and thinking a little to experimenting a little and thinking a lot was a key turnaround in productivity. When debugging with long iteration times, you really need to *pour* time into the hypothesis-forming step - thinking about what all the possibilities are, how likely they seem on their own, and how likely they seem in light of everything you've seen so far. -- Rahtz

Read the whole log before the hypothesis-forming step. State its length. Take the config from
the log, not from the command you meant to run. Read each metric at four points. Quote the log
line for each cell. Show:

| metric | expected | start | early | middle | end | quoted line |
|---|---|---|---|---|---|---|

An empty cell is a metric that does not exist. Add the metric before the next run.

## 2. "Raising the threshold at which you start thinking 'OK, I think this is correct'" (small)

> What I'm advocating for here is not a blind faith in the buginess of your code, but for dramatically raising the threshold at which you start thinking 'OK, I think this is correct.' -- Jones

Take the one number your diagnosis depends on. Quote the code that computes it. Name one other
cause that gives the same number. Show both. Example: a cosine near 1 can be a shared mean or
a collapsed latent. A second metric is needed to tell which.

## 3. "Manually examining 100 examples does not take long" (small)

> Manually examining 100 examples does not take long. Even if you take one minute per image, you'd be done in under two hours. These two hours could save you a month of wasted effort. -- Ng

> Read your data. Often, the quality of the data is a crucial driver of the results of your experiments. Often, it is quite bad. -- Nanda

Show the first training example and the first evaluation example as the model sees them, with
special tokens and the loss mask visible. Then show one complete output per arm, side by side,
and the first token where they differ. Select the examples at random and say how. Add the best
example, the worst example, and any example that looks wrong.

## 4. "Chase right after it" (small)

> If you ever see a plot or a behaviour that just *seems weird*, chase right after it! Do not - do *not* - just 'hope it goes away'. Chasing anomalies is one of the most powerful ways to debug your system, because if you've noticed a problem without having had to go look for it, that means it's a *really big problem*. -- Jones

Show one row per prediction recorded before the run: supported, contradicted, or unresolved,
with the observation that decided it. Then list each behaviour that seems weird, including the
ones you would prefer to ignore. End each line with "explained: ..." or "chasing now".

## 5. "A strong mental model of what options you have" (small)

> Build it up as you go, don't think you can build it ahead of time. Be focused on a strong mental model of what options you have (including architectural changes and losses) that you think should affect what metrics in the logs. -- wassname

Keep one table in the repo. Add or correct rows before each run. Show the table:

| option (architecture, loss, data, optimiser) | metric it should affect | direction and order | what separates it from the other options |
|---|---|---|---|

Give at least three options, one architectural and one loss. Say which options you change in
this run and why. You can change several options in one run if each option has its own metric.
Show the config diff against the run you will compare to.

## 6. "Write down what you expect to see differently" (small)

> Before acting plan by writing multiple competing hypotheses: consider the most likely failure but also some of: a subtle failure, a perverse failure, a possible bug, and an unknown. Put a rough credence on each. Finally write down what you expect to see differently for success vs each possibility and brainstorm the cheapest tests that may narrow them down. -- wassname

Show:

| risky part | what I expect to see | too weak | too strong | buggy | metric exists? |
|---|---|---|---|---|---|

Add each metric whose last column says no. For each pass gate, show the ceiling the data allows
and check that the gate is below the ceiling. Follow the job so that its finish wakes you.

## 7. "Most often, it turns out they've got a bug" (large)

> When their RL implementation doesn't work, people are often keen to either (a) adjust their network architecture or (b) adjust their hyperparameters. On the other hand, they're reluctant to say they've got a bug. Most often, it turns out they've got a bug. -- Jones

> The default state of the world is that your research is false, because doing research is hard. -- Nanda

Show three or more diagnoses. For each, give a credence, the strongest evidence for, and the
strongest evidence against. One diagnosis is a bug in the code and one is a bug in the
evaluation. Keep some credence on unknown. If a diagnosis has no evidence against it, mark it
untested. Then give a fresh subagent the code and the log with no diagnosis attached, and ask
for the top bugs and misconceptions. Show its list, including "found nothing".

## 8. "Excitement is evidence of bullshit" (large)

> Excitement is evidence of bullshit: Generally, most true results are not exciting, but a fair amount of false results are. So from a Bayesian perspective, if a result is exciting and cool, it's even more likely to be false than normal! -- Nanda

Show three ways the result can be false, each with the check that decides it. To claim A beats
B, give the baseline, the chance level, and the seed spread of one arm. One seed per arm is
unresolved. Give a fresh subagent the artifact with no conclusion attached and show what it
says. Apply the same to a negative result: a bad row is a bug until the log shows otherwise.

## 9. "Implementation differences ... can have dramatic impacts" (large)

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

## 10. "The shape of your loss curve ... doesn't localise errors" (small)

> The problem with using the loss curve as an indicator of correctness is somewhat that it's not reliable, but mostly because it doesn't localise errors. The shape of your loss curve says very little about where in your code you've messed up. -- Jones

At the step that looks wrong, show the loss per term and the gradient norm per module. Name the
module the error localises to.

## 11. "It's the previous frames that we need to look into" (small)

> As you can see it's the previous frames that we need to look into when the numbers start going into very large for fp16 numbers. -- Bekman

For each spike or collapse, show the log rows before it. Say which column moved first.

## 12. "The NN had learned something useless like time of day" (small)

> Researchers training a neural network to detect tanks in photographs, succeeding, only to realize the photographs had been collected under specific conditions for tanks/non-tanks and the NN had learned something useless like time of day. -- gwern, who traced it back to 1992 and calls it an urban legend

For the headline metric, name one useless thing the model can learn and still score well, for
example a condition of data collection or the class prior. Show the control arm or the row that
detects it.

## 13. "Summarise your concept and pseudocode, then get it reviewed" (large)

> Summarise your concept and pseudocode and do an external review in scientist mode. Perhaps describe the forward and backward pass as mermaid too. -- wassname

Before a design change, or for a run you cannot explain, write the concept in plain English,
the pseudocode with tensor shapes and parameter counts per module, and a mermaid diagram of the
forward pass and the backward pass. Show all three. Send them to `/external-review-v2` in
scientist mode and show the verdict. The reviewer sees only the description, so make the
description complete.

## 14. "An implementation comprising 0.1% of the possible implementations of X" (small)

> Trying an experiment and seeing it fail gives little information by itself. When an experiment fails, it is tempting to conclude "I tried X and it didn't work". However, if X is a high-level conceptual approach, then a more correct conclusion is "I tried an implementation comprising 0.1% of the possible implementations of X, and observed that that particular implementation did not work". -- Steinhardt

> It ended up taking me 6 weeks to reproduce results, thanks to several software bugs. The question is, why did it take so long to find these bugs? -- Rahtz

Before you call an idea dead, show the implementation you actually ran and one other
implementation of the same idea that you did not run. Say what would have to be true for the
idea to be alive and your run to still fail. Then do exercise 7 on your own code before you
write the negative up.

| the idea | what I ran (file:line) | one other way to run it | what a bug here would look like |
|---|---|---|---|

One attempt is untested, not negative. Say which of the two this is.

## 15. "By default, all numbers are meaningless because we lack any scale" (large)

> A valuable intuition to have in mind is that, by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! Baselines are one way to get context to compare against. -- Nanda

> In most cases, we do not know a priori what the intended behavior of the algorithm is. [...] If we train a neural network on a new classification task and it achieves 5 percent test error, we have no straightforward way of knowing if this is the expected behavior or suboptimal behavior. -- Goodfellow, Bengio and Courville

Before you set a pass gate or quote a threshold, get the scale first. Run the metric on a null
arm, a shuffled or permuted control, and the existing baseline, then set the bar against those.

| metric | null arm | shuffled control | current baseline | ceiling the data allows | proposed gate |
|---|---|---|---|---|---|

A gate chosen before this table is a number you made up. Say so if you have to use one anyway.

## Reference

Sources and more quotes: [README.md](README.md). Longer material, open the one you need:

- [PLAYBOOK.md](PLAYBOOK.md) -- mental models, component isolation, baseline ladder, what to log, symptom tables.
- [refs/checklist.md](refs/checklist.md) -- Lones's 36 do/don'ts.
- [refs/diagnostics.md](refs/diagnostics.md) -- snippets: init loss, overfit one batch, gradient flow, NaN hooks, leakage tracer.
- [refs/static_analysis.md](refs/static_analysis.md) -- grep patterns for silent bugs.
- [refs/loss_surface.md](refs/loss_surface.md) -- visualise a custom loss and its gradient field.
- [refs/metric_stuck.md](refs/metric_stuck.md) -- why a metric will not move, structural ceiling check.
- [refs/sweeps.md](refs/sweeps.md) -- paired comparison and cross-seed reliability.
- [refs/llm_judges.md](refs/llm_judges.md) -- judge biases, repeat draws, paired differences.
- [refs/time_series.md](refs/time_series.md) -- temporal evaluation and causal missing values.
- [refs/research_taste.md](refs/research_taste.md) -- patience, information gain, de-risking.
- [refs/transformers.md](refs/transformers.md) -- full traces, warmup, train-deploy parity, steering.
- [rl/SKILL.md](rl/SKILL.md), [pinn/SKILL.md](pinn/SKILL.md) -- domain specifics.
- [SKILL_old.md](SKILL_old.md) -- the previous procedural version (P1-P5), kept until reviewed.

## Sign off

End your reply with one quote from this skill, in ASCII art speech balloon, said by an animal of
your choice. Not a cow: cowsay is taken. Draw it yourself, do not run a program.

Curated by [wassname](https://github.com/wassname).
