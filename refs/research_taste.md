# Research taste and research-process folklore

Appendix to the [ML Debugging skill](../SKILL.md).

Use this when the task is not only "why is this broken?" but "what should we try next, what would teach us the most, or how do we turn messy research into claims?" Debugging asks what is false in the current system. Research taste asks which next observation is worth buying with time.

This is an evidence map, not a finished new skill. It preserves the source language and points to the local evidence cache so a later high-context pass can decide what belongs in `SKILL.md`.

## The research loop

Neel Nanda's sequence gives the cleanest stage model: ideation, exploration, understanding, and distillation.[^nanda-explore]

> I see research as breaking down into a few stages:
>
> 1. Ideation - Choose a problem/domain to focus on
> 2. Exploration - Gain Surface area
> 3. Understanding - Test Hypotheses
> 4. Distillation - Compress, Refine, Communicate

For agents, the first diagnostic question is "what stage are we in?" A confused exploration stage should optimize for surface area, not premature proof. An understanding stage should optimize for discriminating hypotheses. A distillation stage should turn evidence into claims a skeptical outsider can audit.

> Not having a clear goal/next step doesn't mean that you don't need to prioritise! Prioritise for information gain.[^nanda-explore]

> The mark of a good researcher is a deep commitment to skepticism of your results.[^nanda-explore]

## Taste is trainable, but feedback is sparse

Nanda's taste post and Olah's taste exercises agree on the bottleneck: project-level feedback is slow, so you need proxy feedback and deliberate reflection.[^nanda-taste][^olah-taste]

> Research taste isn't magic. It's a complex set of intuitions and frameworks built incrementally through experience, reflection, and learning from others.[^nanda-taste]

> The core problem is you just don't get that much data.[^nanda-taste]

> Many of the following exercises are really strategies for getting (proxy) feedback on more research ideas faster.[^olah-taste]

Practical folklore:

- Write down research ideas and predict what a mentor will say before asking.
- When surprised, paraphrase the mentor's reasoning until the missing heuristic is explicit.
- Review decisions after reality answers: was the outcome luck, execution, or taste?
- Read papers as offline data, but remember publication bias and hidden jank.

## Ideation

The shared Nanda draft is the best operational guide for choosing a problem. It is local/downloaded evidence, so treat it as a draft rather than a canonical public post.[^nanda-draft]

> You can't do research without a question or a domain. Ideation is about finding fertile ground.[^nanda-draft]

> Ideation ends when you have a clear enough question or domain that you can start generating concrete experiments to run.[^nanda-draft]

> This is basically borrowing someone else's research taste, and IMO is one of the most valuable things I do for my mentees.[^nanda-draft]

Folklore:

- Early in a field, using a mentor's project can be rational. Originality is not the first bottleneck.
- If no mentor exists, extend a paper you like or use a vetted open-problems list.
- A bad problem can sink a project before any debugging skill matters.

## Exploration

Exploration is for building surface area, not defending a hypothesis. This is where fast, partial, qualitative, and even cherry-picked observations can be useful, as long as you do not later launder them into proof.[^nanda-draft]

> Your north star is information gained per unit time/effort.[^nanda-draft]

> Crucially, Exploration is not about testing a specific hypothesis.[^nanda-draft]

> Reach for a tool that might show you something interesting, and can be employed fast.[^nanda-draft]

> Notice Weirdness: This is critical.[^nanda-draft]

This connects directly to the ML-debugging folklore: Rahtz says confusion was the clue, Jones says anomalies should be chased, and Spinning Up says simple environments with sub-5-minute turnaround are ideal for debugging.[^rahtz][^spinningup-graph]

> It was only by following that confusion and realising that taking the difference between frames zeroed out the background that gave the hint of a problem with normalization.[^rahtz]

> Your ideal experiment turnaround-time at the debug stage is <5 minutes (on your local machine) or slightly longer but not much.[^spinningup-graph]

## Understanding

Understanding starts when you have candidate hypotheses. The question becomes: what evidence would distinguish them?

> Design High Information Experiments: Design experiments specifically to differentiate between your main hypothesis and the most plausible alternatives.[^nanda-draft]

