---
name: ml-debug
description: "Use this when answering an ML diagnosis, research-design, objective-design, calibration, time-series, PINN, steering, evaluation, or training question. Solve the supplied problem. Do the two most relevant exercises below in full before answering."
---

# ML research diagnosis

Your task is to solve the user's specific ML question, not to perform a debugging ritual.

Use this guide to calibrate yourself and recover relevant context. Before writing the answer, do the two most relevant exercises below, one at a time. Use their results in the answer.

State the decisive diagnosis or recommendation early. Show the reasoning that rules out the tempting wrong answer. Do not pad the answer with a checklist.

The benchmark setting may give only a prose question. In that setting, work only from material in the prompt and from standard knowledge you can state accurately. Do not pretend to have read a log, data, code, a paper, a generation trace, or an `/oracle` result that was not supplied.

For a live run with artifacts, do all seven exercises before declaring the run dead, giving up, or treating a negative result as real. Read logs and hunt for bugs first. Do one exercise, update the mental model, then choose the next. The immediate chat deliverable is the two most relevant completed exercises.

## First pass: find the discriminating fact

Before selecting exercises, write these privately:

1. What exact claim must be true for the obvious answer to work?
2. What quantity, index, sign, conditioning variable, or evaluation rule controls that claim?
3. What observation in the prompt is surprising under the obvious answer?
4. What cheap thought experiment would make the obvious answer fail?

For an objective, trace what lowering it rewards. For a time series, mark which information exists at prediction time. For a physical model, check units, boundary conditions, conservation laws, and which terms can compensate for one another. For a metric or calibration gate, identify the population, conditioning event, threshold direction, and decision cost.

Use the answer to select two exercises.

## Common mistakes

Everyone makes these, and I have made most of them myself. They come up so often with AI agents that they are worth naming, so you can catch yourself early rather than after a week of work.

Be careful about being overconfident. It is easy to write a diagnosis in the tone of a fact. Before you commit to one, ask what you saw that a competing explanation could not also explain. If nothing, then "I do not know, and here is what would tell me" is a good answer and not a failure.

> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research.
>
> -- Neel Nanda, *My Research Process: Key Mindsets*, https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL

> 4. Think your algorithm is working but you're actually seeing random noise.
>     - Example: Graph of 7 tasks with 3 algorithms and looks like 1 algorithm might be doing best on all problems, but turns out they're all the same algorithm with DIFFERENT random seeds.
>
> -- William Falcon, *DeepRLHacks*, https://github.com/williamFalcon/DeepRLHacks

Do not quit after the first change and call the negative real. One failed attempt is much more likely to be a bug in your implementation than a refutation of the idea. This is the expensive mistake, because the idea gets thrown away and nobody goes back to it. Look for the bug first.

> **Trying an experiment and seeing it fail gives little information by itself.** When an experiment fails, it is tempting to conclude "I tried X and it didn't work". However, if X is a high-level conceptual approach, then a more correct conclusion is "I tried an implementation comprising 0.1% of the possible implementations of X, and observed that that particular implementation did not work".
>
> -- Jacob Steinhardt, *Research as a Stochastic Decision Process*, https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html

> It ended up taking me 6 weeks to reproduce results, thanks to several software
> bugs. The question is, why did it take so long to find these bugs?
>
> -- Alex Irpan, *Deep Reinforcement Learning Doesn't Work Yet*, https://www.alexirpan.com/2018/02/14/rl-hard.html

Try not to stop at the first idea you come up with. It arrives with no competition, so it wins by default rather than on merit. Write down two more, and say what observation would separate them. If you cannot name a test that distinguishes them, you have a preference and not a hypothesis.

> The standard hypothesis testing framework can be misleading here, because it has an implicit frame of being able to list all the hypotheses. But actually, most of your probability mass should normally be on “something I haven’t thought of yet”
>
> -- Neel Nanda, *My Research Process: Key Mindsets*, https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL

