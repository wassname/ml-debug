# wassname's ML Debugging Folklore

In an attempt to upskill the machine learning debugging on AI coding assistants (and humans), I've collected high quality sources on how to debug machine learning projects, focusing on the mindset and the "taste". When I started ML I went searching for discussions on best practices, and started a few discussions of my own and they helped me a lot, over the years I've collected good ones. I hope they can help others, as well as help in auto research setups. This intro is human written, and the below is AI written with human guidance.

## Use as a Claude skill

```
/skills add https://github.com/wassname/ml-debug
```

Or paste `SKILL.md` into your system prompt / context when debugging.

## What's here

- **This README** -- the folklore, for humans: verbatim sourced quotes from practitioners, general lessons first, modern transformers and LLM fine-tuning in their own section.

- **[SKILL.md](SKILL.md)** -- what an agent loads: the folklore turned into instructions, each with a trigger, a form to fill, and output to show the user. "Assume you have a bug" becomes "send a subagent to find one and report what it found". This is a bet that a form gets filled where a principle gets skipped, and it is untested. The bet is worth making because the folklore version measured no gain (below), and because forms have their own failure mode: they get filled with plausible content that nobody checked.

- **[PLAYBOOK.md](PLAYBOOK.md)** -- the synthesized long-form: mental models, practitioner priors, step catalogs, symptom tables, the agent debugging loop, triage, and anti-patterns. Menus of hypotheses distilled from the same sources, not quotes. Deeper one-off tricks (loss-surface analysis, stuck-metric diagnosis, sweep reliability) live in [references/](references/).

- **[docs/evidence/](docs/evidence/)** -- frozen local copies of source material (blog posts, talks, papers, reddit threads). Claims here link back to exact quotes.

## Folklore


### Think more, experiment less

> before acting plan by writing multiple competing hypotheses: consider the most likely failure but also some of: a subtle failure, a perverse failure, a possible bug, and an unknown. Put a rough credence on each. Finally write down what you expect to see differently for success vs each possiblity and brainstorm the cheapest tests that may narrow them down. - wassname

> Switching from experimenting a lot and thinking a little to experimenting a little and thinking a lot was a key turnaround in productivity. When debugging with long iteration times, you really need to *pour* time into the hypothesis-forming step - thinking about what all the possibilities are, how likely they seem on their own, and how likely they seem in light of everything you've seen so far. Spend as much time as you need, even if it takes 30 minutes, or an hour. Reserve experiments for once you've fleshed out the hypothesis space as thoroughly as possible and know which pieces of evidence would allow you to best distinguish between the different possibilities.[^rahtz]


### Don't write from scratch; start or compare to a working a reference

> If you are stuck, find a working reference implementation and compare it to yours. Relvent as the hyperparameters, model, data but especially subtle things like algorithm tweaks, and engineering tricks. If nothing jumps out, the fastest way might be to try a bisection search. Here you adapt their code wholesale and try the quickest test you can. If their code works then try again with half their features and so on. Eventuall you narrow down the features that are nessesary - wassname

> If you're doing anything that involves an RL algorithm as a component in a larger system, don't try and implement the RL algorithm yourself. [...] RL is unstable enough at the moment that you'll never be sure whether your system doesn't work because of a bug in your RL implementation or because of a bug in your larger system.[^rahtz]

> We find that implementation differences which are often not reflected in publications can have dramatic impacts on performance.[^henderson]

When you're stuck after a diagnostic cycle or two, the generalization of this advice is to find a working implementation (rank candidates by community adoption > papers citing it > code that runs > author reputation) and diff your math, computation graph, and hyperparameters against it. For RL see [rl/SKILL.md](rl/SKILL.md).

### Assume you have a bug

> When their RL implementation doesn't work, people are often keen to either (a) adjust their network architecture or (b) adjust their hyperparameters. On the other hand, they're reluctant to say they've got a bug. Most often, it turns out they've got a bug. Why bugs are so much more common in RL code is discussed above, but there's another advantage to assuming you've got a bug: bugs are a damn sight faster to find and fix than validating that your new architecture is an improvement over the old one.[^jones]

> What I'm advocating for here is not a blind faith in the buginess of your code, but for dramatically raising the threshold at which you start thinking 'OK, I think this is correct.'[^jones]

A bug can also hide, because most ML models have multiple adaptive parts: 

> "If one part is broken, the other parts can adapt and still achieve roughly acceptable performance" [^goodfellow],
and it may not show in the output at all.

### Default to disbelieving your own results (Neel Nanda)

> The default state of the world is that your research is false, because doing research is hard.[^nanda]

> Excitement is evidence of bullshit: Generally, most true results are not exciting, but a fair amount of false results are. So from a Bayesian perspective, if a result is exciting and cool, it's even more likely to be false than normal![^nanda]

The cheapest antidote he gives: "Read your data ... Often, the quality of the data is a crucial driver of the results of your experiments. Often, it is quite bad."[^nanda]

I'll add. for LLM's I suggest assuming every negative results is a bug, and 1) reviewing associated code and output logs to find the top 5 reasons/probabilities why the results might be invalid 2) to avoid skimming this report should involve quoting and interpreting to the user about everything, which should include at least: config, weird code / engineering, data, eval and importantly the log and metrics behaviour and demos in it. It should often include looking at a random sample of output and comparing it to the expected output. - wassname

### Understand the system to shrink the search (Ulisse Mini)

> When good programmers debug hard problems fast, it's usually because they understand the system well enough to *track the important internal state* in their head, letting them drastically *reduce the solution space they're searching over.*[^ulisse]

### Gears beat black boxes (John Wentworth)

> figuring out a system's gears takes extra work up-front, but yields dividends forever. [...] The black-box approach is cheaper for one-off tasks, but usually doesn't yield any insights which will generalize to new tasks using the same system[^wentworth]


### Broken code fails silently; measure everything (Spinning Up)

Josh Achiam's warning is RL-framed but general:

> broken RL code almost always fails silently, where the code appears to run fine except that the agent never learns how to solve the task.[^spinningup]

So instrument heavily, because "you can't tell it's broken if you can't see that it's breaking,"[^spinningup] and don't trust one passing setup: "sometimes things will work in one environment even when you have a breaking bug, so make sure to test in more than one environment."[^spinningup]

### Pursue anomalies; investigate confusion

> If you ever see a plot or a behaviour that just *seems weird*, chase right after it! Do not - do *not* - just 'hope it goes away'. Chasing anomalies is one of the most powerful ways to debug your system, because if you've noticed a problem without having had to go look for it, that means it's a *really big problem*. [...] It's really tempting to think that the cool extra functionality you were planning to write today [...] might just magically fix this anomalous behaviour. It won't. Give up on your plan for the day and chase the anomaly instead.[^jones]

> It was only by following that confusion and realising that taking the difference between frames zeroed out the background that gave the hint of a problem with normalization.[^rahtz]
>
> It seems important to really commit yourself to *always* investigate whenever you notice confusion.[^rahtz]

These are really important to flag to the user and investigate patiently

### Read what you actually wrote, not what you meant (gwern)

> you can't find typos in your own writing without a great deal of effort because you know what it's *supposed* to say; so copyediting advice runs like 'read it out loud' or 'print it out and read it' or 'wait a week' [...] or even 'read it upside down'. That's the sort of thing it takes to force you to read what you actually wrote, and not what you thought you wrote.[^gwern-unseeing]

