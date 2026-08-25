# Unused quotes from the ml-debug evidence cache

Mined from `/home/wassname/.agents/skills/ml-debug/docs/evidence/` (about 40 cached sources) and
`/home/wassname/.agents/skills/ml-debug/refs/`. Every quote here was checked against
`/home/wassname/.agents/skills/ml-debug/README.md` and is not used there. Line numbers were
verified by grep on a distinctive substring; long source lines are single wrapped paragraphs, so
one line number can hold a long quote.

Target failure modes, as given:

1. Overconfidence, stating a diagnosis as fact without the evidence.
2. Quitting after one change and calling the negative result real.
3. Anchoring on the first idea, never generating a second or third hypothesis.
4. Obsession with legible hyperparameters when the bug is data, sign, mask, or metric.
5. Not reading the data.
6. Not reading the log.
7. Reaching for a cheap indirect probe instead of building the training script and running it.
8. Fixing on an arbitrary numeric threshold before knowing what a fair value is.

Count per mode (a quote can serve more than one): mode 1 six, mode 2 seven, mode 3 six, mode 4 six,
mode 5 six, mode 6 three, mode 7 five, mode 8 seven. Thirty quotes total.

Coverage warning up front. Mode 6, not reading the log, is the thinnest in this corpus. Only three
quotes touch it and none of them says "read the log" in those words; the corpus argues for
instrumenting a run more than for reading the run you already have. Mode 7 is the second thinnest.
Nothing in the cache argues against representation similarity probes by name. The five mode 7
quotes attack the general move, which is standing in a proxy instead of running the real objective.
If either mode matters most to you, this cache needs a new source, not more mining.

---

## Mode 1: overconfidence, a diagnosis stated as fact

## DeepRLHacks (attendee notes on Schulman's "Nuts and Bolts of Deep RL Research") -- William Falcon -- https://github.com/williamFalcon/DeepRLHacks
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/williamfalcon_deeprl_hacks.md:101
- failure modes: 1
- epistemic context: secondary source, attendee notes on Schulman's talk rather than Schulman's own text; the primary slide deck is cached separately as joschu_nuts_and_bolts.md.

> 4. Think your algorithm is working but you're actually seeing random noise.   
>     - Example: Graph of 7 tasks with 3 algorithms and looks like 1 algorithm might be doing best on all problems, but turns out they're all the same algorithm with DIFFERENT random seeds.   

Why it lands: a confident cross-task ranking read off three copies of one algorithm. It is the shortest demonstration that a conclusion can feel fully supported by a plot and be supported by nothing.

## My Research Process: Key Mindsets -- Neel Nanda -- https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_research_process_key_mindsets.md:44
- failure modes: 1
- epistemic context: published LessWrong post by a DeepMind mech interp lead who has supervised 20+ papers; an introspective claim, unfalsifiable on its own.

> Insufficient skepticism doesn't *feel* like insufficient skepticism from the inside. It just feels like doing research.

Why it lands: explains why no internal warning fires. If the failure has no felt signature, a process check has to replace the vibe check, which is the argument for a form the agent has to fill.

## Simple considerations for simple people building fancy neural networks -- Victor Sanh -- https://huggingface.co/blog/simple-considerations
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/sanh_simple_considerations_hf_2021.md:67
- failure modes: 1, 2
- epistemic context: HF research scientist, DistilBERT author, writing from his own practice; blog post with no measurement behind it.

> **The challenge lies in the fact that you can make these mistakes, train a model without it ever crashing, and still get a decent performance…**

Why it lands: names the state in which a confident report is worthless. A run that neither crashes nor looks obviously wrong is exactly the run an agent reports as a clean result.

## Deep Learning Tuning Playbook -- Godbole, Dahl, Gilmer, Shallue, Nado (Google Research) -- https://github.com/google-research/tuning_playbook
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/google_tuning_playbook.md:1089
- failure modes: 1, 8
- epistemic context: Google Research team practice, widely adopted; the README already cites this source for exploration/exploitation, so this is a different section.

> -   It is all well and good to make comparisons of validation error rates
>     estimated on a finite validation set using fastidious statistical tests, but
>     often the trial variance alone can produce statistically significant
>     differences between two different trained models that use the same
>     hyperparameter settings.

Why it lands: seed noise alone can clear a significance bar. So one A-versus-B gap plus a p-value is not evidence, and the p-value is the thing that makes the claim feel safe to state.

## Highly Opinionated Advice on How to Write ML Papers -- Neel Nanda -- https://www.lesswrong.com/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_highly_opinionated_ml_paper_writing.md:196
- failure modes: 1, 2
- epistemic context: published post by the same author; a checklist question he says he applies to his own key experiments.

> **How reliable is my experiment?** Ask yourself: "How surprised would I be if it turned out to be complete bullshit due to a bug, error, noise, misunderstanding, etc.?" Investigate the most uncertain bits