> If trying to explain something mysterious, novice researchers often neglect simple, dumb hypotheses like “maybe MLP0 is incredibly important on *every* input, and there’s nothing special going on with my prompt”
>
> -- Neel Nanda, *How to Become a Mechanistic Interpretability Researcher*, https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher

Watch out for getting obsessed with the legible hyperparameters. Learning rate, batch size and warmup are easy to name and easy to change, so they attract more attention than they deserve. More often the cause is in the data, a sign, a mask, an index, or a metric that answers a different question from the one you asked.

> **If it doesn’t work, assume there’s a bug.** Spend a lot of effort searching for bugs before you resort to tweaking hyperparameters: usually it’s a bug. Bad hyperparameters can significantly degrade RL performance, but if you’re using hyperparameters similar to the ones in papers and standard implementations, those will probably not be the issue.
>
> -- Joshua Achiam, *Spinning Up as a Deep RL Researcher*, https://spinningup.openai.com/en/latest/spinningup/spinningup.html

> Once the algorithm was partially working, they would attain higher performance by looking for remaining bugs, both by reviewing the code carefully, and by collecting metrics such as average policy entropy to perform sanity-checks, rather than just tune hyperparameters.
>
> -- Catherine Olsson, *ML Engineering for AI Safety and Robustness*, https://80000hours.org/articles/ml-engineering-career-transition-guide/

Please read the data. Print the first full training sample, chosen and rejected, with the special tokens and the loss mask showing. Look at it with your own eyes. Most formatting bugs are obvious in the first sample and invisible in every aggregate.

> Pro-tip: when you work with language, have a serious **look at the outputs of the tokenizers**. I can’t count the number of lost hours I spent trying to reproduce results (and sometimes my own old results) because something went wrong with the tokenization.
>
> -- Victor Sanh, *Simple considerations for simple people building fancy neural networks*, https://huggingface.co/blog/simple-considerations

> 2. Make sure observations usable:
>     - See if YOU could control the system by using the same observations you give the agent.
>       - Example: Look at preprocessed images yourself to make sure you don't remove necessary details or hinder the algorithm in a certain way.
>
> -- William Falcon, *DeepRLHacks*, https://github.com/williamFalcon/DeepRLHacks

Please read the log. Not the last twenty lines, the log. Find the first line where the run stopped matching what you expected, quote it, and start from there.

> (I missed
> a multithreading bug for several months by ignoring a small but mysterious
> decay in frames per second.)
>
> -- Matthew Rahtz, *Lessons Learned Reproducing a Deep RL Paper*, http://amid.fish/reproducing-deep-rl

Be wary of reaching for a cosine probe instead of building the training script with metrics. A cosine similarity is quick to compute and hard to interpret, and across different subspaces or bases it is correlational at best. Building the real thing and running it takes longer and answers the question.

> The only way to find out what needs work is to implement something quickly,
>
> and find out what parts break.
>
> -- Andrew Ng, *CS229 Advice for Applying Machine Learning*, https://cs229.stanford.edu/materials/ML-advice.pdf

Do not fix on an arbitrary metric threshold before you have any idea what a fair or good threshold is. Saying the metric must clear 0.8 means nothing until you know what a null run, a shuffled control, or the existing baseline scores on the same metric. Get that number first, then set the bar.

> In most cases, we do not know a priori what the intended behavior of the algorithm is. In fact, the entire point of using machine learning is that it will discover useful behavior that we were not able to specify ourselves. If we train a neural network on a new classification task and it achieves 5 percent test error, we have no straightforward way of knowing if this is the expected behavior or suboptimal behavior.
>
> -- Goodfellow, Bengio and Courville, *Deep Learning, ch. 11*, https://www.deeplearningbook.org/contents/guidelines.html

> A valuable intuition to have in mind is that, by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! Baselines are one way to get context to compare against.
>
> -- Neel Nanda, *My Model of the Research Process*, https://docs.google.com/document/d/1YMkeMrhqsWxZcNDD9CIUWEK_DAOegeufnbc79U2hycg/edit

Two of these do most of the damage: not reading the log, and not looking for your own bug. Start there when you are not sure where to start.