This is why fresh eyes (or a fresh-eyes subagent) catches what you can't.

### Never accept the kludge (Patrick Kidger)

Kidger, on why research code is so reliably buggy:

> Academic software is almost always a poorly-maintained kludge of leaky abstractions, awful formatting, and bugs that don't cripple things only because some other bug stops them from doing so.[^kidger]

> This is a systemic professional failing. [...] the overwhelming majority of your time will be spent in front of a screen, staring at code. And yet most of you (yes, you) would not pass muster as a junior developer.[^kidger]

His fix is a posture, "never accept the kludge": messed up your git repo? Find the commands to fix it, "don't just delete it and clone from the remote."[^kidger] The instinct that refuses kludges is the same one that refuses `.detach()`-to-silence-autograd and `except: pass`.

### Loss curves are a red herring

> When someone's RL implementation isn't working, they *luuuuuurv* to copy-paste a screenshot of their loss curve to you. They do this because they know they want a pretty, exponentially-decaying loss curve, and they know what they have *isn't that*. The problem with using the loss curve as an indicator of correctness is somewhat that it's not reliable, but mostly because it doesn't localise errors. The shape of your loss curve says very little about where in your code you've messed up, and so says very little about what you need to change to get things working.[^jones]

(But sometimes they are not, they separate underfitting and over, gradient explosion vs vanishing, saturation vs not... and so on)

### Inspect the data first

> The first step to training a neural net is to not touch any neural net code at all and instead begin by thoroughly inspecting your data. [...] The outliers especially almost always uncover some bugs in data quality or preprocessing.[^karpathy-recipe]

Slavv's "37 reasons" list opens with the same anecdote (gradients flowing, loss falling, predictions all background) and puts "Verify that the input data is correct" and "Start with a really small dataset (2-20 samples). Overfit on it" at the top of its emergency checklist[^slavv].

Andrew Ng's error-analysis procedure is the same move applied after your first trained model: before investing a month in any fix, gather ~100 misclassified dev examples and count the failure categories in a spreadsheet.

> Manually examining 100 examples does not take long. Even if you take one minute per image, you'd be done in under two hours. These two hours could save you a month of wasted effort.[^ng-mly]

### Labels are often wrong (koaning)

Vincent Warmerdam:

> It turns out that bad labels are a *huge* problem in many popular benchmark datasets.[^koaning]

His cheap way to find them: train a deliberately high-bias model, then sort by where it disagrees with the label while assigning the correct class low confidence. The takeaway: "maybe we should spend [...] less time tuning parameters and instead spend it trying to get a more meaningful dataset."[^koaning]

### The tank story: your model learns the confound (gwern)

The canonical data-leakage parable:

> A cautionary tale in artificial intelligence tells about researchers training an neural network (NN) to detect tanks in photographs, succeeding, only to realize the photographs had been collected under specific conditions for tanks/non-tanks and the NN had learned something useless like time of day.[^gwern]

gwern traced versions back to 1992 and concluded it is "a classic 'urban legend'" with no solid source[^gwern]. The lesson holds twice over: a model will gladly learn a confound in how the data was collected instead of the task, and even your cautionary tales deserve a citation.

### Test-set contamination is insidious (Domingos)

Domingos' 2012 CACM paper set out to write down ML "folk knowledge" (the same project as this file):

> Doing well on the training set is easy (just memorize the examples). The most common mistake among machine learning beginners is to test on the training data and have the illusion of success.[^domingos]

> Contamination of your classifier by test data can occur in insidious ways, for example, if you use test data to tune parameters and do a lot of tuning. (Machine learning algorithms have lots of knobs, and success often comes from twiddling them a lot, so this is a real concern.)[^domingos]

Lones catalogs the concrete leak routes: scaling statistics computed on the full dataset before splitting, augmentation before splitting, look-ahead bias when cross-validating time series[^lones].

### Overfit one batch first

> Overfit a tiny subset of data. Lastly and most importantly, before training on the full dataset try to train on a tiny portion (e.g. 20 examples) of your data and make sure you can achieve zero cost. For this experiment it's also best to set regularization to zero [...]. Unless you pass this sanity check with a small dataset it is not worth proceeding to the full dataset.[^cs231n]

> Overfit a single batch of only a few examples (e.g. as little as two). [...] If they do not, there is a bug somewhere and we cannot continue to the next stage.[^karpathy-recipe]

And remove a variable while you're at it: "Always use a fixed random seed [...]. This removes a factor of variation and will help keep you sane."[^karpathy-recipe]

### The most common neural net mistakes (Karpathy)

The 2018 tweet thread that seeded the recipe post. Every item is a silent failure except 5:

> most common neural net mistakes: 1) you didn't try to overfit a single batch first. 2) you forgot to toggle train/eval mode for the net. 3) you forgot to .zero_grad() (in pytorch) before .backward(). 4) you passed softmaxed outputs to a loss that expects raw logits. ; others? :)[^karpathy-mistakes]

> oh: 5) you didn't use bias=False for your Linear/Conv2d layer when using BatchNorm, or conversely forget to include it for the output layer .This one won't make you silently fail, but they are spurious parameters[^karpathy-mistakes]

> 6) thinking view() and permute() are the same thing (& incorrectly using view)[^karpathy-mistakes]

Number 6 is the bug the backprop-to-input dependency check catches mechanically ([references/diagnostics.md](references/diagnostics.md)).

### Seed variance: you can't tell a bug from bad luck

> Look, there's variance in supervised learning too, but it's rarely this bad. If my supervised learning code failed to beat random chance 30% of the time, I'd have super high confidence there was a bug in data loading or training. If my reinforcement learning code does no better than random, I have no idea if it's a bug, if my hyperparameters are bad, or if I simply got unlucky.[^irpan]

> Instability to random seed is like a canary in a coal mine. If pure randomness is enough to lead to this much variance between runs, imagine how much an actual difference in the code could make.[^irpan]

Henderson confirmed it quantitatively: splitting 10 same-config runs (differing only in seed) into two groups of five produces "statistically different distributions just from varying random seeds."[^henderson] This is why one good run proves nothing ([references/sweeps.md](references/sweeps.md)).

### Normalize and scale everything

From the slides[^schulman]:
> - If observations have unknown range, standardize
> - Compute running estimate of mean and standard deviation
> - x' = clip((x - mu)/sigma, -10, 10)
> - Rescale the rewards, but don't shift mean, as that affects agent's will to live
> - Standardize prediction targets (e.g., value functions) the same way

Use running statistics over *all* data seen so far, not just recent data; using only recent data silently shifts the input distribution out from under the model.

### Tricks substitute for each other

On the slides[^schulman]:
> Always Be Ablating
> - Different tricks may substitute
> - Especially whitening

Many normalization/regularization tricks do roughly the same job (they improve conditioning), so stacking them adds complexity without proportional benefit.

### Changing anything changes everything (Sculley et al.)

Why ablation and one-change-at-a-time work, from Google's production-ML technical-debt paper:

> **Entanglement.** Machine learning systems mix signals together, entangling them and making isolation of improvements impossible. For instance, consider a system that uses features x1, ...xn in a model. If we change the input distribution of values in x1, the importance, weights, or use of the remaining n − 1 features may all change. [...] No inputs are ever really independent. We refer to this here as the CACE principle: Changing Anything Changes Everything. CACE applies not only to input signals, but also to hyper-parameters, learning settings, sampling methods, convergence thresholds, data selection, and essentially every other possible tweak.[^sculley]

