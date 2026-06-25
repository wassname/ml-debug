# Research taste and research-process folklore

Appendix to the [ML Debugging skill](../SKILL.md).

Use this when the question is closer to "what should we try next?" than "why did this crash?" The quotes do most of the work here. The editorial is just routing.

## Patience and process

Research taste is learned under long, noisy feedback loops. This is the quote I would put nearest the main skill.

> Research taste isn't magic. It's a complex set of intuitions and frameworks built incrementally through experience, reflection, and learning from others. It governs the crucial, often implicit, decisions that shape a research project's success. Because the feedback loops for high-level strategic taste are long and noisy, don't expect to master it quickly. It's perfectly normal, and indeed expected, to rely heavily on external guidance (like mentors or established research directions) early in your career. Focus first on mastering the skills with shorter feedback loops – coding, running experiments, analyzing data, clearly communicating simple results. By actively engaging in research, deliberately reflecting on your decisions and their outcomes, and strategically leveraging the experiences of others, you can accelerate the development of your own research taste. Be patient with the process, especially the long-game aspects like problem selection. Trust that by doing the work and learning effectively from it, your intuition will improve over time.[^nanda-taste]

Olah gives the matching training-data frame:

> One of the most important aspects of growing as a researcher is developing research taste -- roughly, the ability to chose good problems to work on. I think the fundamental issue is that actually testing whether a research idea you come up with is good is very expensive. Often it takes months, so you only really get a few pieces of feedback on your taste every year. Many of the following exercises are really strategies for getting (proxy) feedback on more research ideas faster.[^olah-taste]

## What taste covers

The useful move is not "research taste = picking good projects". Nanda uses it for the hard judgment calls throughout a project.

> What is research taste? As I define it, research taste is far broader than just picking the right problem at the outset. Research is full of key decisions that will affect the future of the project, without an obvious way to find the right answer: from choosing the research problem itself, to identifying which anomalies are and are not worth exploring, distinguishing an experiment that will be compelling from one that’ll have inconclusive results, etc. I think of taste as the set of intuitions and good judgment that guide a researcher’s decisions throughout the research process, any time an ambiguous or open-ended decision like this arises. This can just be gut feeling, but also having conceptual frameworks you reason through, having novel ideas spark in your mind, etc.[^nanda-taste]

And the stage model:

> I see research as breaking down into a few stages:
> 1. Ideation - Choose a problem/domain to focus on
> 2. Exploration - Gain Surface area
>    1. North star: Gain information
> 3. Understanding - Test Hypotheses
>    1. North star: Convince yourself of a key hypothesis
> 4. Distillation - Compress, Refine, Communicate
>    1. North star: Compress your research findings into concise, rigorous truth that you can communicate to the world[^nanda-explore]

## Key mindsets

This is agent-steering material: truth-seeking, prioritization, moving fast, and acting under uncertainty.

> I think the most important mindsets are:
> * Truth-seeking: By default, many research insights will be false - finding truth is hard. It’s not enough to just know this, you must put in active effort to be skeptical and resist bias, lest you risk your research being worthless.
> * Prioritisation: You have finite time, and a lot of possible actions. Your project will live or die according to whether you pick good ones.
> * Moving fast: You have finite time and a lot to do. This doesn’t just mean “push yourself to go faster” - there’s a lot of ways to eliminate inefficiency without sacrificing quality.[^nanda-key]

> This means that you must be putting in constant active effort into ensuring your results are robust. This must be integrated into part of your research process - if you’re not, then there’s a good chance your results are BS. The standard hypothesis testing framework can be misleading here, because it has an implicit frame of being able to list all the hypotheses. But actually, most of your probability mass should normally be on “something I haven’t thought of yet”. Here the Bayesian frame is often helpful. It’s generally overkill to put explicit numbers on everything, but it reminds me to ask the question “was this observation more likely under hypothesis A or B”, not just whether it was predicted by my favourite hypothesis.[^nanda-key]

## Prioritisation and speed

Nanda's prioritisation advice is close to the GSD/UAT habit: write the goal, check whether the work is buying that goal, and separate choosing from executing.