Why it lands: turns "am I overconfident" into one answerable question with a calibration target, and points the next action at the least reliable step rather than the most interesting one.

## My Model of the Research Process (shared draft), as quoted in the skill's own topic note -- Neel Nanda
- file: /home/wassname/.agents/skills/ml-debug/refs/research_taste.md:134
- failure modes: 1, 3
- epistemic context: quoted from an unpublished Google Doc draft, so weaker provenance than the published posts by the same author.

> Insufficient Skepticism: Missing simple alternative explanations, methodological flaws, or bugs. Explicitly list alternatives. Get others (especially mentors) to red team your plans before you run them. Actively try to break your hypothesis. Ask "What observation would make me abandon this?"

Why it lands: "What observation would make me abandon this" is a one-line test that separates a hypothesis from an assertion, and it is cheap enough that an agent has no excuse.

---

## Mode 2: quitting after one change, calling the negative real

## Research as a Stochastic Decision Process -- Jacob Steinhardt -- https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/steinhardt_research_stochastic_decision_process.md:194
- failure modes: 2, 3
- epistemic context: Berkeley ML professor on his own process change, which he says roughly doubled his output; a self-report, but the mechanism is concrete and Nanda links it approvingly.

> **Trying an experiment and seeing it fail gives little information by itself.** When an experiment fails, it is tempting to conclude "I tried X and it didn't work". However, if X is a high-level conceptual approach, then a more correct conclusion is "I tried an implementation comprising 0.1% of the possible implementations of X, and observed that that particular implementation did not work".

Why it lands: the best quote in this whole set for the mode. It gives the error a number, and it distinguishes an approach from one implementation of the approach, which is the substitution an agent makes when it writes "the method does not work".

## Deep Learning, ch. 11 "Practical Methodology" -- Goodfellow, Bengio, Courville -- https://www.deeplearningbook.org/contents/guidelines.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/goodfellow_ch11_practical_methodology.md:194
- failure modes: 2, 1
- epistemic context: standard graduate textbook; the chapter the Google playbook and Ng's book both build on. The README cites this file only for the one-part-broken quote.

> When a machine learning system performs poorly, it is usually difficult to tell whether the poor performance is intrinsic to the algorithm itself or whether there is a bug in the implementation of the algorithm. Machine learning systems are difficult to debug for various reasons.

Why it lands: states the confusion as the default condition of ML debugging, not an edge case. The textbook says the two are not separable without extra work, so declaring one of them for free is a mistake by construction.

## Research as a Stochastic Decision Process -- Jacob Steinhardt -- https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/steinhardt_research_stochastic_decision_process.md:200
- failure modes: 2, 1
- epistemic context: same source; a personal standard, presented as discipline rather than an empirical finding.

> When ruling out ideas, it is important to hold oneself to a high standard. "This doesn't seem like it will work" or "I feel less motivated after trying a few things along this line that didn't work" are _not_ ruling out an idea.

Why it lands: sets the bar for a negative result. The second phrase describes the exact state an agent is in when it moves on, and Steinhardt refuses it as evidence.

## Deep Reinforcement Learning Doesn't Work Yet -- Alex Irpan -- https://www.alexirpan.com/2018/02/14/rl-hard.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/alexirpan_rl_hard.md:626
- failure modes: 2, 1
- epistemic context: Google Brain robotics researcher on his own reproduction attempt, with the paper's first author sitting nearby. The README cites this file only for the seed-variance quotes.

> It ended up taking me 6 weeks to reproduce results, thanks to several software
> bugs. The question is, why did it take so long to find these bugs?

Why it lands: an expert with the author on hand, on a task he had budgeted much shorter. Any negative declared before that much bug hunting is a claim about the implementation, not the method.

## nanochat experiment log -- Andrej Karpathy -- https://github.com/karpathy/nanochat/blob/master/dev/LOG.md
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/karpathy_nanochat_experiments.md:411
- failure modes: 2
- epistemic context: primary experiment log written by the author as he ran it; the README quotes this file only for the BOS dataloader and grad clipping items.

> **Result:** This was not an out-of-the-box win for nanochat even with a mild attempt over a few hours at a bit of tuning and debugging. The idea itself is intuitively appealing. Might come back around later to try harder later.

Why it lands: the model of how to write a negative honestly. He records the effort spent, keeps the idea alive, and does not promote "did not work for me in a few hours" into "does not work".

## Adding Error Bars to Evals -- Evan Miller (Anthropic) -- https://arxiv.org/pdf/2411.00640
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/miller_2024_error_bars_evals.md:11
- failure modes: 2, 8
- epistemic context: arXiv stat.AP preprint, not peer reviewed, but the statistics are textbook and the recommendations already appear in tooling such as Inspect's `epochs`.

> Our specific recommendations to researchers include: 1. Computing standard errors of the mean using the Central Limit Theorem 2. When questions are drawn in related groups, computing clustered standard errors 3. Reducing variance by resampling answers and by analyzing next-token probabilities 4. When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics 5. Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest

Why it lands: item 5 is the check on the whole mode. If the eval never had the power to see the effect, the negative result is about the eval. Item 4 is also the pairing rule this bench's own AGENTS.md enforces.

## Lessons Learned Reproducing a Deep RL Paper -- Matthew Rahtz -- http://amid.fish/reproducing-deep-rl
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/amid_fish_reproducing_deep_rl.md:132
- failure modes: 2, 3
- epistemic context: first-person 8 month project log with hours and costs recorded; cited by OpenAI's Spinning Up. The README quotes a different passage from this file.

> If you keep that strategy when each run takes 10 hours, though, you can easily
> waste a *lot* of time. Last run didn’t work? OK, I think it’s this thing. Let’s
> set off another run to check. Coming back the next morning: still doesn’t work?
> OK, maybe it’s this other thing. Let’s set off another run. A week later, you
> still haven’t solved the problem.

Why it lands: the one-change-then-declare loop written out as a transcript, with the cost measured in a week of wall clock.

---

## Mode 3: anchoring on the first idea

## Lessons Learned Reproducing a Deep RL Paper -- Matthew Rahtz -- http://amid.fish/reproducing-deep-rl
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/amid_fish_reproducing_deep_rl.md:126
- failure modes: 3
- epistemic context: same log; this passage is the diagnosis that precedes the README's "think more, experiment less" prescription.

> than forming hypotheses. Why spend 15 minutes carefully considering everything
> that could be causing what you see when you can check the first idea that jumps
> to mind in a fraction of that (and gather more evidence in the process)? To put
> it another way: if you have rapid feedback, you can narrow down the hypothesis
> space a lot faster by trying things than thinking carefully.

Why it lands: explains why anchoring feels correct. It is correct when feedback is seconds, and an LLM's edit-and-rerun loop feels that fast even when the training run underneath it does not.

## My Research Process: Key Mindsets -- Neel Nanda -- https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_research_process_key_mindsets.md:56
- failure modes: 3, 1
- epistemic context: published post by a supervisor of 20+ papers; a framing claim, not a measured result.

> The standard hypothesis testing framework can be misleading here, because it has an implicit frame of being able to list all the hypotheses. But actually, most of your probability mass should normally be on “something I haven’t thought of yet”

Why it lands: attacks anchoring at the root, and it also attacks the fix. Even after the agent dutifully writes hypotheses 1, 2 and 3, the correct posterior still puts most mass outside the list.

## How to Become a Mechanistic Interpretability Researcher -- Neel Nanda -- https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_how_to_mech_interp.md:614
- failure modes: 3, 7
- epistemic context: same guide; a pattern he reports seeing repeatedly in researchers he supervises. The README quotes this file only for research-is-false, excitement, and read-your-data.

> If trying to explain something mysterious, novice researchers often neglect simple, dumb hypotheses like “maybe MLP0 is incredibly important on *every* input, and there’s nothing special going on with my prompt”

Why it lands: the missing hypothesis 2 is usually the boring one, and an exciting hypothesis 1 is what suppresses it. This is the mech interp version of "your steering vector is just a big norm".

## Research as a Stochastic Decision Process -- Jacob Steinhardt -- https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/steinhardt_research_stochastic_decision_process.md:196
- failure modes: 3, 6
- epistemic context: same source; a first-person admission of his own repeated mistake, which is the kind of self-report that costs the author something.

> Importantly, it is often not obvious that multiple approaches to a problem all have the same issue. In the past, I have spent months trying different approaches to a problem before finally stepping back and realizing that they were all failing for the same reason. Moreover, I had all the data necessary to make this realization a couple weeks in but had failed to do so.

Why it lands: two modes at once. Hypotheses 2 and 3 can be hypothesis 1 wearing a hat, and the evidence that would have shown it was already sitting in the logs for weeks.

## Full Stack Deep Learning Spring 2021, Lecture 7: Troubleshooting Deep Neural Networks -- Josh Tobin (notes by James Le, Vishnu Rachakonda) -- https://fullstackdeeplearning.com/spring2021/lecture-7/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/fsdl_spring2021_lecture7.md:443
- failure modes: 3, 4
- epistemic context: teaching notes from a widely used practitioner course; Tobin was an OpenAI research scientist. Not cited in the README at all.

> * **Error goes up**: Commonly, this is due to a flip sign somewhere in
>   the loss function/gradient.
> * **Error explodes**: This is usually a numerical issue but can also
>   be caused by a high learning rate.
> * **Error oscillates**: You can lower the learning rate and inspect
>   the data for shuffled labels or incorrect data augmentation.
> * **Error plateaus**: You can increase the learning rate and get rid
>   of regulation. Then you can inspect the loss function and the data
>   pipeline for correctness.