This is also why "I changed the method and a hyperparameter and it got better" tells you nothing about the method.

### Exploration over exploitation (Google tuning playbook)

The Google Research tuning playbook opens by admitting there is "an astonishing amount of toil and guesswork" in getting deep nets to work; their counter is experiment-design discipline:

> Although one might think we would spend most of our time trying to maximize performance on the validation set, in practice we spend the majority of our time trying to gain insight into the problem, and comparatively little time greedily focused on the validation error. In other words, we spend most of our time on "exploration" and only a small amount on "exploitation".[^tuning-playbook]

Their experiment-design vocabulary is the reusable part: each round has *scientific* hyperparameters (the thing you're measuring), *nuisance* hyperparameters (must be re-tuned for the comparison to be fair), and *fixed* ones (caveats on your conclusions).

> The learning rate is a nuisance hyperparameter because we can only fairly compare models with different numbers of hidden layers if the learning rate is tuned separately for each number of layers (the optimal learning rate generally depends on the model architecture).[^tuning-playbook]

### Adam at 3e-4 for baselines (Karpathy)

> In the early stages of setting baselines I like to use Adam with a learning rate of 3e-4. In my experience Adam is much more forgiving to hyperparameters, including a bad learning rate.[^karpathy-recipe]

If you change the batch size, the learning rate has to move with it: linearly for SGD[^goyal], with an exponent between 0.5 and 1 for Adam[^mccandlish], and large-batch training without warmup can diverge in the first epoch and look like a code bug[^goyal].

## Modern transformers and LLM fine-tuning

Most of the sources above predate large transformers; these come from the people training and fine-tuning them.

### Tricks hide in reference code (lucidrains)

lucidrains' x-transformers is a catalogue of training tricks, each tied to its paper. The debugging-relevant one: when a transformer diverges, attention logits blowing up is a prime suspect, and the now-standard fix is QK normalization.

> We are nearing the point of wiping out a source of transformer training instability with one simple intervention.[^lucidrains]

Scaled-up recipes accumulate these one-line stability fixes in code long before they're written up.

### Modern LLM-pretraining gotchas (nanochat)

Karpathy's nanochat is one of the few public records of what scaling a transformer from scratch actually takes. Two gotchas:

> Do note that switching to the BOS dataloader changes the validation loss and makes all previous experiments not comparable in absolute value of the loss, because we have a lot fewer "confusing" tokens in the train/val batches. [...] Therefore, the loss appears lower but this is "fake" to some extent.[^nanochat]

> Original implementation clipped local gradients before sync. Since this codebase doesn't use DDP (gradient sync is in the optimizers), each rank was clipping based on its own local norm.[^nanochat]

He then removed clipping altogether: "Grad norm never exceeds 1.0 naturally, so clipping is always inactive", and it cost ~2% in time from the all-reduce.[^nanochat]

### When NaN hits, look at the frames before it (Stas Bekman)

Bekman wrote the `DebugUnderflowOverflow` tool during BLOOM-era large-model training. It keeps a rolling buffer of per-module abs-min/abs-max frames, so when inf/NaN is detected you see the run-up rather than only the crash site.

> As you can see it's the previous frames that we need to look into when the numbers start going into very large for fp16 numbers.[^bekman]

Corollary from the same docstring: validate your debugging instrumentation on a few cheap batches before betting an hours-long run on it.

### Loss spikes usually mean a bad data pocket (Stas Bekman)

Bekman's ML Engineering book has a gallery of real loss-curve pathologies from BLOOM and IDEFICS training, with the honest caveat that "very often we don't really understand why certain types of spikes happen" and pattern recognition is the realistic goal:

> In general there are 3 types of loss spikes: 1. Fast recovering spikes 2. Slow recovering spikes 3. Not fully recovering spikes
>
> The spikes usually happen because of a bad data pocket, either due to badly shuffled data or because it hasn't been cleaned from some garbage scraped from the websites.[^bekman-book]

And the post-mortem of the 104B model that diverged for months before BLOOM-176B succeeded:

> We think the 2 main obstacles were using fp16 and data that had a lot of garbage in it. For BLOOM-176B we switched to bf16, used much cleaner data and also added an embedding layer-norm and that made all the difference.[^bekman-book]

His recommended way to build this intuition: "The best learning is to read Publicly available training LLM/VLM logbooks because there you can see exactly what happened and how the problem has been overcome."[^bekman-book]

### Walk the pipeline in data order (HF course)

The HF LLM course debugging chapter is a worked narrative in the Karpathy-recipe lineage: a deliberately broken fine-tune, fixed step by step, checking each stage at the exact point it enters the model.

> The best way to debug an error that arises in `trainer.train()` is to manually go through this whole pipeline to see where things went awry. The error is then often very easy to solve.[^hfcourse]

> Hyperparameter tuning is always emphasized as being the hardest part of machine learning, but it's just the last step to help you gain a little bit on the metric. [...] don't launch into a time-consuming and costly hyperparameter search until you have something that beats the baseline you have on your dataset.[^hfcourse]

### Chat template and BOS handling must match across train and deploy (unsloth)

When a model trains fine but produces nonsense after export to llama.cpp or Ollama, the cause is usually not the weights:

> The most common cause of this error is using an **incorrect chat template**. It's essential to use the SAME chat template that was used when training the model in Unsloth and later when you run it in another framework, such as llama.cpp or Ollama. [...] It might also be because your inference engine adds an unnecessary "start of sequence" token (or the lack of thereof on the contrary) so ensure you check both hypotheses![^unsloth]

Their FAQ also explains the suspiciously perfect loss curve: when the loss sits at exactly zero, every label has probably been masked out and the model is learning nothing.

> All labels in your dataset are -100. Training losses will be all 0.[^unsloth]

### Shrink every axis at once, and clear the caches (axolotl)

Axolotl's debugging guide (the general tips trace to Hamel Husain) gives the minimal-repro recipe for training loops: one GPU, one process, a tiny model, tiny data, a single step, no eval. It also warns that caching can quietly undo your experiment, because the run you think you changed may be replaying artifacts produced before the change:

> **Eliminate concurrency**: Restrict the number of processes to 1 for both training and data preprocessing[^axolotl]

> Axolotl caches certain steps and so does the underlying HuggingFace trainer. You may want to clear some of these caches when debugging.[^axolotl]

Their training-stability page adds the masking check ("inspect tokenized samples to confirm only the target tokens are trainable") and, bluntly: "Debugging a failed run without metrics is guesswork."[^axolotl-stability]

## The eight common mistakes

On 2026-08-25 I named the eight failure modes I see most often, from AI agents and from myself, and
SKILL.md turns each one into an exercise. The quotes below were mined from the evidence cache in
[docs/evidence/](docs/evidence/) to back them. Coverage is uneven and worth knowing about: mode 6
has only three quotes and none of them says "read the log" in those words, and no source here
argues against similarity probes by name, so the mode 7 quotes attack the general substitution
instead.

### 1. Overconfidence, a diagnosis stated as fact

From William Falcon's attendee notes on Schulman's talk, so a secondary source rather than
Schulman's own text[^deeprlhacks]:

> 4. Think your algorithm is working but you're actually seeing random noise.   
>     - Example: Graph of 7 tasks with 3 algorithms and looks like 1 algorithm might be doing best on all problems, but turns out they're all the same algorithm with DIFFERENT random seeds.   

Nanda on why no internal warning fires:

> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research.[^nanda-mindsets]

Victor Sanh names the state in which a confident report is worthless:

> **The challenge lies in the fact that you can make these mistakes, train a model without it ever crashing, and still get a decent performance…**[^sanh]

Seed noise alone can clear a significance bar, from a different section of the Google playbook:

> -   It is all well and good to make comparisons of validation error rates
>     estimated on a finite validation set using fastidious statistical tests, but
>     often the trial variance alone can produce statistically significant
>     differences between two different trained models that use the same
>     hyperparameter settings.[^tuning-playbook]

The one question that turns "am I overconfident" into something answerable:

> **How reliable is my experiment?** Ask yourself: "How surprised would I be if it turned out to be complete bullshit due to a bug, error, noise, misunderstanding, etc.?" Investigate the most uncertain bits[^nanda-papers]

And from an unpublished Nanda draft quoted in [references/research_taste.md](references/research_taste.md), so
weaker provenance than his published posts:

> Insufficient Skepticism: Missing simple alternative explanations, methodological flaws, or bugs. Explicitly list alternatives. Get others (especially mentors) to red team your plans before you run them. Actively try to break your hypothesis. Ask "What observation would make me abandon this?"[^nanda-taste]

### 2. Quitting after one change, calling the negative real

Steinhardt gives the error a number, and SKILL.md builds an exercise on this one:

> **Trying an experiment and seeing it fail gives little information by itself.** When an experiment fails, it is tempting to conclude "I tried X and it didn't work". However, if X is a high-level conceptual approach, then a more correct conclusion is "I tried an implementation comprising 0.1% of the possible implementations of X, and observed that that particular implementation did not work".[^steinhardt]

> When ruling out ideas, it is important to hold oneself to a high standard. "This doesn't seem like it will work" or "I feel less motivated after trying a few things along this line that didn't work" are _not_ ruling out an idea.[^steinhardt]

The textbook states the confusion as the default condition, not an edge case:

> When a machine learning system performs poorly, it is usually difficult to tell whether the poor performance is intrinsic to the algorithm itself or whether there is a bug in the implementation of the algorithm. Machine learning systems are difficult to debug for various reasons.[^goodfellow]

Irpan, reproducing a paper with its first author sitting nearby, another quote SKILL.md turns into
an exercise:

> It ended up taking me 6 weeks to reproduce results, thanks to several software
> bugs. The question is, why did it take so long to find these bugs?[^irpan]

Karpathy's nanochat log is the model of how to write a negative honestly, recording the effort spent
and keeping the idea alive:

> **Result:** This was not an out-of-the-box win for nanochat even with a mild attempt over a few hours at a bit of tuning and debugging. The idea itself is intuitively appealing. Might come back around later to try harder later.[^nanochat]

Miller's recommendations, where item 5 is the check on the whole mode and item 4 is the pairing rule:

> Our specific recommendations to researchers include: 1. Computing standard errors of the mean using the Central Limit Theorem 2. When questions are drawn in related groups, computing clustered standard errors 3. Reducing variance by resampling answers and by analyzing next-token probabilities 4. When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics 5. Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest[^miller]

Rahtz writes the one-change-then-declare loop out as a transcript, priced in a week of wall clock:

> If you keep that strategy when each run takes 10 hours, though, you can easily
> waste a *lot* of time. Last run didn’t work? OK, I think it’s this thing. Let’s
> set off another run to check. Coming back the next morning: still doesn’t work?
> OK, maybe it’s this other thing. Let’s set off another run. A week later, you
> still haven’t solved the problem.[^rahtz]

### 3. Anchoring on the first idea

Rahtz explains why anchoring feels correct, and when it actually is:

> than forming hypotheses. Why spend 15 minutes carefully considering everything
> that could be causing what you see when you can check the first idea that jumps
> to mind in a fraction of that (and gather more evidence in the process)? To put
> it another way: if you have rapid feedback, you can narrow down the hypothesis
> space a lot faster by trying things than thinking carefully.[^rahtz]

Nanda attacks anchoring at the root, and also attacks the fix:

> The standard hypothesis testing framework can be misleading here, because it has an implicit frame of being able to list all the hypotheses. But actually, most of your probability mass should normally be on “something I haven’t thought of yet”[^nanda-mindsets]

> If trying to explain something mysterious, novice researchers often neglect simple, dumb hypotheses like “maybe MLP0 is incredibly important on *every* input, and there’s nothing special going on with my prompt”[^nanda]

Steinhardt, on hypotheses 2 and 3 turning out to be hypothesis 1 wearing a hat:

> Importantly, it is often not obvious that multiple approaches to a problem all have the same issue. In the past, I have spent months trying different approaches to a problem before finally stepping back and realizing that they were all failing for the same reason. Moreover, I had all the data necessary to make this realization a couple weeks in but had failed to do so.[^steinhardt]

Josh Tobin's symptom table, where every symptom has two or three candidates and only one is a
learning rate:

> * **Error goes up**: Commonly, this is due to a flip sign somewhere in
>   the loss function/gradient.
> * **Error explodes**: This is usually a numerical issue but can also
>   be caused by a high learning rate.
> * **Error oscillates**: You can lower the learning rate and inspect
>   the data for shuffled labels or incorrect data augmentation.
> * **Error plateaus**: You can increase the learning rate and get rid
>   of regulation. Then you can inspect the loss function and the data
>   pipeline for correctness.[^fsdl]

And the explicit step, again from the unpublished draft. Note it asks for the simplest explanations,
not more of the same kind as hypothesis 1:

> Actively Seek Alternatives: Explicitly brainstorm other ways your observations could be explained. What are the simplest explanations? What known circuits or phenomena could be involved? What would a strong skeptic argue?[^nanda-taste]

### 4. Obsession with the legible hyperparameters

Achiam gives both the ordering agents invert and the reason for it:

> **If it doesn’t work, assume there’s a bug.** Spend a lot of effort searching for bugs before you resort to tweaking hyperparameters: usually it’s a bug. Bad hyperparameters can significantly degrade RL performance, but if you’re using hyperparameters similar to the ones in papers and standard implementations, those will probably not be the issue.[^spinningup]

Karpathy's five worked examples of silent failure, where the legible hyperparameters arrive last, in
one clause:

> For example, perhaps you forgot to flip your labels when you left-right flipped the image during data augmentation. Your net can still (shockingly) work pretty well because your network can internally learn to detect flipped images and then it left-right flips its predictions. Or maybe your autoregressive model accidentally takes the thing it’s trying to predict as an input due to an off-by-one bug. Or you tried to clip your gradients but instead clipped the loss, causing the outlier examples to be ignored during training. Or you initialized your weights from a pretrained checkpoint but didn’t use the original mean. Or you just screwed up the settings for regularization strengths, learning rate, its decay rate, model size, etc.[^karpathy-recipe]

Sanh treats a weird optimal hyperparameter as a symptom to explain, not a setting to keep:

> Most importantly, there is no point of launching 1000 runs with different hyperparameters (or architecture tweaks like activation functions): **compare a couple of runs with different hyperparameters to get an idea of which hyperparameters have the highest impact** but in general, it is delusional to expect to get your biggest jumps of performance by simply tuning a few values. For instance, if your best performing model is trained with a learning rate of 4e2, there is probably something more fundamental happening inside your neural network and you want to identify and understand this behavior so that you can re-use this knowledge outside of your current specific context.[^sanh]

Daniel Ziegler's self-study, reported second-hand by an 80,000 Hours career guide:

> Once the algorithm was partially working, they would attain higher performance by looking for remaining bugs, both by reviewing the code carefully, and by collecting metrics such as average policy entropy to perform sanity-checks, rather than just tune hyperparameters.[^olsson]

Sweeping the obvious hyperparameters is brute-force search wearing a lab coat:

> Third, and perhaps most important for building skill,[[1]](https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming#fn289bs9hi65b)you must **notice** when you're going into brute-force search mode, and then **take action** by investing time in understanding the underlying system, until both the problem and solution make sense.[^ulisse]

Last, a specimen rather than advice. An anonymous reddit self-report from a self-described
non-expert, nine hyperparameters turned and the agent still does not learn. In the same thread he
reports his two real bugs on that environment were a terminal-flag masking error and a shape
broadcast, neither of which any of these can reach[^reddit-rl]:

> Things I've tried (but maybe not systematically enough):
> 
> * Different initial LRs
> * Different optimizers
> * Different number of hidden layers/units
> * Shared pi/V NN body (with diff output layers) vs not
> * Changing amount of entropy
> * Adding correlated noise
> * Using TD residual instead of MC version
> * Clipping the gradient
> * Different gamma values

### 5. Not reading the data

The textbook naming the exact drift, and why the scalar cannot police itself:

> Visualize the model in action: When training a model to detect objects in images, view some images with the detections proposed by the model displayed superimposed on the image. When training a generative model of speech, listen to some of the speech samples it produces. This may seem obvious, but it is easy to fall into the practice of looking only at quantitative performance measurements like accuracy or log-likelihood. Directly observing the machine learning model performing its task will help to determine whether the quantitative performance numbers it achieves seem reasonable. Evaluation bugs can be some of the most devastating bugs because they can mislead you into believing your system is performing well when it is not.[^goodfellow]

Henderson et al. on a healthy-looking curve produced by a policy that has learned nothing anyone
wanted (the "demon-strated" break is an OCR artifact in the cached copy):

> By reaching a local optimum, learning curves can indicate successful optimization of the policy over time, when in reality the returns achieved are not qualitatively representative of learning the desired behaviour, as demon-strated in video replays of the learned policy 5. Therefore, it is important to show not only returns but demonstrations of the learned policy in action.[^henderson]

"Read the data" as a pass/fail test that takes a minute, again from the DeepRLHacks attendee
notes[^deeprlhacks]:

> 2. Make sure observations usable:
>     - See if YOU could control the system by using the same observations you give the agent.   
>       - Example: Look at preprocessed images yourself to make sure you don't remove necessary details or hinder the algorithm in a certain way.

For LLM work, the data you have to read is the tokenized data:

> Pro-tip: when you work with language, have a serious **look at the outputs of the tokenizers**. I can’t count the number of lost hours I spent trying to reproduce results (and sometimes my own old results) because something went wrong with the tokenization.[^sanh]

Ng names the motivational failure rather than the procedural one:

> Error analysis can often help you figure out how promising different directions are. I’ve seen many engineers reluctant to carry out error analysis. It often feels more exciting to just jump in and implement some idea, rather than question if the idea is worth the time investment. This is a common mistake: It might result in your team spending a month only to realize afterward that it resulted in little benefit.[^ng-mly]

And reading one process's data is not reading the data when eight processes disagree:

> ⚠️ If you are doing distributed training, print samples of your dataset in each process and triple-check that you get the same thing. One common bug is to have some source of randomness in the data creation that makes each process have a different version of the dataset.[^hfcourse]

### 6. Not reading the log

The closest thing in the cache to a hard rule that you read the run before you report its number,
from a team with every excuse to just read the number:

> -   Although in many cases the primary objective of our experiments only
>     requires considering the validation error of each trial, we must be careful
>     when reducing each trial to a single number because it can hide important
>     details about what’s going on below the surface.
> -   For every study, we always look at the **training curves** (training error
>     and validation error plotted versus training step over the duration of
>     training) of at least the best few trials.[^tuning-playbook]

A price tag on skipping a boring number, from Rahtz:

> (I missed
> a multithreading bug for several months by ignoring a small but mysterious
> decay in frames per second.)[^rahtz]

Bekman, where the visible symptom was an artifact of the resume and the data sampler, so every
hypothesis about the optimizer or the precision would have been confidently wrong:

> There was no real spike in the two earlier runs. The loss never went up in the first place. In both resumes it was under-reporting loss due to an exactly repeated data and then it reached data it hasn't seen before and started reporting correctly. In other words it was overfitting and reporting a false loss.[^bekman-book]

### 7. A cheap indirect probe instead of running the real thing

A published case where a clever mechanism turned out to be norm damage, and the cheap real test
that the indirect story never ran:

> **Do ablations on your fancy method**: It's easy for people to have a fancy method with lots of moving parts, when many actually are unnecessary. You should always try removing one part and see if the method breaks. Do this for each part.
>     *   For example, the [original unlearning method](https://arxiv.org/abs/2403.03218v1) in the [RMU paper](https://arxiv.org/abs/2403.03218) claimed it was based on finding a meaningful steering vector, until follow-up work found that it was just about adding a vector with really high norm that broke the model, and a random vector performed just as well.[^nanda]

Ng's shortest statement of build-it-and-run-it, from CS229 slides, where the line breaks are the
PDF's. His next slide caveats that this is worse advice when the goal is to invent new algorithms.

> The only way to find out what needs work is to implement something quickly,
>
> and find out what parts break.[^cs229]

A convenient proxy metric silently deleting the one object the task was about:

> Figure 15.5: An autoencoder trained with mean squared error for a robotics task has failed to reconstruct a ping pong ball. The existence of the ping pong ball and all its spatial coordinates are important underlying causal factors that generate the image and are relevant to the robotics task. Unfortunately, the autoencoder has limited capacity, and the training with mean squared error did not identify the ping pong ball as being salient enough to encode.[^goodfellow-ch15]

What a scalar proxy costs, which is a different point from reading your data for quality:

> One of the key drivers of progress in mech interp is an openness to qualitative research: summary statistics lose a ton of information. What can we learn by actually looking deeply into what's happening?[^nanda]

When the metric will not move, run the real objective on known inputs:

> 1. **Test reward function standalone**: Run it outside training with known inputs to verify it returns nonzero values.[^axolotl-stability]

### 8. An arbitrary threshold set before you know what is fair

The textbook killing the invented threshold from first principles, and another quote SKILL.md builds
an exercise on:

> In most cases, we do not know a priori what the intended behavior of the algorithm is. In fact, the entire point of using machine learning is that it will discover useful behavior that we were not able to specify ourselves. If we train a neural network on a new classification task and it achieves 5 percent test error, we have no straightforward way of knowing if this is the expected behavior or suboptimal behavior.[^goodfellow]

Nanda states the default and names the fix as a baseline rather than a chosen cutoff. This is from an
unpublished draft, the passage never made the published post, and SKILL.md uses it too:

> A valuable intuition to have in mind is that, by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! Baselines are one way to get context to compare against.[^nanda-draft]

A worked case where a fixed cutoff is meaningless until you know the scale of the quantity. The fix
is a scale-free metric, not an argument about where the cutoff sits. The typo is in the source.

> You might be temped to keep track of the difference \(\mid f’\_a - f’\_n \mid \) or its square and define the gradient check as failed if that difference is above a threshold. However, this is problematic. For example, consider the case where their difference is 1e-4. This seems like a very appropriate difference if the two gradients are about 1.0, so we’d consider the two gradients to match. But if the gradients were both on order of 1e-5 or lower, then we’d consider 1e-4 to be a huge difference and likely a failure.[^cs231n]

Four questions Sanh asks before any number can be called good or bad. The last one, what you cannot
conclude from a perfect score, is the specific antidote:

> *   How would a random predictor perform (especially in classification problems)? Dataset can be unbalanced…
> *   What would the loss look like for a random predictor?
> *   What is (are) the best metric(s) to measure progress on my task?
> *   What are the limits of this metric? If it’s perfect, what can I conclude? What can’t I conclude?[^sanh]

The constructive alternative, compute what random gets and treat any distance from it as a bug
report until shown otherwise:

> If the loss/metric you get on your initial model is very different from the loss/metric you would expect for random predictions, double-check the way your loss or metric is computed, as there is probably a bug there. If you are using several losses that you add at the end, make sure they are of the same scale.[^hfcourse]

The legitimate form of a numeric gate, discovered by reproducing a known-good reference rather than
chosen in advance:

> 5.   **Rule of thumb: 400 episodic return in breakout**: Check if your PPO could obtain 400 episodic return in breakout. We have found this to be a practical rule of thumb to determine the fidelity of online PPO implementations in GitHub. Often we found PPO repositories not able to do this, and we know they probably do not match all implementation details of `openai/baselines`’ PPO.[^ppo37]

And a floor under any target, because a threshold set tighter than the label noise in your
validation set is measuring overfitting to errors:

> The issue here isn't just that we might have bad labels in our training set, the issue is that it appears in the validation set. If a machine learning model can become state of the art by squeezing another 0.5% out of a validation set one has to wonder. Are we really making a better model? Or are we creating a model that is better able to overfit on the bad labels?[^koaning]

## Links and further reading

Start here rather than treating the bibliography as flat:

- **Beginner / broad checklist:** Lones, ["How to avoid machine learning pitfalls"](https://arxiv.org/pdf/2108.02497), with its full do/don't list extracted in [references/checklist.md](references/checklist.md).
- **Debugging a neural net:** Karpathy, ["A Recipe for Training Neural Networks"](https://karpathy.github.io/2019/04/25/recipe/).
- **Designing tuning experiments:** Google, [Deep Learning Tuning Playbook](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook).
- **Transformer and LLM runs:** [references/transformers.md](references/transformers.md), then the HF, Axolotl, Unsloth, nanochat, and Bekman sources below.

Folklore sources (the quotes above trace to these):

[^jones]: Andy Jones, "Debugging RL, Without the Agonizing Pain" — https://andyljones.com/posts/rl-debugging.html ([cache](docs/evidence/andyljones_rl_debugging.md): anomalies, write-from-scratch, assume-bug, raise-threshold, loss-curve)
[^rahtz]: Matthew Rahtz (Amid Fish), "Lessons Learned Reproducing a Deep RL Paper" — http://amid.fish/reproducing-deep-rl ([cache](docs/evidence/amid_fish_reproducing_deep_rl.md): frame-diff confusion, investigate-confusion, think-more, don't-implement-RL-yourself)
[^karpathy-recipe]: Andrej Karpathy, "A Recipe for Training Neural Networks" (2019) — https://karpathy.github.io/2019/04/25/recipe/ ([cache](docs/evidence/karpathy_recipe_training_nn_2019.md): inspect-data, fixed-seed, overfit-one-batch, Adam-3e-4; note: this is an abridged note with its own "..." elisions)
[^karpathy-mistakes]: Andrej Karpathy, "most common neural net mistakes" tweet thread, 1 Jul 2018 — https://x.com/karpathy/status/1013244313327681536 ([cache](docs/evidence/karpathy_common_mistakes_tweet_2018.md): tweets 1-3 verbatim, cross-checked against threadreaderapp; x.com itself blocks fetching)
[^sculley]: Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf ([cache](docs/evidence/sculley_2015_hidden_technical_debt.md): abstract, CACE/entanglement, ensemble caveat)
[^schulman]: John Schulman, "Nuts and Bolts of Deep RL Research" slides — http://joschu.net/docs/nuts-and-bolts.pdf ([cache](docs/evidence/joschu_nuts_and_bolts.md): Always-Be-Ablating, standardize-observations; clean slide transcript)
[^henderson]: Henderson et al., "Deep Reinforcement Learning that Matters" (AAAI 2018) — https://arxiv.org/pdf/1709.06560 ([cache](docs/evidence/henderson_2018_deep_rl_matters.md): seeds-create-different-distributions, implementation-differences)
[^irpan]: Alex Irpan, "Deep Reinforcement Learning Doesn't Work Yet" (2018) — https://www.alexirpan.com/2018/02/14/rl-hard.html ([cache](docs/evidence/alexirpan_rl_hard.md): variance-bug-or-unlucky, seed-canary)
[^cs231n]: Stanford CS231n, "Neural Networks Part 3" — https://cs231n.github.io/neural-networks-3/ ([cache](docs/evidence/cs231n_neural_networks_3.md): overfit-tiny-subset)
[^slavv]: Slav Ivanov, "37 Reasons why your Neural Network is not working" (2017) — https://blog.slavv.com/37-reasons-why-your-neural-network-is-not-working-4020854bd607 ([cache](docs/evidence/slavv_37_reasons_nn.md): opening anecdote, emergency checklist)
[^goodfellow]: Goodfellow, Bengio, Courville, *Deep Learning*, ch. 11 "Practical Methodology" — https://www.deeplearningbook.org/ ([cache](docs/evidence/goodfellow_ch11_practical_methodology.md): one-part-broken-others-adapt, weights-adapt-to-compensate)
[^mccandlish]: McCandlish, Kaplan et al., "An Empirical Model of Large-Batch Training" (2018) — https://arxiv.org/pdf/1812.06162 ([cache](docs/evidence/mccandlish_2018_large_batch.md))
[^goyal]: Goyal et al., "Accurate, Large Minibatch SGD" (2017) — https://arxiv.org/pdf/1706.02677
[^lucidrains]: Phil Wang (lucidrains), x-transformers README — https://github.com/lucidrains/x-transformers ([cache](docs/evidence/lucidrains_x_transformers_readme.md): post-embedding LayerNorm / BLOOM+YaLM, attention-overflow / cosine-sim norm, autoregressive validation, "wiping out a source of instability" / QK RMSNorm)
[^koaning]: Vincent D. Warmerdam (koaning), "Bad Labels" (2021) — https://koaning.io/posts/labels/ ([cache](docs/evidence/koaning_bad_labels.md): bad-labels-huge-problem, confidence-sort trick, spend-less-time-tuning)
[^nanochat]: Karpathy, [nanochat experiment log](https://github.com/karpathy/nanochat/blob/master/dev/LOG.md) ([cache](docs/evidence/karpathy_nanochat_experiments.md))
[^kidger]: Patrick Kidger, "Just Know Stuff" (2023) — https://kidger.site/thoughts/just-know-stuff/ ([cache](docs/evidence/kidger_just_know_stuff.md): kludge-definition, junior-developer, never-accept-the-kludge, don't-delete-and-clone)
[^gwern]: Gwern Branwen, "The Neural Net Tank Legend" — https://gwern.net/tank ([cache](docs/evidence/gwern_tank.md): cautionary tale, urban-legend conclusion)
[^spinningup]: Joshua Achiam, "Spinning Up as a Deep RL Researcher" (OpenAI, 2018) — https://spinningup.openai.com/en/latest/spinningup/spinningup.html ([cache](docs/evidence/spinningup_researcher.md): fails-silently, test-more-than-one-env, measure-everything)
[^nanda]: Neel Nanda, "How to Become a Mechanistic Interpretability Researcher" — https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher ([cache](docs/evidence/nanda_how_to_mech_interp.md): research-is-false, excitement-is-bullshit, read-your-data)
[^gwern-unseeing]: Gwern Branwen, "Unseeing" — https://gwern.net/unseeing ([cache](docs/evidence/gwern_unseeing.md): read-what-you-wrote, single-anomaly)
[^ulisse]: Ulisse Mini, "How to get good at programming" — https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming ([cache](docs/evidence/ulisse_how_to_get_good_at_programming.md): track-internal-state, brute-force-search, leaky-abstractions)
[^wentworth]: John Wentworth, "Gears-Level Models are Capital Investments" — https://www.lesswrong.com/posts/nEBbw2Bc2CnN2RMxy/gears-level-models-are-capital-investments ([cache](docs/evidence/wentworth_gears_level_models.md): gears-dividends, valley-of-bad-theory)
[^hfcourse]: Sylvain Gugger et al., HF LLM Course ch. 8.4, "Debugging the training pipeline" — https://huggingface.co/learn/llm-course/chapter8/4 ([cache](docs/evidence/hf_llm_course_ch8_4_debugging_pipeline.md): walk-the-pipeline, overfit-one-batch, no-tuning-before-baseline)
[^bekman]: Stas Bekman, `DebugUnderflowOverflow` docstring, transformers `debug_utils.py` (2021) — https://github.com/huggingface/transformers/blob/main/src/transformers/debug_utils.py ([cache](docs/evidence/bekman_debug_utils_transformers.md): purpose, detection-and-frame-buffer, previous-frames)
[^unsloth]: Unsloth (Daniel & Michael Han-Chen), "Troubleshooting & FAQs" — https://docs.unsloth.ai/basics/troubleshooting-and-faqs ([cache](docs/evidence/unsloth_troubleshooting_faqs.md): template-mismatch + BOS, shuffle-eval, all-labels–100-loss-0)
[^axolotl]: Axolotl, "Debugging" (general tips: Hamel Husain) — https://docs.axolotl.ai/docs/debugging.html ([cache](docs/evidence/axolotl_debugging.md): simplify, one-process, small-model + fast-iteration, caches)
[^axolotl-stability]: Axolotl, "Training Stability" — https://docs.axolotl.ai/docs/training_stability.html ([cache](docs/evidence/axolotl_training_stability.md): metrics-from-the-start, inspect-tokenized-masking, reward-fn-standalone)
[^ng-mly]: Andrew Ng, *Machine Learning Yearning* (2018 draft), ch. 13-19 on error analysis — https://github.com/ajaymache/machine-learning-yearning ([cache](docs/evidence/ng_ml_yearning_error_analysis.md): build-first-system, 100-examples procedure, Eyeball/Blackbox dev sets)
[^tuning-playbook]: Godbole, Dahl, Gilmer, Shallue, Nado, "Deep Learning Tuning Playbook" (Google Research / Google Developers, 2023; Google Developers page last updated 2025-08-25) — https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook ([cache](docs/evidence/google_tuning_playbook.md): exploration-over-exploitation, scientific/nuisance/fixed, incremental-tuning)
[^domingos]: Pedro Domingos, "A Few Useful Things to Know About Machine Learning" (CACM, Oct 2012) — https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf ([cache](docs/evidence/domingos_2012_few_useful_things.md): test-on-train illusion, insidious-contamination, overfitting-bugbear, features-are-key)
[^bekman-book]: Stas Bekman, *Machine Learning Engineering Open Book*, "Understanding Training Loss Patterns" + "Instabilities" — https://github.com/stas00/ml-engineering ([cache](docs/evidence/bekman_ml_engineering_instabilities.md): heartbeat, 104B post-mortem, spike types + bad-data-pocket, init-std, PaLM batch-skipping, logbooks)
[^deeprlhacks]: William Falcon, "DeepRLHacks", attendee notes on Schulman's "Nuts and Bolts of Deep RL Research" -- https://github.com/williamFalcon/DeepRLHacks ([cache](docs/evidence/williamfalcon_deeprl_hacks.md): random-noise-not-signal, observations-usable). Secondary source; the primary slide deck is `[^schulman]`.
[^nanda-mindsets]: Neel Nanda, "My Research Process: Key Mindsets" -- https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL ([cache](docs/evidence/nanda_research_process_key_mindsets.md): insufficient-skepticism-feels-like-research, mass-on-unlisted-hypotheses)
[^nanda-papers]: Neel Nanda, "Highly Opinionated Advice on How to Write ML Papers" -- https://www.lesswrong.com/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers ([cache](docs/evidence/nanda_highly_opinionated_ml_paper_writing.md): how-reliable-is-my-experiment)
[^nanda-taste]: Neel Nanda, "My Model of the Research Process", unpublished shared draft, as quoted in [references/research_taste.md](references/research_taste.md) (insufficient-skepticism, actively-seek-alternatives). Draft quality, weaker provenance than the published posts.
[^nanda-draft]: Neel Nanda, "My Model of the Research Process", unpublished shared draft -- https://docs.google.com/document/d/1YMkeMrhqsWxZcNDD9CIUWEK_DAOegeufnbc79U2hycg/edit ([cache](docs/evidence/nanda_research_process_shared_draft.md): all-numbers-are-meaningless). This passage never made it into the published post.
[^sanh]: Victor Sanh, "Simple considerations for simple people building fancy neural networks" (HF, 2021) -- https://huggingface.co/blog/simple-considerations ([cache](docs/evidence/sanh_simple_considerations_hf_2021.md): decent-performance-without-crashing, read-the-tokenizer-output, 4e2-is-a-symptom, pre-training questions)
[^steinhardt]: Jacob Steinhardt, "Research as a Stochastic Decision Process" -- https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html ([cache](docs/evidence/steinhardt_research_stochastic_decision_process.md): 0.1%-of-implementations, high-standard-for-ruling-out, months-of-approaches-one-cause)
[^miller]: Evan Miller (Anthropic), "Adding Error Bars to Evals" (2024) -- https://arxiv.org/pdf/2411.00640 ([cache](docs/evidence/miller_2024_error_bars_evals.md): five recommendations, question-level pairing, power analysis). arXiv preprint, not peer reviewed.
[^fsdl]: Josh Tobin, Full Stack Deep Learning Spring 2021 lecture 7, "Troubleshooting Deep Neural Networks", notes by James Le and Vishnu Rachakonda -- https://fullstackdeeplearning.com/spring2021/lecture-7/ ([cache](docs/evidence/fsdl_spring2021_lecture7.md): error up/explodes/oscillates/plateaus table)
[^olsson]: Catherine Olsson and the 80,000 Hours team, "ML Engineering for AI Safety and Robustness" -- https://80000hours.org/articles/ml-engineering-career-transition-guide/ ([cache](docs/evidence/olsson_80000hours_ml_engineering_ai_safety.md): bug-hunting-with-diagnostics-over-tuning). Reports Daniel Ziegler's self-study second-hand.
[^reddit-rl]: u/GrundleMoof, "How to more intelligently debug RL roadblocks?" -- https://old.reddit.com/r/reinforcementlearning/comments/bzg3l2/ ([cache](docs/evidence/reddit_rl_roadblocks_bzg3l2.md): nine-knobs list, terminal-flag and broadcast bugs in the replies). Anonymous self-report from a self-described non-expert; quoted as a specimen of the failure mode, not as authority.
[^cs229]: Andrew Ng, "Advice for Applying Machine Learning" (CS229 slides) -- https://cs229.stanford.edu/materials/ML-advice.pdf ([cache](docs/evidence/cs229_ml_advice.md): implement-quickly-find-what-breaks, and his own caveat for algorithm invention)
[^goodfellow-ch15]: Goodfellow, Bengio, Courville, *Deep Learning*, ch. 15 "Representation Learning" -- https://www.deeplearningbook.org/contents/representation.html ([cache](docs/evidence/goodfellow_ch15_representation_learning.md): Figure 15.5 ping pong ball / MSE salience)
[^ppo37]: Huang, Dossa, Raffin, Kanervisto, Wang, "The 37 Implementation Details of Proximal Policy Optimization" (ICLR Blog Track, 2022) -- https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/ ([cache](docs/evidence/cleanrl_37_ppo_details.md): 400-return-in-breakout rule of thumb)
[^lones]: Michael A. Lones, "How to avoid machine learning pitfalls" (2021, updated annually) — https://arxiv.org/pdf/2108.02497 ([cache](docs/evidence/lones_2021_ml_pitfalls.md): full do/don't TOC, leakage, look-ahead bias). Aimed at beginners but the most exhaustive checklist here: 36 do/don'ts across data prep, training, evaluation, comparison, and reporting.

For modern transformer pretraining specifically (most sources above predate it), see [Karpathy's recipe](https://karpathy.github.io/2019/04/25/recipe/) and the [nanochat experiment log](https://github.com/karpathy/nanochat/blob/master/dev/LOG.md) (320+ empirical HP sweeps for a GPT-2-scale run). For LLM-as-judge eval debugging workflow more broadly, Hamel Husain's ["Your AI Product Needs Evals"](https://hamel.dev/blog/posts/evals/) covers the error-analysis-first approach for LLM products. Most multi-source claims trace to quotes in [docs/ml_debug_folklore.argdown](docs/ml_debug_folklore.argdown) (vargdown); the full evidence set is in [docs/evidence/](docs/evidence/).

## Does it help?

Measured on [ml-bench](https://github.com/wassname/ml-bench): 12 hard machine learning research
problems from my own work, none of them in any training set, each answer graded against my own
answer by a panel of five LLM judges. A score of 1.00 means the model matched me. The test gives the
model this SKILL.md and nothing else, so the only change is the document.

No measurable gain, from three answers per question in each arm:

| deepseek-v4-flash-0731, 12 questions | bare | with SKILL.md |
| --- | --- | --- |
| mean score | +0.643 | +0.667 |
| the three runs | +0.608, +0.648, +0.674 | +0.746, +0.641, +0.614 |

The difference is +0.023 with a standard error of 0.044, so it is not distinguishable from zero.
Pairing by question rather than by run gives the same +0.023 with a standard error of 0.031, t of
0.76. The runs themselves scatter by more than the difference between the two columns.

An earlier version of this section reported +0.135, or 59% of the distance to gpt-5.6-sol. That was
one run of each arm, and it happens to be the first run in each column above. It did not survive the
other two.

Two other readings. With SKILL.md the model writes 31% more text for the same score, so any
verbosity bias in the judges makes the true effect smaller than +0.023, not larger. And only 1 answer
in 36 uses the document's own vocabulary, so the document is in the context without changing much of
what the model writes. The header does tell it not to quote the document back.

Caveats: one model, three answers per question, one judge panel, at bench version v96. The result is
that this document did not help this model on these questions. It is not evidence about a stronger
model, a longer task, or an agent that can run code.

### Which part of the document does the work?

A later round swapped the document for cut-down versions of it, on three of the twelve questions,
four answers per question, grok-4.6 at high reasoning effort. Both controls are documents that
contain none of this material: `inert doc` gives no instruction at all, and `be thorough` is five
lines telling the model to work the problem in full and show its work.

*One row is one document loaded in place of SKILL.md. Controls are italic. `struggling` counts
answers that narrate fetching evidence in a bench that offers no tools, and `mean clean` is the
mean with those dropped.*

| document | size | mean↑ | mean clean↑ | struggling↓ | version |
| --- | ---: | ---: | ---: | ---: | --- |
| *be thorough (control)* | 636 B | *+0.66* | *+0.66* | 0/12 | control |
| be diligent first, named exercises | 29 K | +0.56 | +0.56 | 0/12 | [`3a58c54`](https://github.com/wassname/ml-debug/blob/3a58c54/SKILL.md) |
| exercises, almost no quotes | 19 K | +0.53 | +0.53 | 0/10 | ablation |
| *inert doc (control)* | 771 B | *+0.53* | *+0.53* | 0/12 | control |
| *bare, no document* | 0 | *+0.44* | *+0.44* | 0/12 | -- |
| read the data, and give hypotheses | 3.0 K | +0.44 | +0.44 | 0/11 | ablation |
| quotes and exercises | 26 K | +0.35 | +0.47 | 3/12 | [`efcac5c`](https://github.com/wassname/ml-debug/blob/efcac5c/SKILL.md) |
| quotes only, no exercises | 40 K | +0.13 | -- | 10/12 | [`d5d725e`](https://github.com/wassname/ml-debug/blob/d5d725e/SKILL.md) |

<sub>Table: 0.0 is the obvious answer each question rejects and 1.0 is my own answer, so a
negative row is worse than the answer the question was built to reject. Judge `gpt-5.6-terra`,
bench version v102. The ablation rows were built for the bench and were never committed here; each
one is kept verbatim in the bench repo, listed in `docs/audits/skill_snapshots/MANIFEST.md`.</sub>

Three readings, all from grok-4.6 alone. The exercises carry what lift there is and the quotes
cost more than they pay: the two best of the real documents are the ones that lead with the
exercises, and the quotes-only document collapses, with 10 of its 12 answers going off to narrate
tool calls instead of answering. A short instruction to be thorough beats every version of this
document. And the
quotes do move the specific point they encode, so the loss is elsewhere: on the question about a
number repeated across windows, bare and the inert control both score 0.00 while every document
carrying that quote scores 0.75 or better.

The line at the top of SKILL.md telling you to be diligent and show your work is there because of
the first row of this table. Adding it, and naming the exercises, moved the current document from
0.096 below bare to 0.115 above it, standard error 0.059, and it gained on all three questions.
That is the difference of two arm means over 12 answers each, not a paired difference.


## Other skills

- https://github.com/param087/agent-ml-skills/blob/main/skills/ml-debugging/SKILL.md (ok, aimed at diverging training not development of novel ml)
- https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/main/22-agent-native-research-artifact (dubious, seems mostly vibe written)

## Citation

```bibtex
@misc{wassname2026mldebug,
  title = {ML Debugging Folklore: A Practitioner Debugging Skill for LLM Agents},
  author = {Michael J. Clark},
  year = {2026},
  url = {https://github.com/wassname/ml-debug/}
}
```