> Ultimately, time is scarce. The space of possible actions you can take when doing research is wide and open ended, and some are far more valuable than others. The difference between a failed and a great research project is often prioritisation skill. Improved prioritisation is one of the key sources of value I add as a mentor Fundamentally, good prioritisation is about having a clear goal (north star) in mind. You need good judgement about how well different actions achieve this goal. You need to actually make the time to think about how well actions achieve this goal![^nanda-draft]

> Being great at prioritisation is pretty difficult, and requires good research taste, which will take a lot of time to develop. But there’s often basic mistakes and low-hanging fruit to improve, if you just try. The first step is just making time to stop and ask yourself “do I endorse what I’m doing, and could I be doing something better?” This advice may seem obvious, but is deceptively hard to put into practice! You need regular prompts  Often it’s very easy to think of a better idea, but by default nothing prompts you to think. I like to explicitly write goals down and regularly check in that they’re being achieved - it sounds obvious, but you would be shocked at how effective it is to ask people if they’re doing the best thing for the project goals.[^nanda-draft]

> I recommend actually writing a plan, and estimate how long each step will take, at least for the current research stage you’re in. You don’t need to take it very seriously, and you’ll totally deviate a ton. But it forces you to think through the project, notice uncertainties you could ask someone about, question if parts are really necessary to achieve your goals.[^nanda-draft]

> Prioritising and executing are different mental modes and should not be done simultaneously. Keep them separate, and make time to regularly reflect, and time to lock-in and execute on a plan without stressing about if it’s the best plan Concrete advice: Work to a schedule where you regularly (ideally at least once a day, and with extended reflection at least once a week), zoom out and check that what you’re doing is your highest priority. E.g. work in pomodoros Having a weekly review can be incredibly useful -  where you zoom out and check in on what’s going on, any current issues, etc.[^nanda-draft]

> Tight feedback loops are crucial: A key thing to track when doing research is your feedback loops. Definition: A feedback loop is the process from having an experiment idea and to results. Tight feedback loops are when the time taken is short. It will make an enormous difference to your research velocity if you can get your feedback loops as tight as possible, and this is a big priority.[^nanda-draft]

> A corollary of this is that you should (often) do fast experiments first. It is far better to do a quick and dirty experiment to get some preliminary signs of life than an extremely long and expensive experiment that will produce conclusive data but only after weeks of work. Realistically you should be prioritising by information gain per unit time. This is especially important in exploration where it's hard to have a clear sense of which experiments are the most useful while estimating their tractability is pretty easy.[^nanda-draft]

> Fail fast. One of the largest time sinks possible is investing weeks to months of effort into a failed research direction. Thus, a key question to ask yourself is: if this direction is doomed, how could I discover this as fast as humanly possible? I often try to think through what kind of confident predictions a hypothesis I care about makes in the understanding stage, or what fundamental assumptions make me think my domain is interesting at all in the exploration stage, and then think of the quickest and dirtiest experiments I can to test these. It's often much better to have several quick and dirty experiments to attack different angles where you could fail fast than to put a lot of effort into one.[^nanda-draft]

> Ultimately, you just need to accept on an emotional level that you don’t get to know the “right” answer for what to do next - in practice, there’s no such thing as the right answer. The ideal is to strive to carefully evaluate the extremely noisy evidence, make a best guess for what to do next, and act on it, while also being self-aware enough to notice if it no longer seems the best action. This is a hard balance to achieve, but super useful if you can do it. Especially when you’re starting out, this can be very low stakes: the value of anything you do is dominated by the learning value![^nanda-draft]

## Ideation

This is the most mentor-dependent stage. The quote is useful because it gives permission to borrow taste without pretending that borrowed taste is yours.

> You can't do research without a question or a domain. Ideation is about finding fertile ground. It might be quick, eg deferring to a mentor, or it might involve significant exploration itself, with explorations of many unpromising domains before you settle on one. Find a Domain: You need something concrete to study. This could be a specific model (Pythia 2.8B), a specific phenomenon (grokking, factual recall), a specific capability (how models do addition), or a specific technique (improving SAEs). Ideation ends when you have a clear enough question or domain that you can start generating concrete experiments to run[^nanda-draft]