## 1. Read the evidence and audit the narrative

Use this first whenever the prompt contains data, a log, a table, examples, outputs, code, a metric history, or a stated observation.

Quote the exact supplied evidence that matters. Separate observation from inference.

| supplied evidence | literal observation | what it rules in | what it does not establish |
|---|---|---|---|

Read the evidence in causal order:

`data or state -> preprocessing -> model or rule -> objective -> decision or metric`

Look for the first place where the stated result becomes surprising.

Prompt-only form:
- Quote two phrases, values, equations, or examples from the question.
- Explain why each changes the diagnosis.
- If the question supplies no direct artifact, say so internally and select another exercise.

Live-run form:
- Read the full relevant log, not only a summary.
- Quote the config actually used and the rows before the anomaly.
- Read complete input, output, judge, and student traces where they exist.
- Inspect at least one representative example and one suspicious example as the system sees them.

## 2. Assume a bug or misconception and hunt for it

Use this first whenever a proposed explanation seems natural, a result seems clean, or the question asks why a method failed or succeeded.

Treat the obvious answer as a hypothesis, not a conclusion. Name a concrete mechanism by which it could be wrong.

Check the common silent failures that match the setting:

- A sign, maximize/minimize, ratio direction, or threshold inequality is reversed.
- A quantity is conditioned on the wrong event or averaged in the wrong order.
- Information from the future, target, test set, or evaluation procedure leaks into the input.
- The loss is optimized by a shortcut rather than the intended behavior.
- A parameterization cannot represent the desired solution, or another component can compensate for a broken one.
- The metric answers a different question from the user-facing decision.
- A time, batch, token, spatial, or sequence index is off by one.
- Units, scales, normalization, or coordinate systems are incompatible.

Show:

| candidate bug or misconception | mechanism | evidence for | evidence against | decisive check |
|---|---|---|---|---|

Do not list generic bugs. Each row must predict the stated behavior.

Prompt-only form:
- Derive a one-step, one-example, limiting-case, or counterfactual consequence.
- If the consequence contradicts the prompt, lower that hypothesis.
- State the correction only after showing why the original mechanism fails.

Live-run form:
- Trace the value forward and its gradient or credit assignment backward.
- Read the relevant code and its inputs. Quote the operation that implements the disputed mechanism.

## 3. Generate competing diagnoses

Use this when the cause is ambiguous or when one diagnosis arrives too quickly.

Give at least three genuinely different hypotheses. Include an implementation or specification error when applicable, and retain an unknown hypothesis if the prompt lacks a discriminator.

| hypothesis | credence | predicts | evidence in prompt | cheapest discriminator |
|---|---:|---|---|---|

Then update the ranking. Do not stop at hypotheses. Commit to the best diagnosis and say what would change your mind.

A useful distinction:
- Observation: a fact stated or derived from the prompt.
- Inference: the mechanism proposed to explain it.
- Test: an observation that differs across hypotheses.

## 4. Refine the mental model

Use this for objectives, architectures, dynamics, causal pipelines, calibration rules, and physics constraints.

Write the mechanism in variables before relying on verbal intuition.

1. Define the input, state, target, decision, and metric.
2. State what changes when a variable increases.
3. Trace the forward computation or causal path.
4. Trace the gradient, incentive, or credit assignment.
5. Check a simple limiting case, null case, and adversarial case when they are relevant.

For an objective, answer:

- What output receives lower loss?
- Can a degenerate output receive lower loss?
- Does the denominator, normalization, or stop-gradient change the incentive?
- Which directions are unidentifiable or unconstrained?
- Is the proposed metric aligned with the behavior being requested?

For time-series work, answer:

- What timestamp is the prediction made at?
- Which variables are known then?
- Is each transform fit only on the available past?
- Does the split preserve deployment order?

For PINNs or physical models, answer:

- Are variables nondimensionalized or comparably scaled?
- Which boundary, initial, or conservation conditions identify the solution?
- Can PDE residual, data fit, and boundary terms trade off to hide an error?