Why it lands: a symptom-to-cause table where every symptom has two or three candidates and only one of them is a learning rate. It is a ready-made hypothesis-2-and-3 generator for the moment the agent reaches for the knob.

## My Model of the Research Process (shared draft), as quoted in the skill's own topic note -- Neel Nanda
- file: /home/wassname/.agents/skills/ml-debug/refs/research_taste.md:120
- failure modes: 3
- epistemic context: unpublished draft quoted in a local topic note; weaker provenance than the published posts.

> Actively Seek Alternatives: Explicitly brainstorm other ways your observations could be explained. What are the simplest explanations? What known circuits or phenomena could be involved? What would a strong skeptic argue?

Why it lands: hypothesis 2 and 3 made into an explicit step with a prompt for each. Note that it asks for the simplest explanations, not more of the same kind as hypothesis 1.

---

## Mode 4: obsession with the legible hyperparameters

## Spinning Up as a Deep RL Researcher -- Joshua Achiam (OpenAI, 2018) -- https://spinningup.openai.com/en/latest/spinningup/spinningup.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/spinningup_researcher.md:56
- failure modes: 4, 1
- epistemic context: OpenAI research scientist, official Spinning Up documentation. The README quotes the tail of this same paragraph ("test in more than one environment"), so only this front half is unused.

> **If it doesn’t work, assume there’s a bug.** Spend a lot of effort searching for bugs before you resort to tweaking hyperparameters: usually it’s a bug. Bad hyperparameters can significantly degrade RL performance, but if you’re using hyperparameters similar to the ones in papers and standard implementations, those will probably not be the issue.

Why it lands: gives both the ordering the agent inverts and the reason. Published hyperparameters are already close to right, so the prior on the knob being your problem is low before you touch it.

## A Recipe for Training Neural Networks -- Andrej Karpathy -- https://karpathy.github.io/2019/04/25/recipe/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/karpathy_recipe_training_nn_2019.md:41
- failure modes: 4, 2, 1
- epistemic context: the canonical practitioner post; the README cites it for inspect-data, fixed-seed, overfit-one-batch and Adam 3e-4, so this "fails silently" passage is separate. The cached file is an abridged note with its own elisions.

> For example, perhaps you forgot to flip your labels when you left-right flipped the image during data augmentation. Your net can still (shockingly) work pretty well because your network can internally learn to detect flipped images and then it left-right flips its predictions. Or maybe your autoregressive model accidentally takes the thing it’s trying to predict as an input due to an off-by-one bug. Or you tried to clip your gradients but instead clipped the loss, causing the outlier examples to be ignored during training. Or you initialized your weights from a pretrained checkpoint but didn’t use the original mean. Or you just screwed up the settings for regularization strengths, learning rate, its decay rate, model size, etc.

Why it lands: five worked examples, and every one is a label, sign, mask or target bug. The legible hyperparameters arrive last, in one clause, as an afterthought. That ordering is the whole of the mode.

## Simple considerations for simple people building fancy neural networks -- Victor Sanh -- https://huggingface.co/blog/simple-considerations
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/sanh_simple_considerations_hf_2021.md:96
- failure modes: 4, 3
- epistemic context: same post; a practitioner heuristic, no experiment behind the 4e2 example.

> Most importantly, there is no point of launching 1000 runs with different hyperparameters (or architecture tweaks like activation functions): **compare a couple of runs with different hyperparameters to get an idea of which hyperparameters have the highest impact** but in general, it is delusional to expect to get your biggest jumps of performance by simply tuning a few values. For instance, if your best performing model is trained with a learning rate of 4e2, there is probably something more fundamental happening inside your neural network and you want to identify and understand this behavior so that you can re-use this knowledge outside of your current specific context.

Why it lands: treats a weird optimal hyperparameter as a symptom to explain rather than a setting to keep. That is the opposite reflex to "the sweep found 4e2, ship it".

## ML Engineering for AI Safety and Robustness -- Catherine Olsson and the 80,000 Hours team -- https://80000hours.org/articles/ml-engineering-career-transition-guide/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/olsson_80000hours_ml_engineering_ai_safety.md:122
- failure modes: 4, 2
- epistemic context: career guide reporting Daniel Ziegler's self-study second-hand, so weaker than a practitioner writing in their own voice.

> Once the algorithm was partially working, they would attain higher performance by looking for remaining bugs, both by reviewing the code carefully, and by collecting metrics such as average policy entropy to perform sanity-checks, rather than just tune hyperparameters.

Why it lands: the explicit contrast between tuning and bug-hunting-with-diagnostics, from someone who took a partly working implementation to full performance. The named metric is a diagnostic, not a score.

## How to get good at programming -- Ulisse Mini -- https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/ulisse_how_to_get_good_at_programming.md:31
- failure modes: 4, 3
- epistemic context: LessWrong post by a self-described "~5yrs of linux & programming experience" author, marked "Epistemic status: very confident". Low external validation, but the README already cites this source and the mechanism is checkable against your own behaviour.