> Make or break: Ideation is very important - if you choose a problem that’s not an interesting question or doomed then it doesn’t matter what else you do, the project is sunk. One of the most common reasons I don’t read an interpretability paper is that I think it’s answering the wrong question High-level research taste: One facet of the general notion of ‘research taste’ is noticing which problems are promising and interesting.[^nanda-draft]

> Leverage Mentors: Especially early on, it’s fine to let someone else do the work here, i.e. have a mentor recommend a problem. If you don’t have a mentor, try a natural extension of an existing paper you like, or pick a problem from a vetted open problems list, This is basically borrowing someone else’s research taste, and IMO is one of the most valuable things I do for my mentees.[^nanda-draft]

## Exploration

Exploration should feel different from proof. It is for gaining surface area.

> Goal: Gain understanding of the problem/domain, start to identify and crystallise interesting hypotheses. Your north star is information gained per unit time/effort. Crucially, Exploration is not about testing a specific hypothesis. Exploration is about gaining enough of an understanding of a domain that you know what the interesting hypotheses even are.[^nanda-draft]

> It’s OK to be confused: It’s totally normal to spend a large fraction of this stage feeling pretty confused about what’s going on. This is fine and does not mean that you’re failing! The key question is whether you feel like you are learning things and becoming less confused. Reach for a tool that might show you something interesting, and can be employed fast. Don’t hold yourself to the standard of tools that you’re confident are good. Notice Weirdness: This is critical. Pay close attention to results that are surprising, counter-intuitive, inconsistent, or just feel off. Ask "Why?" relentlessly.[^nanda-draft]

This matches the older debugging folklore about confusion and anomalies:

> It was only by following that confusion and realising that taking the difference between frames zeroed out the background that gave the hint of a problem with normalization. I’m not entirely sure how to make one’s mind do more of this, but my best guesses at the moment are:
> * Learn to recognise what confusion feels like.[^rahtz]

More exploration mechanics:

> Gaining surface area: A key concept here is surface area: knowledge and intuition about the domain/problem. Most of the way I prioritise is by asking myself what decisions would maximise my surface area on a problem/domain. I want to put myself in a position where I can notice cool patterns and phenomena and spark hypotheses about what’s going on. This is a different mindset from what gains me rigorous evidence. Qualitative experiments, cherry-picked case studies, low sample size quick and dirty experiments, etc can all be high value for gaining surface area. While often the best way to test a specific hypothesis is with a narrow quantitative test with a large sample size, which teaches me little if I was asking the wrong questions.[^nanda-draft]

> Productive flailing: Use simple mech interp techniques wherever they seem applicable and look for patterns - you don’t need to have a plan in mind, just try lots of stuff quickly and see what sticks. Get your hands dirty with the model and data, so you build a mental bank of interesting phenomena, so you can notice connections Reach for a tool that might show you something interesting, and can be employed fast. Don’t hold yourself to the standard of tools that you’re confident are good. Notice Weirdness: This is critical. Pay close attention to results that are surprising, counter-intuitive, inconsistent, or just feel off. Ask "Why?" relentlessly. These anomalies often point towards deeper insights.[^nanda-draft]

> Micro-Hypotheses: Generate small, speculative hypotheses ("Maybe head L5H6 is detecting syntax?") and devise quick ways to test them. Don't get attached; the goal is quick learning, not proof. The process of investigating this will often teach you something interesting. The important thing is to generate ideas at all, not to find the perfect ones. If you can test them fast, then it’s much better to come up with 10 ideas of which 1 is true, rather than 1 idea with a 50% chance of being true. The Understanding phase is where we start being more discriminating.[^nanda-draft]