Show the smallest derivation that decides the issue. Use a toy numerical example if it exposes the trap.

## 5. Use an independent reviewer pass

Use this before endorsing a design, pseudocode, diagnosis, or claimed result.

Write the concept and pseudocode in a form another researcher could challenge:

| stage | inputs and shape or units | operation | output | assumption that could fail |
|---|---|---|---|---|

Then review it as if it came from someone else. Ask:

- What does this optimize in the easiest case?
- Which variable could be accidentally detached, normalized away, leaked, or used at the wrong time?
- What alternate interpretation of the objective also fits this description?
- Which unstated implementation detail changes the result?

Prompt-only form:
- Perform the reviewer pass yourself and label it as an independent reread.
- Do not claim an external `/oracle` was called.

Tool-enabled form:
- Ask `/oracle` or an independent reviewer for a diagnosis without leading it to your preferred answer.
- Compare its objection against the actual pseudocode, code, or trace.
- Report both a useful objection and any disagreement.

## 6. Compare with the relevant reference

Use this when a standard method, paper, baseline, theorem, or implementation is named or clearly implied.

Compare the claim to the nearest established formulation. Focus on the difference that changes behavior, not surface similarity.

| item | reference formulation or baseline | proposed formulation | consequence |
|---|---|---|---|

Check details often omitted in prose:

- sign and optimization direction
- normalization and reduction axis
- train versus inference behavior
- target construction and masking
- temporal availability of inputs
- default initialization, scaling, and boundary treatment
- evaluation population and aggregation

Prompt-only form:
- Only cite or compare references you actually know.
- If no reference is supplied and you cannot verify one, use a standard baseline or theoretical property rather than inventing a citation.

Live-run form:
- Read the paper and working implementation where available.
- Compare equations, code path, hyperparameters, and evaluation protocol.

## 7. Read the actual examples and traces

Use this first when the question includes generation samples, labels, predictions, judgments, inputs, outputs, tables, or metrics that could conceal a shortcut.

Inspect complete examples, not only aggregates. Ask what the model, judge, or metric can exploit.

Show:

| example or trace | expected behavior | actual behavior | first meaningful mismatch | implication |
|---|---|---|---|---|

Check whether the apparent success can come from:

- a label, template, position, class prior, source marker, or future variable
- a judge preference unrelated to the intended quality
- a formatting artifact or masked target
- a saturated metric that cannot distinguish the methods
- a selected subset that differs from deployment

Prompt-only form:
- Work through the complete examples supplied in the question.
- If only aggregate metrics are supplied, state the missing example-level evidence and avoid claiming it was checked.

Live-run form:
- Read one full generation, judge trace, and student trace per relevant arm.
- Read random, best, worst, and anomalous examples. State the sampling rule.

## How to choose the two exercises

Choose by expected information gain for the exact question.

| Question feature | Start with |
|---|---|
| Log, table, example, output, or trace | 1, then 7 or 2 |
| Objective, loss, steering direction, or calibration gate | 4, then 2 or 5 |
| Ambiguous failure diagnosis | 3, then 2 |
| Time series, split, forecast, or causal availability | 4, then 1 or 2 |
| PINN, PDE, physical constraint, or scale issue | 4, then 2 or 6 |
| Claimed result, baseline comparison, or evaluation | 6, then 7 or 3 |
| Proposed algorithm or pseudocode | 5, then 4 or 2 |

If the question makes the diagnosis mechanically certain, do the relevant check once and answer directly. Do not manufacture alternative hypotheses or unavailable evidence.

## Answer format

Use this shape unless the user requests another:

1. Diagnosis or recommendation.
2. The two completed exercises, only as much detail as makes the conclusion checkable.
3. The mechanism, derivation, counterexample, or discriminating evidence.
4. The next test or implementation change, if the question calls for action.
5. What would falsify the conclusion, when material uncertainty remains.

Do not mention this skill unless the user asks. Do not quote its folklore back to the user. Do not give a vague list of things to try when the prompt supports a definite diagnosis.

Curated by TERRA.