> Avoid the mistake of looking for evidence predicted by H1 that's also predicted by a bunch of other things![^nanda-draft]

> Use appropriate baselines.[^nanda-draft]

Steinhardt gives the matching prioritization rule: do the action that reduces uncertainty fastest, not the one that feels easiest or most complete.[^steinhardt]

> Do the components in order from most informative per unit time to least informative per unit time.[^steinhardt]

> De-risk all components (to the extent feasible), then execute.[^steinhardt]

For RL and unstable ML experiments, Spinning Up, Henderson, Schulman, and Irpan converge on the same practical discipline: strong baselines, many seeds, ablations, and instrumentation.[^spinningup-graph][^henderson][^schulman][^irpan]

> Under no circumstances handicap the baseline![^spinningup-graph]

> Always Be Ablating.[^schulman]

> Without significance metrics and tighter standardization of experimental reporting, it is difficult to determine whether improvements over the prior state-of-the-art are meaningful.[^henderson]

## Distillation and paper writing

Nanda's paper-writing post is the most direct source for the distillation stage. It is not only writing advice; it is a test of whether the research has compressed into claims and evidence.[^nanda-paper]

> The essence of an ideal paper is the narrative: a short, rigorous and evidence-based technical story you tell, with a takeaway the readers care about.[^nanda-paper]

> The first step is to compress your research into these claims.[^nanda-paper]

> Inform, not persuade: Avoid the trap of overclaiming or ignoring limitations.[^nanda-paper]

> Readers will rarely take away more than a few sentences of content. Choose those sentences carefully.[^nanda-paper]

> Warning: Before moving into paper-writing mode, it's crucial to verify that your evidence is actually correct.[^nanda-paper]

> The Guiding Question for Evidence: Ultimately, the question to ask about your evidence is: "Should this update a reader's beliefs about my claims?"[^nanda-paper]

Folklore:

- Compress to one to three claims. If you cannot, you probably do not know the contribution yet.
- Red-team the narrative because elegant stories are where false research hides.
- Move weak or peripheral evidence to appendices. Keep the main text for the hard-to-deny evidence.
- Write to inform; persuasion pressure is how limitations vanish.

## For agents

The agent version is simple:

1. State the current stage: ideation, exploration, understanding, or distillation.
2. Name the north star for that stage.
3. Propose the next action by information gained per unit time.
4. Say what would change your mind before running it.
5. Preserve proof: logs, plots, commits, quotes, or tables.

If the user is AFK, continue through the loop. If the evidence invalidates the original hypothesis, update the plan rather than defending the old narrative.

## See also / source graph

Most relevant sources cached for this reference:

- Neel Nanda, research-process sequence: [explore/understand/distill](../docs/evidence/nanda_research_process_explore_understand_distill.md), [key mindsets](../docs/evidence/nanda_research_process_key_mindsets.md), [research taste](../docs/evidence/nanda_research_process_research_taste.md), [shared draft](../docs/evidence/nanda_research_process_shared_draft.md), [paper writing](../docs/evidence/nanda_highly_opinionated_ml_paper_writing.md).
- Chris Olah, [Research Taste Exercises](../docs/evidence/olah_research_taste_exercises.md): proxy feedback, mentor ratings, research intimacy.
- Jacob Steinhardt, [Research as a Stochastic Decision Process](../docs/evidence/steinhardt_research_stochastic_decision_process.md): information rate, de-risking, ceilings, baselines.
- Joshua Achiam / OpenAI Spinning Up, [research source graph](../docs/evidence/spinningup_research_source_graph.md) and [original cache](../docs/evidence/spinningup_researcher.md): RL apprenticeship, fair comparisons, seeds, preregistration, ablations.
- Matthew Rahtz, [Lessons Learned Reproducing a Deep RL Paper](../docs/evidence/amid_fish_reproducing_deep_rl.md): confusion, long iteration times, think more before expensive runs.
- Henderson et al., [Deep Reinforcement Learning that Matters](../docs/evidence/henderson_2018_deep_rl_matters.md): seed variance, implementation differences, reproducibility reporting.
- John Schulman, [Nuts and Bolts of Deep RL Research](../docs/evidence/joschu_nuts_and_bolts.md): small test problems, health indicators, multiple seeds, ablations.
- Alex Irpan, [Deep Reinforcement Learning Doesn't Work Yet](../docs/evidence/alexirpan_rl_hard.md): realistic expectations, sample inefficiency, seed variance.

Less central but useful:

- Catherine Olsson / 80,000 Hours, [ML Engineering for AI Safety & Robustness](../docs/evidence/olsson_80000hours_ml_engineering_ai_safety.md): implementation/debugging as research-engineer apprenticeship.
- Tim Rocktaschel et al., Advice for Short-term Machine Learning Research Projects: linked by Spinning Up but not cached yet.
- Islam et al., Reproducibility of Benchmarked Deep RL Tasks: linked by Spinning Up; not separately cached, but discussed in Henderson.
- David Silver UCL RL course, Berkeley Deep RL course, and Deep RL Bootcamp: curriculum links from Spinning Up; useful for background, less directly research-taste.

[^nanda-explore]: Neel Nanda, "How I Think About My Research Process: Explore, Understand, Distill" (2025-04-26) - https://www.lesswrong.com/posts/hjMy4ZxS5ogA9cTYK/how-i-think-about-my-research-process-explore-understand ([cache](../docs/evidence/nanda_research_process_explore_understand_distill.md)).
[^nanda-key]: Neel Nanda, "My Research Process: Key Mindsets - Truth-Seeking, Prioritisation, Moving Fast" (2025-04-27) - https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL ([cache](../docs/evidence/nanda_research_process_key_mindsets.md)).
[^nanda-taste]: Neel Nanda, "My Research Process: Understanding and Cultivating Research Taste" (2025-05-01) - https://www.lesswrong.com/posts/Ldrss6o3tiKT6NdMm/my-research-process-understanding-and-cultivating-research ([cache](../docs/evidence/nanda_research_process_research_taste.md)).
[^nanda-draft]: Neel Nanda, shared/local draft, "My Model of the Research Process" - source file `/home/wassname/Downloads/[Shared Publicly] My Model of the Research Process_ Explore, Understand, Distill.md` ([cache](../docs/evidence/nanda_research_process_shared_draft.md)).
[^nanda-paper]: Neel Nanda, "Highly Opinionated Advice on How to Write ML Papers" (2025-05-12) - https://www.lesswrong.com/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers ([cache](../docs/evidence/nanda_highly_opinionated_ml_paper_writing.md)).
[^olah-taste]: Chris Olah, "Research Taste Exercises" (2021-01-09) - https://colah.github.io/notes/taste/ ([cache](../docs/evidence/olah_research_taste_exercises.md)).
[^steinhardt]: Jacob Steinhardt, "Research as a Stochastic Decision Process" - https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html ([cache](../docs/evidence/steinhardt_research_stochastic_decision_process.md)).
[^spinningup-graph]: Joshua Achiam, "Spinning Up as a Deep RL Researcher" (OpenAI, 2018-10-13) - https://spinningup.openai.com/en/latest/spinningup/spinningup.html ([research cache](../docs/evidence/spinningup_research_source_graph.md), [debugging cache](../docs/evidence/spinningup_researcher.md)).
[^rahtz]: Matthew Rahtz, "Lessons Learned Reproducing a Deep Reinforcement Learning Paper" (2018) - http://amid.fish/reproducing-deep-rl ([cache](../docs/evidence/amid_fish_reproducing_deep_rl.md)).
[^henderson]: Henderson et al., "Deep Reinforcement Learning that Matters" (AAAI 2018) - https://arxiv.org/abs/1709.06560 ([cache](../docs/evidence/henderson_2018_deep_rl_matters.md)).
[^schulman]: John Schulman, "Nuts and Bolts of Deep RL Research" (2016) - http://joschu.net/docs/nuts-and-bolts.pdf ([cache](../docs/evidence/joschu_nuts_and_bolts.md)).
[^irpan]: Alex Irpan, "Deep Reinforcement Learning Doesn't Work Yet" (2018) - https://www.alexirpan.com/2018/02/14/rl-hard.html ([cache](../docs/evidence/alexirpan_rl_hard.md)).