> Research Log: Keep a detailed log (daily or per session). Note down: goals for the session, what you tried, observations (especially weird ones!), links to code/plots (eg to notebooks or git commits or saved plots), brief thoughts/interpretations, ideas for next steps. This fights confusion and helps track progress. Highlights Doc: Separately, keep a running document of your most interesting findings, key graphs, and solidified insights. This helps distill progress and is useful for sharing/communicating. A decent metric of progress is “did I add anything to my highlights doc recently”[^nanda-draft]

> Create Fast Feedback Loops! This is a major benefit of mech interp - in some fields you can’t get any data for weeks or months, in mech interp it can be seconds or minutes. Optimize for quick iterations. If you have slow feedback loops fixing this is high priority. Use the smallest model that can do your task. Favour cheap, partially-trusted metrics.[^nanda-draft]

> Analysis Paralysis: Getting stuck trying to understand everything perfectly before running code. Solution: Bias towards action, then reflect. Keep experiments simple. It can help to set a rule for yourself like, if I’ve spent more than 4 hours without running any code, I should just do a quick experiment.[^nanda-draft]

> When to go back to problem selection? Sometimes this just isn’t very promising and you should go back to choosing a problem. When to do this is a complex question, but a good heuristic is when things seem to be messy and you’ve tried a bunch of things to gain surface area but not found interesting structure or hypotheses to investigate further When to move on to understanding? Once you have enough understanding of the problem to have identified one/a few hypotheses that seem plausible and interesting, you can move on to understanding them in more detail. Note that, often, most of the work of the research project is identifying what the correct hypotheses are! This typically isn’t written up in papers, which is a shame, and gives quite a mistaken impression IMO[^nanda-draft]

## Think more, experiment less

This is from Rahtz and belongs in the main skill too.

> Switching from experimenting a lot and thinking a little to experimenting a little and thinking a lot was a key turnaround in productivity. When debugging with long iteration times, you really need to pour time into the hypothesis-forming step - thinking about what all the possibilities are, how likely they seem on their own, and how likely they seem in light of everything you've seen so far. Spend as much time as you need, even if it takes 30 minutes, or an hour. Reserve experiments for once you've fleshed out the hypothesis space as thoroughly as possible and know which pieces of evidence would allow you to best distinguish between the different possibilities. It's especially important to be deliberate about this if you're working on something as a side project.[^rahtz]

## Understanding

Understanding is where hypotheses become objects to test.

> Design High Information Experiments: Design experiments specifically to differentiate between your main hypothesis and the most plausible alternatives. Ask: "What prediction does H1 make that H2 contradicts?" Think like a Bayesian: what evidence is most likely under H1 relative to H2? Avoid the mistake of looking for evidence predicted by H1 that’s also predicted by a bunch of other things! Use appropriate baselines - e.g. it’s not enough to show that your technique helps to lower a model’s performance on harmful tasks. Does a random vector do worse?[^nanda-draft]

> Actively Seek Alternatives: Explicitly brainstorm other ways your observations could be explained. What are the simplest explanations? What known circuits or phenomena could be involved? What would a strong skeptic argue? Mentorship Role: Aggressively red teaming hypotheses and experimental designs. Suggesting crucial alternative hypotheses or experiments. Helping interpret confusing results. Conveying conceptual frameworks to make sense of findings. Pushing for higher standards of rigor and clarity.[^nanda-draft]

Steinhardt's de-risking frame is the same habit in a different language:

> This reveals that harder tasks should not necessarily be prioritized. Rather, we should prioritize tasks that are more likely to fail (so that we remove the risk of them failing) but also tasks that take less time. Do the components in order from most informative per unit time to least informative per unit time. De-risk all components (to the extent feasible), then execute.[^steinhardt]

More understanding mechanics:

> Execute Carefully & Rigorously: Now is the time for more careful experiments. Consider controls, potential confounds, statistical significance (if applicable), and robustness checks. Increase sample sizes from Exploration (though even N=5 case studies can be much better than N=1). Document methods clearly. Try harder to avoid cherry-picking here - sample random data points rather than just picking the most convenient ones Use appropriate baselines - e.g. it’s not enough to show that your technique helps to lower a model’s performance on harmful tasks. Does a random vector do worse?[^nanda-draft]