> Third, and perhaps most important for building skill,[[1]](https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming#fn289bs9hi65b)you must **notice** when you're going into brute-force search mode, and then **take action** by investing time in understanding the underlying system, until both the problem and solution make sense.

Why it lands: sweeping the legible knobs is brute-force search wearing a lab coat. The paired footnote at line 51 of the same file names the cost, that his CSS skills did not improve for several years because he stayed in try-random-stuff mode.

## How to more intelligently debug RL roadblocks? -- u/GrundleMoof -- https://old.reddit.com/r/reinforcementlearning/comments/bzg3l2/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/reddit_rl_roadblocks_bzg3l2.md:41
- failure modes: 4, 3
- epistemic context: LOW CREDIBILITY. Anonymous reddit self-report from a self-described non-expert. Its value is as a specimen of the failure mode, not as advice, and it should not be quoted as authority.

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

Why it lands: nine knobs turned, all of them legible, and the agent still does not learn. This is a photograph of the default LLM search. A reply in the same thread, at line 60 of the same file, reports that his own two bugs on that environment were a terminal-flag masking error and a shape broadcast, neither of which any of those nine knobs can reach.

---

## Mode 5: not reading the data

## Deep Learning, ch. 11 "Practical Methodology" -- Goodfellow, Bengio, Courville -- https://www.deeplearningbook.org/contents/guidelines.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/goodfellow_ch11_practical_methodology.md:210
- failure modes: 5, 7, 1
- epistemic context: standard textbook, in its list of debugging tests.

> Visualize the model in action: When training a model to detect objects in images, view some images with the detections proposed by the model displayed superimposed on the image. When training a generative model of speech, listen to some of the speech samples it produces. This may seem obvious, but it is easy to fall into the practice of looking only at quantitative performance measurements like accuracy or log-likelihood. Directly observing the machine learning model performing its task will help to determine whether the quantitative performance numbers it achieves seem reasonable. Evaluation bugs can be some of the most devastating bugs because they can mislead you into believing your system is performing well when it is not.

Why it lands: the textbook naming the exact drift, that it is easy to fall into looking only at the scalars. The last sentence explains why the scalar cannot police itself.

## Deep Reinforcement Learning that Matters -- Henderson, Islam, Bachman, Pineau, Precup, Meger (AAAI 2018) -- https://arxiv.org/pdf/1709.06560
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/henderson_2018_deep_rl_matters.md:243
- failure modes: 5, 6, 8
- epistemic context: peer reviewed, backed by their own controlled reruns of four algorithms across four environments. The README quotes this file for seed splits and implementation differences, not for this.

> By reaching a local optimum, learning curves can indicate successful optimization of the policy over time, when in reality the returns achieved are not qualitatively representative of learning the desired behaviour, as demon-strated in video replays of the learned policy 5. Therefore, it is important to show not only returns but demonstrations of the learned policy in action.

Why it lands: a healthy-looking curve produced by a swimmer curling up and flailing. Peer reviewed, and the only way anyone saw it was by watching the output. Note the OCR artifacts ("demon-strated") are in the cached file.

## DeepRLHacks (attendee notes on Schulman's talk) -- William Falcon -- https://github.com/williamFalcon/DeepRLHacks
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/williamfalcon_deeprl_hacks.md:49
- failure modes: 5
- epistemic context: secondary attendee notes; the matching primary slide is "Atari: can you see game features in downsampled image?" in the cached joschu_nuts_and_bolts.md.

> 2. Make sure observations usable:
>     - See if YOU could control the system by using the same observations you give the agent.   
>       - Example: Look at preprocessed images yourself to make sure you don't remove necessary details or hinder the algorithm in a certain way.

Why it lands: turns "read the data" into a pass/fail test that takes a minute. If you cannot do the task from the model's inputs, no hyperparameter will save it.

## Simple considerations for simple people building fancy neural networks -- Victor Sanh -- https://huggingface.co/blog/simple-considerations
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/sanh_simple_considerations_hf_2021.md:84
- failure modes: 5
- epistemic context: same post; self-reported experience, and the costly kind, an admission of repeated personal loss.

> Pro-tip: when you work with language, have a serious **look at the outputs of the tokenizers**. I can’t count the number of lost hours I spent trying to reproduce results (and sometimes my own old results) because something went wrong with the tokenization.

Why it lands: for LLM work, reading the data means reading the tokenized data, the artifact that actually enters the model, not the source text you believe you passed in.

## Machine Learning Yearning (draft), ch. 14 -- Andrew Ng -- https://github.com/ajaymache/machine-learning-yearning
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/ng_ml_yearning_error_analysis.md:282
- failure modes: 5, 3
- epistemic context: widely circulated unpublished draft. The README quotes the "Manually examining 100 examples" sentence from this same long line, so only this earlier part is unused.

> Error analysis can often help you figure out how promising different directions are. I’ve seen many engineers reluctant to carry out error analysis. It often feels more exciting to just jump in and implement some idea, rather than question if the idea is worth the time investment. This is a common mistake: It might result in your team spending a month only to realize afterward that it resulted in little benefit.

Why it lands: names the motivational failure rather than the procedural one. "It often feels more exciting to just jump in and implement some idea" is the agent that skips the data and starts editing the config.

## Debugging the training pipeline (HF LLM Course ch. 8.4) -- Sylvain Gugger et al. -- https://huggingface.co/learn/llm-course/chapter8/4
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/hf_llm_course_ch8_4_debugging_pipeline.md:670
- failure modes: 5
- epistemic context: official HF teaching material by the Trainer maintainers; instructional, not measured.

> ⚠️ If you are doing distributed training, print samples of your dataset in each process and triple-check that you get the same thing. One common bug is to have some source of randomness in the data creation that makes each process have a different version of the dataset.

Why it lands: sharpens "read the data" to per-rank. Reading one process's data is not reading the data when eight processes disagree with each other.

---

## Mode 6: not reading the log

Thin, as flagged above. Three quotes, and none of them uses the words.

## Deep Learning Tuning Playbook -- Godbole, Dahl, Gilmer, Shallue, Nado (Google Research) -- https://github.com/google-research/tuning_playbook
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/google_tuning_playbook.md:916
- failure modes: 6, 1
- epistemic context: Google Research team practice; the "Examining the training curves" section, which the README does not touch.

> -   Although in many cases the primary objective of our experiments only
>     requires considering the validation error of each trial, we must be careful
>     when reducing each trial to a single number because it can hide important
>     details about what’s going on below the surface.
> -   For every study, we always look at the **training curves** (training error
>     and validation error plotted versus training step over the duration of
>     training) of at least the best few trials.

Why it lands: the closest thing in the cache to a hard rule that you read the run before you report its number, from a team that had every excuse to just read the number.

## Lessons Learned Reproducing a Deep RL Paper -- Matthew Rahtz -- http://amid.fish/reproducing-deep-rl
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/amid_fish_reproducing_deep_rl.md:237
- failure modes: 6, 1
- epistemic context: same project log; a self-reported cost for one specific ignored log signal. The quote spans lines 237 to 239.

> (I missed
> a multithreading bug for several months by ignoring a small but mysterious
> decay in frames per second.)

Why it lands: a price tag on skipping a boring number. The signal was in the log the whole time, it was not the loss curve, and it cost months.

## Machine Learning Engineering Open Book, "Understanding Training Loss Patterns" -- Stas Bekman -- https://github.com/stas00/ml-engineering
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/bekman_ml_engineering_instabilities.md:257
- failure modes: 6, 1, 3
- epistemic context: first-hand post-mortem from BLOOM and IDEFICS scale training by the engineer who ran it; one incident, self-reported. The README quotes this file for spike types and the 104B post-mortem, not this.

> There was no real spike in the two earlier runs. The loss never went up in the first place. In both resumes it was under-reporting loss due to an exactly repeated data and then it reached data it hasn't seen before and started reporting correctly. In other words it was overfitting and reporting a false loss.

Why it lands: the visible symptom was an artifact of the resume and the data sampler, so every hypothesis about the optimizer or the precision would have been confidently wrong. Reading the whole log across resumes is what found it.

---

## Mode 7: a cheap indirect probe instead of running the real thing

Second thinnest. No source here names representation-similarity probes. These five attack the general substitution.

## How to Become a Mechanistic Interpretability Researcher -- Neel Nanda -- https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_how_to_mech_interp.md:605
- failure modes: 7, 4
- epistemic context: opinionated guide by a DeepMind mech interp lead; the RMU example is a published follow-up result, not a self-report.

> **Do ablations on your fancy method**: It's easy for people to have a fancy method with lots of moving parts, when many actually are unnecessary. You should always try removing one part and see if the method breaks. Do this for each part.
>     *   For example, the [original unlearning method](https://arxiv.org/abs/2403.03218v1) in the [RMU paper](https://arxiv.org/abs/2403.03218) claimed it was based on finding a meaningful steering vector, until follow-up work found that it was just about adding a vector with really high norm that broke the model, and a random vector performed just as well.

Why it lands: a published case where a clever mechanism was actually norm damage. The random-vector control is the cheap real test that the indirect story never bothered to run.

## CS229 Advice for Applying Machine Learning -- Andrew Ng -- https://cs229.stanford.edu/materials/ML-advice.pdf
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/cs229_ml_advice.md:638
- failure modes: 7
- epistemic context: Stanford course slides by Ng; the README cites the later Machine Learning Yearning instead, so this file is unused. Slide text, so the line breaks are the PDF's.

> The only way to find out what needs work is to implement something quickly,
>
> and find out what parts break.

Why it lands: the shortest statement of build-it-and-run-it. Carry Ng's own caveat with it, since the next slide says this is worse advice when your goal is to invent new algorithms.

## Deep Learning, ch. 15 "Representation Learning" -- Goodfellow, Bengio, Courville -- https://www.deeplearningbook.org/contents/representation.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/goodfellow_ch15_representation_learning.md:180
- failure modes: 7, 8
- epistemic context: standard textbook, describing a figure from Chelsea Finn's robotics work.

> Figure 15.5: An autoencoder trained with mean squared error for a robotics task has failed to reconstruct a ping pong ball. The existence of the ping pong ball and all its spatial coordinates are important underlying causal factors that generate the image and are relevant to the robotics task. Unfortunately, the autoencoder has limited capacity, and the training with mean squared error did not identify the ping pong ball as being salient enough to encode.

Why it lands: the convenient proxy metric silently deleted the one object the task was about, and the metric looked fine the whole time. A cheap measure decides what counts as signal before you get to look at anything.

## How to Become a Mechanistic Interpretability Researcher -- Neel Nanda -- https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_how_to_mech_interp.md:615
- failure modes: 7, 5
- epistemic context: same guide; a methodological preference he argues for, stated as opinion.

> One of the key drivers of progress in mech interp is an openness to qualitative research: summary statistics lose a ton of information. What can we learn by actually looking deeply into what's happening?

Why it lands: names what a scalar proxy costs. Distinct from the README's read-your-data quote, which is about data quality; this one is about the aggregate hiding the phenomenon.

## Training Stability and Debugging -- Axolotl docs -- https://docs.axolotl.ai/docs/training_stability.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/axolotl_training_stability.md:99
- failure modes: 7, 2
- epistemic context: vendor documentation for a widely used fine-tuning framework; engineering advice distilled from user reports, not measured. The README quotes two other lines from this file.

> 1. **Test reward function standalone**: Run it outside training with known inputs to verify it returns nonzero values.

Why it lands: when the metric will not move, the first move is to run the real objective on known inputs. The same page's table at line 41 says a reward stuck at zero means the reward function is broken or the task is too hard, which is two hypotheses, not one.

---

## Mode 8: an arbitrary threshold set before you know what is fair

## Deep Learning, ch. 11 "Practical Methodology" -- Goodfellow, Bengio, Courville -- https://www.deeplearningbook.org/contents/guidelines.html
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/goodfellow_ch11_practical_methodology.md:196
- failure modes: 8, 1
- epistemic context: standard textbook, the paragraph after the debugging-is-hard one.

> In most cases, we do not know a priori what the intended behavior of the algorithm is. In fact, the entire point of using machine learning is that it will discover useful behavior that we were not able to specify ourselves. If we train a neural network on a new classification task and it achieves 5 percent test error, we have no straightforward way of knowing if this is the expected behavior or suboptimal behavior.

Why it lands: the best quote in the set for this mode, and it kills the invented threshold from first principles. If you cannot say whether 5 percent error is good, then the 0.8 you wrote into the success criterion was a number you made up.

## My Model of the Research Process (shared draft) -- Neel Nanda -- https://docs.google.com/document/d/1YMkeMrhqsWxZcNDD9CIUWEK_DAOegeufnbc79U2hycg/edit
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/nanda_research_process_shared_draft.md:337
- failure modes: 8
- epistemic context: unpublished draft of a published LessWrong sequence; this passage never made it to the published post, so it is draft quality from the same author.

> A valuable intuition to have in mind is that, by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! Baselines are one way to get context to compare against.

Why it lands: states the default, that a number carries no information until something supplies its scale, and names the fix as a baseline rather than a chosen cutoff. The example is literally a probe accuracy.

## CS231n, Neural Networks Part 3 -- Stanford (Andrej Karpathy) -- https://cs231n.github.io/neural-networks-3/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/cs231n_neural_networks_3.md:50
- failure modes: 8
- epistemic context: long-running Stanford course notes; the README cites this file only for the overfit-tiny-subset check.

> You might be temped to keep track of the difference \(\mid f’\_a - f’\_n \mid \) or its square and define the gradient check as failed if that difference is above a threshold. However, this is problematic. For example, consider the case where their difference is 1e-4. This seems like a very appropriate difference if the two gradients are about 1.0, so we’d consider the two gradients to match. But if the gradients were both on order of 1e-5 or lower, then we’d consider 1e-4 to be a huge difference and likely a failure.

Why it lands: a fully worked case where a fixed numeric cutoff is meaningless until you know the scale of the quantity. The fix is to change the metric to a scale-free one, not to argue about where the cutoff should sit. The typo "temped" is in the source.

## Simple considerations for simple people building fancy neural networks -- Victor Sanh -- https://huggingface.co/blog/simple-considerations
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/sanh_simple_considerations_hf_2021.md:58
- failure modes: 8, 5
- epistemic context: same post; the questions he says he asks himself before starting, not a result.

> *   How would a random predictor perform (especially in classification problems)? Dataset can be unbalanced…
> *   What would the loss look like for a random predictor?
> *   What is (are) the best metric(s) to measure progress on my task?
> *   What are the limits of this metric? If it’s perfect, what can I conclude? What can’t I conclude?

Why it lands: four questions that have to be answered before any number can be called good or bad. The last one, what you cannot conclude from a perfect score, is the specific antidote to a made-up pass threshold.

## Debugging the training pipeline (HF LLM Course ch. 8.4) -- Sylvain Gugger et al. -- https://huggingface.co/learn/llm-course/chapter8/4
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/hf_llm_course_ch8_4_debugging_pipeline.md:674
- failure modes: 8, 6
- epistemic context: official HF course; instructional, not measured. The README quotes two other passages from this file.

> If the loss/metric you get on your initial model is very different from the loss/metric you would expect for random predictions, double-check the way your loss or metric is computed, as there is probably a bug there. If you are using several losses that you add at the end, make sure they are of the same scale.

Why it lands: gives the constructive alternative. Compute what random gets, then treat any distance from it as a bug report until you have shown otherwise. The second sentence is your own combined-loss objection stated by HF.

## The 37 Implementation Details of Proximal Policy Optimization -- Huang, Dossa, Raffin, Kanervisto, Wang -- https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/cleanrl_37_ppo_details.md:624
- failure modes: 8, 2
- epistemic context: ICLR Blog Track, a reviewed venue, with every claim linked to a code line and to tracked W&B runs. Not cited in the README.

> 5.   **Rule of thumb: 400 episodic return in breakout**: Check if your PPO could obtain 400 episodic return in breakout. We have found this to be a practical rule of thumb to determine the fidelity of online PPO implementations in GitHub. Often we found PPO repositories not able to do this, and we know they probably do not match all implementation details of `openai/baselines`’ PPO.

Why it lands: shows the legitimate form of a numeric gate. The number was discovered by reproducing a known-good reference, not chosen in advance. The sting is in the last sentence, that most public repos fail it, so a plausible-looking implementation is usually still broken.

## Bad Labels -- Vincent D. Warmerdam (koaning) -- https://koaning.io/posts/labels/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/koaning_bad_labels.md:25
- failure modes: 8, 5
- epistemic context: practitioner blog; the surrounding claim is backed by the labelerrors.com paper (arXiv:2103.14749), this sentence is his argument. The README quotes three other lines from this file.

> The issue here isn't just that we might have bad labels in our training set, the issue is that it appears in the validation set. If a machine learning model can become state of the art by squeezing another 0.5% out of a validation set one has to wonder. Are we really making a better model? Or are we creating a model that is better able to overfit on the bad labels?

Why it lands: puts a floor under any target. A threshold set tighter than the label noise in your validation set is measuring overfitting to errors.

---

## Extra: good and unused, fits none of the eight cleanly

## Nuts and Bolts of Deep RL Research (Deep RL Bootcamp lecture 6, audience Q&A) -- John Schulman -- https://www.youtube.com/watch?v=8EcdaCk9KaQ
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/schulman_nuts_bolts_deeprl_bootcamp_2017_subtitles.md:870
- failure modes: 8, 2 (partially), but it is really about unit testing ML
- epistemic context: the PPO and TRPO author answering a live question. The cached text is auto-generated captions, so there is no punctuation and there may be transcription slips. Quote with that caveat visible.

> so if you try to write a test saying I
> should be at performance 100 after this
> many iterations it might fail just out
> of random noise but yeah I think
> probably unit tests are a good idea

Why it lands: it is the pinned numeric target problem stated by someone who would know, but the caption format makes it awkward to quote in a README, which is why it is down here rather than under mode 8.

## r/MachineLearning thread on "37 Reasons why your NN is not working" -- anonymous commenter -- https://old.reddit.com/r/MachineLearning/comments/6pfsyk/
- file: /home/wassname/.agents/skills/ml-debug/docs/evidence/reddit_37_reasons_nn_6pfsyk.md:149
- failure modes: 2 and 4, but as a specimen not as advice
- epistemic context: LOW CREDIBILITY. Anonymous reddit comment from 2017, no verifiable identity, retrieved via a Wayback snapshot. Do not cite this as authority.

> My point is that if I came up with the idea of GANs, they wouldn't be recognized because I can't make the idea work in practice. I want to learn the tools I need to find out what is wrong with my current implementation.

Why it lands: a person who has swept hyperparameters, glanced at gradients, failed to localise the bug, and concluded that a method known to work would have died in his hands. That is the mode 2 error stated from the inside, but it is a reddit comment and should be presented as a specimen.

---

Compiled by CLAUDE-OPUS, 2026-08-25. Read-only pass over the ml-debug cache; nothing under
`/home/wassname/.agents/` was modified.