> Types of evidence: I think of experiments as falling into four categories, it’s worth tracking which one: Strong evidence: This will give a strong update for or against the hypothesis (the best kind!) Big if true: Experiments that probably fail, but are a big deal for our hypothesis if they work.[^nanda-draft]

> Sanity checks: Experiments that probably work but are a big deal against our hypothesis if they fail Weak evidence: This will give a weak update for or against the hypothesis (or maybe just be inconclusive) Poor Baselines/Controls: Comparing results against a weak or irrelevant null hypothesis, or failing to isolate the variable of interest.[^nanda-draft]

> Insufficient Skepticism: Missing simple alternative explanations, methodological flaws, or bugs. Explicitly list alternatives. Get others (especially mentors) to red team your plans before you run them. Actively try to break your hypothesis. Ask "What observation would make me abandon this?"[^nanda-draft]

> Be Able to Discard False Hypotheses: Sometimes you’ll have a hypothesis that you’re really excited about, and it turns out to be false. This is OK! This is all just part of science. Move on and try new hypotheses, or write up your negative results if they’re interesting enough! Be exploratory: You should still be partially in explore mode in this stage - often your conception of the hypothesis, or the right kinds of experiment, will shift. This is an important part of the research process, not a sign that you screwed anything up! When to move on to distillation? When you are fairly convinced of some hypotheses, and think they’re interesting enough to be worth communicating.[^nanda-draft]

## Rigorous comparisons

Spinning Up is RL-framed but generally useful for research agents doing method comparisons.

> Set up fair comparisons. If you implement your baseline from scratch [...] it's important to spend as much time tuning your baseline as you spend tuning your own algorithm. This will make sure that comparisons are fair. Also, do your best to hold "all else equal" [...]. Under no circumstances handicap the baseline! Remove stochasticity as a confounder. Beware of random seeds making things look stronger or weaker than they really are, so run everything for many random seeds (at least 3, but if you want to be thorough, do 10 or more). Run high-integrity experiments. Don't just take the results from the best or most interesting runs to use in your paper.[^spinningup]

Schulman and Henderson are the harder-edged RL versions:

> Always Be Ablating
> - Different tricks may substitute
> - Especially whitening
> - “Regularize” to favor simplicity in algorithm design space
> - As usual, simplicity → generalization[^schulman]

> Without significance metrics and tighter standardization of experimental reporting, it is difficult to determine whether improvements over the prior state-of-the-art are meaningful. In this paper, we investigate challenges posed by reproducibility, proper experimental techniques, and reporting procedures. We illustrate the variability in reported metrics and results when comparing against common baselines and suggest guidelines to make future results in deep RL more reproducible.[^henderson]

## Distillation and paper writing

This belongs in the appendix more than the main skill, but it is the right source for "when do I write this up?"

> The essence of an ideal paper is the narrative: a short, rigorous and evidence-based technical story you tell, with a takeaway the readers care about. The first step is to compress your research into these claims. Experimental Evidence: This is absolutely crucial to get right and aggressively red-team, it’s how you resist the temptation of elegant but false narratives.[^nanda-paper]

> At its core, a paper should present a narrative of one to three specific concrete claims that you believe to be true, that build to some useful takeaway(s). Readers will rarely take away more than a few sentences of content. Choose those sentences carefully. Generally, stronger statements make for more interesting papers, but require higher standards of evidence - resist the temptation to overclaim for clicks![^nanda-paper]

> The Guiding Question for Evidence: Ultimately, the question to ask about your evidence is: "Should this update a reader's beliefs about my claims?" Reproducibility & Publishing code: Rigour can be in the eye of the beholder: if readers cannot understand or verify it for themselves, it’s far harder to consider it rigorous. A key challenge in paper writing is the illusion of transparency - you have spent months steeped in the context of this research project.[^nanda-paper]

From the shared draft:

> Goal: Distill all the messy insights from your research into concise, rigorous truth to communicate it to the world. Compress what you’ve learned into some key claims, something you can convey via a short series of bullet points Refine the evidence that convinced you into clear, rigorous, legible experiments that provide strong evidence for the key claims[^nanda-draft]

> Compress the Core Narrative: What are the most important takeaways? What's the simplest, truest story that explains your key findings and answers your initial research question? What have you learned? A useful framing: “how would you explain your research to a friend?” or “how would you compress your findings into 150 words or less?” or “how would you give a lightning talk on this?”. You want something that’s a short series of bullet points. It often helps to discuss your research with a range of people at this point - what are they interested in? What confuses them? What points do you keep emphasising and coming back to?[^nanda-draft]

> Refine your evidence North star: How can I build an evidence base that makes my key claims obviously correct? Research is messy, so “obviously correct” is a high bar, but useful to aspire to IMO Select Strongest Evidence: To start, choose the clearest, most convincing experiments, visualizations, and analyses that directly support your main claims. Ask: "What evidence best distinguishes my claims from alternatives? What would convince a knowledgeable skeptic?"[^nanda-draft]

> Red team your existing evidence: Then, red team this strongest evidence - if you were wrong, what’s the flaw in your case? What objections would an intelligent external researcher raise? If you presented this to a specific mentor what feedback do you think they’d give? This is typically a mix of conceptual flaws, e.g. there are multiple hypotheses equally consistent with the data, and methodological laziness - poor baselines, low sample size, poor randomisation/cherry-picking, etc Check Robustness: How general are the findings? Do they hold across different models/datasets/prompts (where applicable and feasible)? Sanity-check against known results.[^nanda-draft]

> Acknowledge limitations: Inevitably, your results will have some limitations - edge cases, ways your evidence could be wrong, etc. I strongly encourage you to discuss these clearly and prominently in a write-up, even if you don’t have good counters to it. This is a key part of doing good science. Pragmatically, when I read a paper, I’ll generally notice at least some limitations anyway, and judge a paper if it ignores them and respect one that discusses them clearly even if it weakens the narrative - so if you’re optimising for experienced researchers liking your work, acknowledging limitations is generally in your interests Your goal is to inform not persuade[^nanda-draft]

> When to go back to Understanding? If you discover that your narrative no longer seems true/well supported, you should go back to Understanding This is fine: It's totally natural that in the course of trying to refine your evidence and case, you discover you were wrong about something. Sometimes results from a few cherry-picked prompts don't generalize. This is the point of refining. Switch mode: If you discover that you no longer think your list of key claims is true, then you should return to understanding or possibly even exploration.[^nanda-draft]

## Agent habit

Minimal loop:

1. Name the stage.
2. Quote the north star for that stage.
3. Pick the action with the best information per unit time.
4. Say what would change your mind.
5. Preserve proof in a log, plot, table, commit, or source quote.

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
[^spinningup]: Joshua Achiam, "Spinning Up as a Deep RL Researcher" (OpenAI, 2018-10-13) - https://spinningup.openai.com/en/latest/spinningup/spinningup.html ([research cache](../docs/evidence/spinningup_research_source_graph.md), [debugging cache](../docs/evidence/spinningup_researcher.md)).
[^rahtz]: Matthew Rahtz, "Lessons Learned Reproducing a Deep Reinforcement Learning Paper" (2018) - http://amid.fish/reproducing-deep-rl ([cache](../docs/evidence/amid_fish_reproducing_deep_rl.md)).
[^henderson]: Henderson et al., "Deep Reinforcement Learning that Matters" (AAAI 2018) - https://arxiv.org/abs/1709.06560 ([cache](../docs/evidence/henderson_2018_deep_rl_matters.md)).
[^schulman]: John Schulman, "Nuts and Bolts of Deep RL Research" (2016) - http://joschu.net/docs/nuts-and-bolts.pdf ([cache](../docs/evidence/joschu_nuts_and_bolts.md)).
[^irpan]: Alex Irpan, "Deep Reinforcement Learning Doesn't Work Yet" (2018) - https://www.alexirpan.com/2018/02/14/rl-hard.html ([cache](../docs/evidence/alexirpan_rl_hard.md)).
