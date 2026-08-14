# Shared Publicly: My Model of the Research Process - Neel Nanda (shared draft)

Source: https://docs.google.com/document/d/1YMkeMrhqsWxZcNDD9CIUWEK_DAOegeufnbc79U2hycg/edit (user-supplied link, 2026-08-15)
Author: Neel Nanda
Date: not dated in the draft; contains the material published 2025-04-26, 2025-04-27 and 2025-05-01, plus expanded stage-guide sections that never went to LessWrong.
Fetched-via: curl of the Google Docs plain-text export (/export?format=txt), 2026-08-15 (CLAUDE agent)
Fetch-status: full draft, 11318 words. Replaces a 902-word excerpt of a local download.
Use: practical stage guide for agents. The most operational source for ideation, exploration, understanding, distillation, failure modes, and the mentor role.

## Why this matters for agents

The published posts establish the frame. This local draft contains the useful agent checklist: when to ideate, when to explore, what counts as surface area, how to test hypotheses, how to refine evidence, and when to go back a stage.

---

How I Think About My Research Process: Explore, Understand, Distill
This is the first post in a sequence about how I think about and break down my research process. Post 2 is coming soon!


Thanks to Oli Clive-Griffin, Paul Bogdan, Shivam Raval and especially to Jemima Jones for feedback, and to my co-author Gemini 2.5 Pro - putting 200K tokens of past blog posts and a long voice memo in the context window is OP.
Introduction
Research, especially in a young and rapidly evolving field like mechanistic interpretability (mech interp), can often feel messy, confusing, and intimidating. Where do you even start? How do you know if you're making progress? When do you double down, and when do you pivot?
These are far from settled questions, but I’ve supervised 20+ papers by now, and have developed my own mental model of the research process that I find helpful. This isn't the definitive way to do research (and I’d love to hear other people’s perspectives!) but it's a way that has worked for me and others. 
My goal here is to demystify the process by breaking it down into stages and offering some practical advice on common pitfalls and productive mindsets for each stage. I’ve also tried to be concrete about what the various facets of ‘being a good researcher’ actually mean, like ‘research taste’. I’ve written this post for a mech interp audience, but hopefully it is useful for any empirical science with short feedback loops, and possibly even beyond that.
This guide focuses more on the strategic (high-level direction, when to give up or pivot, etc) and tactical (what to do next, how to prioritise, etc) aspects of research – the "how to think about it" rather than just the "how to do it." Some of skills (coding, reading papers, understanding ML/mech interp concepts) are vital for how to do it, but not in scope here (I recommend the ARENA curriculum and my paper reading list if you need to skill up). 
How to get started? Strategic and tactical thinking are hard skills, and it is rare to be any good at them when starting out at research (or ever tbh). The best way to learn them is by trying things, making predictions, seeing what you get right or wrong (i.e., getting feedback from reality), and iterating. Mentorship can substantially speed up this process by providing "supervised data" to learn from, but either way you ultimately learn by doing. 
I’ve erred towards making this post comprehensive, which may make it somewhat overwhelming. You do not need to try to remember everything in here! Instead think of it more as a guide for the high level things to keep in mind, and a source of advice for what to do at each stage. And, obviously, this is massively flavoured by my own subjective experience and may not generalise to you - I’d love to hear what other researchers think.
A cautionary note: Research is hard. Expect frustration, dead ends, and failed hypotheses. Imposter syndrome is common. Focus on the process and what you're learning. Take breaks, the total change to productive time is typically positive. Find sustainable ways to work. Your standards are likely too high.
The key stages
I see research as breaking down into a few stages:
* Ideation (Stage 0): Choose a problem
   * This can vary from a long, high-effort exploration across areas looking for a promising angle, to just being handed a problem by a mentor. 
      * Replicating and extending an existing paper can be a good starting point, especially if you don’t have an existing mentor.
   * This stage is crucial, and doing it well yourself often requires “research taste” (more on this later!). But if you have a mentor (or other high quality source of suggestions, like someone else’s research agenda) it can be quick to just lean on them, so I’m labelling it stage 0.
* Exploration (Stage 1): Gain surface area
   * Examples: My research streams, and my Othello research process write-up
   * At the start, your understanding of the problem is often vague. Naively, it’s easy to think of research as being about testing specific hypotheses, but in practice you often start out not even knowing the right questions to ask, or the most promising directions. The exploration stage is about moving past this.
      * E.g. starting with “what changes in an LLM during chat fine-tuning?” or even “I’m sure there’s something interesting about how chat models behave, let’s mess around and find out”
   * Your north star is just to gain information - do exploratory experiments, visualise data, follow your curiosity, prioritise moving fast.
   * Junior researchers often get stuck in the early stages of a project and don’t know what to do next. In my opinion this is because they think they are in the understanding stage, but are actually in the exploration stage.
      * That is, they think they ought to have a clear goal, and hypothesis, and obvious next step, and feel bad when they don’t. But this is totally fine and normal!
      * The solution is to have a toolkit of standard ways to gain surface area, brainstorm experiments that might teach something interesting, and be comfortable exploring a bunch and hoping something interesting happens.
   * Not having a clear goal/next step doesn’t mean that you don’t need to prioritise! Prioritise for information gain. 
      * Try to do a lot of experiments (and don’t be a perfectionist about finding the ‘best’ experiments!), visualise things in many different ways, ensure you’re always learning.
      * Frequently ask yourself “am I getting enough information per unit time?” If you haven’t learned anything recently, shake it up.
      * Having fast feedback loops and powerful, flexible tooling is absolutely crucial here.
   * Note: often most of the work in the exploration was about discovering the right kinds of questions to be asking, e.g. that where information was stored is an important and interesting question, crystallising that into a precise hypothesis is often easy after that.
      * This both means ‘identify the right questions to ask’, but also gain a deeper understanding and intuition of the domain so you can design experiments that make sense, and build a more gears-level model of why a certain question may or may not be true.
   * A key practical tip is to keep a highlights doc of particularly interesting results, this makes it easier to spot connections
* Understanding (Stage 2): Test Hypotheses
   * This stage begins when you understand the problem domain enough to have some specific hypotheses that you think are interesting - hypotheses you can write down, and have some idea of what evidence you could find to show if they’re true or false.
      * E.g. “do chat models store summarised information about the user prompt in the <end_of_turn> special token?”
   * Your north star is to gain evidence for and against these hypotheses
      * Here the prioritisation is a mix of goal-directed and exploratory - you often need to briefly dip back into explore mode as you realise your hypothesis was ill-posed, your experiment didn’t make sense, you get weird and anomalous results, etc.
      * Frequently ask yourself “what am I learning and is it relevant?”
   * The mark of a good researcher is a deep commitment to skepticism of your results. 
      * You’ll have hypotheses that are wrong, experiments that are inconclusive, beautiful methods that lose to dumb baselines, etc. This is totally fine and normal, and a part of the natural process of science, but emotionally can be pretty hard to accept.
      * This sounds obvious, but in practice this requires constant active effort, and if you are not actively doing this you’ll inevitably fall into traps. Always seek alternative explanations, seek and implement strong baselines, check for bugs, etc.
   * A surprisingly deep and nuanced skill is designing good experiments. I think of this as one fact of “research taste”
      * A great experiment elegantly, and conclusively distinguishes between several plausible hypotheses, validates non-trivial predictions made by one hypothesis, and is tractable to implement in practice.
         * This is an ideal rarely reached in practice but helpful to have in mind
      * My internal experience when generating good experiments is often that I try to simulate the world where hypothesis X is true, think through what this would mean and all the various implications of this, and notice if any can be turned into good experiments.
      * When reading papers, pay attention to the key experiments that their core claims hinge upon and ask yourself what made it important and how you might've thought of that experiment.
* Distillation (Stage 3): Compress, Refine, Communicate
   * This stage begins when you have enough evidence for you to be fairly convinced that your hypotheses are true/false
   * The north star here is to distill your research findings into concise, rigorous truth that you can communicate to the world
      * Compress your work into some concrete, well-scoped claims - something you could list in a few bullet points. Compress it as far as you can without losing the message. Readers will not take away more than a few claims.
         * How would you explain your work to a peer? How would you write a lightning talk?
      * Refine your evidence into a rigorous case for each key claim, enough to be persuasive to a skeptical observer
         * This is persuasive in the sense of “actually provide strong evidence”, not just writing well enough that people don’t notice flaws! This means sanity checks, statistical robustness, and strong baselines.
         * Note that this is a higher bar than convincing yourself, both since you’re aiming for a more skeptical observer and you need to make all the key evidence you’ve seen legible to an outsider.
         * You should spend a lot of time on red-teaming here - what could you be missing? What alternative hypotheses could explain your observations? What experiments could distinguish between them? Etc
      * Communicate these with a clear and concise write-up - make clear what your points are, what evidence you provide, and its limitations. Write to inform, not persuade - if you are clear (a high bar), and your results are interesting, people will likely appreciate your work.
         * The form of write-up doesn’t really matter - Arxiv paper, blog post, peer-reviewed paper, etc. It doesn’t need to be polished, it just needs to present the evidence clearly, and to have strong enough evidence to meaningfully inform someone’s opinion
   * People often over- or under-rate this stage
      * Some default to writing a paper with the main goal of getting accepted to a conference. This has obvious advantages but can also lead to warped thinking if you’re thinking about it from the start. E.g. choosing questions that look good rather than being important, or focusing on forms of evidence that reviewers will like or understand, rather than ruthlessly focusing on actually establishing what’s true.
      * Others think doing the write-up is wasting time better spent on research, and can be left to the last minute. I think it’s actually a great use of time, at least for the first draft! I typically recommend my scholars make a start on distillation a month before conference deadlines.
         * Writing things up forces you to clarify your understanding to yourself. You also often notice holes and missing experiments. A common anecdote is that people didn’t really understand their project until they wrote it up.
         * If you don’t communicate your research well, it’s very hard to have an impact with it! (or to get recognition and career capital)
   * Sometimes you’ll discover that actually things are way messier than thought. It’s important to acknowledge this, rather than denying inconvenient truths! Your ultimate goal is to find truth, not to produce an exciting paper. You may need to go back to understanding or even exploration - this is totally fine and normal, and does not mean you’ve screwed anything up.
Post 2 of the sequence, on key skills, is coming out soon - if you’re impatient you can read a draft of the whole sequence here.
Key Mindsets
This is post 2 of a sequence on my framework for doing and thinking about research. Start here.
Before I get into what exactly to do at each stage of the research process, it’s worth reflecting on the key mindsets that are crucial throughout the process, and how they should manifest at each stage.
I think the most important mindsets are:
* Truth-seeking: By default, many research insights will be false - finding truth is hard. It’s not enough to just know this, you must put in active effort to be skeptical and resist bias
* Prioritisation: You have finite time, and a lot of possible actions. Your project will live or die according to whether you pick good ones.
* Moving fast: You have finite time and a lot to do. This doesn’t just mean “push yourself to go faster” - there’s a lot of ways to eliminate inefficiency without sacrificing quality.
   * In particular, you must learn to act without knowing the “correct” next step, and avoid analysis paralysis.
Warning: It is extremely hard to be anywhere near perfect on one of these mindsets, let alone all three. I’m trying to describe an ideal worth aiming towards, but you should be realistic about the amount of mistakes you will make - I certainly am nowhere near the ideal on any of these! Please interpret this post as a list of ideals to aim for, not something to beat yourself up about failing to meet.
Truth Seeking
Our ultimate goal in doing research is to uncover the truth about what’s really going on in the domain of interest. The truth exists, whether I like it or not, and being a good researcher is about understanding it regardless. 
* This sounds pretty obvious. Who doesn't like truth? It’s easy to see this section, dismiss it as obvious and move on. But in practice this is extremely hard to achieve. 
   * We have many biases that cut against finding truth
   * Insufficient skepticism doesn't feel like insufficient skepticism from the inside. It just feels like doing research. 
* This means that you must be putting in constant active effort into ensuring your results are robust. This must be integrated into part of your research process - if you’re not, then there’s a good chance your results are BS.
   * “Just try harder to be skeptical” is empirically a fairly ineffective strategy
   * One of the most common reasons I dismiss a paper is because I see a simple and boring explanation for the author’s observations, and they didn’t test for it - this often renders the results basically worthless. 
      * I’d estimate that at least 50% of papers are basically useless due to insufficient skepticism
What does putting in active effort actually mean?
This takes different forms for the different stages:
* For exploration, the key failure mode is not being creative enough when thinking about hypotheses, getting attached to one or two ideas, and missing out on what’s actually going on. 
   * Resist the urge to move on to the understanding stage the moment you have a plausible hypothesis - are there any unexplained anomalies? Could you do more experiments to gain more surface area first? What other hypotheses could explain your results? Etc
   * The standard hypothesis testing framework can be misleading here, because it has an implicit frame of being able to list all the hypotheses. But actually, most of your probability mass should normally be on “something I haven’t thought of yet”
      * You should regularly zoom out and look for alternative hypotheses for your observations. Asking another researcher, especially a mentor is a great source of perspective, asking LLMs is very cheap and can be effective.
      * That said, I still often find it helpful to think in a Bayesian way when doing research - if I have two hypotheses, how likely was some piece of evidence under each, and how should I update? Exploration often finds scattered pieces of inconclusive evidence, and there’s a skill to integrating them well. 
   * It’s not too bad if you end up believing false things for a bit, the key thing is to move fast and reflexively try to falsify any beliefs you form, so you don’t get stuck in a rabbit hole based on false premises. This means it’s totally fine to investigate case studies and qualitative data, e.g. a deep dive into a single prompt. 
      * If you’re getting lots of (diverse) information per unit time you’ll notice any issues.
   * It is also an issue if you are too skeptical and don’t let yourself explore the implications of promising but unproven hypotheses, as this is crucial to designing good experiments
* For understanding, you want to be careful and precise about what your experiments actually show you, alternative explanations for your results, whether your experiments make sense on a conceptual level, etc.
   * Here the Bayesian frame is often helpful. It’s generally overkill to put explicit numbers on everything, but it reminds me to ask the question “was this observation more likely under hypothesis A or B”, not just whether it was predicted by my favourite hypothesis
   * In exploration it’s OK to be somewhat qualitative and case study focused, but here you want to be more quantitative. If you must do qualitative case studies, do them on randomly sampled things, (or at least several examples, if your sampling space is small) )since it’s so easy to implicitly cherry-pick
      * The one exception is if your hypothesis is “there exists at least one example of phenomenon X”, e.g. ‘we found multidimensional SAE latents’.
* For distillation, in addition to the above, it’s important to avoid the temptations of choosing a narrative that looks good, rather than the best way to communicate the truth.
   * E.g. publishing negative results
      * While it can be emotionally hard to acknowledge to myself that my results are negative, mechanistic interpretability has a healthy culture and I’ve gotten nothing but positive feedback for publishing negative results.
   * E.g. exaggerating results or stating an overconfident narrative to seem more publishable. 
      * I find it pretty easy to tell when a paper is doing this - generally you should care more about impressing the more experienced researchers in a field, who are least likely to be fooled by this! So I don’t even think it’s a good selfish strategy.
   * E.g. not acknowledging and discussing key limitations. 
      * If I notice a key limitation that a paper has not addressed or acknowledged, I think far less of the paper.
      * If a paper discusses limitations, and provides a nuanced partial rebuttal, I think well of it.
Prioritisation
Ultimately, time is scarce. The space of possible actions you can take when doing research is wide and open ended, and some are far more valuable than others. The difference between a failed and a great research project is often prioritisation skill. Improved prioritisation is one of the key sources of value I add as a mentor
* Fundamentally, good prioritisation is about having a clear goal (north star) in mind. 
   * You need good judgement about how well different actions achieve this goal
      * You need to actually make the time to think about how well actions achieve this goal!
   * You need to be ruthless about dropping less promising directions where necessary. 
      * But beware switching costs - if you switch all the time without exploring anything properly you’ll learn nothing!
* The goals at each stage are:
   * Ideation: Choose a fruitful problem
   * Exploration: Gain information and surface area on the problem
   * Understanding: Find enough evidence to convince you of some key hypotheses
   * Distillation: Distill your research into concise, well-supported truth, and communicate this to the world.
* Being great at prioritisation is pretty difficult, and requires good research taste, which will take a lot of time to develop. But there’s often basic mistakes and low-hanging fruit to improve, if you just try. 
   * The first step is just making time to stop and ask yourself “do I endorse what I’m doing, and could I be doing something better?”
      * This advice may seem obvious, but is deceptively hard to put into practice! You need regular prompts  Often it’s very easy to think of a better idea, but by default nothing prompts you to think.
   * I like to explicitly write goals down and regularly check in that they’re being achieved - it sounds obvious, but you would be shocked at how effective it is to ask people if they’re doing the best thing for the project goals. I think in 3 tiers of goals:
      * Goal: What is the overall north star of the project? (generally measured in months)
      * Sub-goal: What is my current bit of the project working towards (measured in weeks)
      * Objective: What is the concrete short-term outcome I am aiming for right now (measured in days, e.g. 1 week)
   * I recommend actually writing a plan, and estimate how long each step will take, at least for the current research stage you’re in. 
      * You don’t need to take it very seriously, and you’ll totally deviate a ton. 
      * But it forces you to think through the project, notice uncertainties you could ask someone about, question if parts are really necessary to achieve your goals.
      * This is most important for understanding & distillation, though can be useful for exploration
      * If you feel stuck, set a 5 minute timer and brainstorm possible things you could do! 
      * I typically wouldn’t spend more than a few hours on this
         * Unless you have a mentor giving high quality feedback - then it’s a great way to elicit their advice! 
         * But even then, feel free to deviate - mentors typically have good research priors, but you know way more about your specific problem than them, which can be enough to make better decisions than even a very senior researcher
* You need to prioritise at many different layers of abstraction, from deciding when to move on from an experiment to deciding which hypothesis to test first to deciding when to give up on testing a hypothesis and pivot to something else (or just back to exploration)
* Prioritising and executing are different mental modes and should not be done simultaneously. Keep them separate, and make time to regularly reflect, and time to lock-in and execute on a plan without stressing about if it’s the best plan
   * Concrete advice: Work to a schedule where you regularly (ideally at least once a day, and with extended reflection at least once a week), zoom out and check that what you’re doing is your highest priority. E.g. work in pomodoros
   * Having a weekly review can be incredibly useful -  where you zoom out and check in on what’s going on, any current issues, etc. Some useful prompts:
      * What is my goal right now?
      * What progress have I made towards that goal?
      * What’s consumed the most time recently?
      * What’s blocked me?
      * What mistakes have I made, and how could I systematically change my approach so it doesn’t happen again in future?
      * What am I currently confused about?
      * Am I missing something?
* See Jacob Steinhardt’s excellent blog post on research prioritisation.
* Warning: Different people need to hear different advice! (An eternal issue of writing public advice…). Some get stuck in rabbit holes and need to get better at moving on. Others get caught in analysis paralysis and never do anything, because they’re always waiting for the (non-existent) perfect opportunity. 
   * Real prioritisation is about a careful balance between exploration and exploitation.
   * You probably know which failure mode you tend towards. Please focus on the advice relevant to you, and ignore the rest!
Moving Fast
A core aspect of taking action in general is being able to move fast. Researchers vary a lot in their rate of productive output, and it gets very high in the best people - this is something I value a lot in potential hires. 


This isn’t just about working long hours or cutting corners - there’s a lot of skill to having fast feedback loops, noticing and fixing inefficiency where appropriate, and being able to take action or reflect where appropriate. In some ways this is just another lens onto prioritisation.


* Tight feedback loops are crucial: A key thing to track when doing research is your feedback loops. 
   * Definition: A feedback loop is the process from having an experiment idea and to results. Tight feedback loops are when the time taken is short.
   * It will make an enormous difference to your research velocity if you can get your feedback loops as tight as possible, and this is a big priority. 
      * This is because you typically start a project confused, and you need to repeatedly get feedback from reality to understand what’s going on. This inherently requires a bunch of feedback loops that can’t be parallelised, so you want them to be as short as possible.
      * This is one of the big advantages of mech interp over other fields of ML - we can get much shorter feedback loops.
   * A mindset that I often find helpful is a deep-seated sense of impatience and a feeling that something should be possible to do faster. Sometimes I just need to accept that it will take a while, but often there is a better way, or at least a way that things can be reduced.
   * Coding in a notebook is a lifesaver (eg Jupyter, VS Code Interactive Mode or Colab)
   * Tips for tight feedback loops in mech interp:
      * Putting your data in a data frame rather than in a rigid plotting framework like Weights and Biases allows you to try arbitrary visualizations rapidly. 
      * De-risking things on the smallest model you can, such as writing code and testing it on a small model before testing it on the model you're actually interested in. 
      * Train things on fairly small amounts of data just to verify that you're seeing signs of life.
      * Sometimes there’s irreducible length, e.g. you need to train a model/SAE and this takes a while, but you can still often do something - train on less data, have evals that let you fail fast, etc.
* Good tooling accelerates everything. All stages benefit from flexible exploration tools (e.g., interactive notebooks, libraries like TransformerLens or nnsight), efficient infrastructure for running experiments, and helpful utilities (e.g., plotting functions, data loaders). 
   * Flexible tooling tightens feedback loops by shortening the time between an arbitrary creative experiment idea and results, even if it’s less efficient for any given idea.
   * The balance shifts: more flexibility needed early, more optimization/robustness potentially useful later e.g. during the distillation stage it can make sense to write a library to really easily do a specific kind of fine-tuning run that happens a ton
* A corollary of this is that you should (often) do fast experiments first. It is far better to do a quick and dirty experiment to get some preliminary signs of life than an extremely long and expensive experiment that will produce conclusive data but only after weeks of work. 
   * Realistically you should be prioritising by information gain per unit time. 
   * This is especially important in exploration where it's hard to have a clear sense of which experiments are the most useful while estimating their tractability is pretty easy. When distilling you may know enough to be comfortable implementing a long running but conclusive experiment.
* Audit your time. It's all well and good to talk about the importance of speed and moving fast, but how do you actually do this in practice? One thing that might be helpful is to log how you spend your time and then reflect on it, and ways you might be able to go faster next time. 
   * For example, you could use a tool like Toggl to roughly track what you're doing each day and then look back on how long everything took you and ask, "How could I have done this faster? Was this a good use of my time?"
      * Often it’s easy to fix inefficiencies and the hard part is noticing them - e.g. making a util function for a common tedious task, or noticing things that an LLM could automate.
   * Note: It is not productive to look back and feel really guilty about wasting time. Nobody is perfect and you will always waste time. I am advocating for maintaining a mindset of optimism that you will be able to do even better next time.
* Fail fast. One of the largest time sinks possible is investing weeks to months of effort into a failed research direction. Thus, a key question to ask yourself is: if this direction is doomed, how could I discover this as fast as humanly possible? 
   * I often try to think through what kind of confident predictions a hypothesis I care about makes in the understanding stage, or what fundamental assumptions make me think my domain is interesting at all in the exploration stage, and then think of the quickest and dirtiest experiments I can to test these. 
      * It's often much better to have several quick and dirty experiments to attack different angles where you could fail fast than to put a lot of effort into one.
* Are you moving too fast? This is a natural pushback to the advice of ‘try hard to move fast’. It’s easy to e.g. be sloppy in the name of speed and introduce many bugs that cost you time in the long-run. 
   * This is a hard balance, and I largely recommend just exploring and seeing how things go. But there are often things that can speed you up beyond ‘just push yourself to go harder in the moment’, which don’t have these trade-offs, like choosing the right experiments to run.
   * Make sure you still regularly take time to think and reflect, rather than feeling pressure to constantly produce results
Taking action under uncertainty
A difficulty worth emphasising when trying to move fast is that there are a lot of possible next steps when doing research. And it’s pretty difficult to predict how they’ll go. Prioritisation remains crucial, but this means it’s also very hard, and you will be highly uncertain about the best next step. A crucial mindset is being able to do something anyway, despite being so uncertain.
* As a former pure mathematician, this is something I’ve struggled a fair bit with - I miss doing things grounded in pure, universal truth! But it’s learnable
* Ultimately, you just need to accept on an emotional level that you don’t get to know the “right” answer for what to do next - in practice, there’s no such thing as the right answer. 
   * The ideal is to strive to carefully evaluate the extremely noisy evidence, make a best guess for what to do next, and act on it, while also being self-aware enough to notice if it no longer seems the best action. This is a hard balance to achieve, but super useful if you can do it. 
* Especially when you’re starting out, this can be very low stakes: the value of anything you do is dominated by the learning value! If you make bad decisions you will learn and can do better next time, so it’s hard to really have a bad outcome.
Post 3 of the sequence, on research taste and stage 1 (ideation), is coming out soon - if you’re impatient you can read a draft of the whole sequence here.
The (Fuzzy) Stages of Research
Ideation (Stage 0): Choose a Problem
You can't do research without a question or a domain. Ideation is about finding fertile ground. It might be quick, eg deferring to a mentor, or it might involve significant exploration itself, with explorations of many unpromising domains before you settle on one.
What is research taste?
There's a semi-mystical notion of research taste that is often discussed, especially as a distinguishing factor between senior and junior researchers. It's described as a mystical ability to determine whether a research idea will work. I do think this is a real skill that improves over time and represents significant research experience - I’ve definitely improved at it over time and seen real positive results in my work. But it’s also pretty confusing and opaque, especially to junior researchers.


While research taste is important, there are many other crucial skills, and research taste itself comprises several distinct abilities that shouldn't be naively conflated. Rather than focusing solely on research taste, I’ve tried to break down the research process into concrete and specific skills. But it's worth examining the different facets of research taste within this framework. Note that this significantly overlaps with the value provided by a mentor.


Note - Chris Olah has an excellent short post on what research taste is and exercises to learn it. In this spirit, for each of the aspects of the below, I highly recommend predicting a mentor’s answer before asking. And, if they surprise you, probing into why they acted unexpectedly - this is fantastic supervised training data


Key aspects of research taste include:


* Problem Selection: High-level strategic judgment in determining which problems will be both tractable and interesting.
* Exploration: Tactical decision-making about which experiments will provide the most insight, distinguishing between interesting and mundane results, and effectively planning how to investigate promising findings.
* Understanding: Developing creative experiments that get to the core of a question, identifying important hypotheses worth proving, assessing their likelihood of being true, and recognizing when an experiment is inadequate.
* Communication: Identifying the core claims in your findings and what would be most interesting to an audience
Advice for Stage 1: How to Ideate?
* Find a Domain: You need something concrete to study. This could be a specific model (Pythia 2.8B), a specific phenomenon (grokking, factual recall), a specific capability (how models do addition), or a specific technique (improving SAEs).
   * Vague goals like "find a non-linear representation" are usually doomed without grounding in a specific context.
      * But if you brainstorm at least a specific context where you might find a non-linear representation, then it’s a fine approach.
   * Ideation ends when you have a clear enough question or domain that you can start generating concrete experiments to run
* Make or break: Ideation is very important - if you choose a problem that’s not an interesting question or doomed then it doesn’t matter what else you do, the project is sunk. 
   * One of the most common reasons I don’t read an interpretability paper is that I think it’s answering the wrong question
* High-level research taste: One facet of the general notion of ‘research taste’ is noticing which problems are promising and interesting.
   * This is really hard! It’s very difficult to get ‘training data’ for this, since a research project takes so long. When you’re starting out, you should not expect to be good at this.
* Leverage Mentors: Especially early on, it’s fine to let someone else do the work here, i.e. have a mentor recommend a problem. 
   * If you don’t have a mentor, try a natural extension of an existing paper you like, or pick a problem from a vetted open problems list,
   * This is basically borrowing someone else’s research taste, and IMO is one of the most valuable things I do for my mentees.
   * This is a bit nuanced - I’m not saying you should work on a project you don’t understand or aren’t excited about. And sometimes a problem suggested by a mentor sucks or is based on a flawed understanding - you should try to understand it, do a bit of exploration, and give up where appropriate. But ideally you’ll be able to find a problem that does catch your interest and that you can get excited about even if you didn’t come up with it.
   * A common mistake I see in junior researchers is “not invented here” syndrome, where they’re insistent about doing a problem they came up with, and think it’s admitting defeat or unoriginal to take a problem I recommend.
      * Empirically, most people new to mech interp have pretty bad research ideas. So, unfortunately, this strategy normally results in failure. 
         * Though occasionally I meet people new to the field with great, original ideas, so it’s not entirely doomed!
      * If you do strongly prefer your own research ideas, generating several and trying to get a more experienced researcher to vet them is much better than nothing. But be prepared to be told they’re all bad (and ask someone who you think is direct enough to say so…)
         * This is generally a good exercise even if you intend to take on a different idea tbh.
   * You may not grow as much directly at high-level research taste if you work on someone else’s idea. But I think working on a successful research project is more important and you’ll still learn a lot of useful things, which lead to better research taste.
   * Some people (somewhat including myself) are just very picky and only want to work on very specific problems that they came up with.
      * Honestly, I largely consider this a weakness as a researcher, though it does correlate with the strength of having good conceptual understanding of the problem and being highly motivated to work on it. But some people have the motivation, understanding and flexibility - a state to aspire to!
Facets of Research Taste
________________
Exploration (Stage 1): Gain Surface Area
* Goal: Gain understanding of the problem/domain, start to identify and crystallise interesting hypotheses.
   * Your north star is information gained per unit time/effort.
   * Crucially, Exploration is not about testing a specific hypothesis. Exploration is about gaining enough of an understanding of a domain that you know what the interesting hypotheses even are.
   * Taking my grokking work as an example: 
      * Ideation: I decided to focus on “what’s up with grokking”
      * Exploration: I trained a modular addition model, plotted a lot of things, and noticed that the PCA of the embedding is surprisingly periodic - it’s learning Fourier terms.
         * I then predicted that the model is doing addition with trig identities, and spent another few days playing around to guess the underlying circuit. 
      * Now I moved onto Understanding and tried to formalise and test this hypothesis.
   * Even if you end Ideation with a hypothesis, it’s still typically valuable to spend some time in Exploration rather than jumping to Understanding: generally exploring, testing variations of that hypothesis etc, and forming an intuition for why it’s true, how exactly to operationalise it, and how you might prove it.
* It’s OK to be confused: It’s totally normal to spend a large fraction of this stage feeling pretty confused about what’s going on. This is fine and does not mean that you’re failing! The key question is whether you feel like you are learning things and becoming less confused.
   * In particular, it’s easy to feel overwhelmed by prioritisation here, because often you start a project without knowing enough to know what the right goals even are. This is fine! You can always have the meta-goal of ‘am I learning things about the domain?’
* Mindset: Curiosity-driven, embrace confusion, prioritize speed, and low-cost experiments. 
   * Think breadth-first initially, but be willing to do short depth-first dives on interesting leads.
* Gaining surface area: A key concept here is surface area: knowledge and intuition about the domain/problem. Most of the way I prioritise is by asking myself what decisions would maximise my surface area on a problem/domain. I want to put myself in a position where I can notice cool patterns and phenomena and spark hypotheses about what’s going on.
   * This is a different mindset from what gains me rigorous evidence. Qualitative experiments, cherry-picked case studies, low sample size quick and dirty experiments, etc can all be high value for gaining surface area. 
      * While often the best way to test a specific hypothesis is with a narrow quantitative test with a large sample size, which teaches me little if I was asking the wrong questions.
So, how can you go about gaining surface area?
* Get Oriented:
   * Replicate/Baseline: If applicable, start by replicating key results from relevant papers or establishing simple baselines. What's the simplest version of this problem? What happens in a random network?
      * It can be productive to play around with toy models of a phenomenon, but I’m often wary of this - if you don’t understand the real phenomenon well enough, your toy models may not be accurate enough to teach you anything
   * Productive flailing: Use simple mech interp techniques wherever they seem applicable and look for patterns - you don’t need to have a plan in mind, just try lots of stuff quickly and see what sticks. Get your hands dirty with the model and data, so you build a mental bank of interesting phenomena, so you can notice connections
      * Some tactics to generally increase my surface area on a problem, by giving me more chances to notice some interesting patterns or structures:
         * Visualising data and activations, maybe with some dimensionality reduction like PCA or SVD
            * Note: Non-linear dimensionality reduction like t-SNE or UMAP are very hard to interpret correctly and often are useless.
         * Giving diverse inputs to a model and seeing what happens, including surgically changing specific tokens in an input to see the effects
         * Patching or ablating things that seem maybe interesting, or just sweeping across all layer/tokens
         * Looking at SAE latent activation or attribution
         * Doing logit lens
         * Designing ad hoc summary statistics and calculating/plotting them
         * Try simple probes to see what’s represented
   * Reach for a tool that might show you something interesting, and can be employed fast. Don’t hold yourself to the standard of tools that you’re confident are good.
* How to Make Progress:
   * Notice Weirdness: This is critical. Pay close attention to results that are surprising, counter-intuitive, inconsistent, or just feel off. Ask "Why?" relentlessly. These anomalies often point towards deeper insights.
      * This is an example of tactical research taste. I don’t have great advice on how to develop it beyond trying, getting more experience, and getting feedback from mentors on what is and is not interesting.
      * Some common things to look out for are sparsity (some components being particularly important) and structure (e.g. a graph that could have been random being straight or periodic, or two variables being surprisingly correlated)
   * Micro-Hypotheses: Generate small, speculative hypotheses ("Maybe head L5H6 is detecting syntax?") and devise quick ways to test them. Don't get attached; the goal is quick learning, not proof. The process of investigating this will often teach you something interesting. 
      * The important thing is to generate ideas at all, not to find the perfect ones. If you can test them fast, then it’s much better to come up with 10 ideas of which 1 is true, rather than 1 idea with a 50% chance of being true. The Understanding phase is where we start being more discriminating.
   * Information Gathering: Skim relevant papers (focus on motivation, methods, key results, limitations). Talk to people – explain what you're seeing, ask "dumb" questions, try to understand their models.
      * I think people often over-emphasise this, and that you’ll learn more from exploratory experiments, but it can be high value. The main issue is that your problem domain is often subtly different from what’s been studied before, and existing results may not transfer well.
* Advice for exploring well:
   * Research Log: Keep a detailed log (daily or per session). Note down: goals for the session, what you tried, observations (especially weird ones!), links to code/plots (eg to notebooks or git commits or saved plots), brief thoughts/interpretations, ideas for next steps. This fights confusion and helps track progress.
      * Often you’ll want to come back to a result from a while ago
      * This advice also applies to later stages!
      * People’s preferred software here differs. I personally like Roam (Obsidian, Dynalist, LogSeq etc are similar). Notion and Google Docs are also reasonable choices.
   * Highlights Doc: Separately, keep a running document of your most interesting findings, key graphs, and solidified insights. This helps distill progress and is useful for sharing/communicating.
      * A decent metric of progress is “did I add anything to my highlights doc recently”
   * Structured Flailing: Explicitly allocate time for generating ideas/experiments (breadth) vs. executing a specific one (depth). Reflect regularly (at least daily): "What did I learn? What's most confusing/interesting? What should I try next?"
   * Reflect/synthesise: If you ever feel stuck for ideas on how to explore, taking time to reflect on what exactly you’ve learned and what confusions remain can often be a productive way to get unstuck.
   * Create Fast Feedback Loops! This is a major benefit of mech interp - in some fields you can’t get any data for weeks or months, in mech interp it can be seconds or minutes. Optimize for quick iterations. If you have slow feedback loops fixing this is high priority.
      * Use the smallest model that can do your task. 
      * Favour cheap, partially-trusted metrics.
      * Work in interactive environments (Colab/Jupyter/VSCode Interactive Mode).
      * Build and use flexible tooling, e.g. TransformerLens was designed for this kind of exploration. 
         * It can be worth designing tooling for your project to speed yourself up. Generally for exploration I’d only design very quick or very general tooling. But when testing or refining hypotheses it can make sense to build more boutique stuff.
      * You want the time between having an experiment idea and seeing the results to be as short as possible.
      * Caveat: Sometimes the feedback loops are irreducibly long, eg they involve training a model/SAE. But you can often still get quick and dirty results by eg training on less data, making a smaller model, etc, but sometimes you just need to accept worse feedback loops.
* Failure Modes:
   * Analysis Paralysis: Getting stuck trying to understand everything perfectly before running code.
      * Solution: Bias towards action, then reflect. Keep experiments simple.
      * It can help to set a rule for yourself like, if I’ve spent more than 4 hours without running any code, I should just do a quick experiment.
   * Never Focusing: Flitting between too many ideas without digging deep enough into any promising ones. 
      * Solution: Timebox explorations. Check your research log – if you haven't learned anything concrete or refined your focus in e.g. 1-2 days (highly context-dependent!), maybe pick one thread and commit to a deeper dive for a set period.
   * Rabbit Holes: Spending too much time on minor, unpromising details or debugging intractable technical issues unrelated to the core question.
      * Solution: Set time limits for tangents. Ask if this detail is really essential for the phenomena you care about. Can you mock it out or simplify?
      * Figuring out what details are unpromising can be the hard part, of course. 
         * For example, a common rabbit hole I saw when people do circuit analysis on GPT-2 Small is that they find that deleting the first MLP layer makes performance go down loads on their task. People often thought this was really interesting since the effect size was so large. But actually, deleting the first MLP layer makes performance go way down on all inputs (a known phenomenon, and not super interesting) and was nothing to do with their task. This is easy for me to point out but can be hard for them to notice!
* Mentorship Role: Suggesting initial explorations & relevant resources, distinguishing genuinely weird results from known artifacts, providing sanity checks, helping prioritize which weirdness to pursue first.
* When to go back to problem selection? Sometimes this just isn’t very promising and you should go back to choosing a problem. When to do this is a complex question, but a good heuristic is when things seem to be messy and you’ve tried a bunch of things to gain surface area but not found interesting structure or hypotheses to investigate further
* When to move on to understanding? Once you have enough understanding of the problem to have identified one/a few hypotheses that seem plausible and interesting, you can move on to understanding them in more detail.
   * Note that, often, most of the work of the research project is identifying what the correct hypotheses are! This typically isn’t written up in papers, which is a shame, and gives quite a mistaken impression IMO
________________
Understanding (Stage 2): Test Hypotheses
* Goal: Rigorously testing specific, plausible hypotheses.
   * Your north star is convincing you that the hypotheses are true - prioritise actions by asking whether they will provide information that updates your beliefs about the hypothesis
   * For example, 
   * What’s the difference between the understanding stage and the distillation stage? It’s pretty fuzzy, but the key difference is that understanding is about finding sufficient evidence to convince you, refining is about convincing everyone else.
      * When you have lots of surface area on a problem, the evidence required to convince you can be fairly illegible to others, e.g. based on what you’ve seen from a bunch of qualitative examples, etc.
      * Further, Understanding often involves tweaking and reframing the hypotheses (or giving up entirely and going back to exploration), such that they are hopefully stable by the time you start refining
* Experiment design: 
   * Design High Information Experiments: Design experiments specifically to differentiate between your main hypothesis and the most plausible alternatives. Ask: "What prediction does H1 make that H2 contradicts?" Think like a Bayesian: what evidence is most likely under H1 relative to H2?
      * Avoid the mistake of looking for evidence predicted by H1 that’s also predicted by a bunch of other things!
   * Crucial skill: There’s a lot of skill that goes into spotting the right experiments to run - one that will get a lot of evidence distinguishing different hypotheses. This requires creativity, having a good conceptual understanding of what’s going on inside the model and why your hypothesis might be true, good skepticism so you find experiments that won’t have simpler explanations for their outcomes, and the technical skill to design experiments that you can run fast and reliably.
      * You can still do a lot without being good at this skill, but it’s worth tracking that this is a very useful thing to get better at - notice when papers have great experiments and learn from them, seek feedback on your experiments, etc.
   * Conceptual understanding: This is far easier if you have enough of an intuitive grasp of the key concepts of mech interp that you have an intuition for why the hypothesis might be true, or at least guesses. Often my best experiment ideas come from thinking about why the hypothesis should be true, and what other things should be true in that world.
   * Execute Carefully & Rigorously: Now is the time for more careful experiments. Consider controls, potential confounds, statistical significance (if applicable), and robustness checks. Increase sample sizes from Exploration (though even N=5 case studies can be much better than N=1). Document methods clearly.
      * Try harder to avoid cherry-picking here - sample random data points rather than just picking the most convenient ones
      * Use appropriate baselines - e.g. it’s not enough to show that your technique helps to lower a model’s performance on harmful tasks. Does a random vector do worse?
         * A valuable intuition to have in mind is that, by default, all numbers are meaningless because we lack any scale to compare them. E.g. if a probe gets 95% classification accuracy on some task, is this good? Is this bad? Hard to say without knowing more! Baselines are one way to get context to compare against.
   * Try Out Stronger Hypotheses: Often we have a somewhat vague hypothesis, like “late attention heads are important for this task”. Ideally we would make it specific, mechanistic, and ideally, falsifiable. But this has the problem that we don’t know the correct way to make it specific. One solution is to make an educated guess for a stronger hypothesis, like "Head L10H7 computes feature X using mechanism Y, which contributes Z to the output", and test it.
      * To make an educated guess it’s useful to have surface area and ensure you deeply understand the hypothesis, its moving parts, and why it's plausible.
   * Quantitative vs. Qualitative: Don't feel obligated to quantify everything if good qualitative analysis is more insightful. Randomly sampling examples and analyzing them carefully can be very effective, especially if quantification is difficult or misleading.
      * The right mindset is “what would it take to convince me that this is true”, not “what would be legible and defensible to other people”
   * Actively Seek Alternatives: Explicitly brainstorm other ways your observations could be explained. What are the simplest explanations? What known circuits or phenomena could be involved? What would a strong skeptic argue? (Crucial: Avoid getting tunnel vision on just one idea).
   * Failing fast: Aim for experiments with fast iteration loops, and where you’ll get strong evidence against your hypothesis fast (if it’s false) so you can move on. 
   * Types of evidence: I think of experiments as falling into four categories, it’s worth tracking which one:
      * Strong evidence: This will give a strong update for or against the hypothesis (the best kind!)
      * Big if true: Experiments that probably fail, but are a big deal for our hypothesis if they work.
         * E.g. if we have a vector in a thinking model that we think represents uncertainty, steer with it, and observe the model backtracking way more on a single prompt, this is strong evidence it’s something to do with uncertainty or backtracking. But if it doesn’t work it’s unclear what to think, there’s a lot of ways for steering to fail.
      * Sanity checks: Experiments that probably work but are a big deal against our hypothesis if they fail
         * E.g. if we think we’ve found the maths vector, and show that when we subtract it the model gets worse at maths problems, this is some evidence. But it also has many other explanations - subtracting any random vector generally degrades performance.
      * Weak evidence: This will give a weak update for or against the hypothesis (or maybe just be inconclusive)
* Failure Modes:
   * Poor Baselines/Controls: Comparing results against a weak or irrelevant null hypothesis, or failing to isolate the variable of interest. 
   * Weak Experiments: Running studies that don't effectively distinguish between the hypotheses you care about, even if they seem related.
   * Insufficient Skepticism: Missing simple alternative explanations, methodological flaws, or bugs. Solution: 
      * Explicitly list alternatives.
      * Get others (especially mentors) to red team your plans before you run them.
      * Actively try to break your hypothesis. Ask "What observation would make me abandon this?"
      * Define falsification criteria before running the experiment.
   * Technical Errors: Bugs or flawed analysis invalidating results. Solution: Code reviews, unit tests, sanity-checking outputs, and replicating results with different code paths if possible.
* Be Able to Discard False Hypotheses: Sometimes you’ll have a hypothesis that you’re really excited about, and it turns out to be false. This is OK! This is all just part of science. Move on and try new hypotheses, or write up your negative results if they’re interesting enough!
* Be exploratory: You should still be partially in explore mode in this stage - often your conception of the hypothesis, or the right kinds of experiment, will shift. This is an important part of the research process, not a sign that you screwed anything up!
   * As in the exploration stage, it’s really useful to have flexible tooling that lets you run a range of experiments fast, and rapidly go from idea to results. 
      * Often you have a clearer idea of what experiments you need to run and can make more specialised tooling. But don’t take this too far - you don’t want to shoehorn yourself into a specific kind of experiment, and restrict your ability to shift approach if you realise you’d made a mistaken assumption.
* Mentorship Role: Aggressively red teaming hypotheses and experimental designs. Suggesting crucial alternative hypotheses or experiments. Helping interpret confusing results. Conveying conceptual frameworks to make sense of findings. Pushing for higher standards of rigor and clarity.
* When to go back to exploration? When you experience enough negative results, and don’t think they’re interesting enough to write-up, you should return to exploration.
   * What makes negative results interesting? It’s often said that “negative results are results too”. This is kind of true, but nuanced. It depends on how interesting your hypothesis was. 
      * If you took a common prediction and falsified it, this is great science! 
      * If you used a standard technique in a standard way to learn something and then discovered it was false, this is fantastic work!
      * If you came up with a random hypothesis based on an anomaly you observed, that no one other than you had ever thought about, this is not interesting
      * There’s a grey area where you tried one of 20 ish reasonable approaches on a problem people care about - if you did your job right, then you’ve shown that one approach doesn’t work, which is useful, but it’s not clear if this means the other 19 will also fail. 
      * Empirically, when I’ve published negative results I’ve gotten an overwhelmingly positive reception for the scientific integrity - so many people are aware that it’s scary to release negative results and want to applaud the bravery that it actually feels more incentivised in some ways than positive results 
      * There seems to be an implicit pressure in academia to spin your negative results as somehow positive - p-hacking is a very egregious example, but there’s a bunch of other ways a narrative can be shaped to be positive.
         * I strongly recommend ignoring this, I think it’s super corrosive to doing good science, and will generally lose you respect from other researchers in your field, who’ll be able to notice
* When to move on to distillation? When you are fairly convinced of some hypotheses, and think they’re interesting enough to be worth communicating.
   * Note: When you’re starting out as a researcher, you should have a low bar for writing up your results (e.g. as a blog post)! It’s a good experience and helps you understand them better, even if they aren’t objectively very interesting.
________________
Distillation (Stage 3): Compress, Refine, Communicate
* Goal: Distill all the messy insights from your research into concise, rigorous truth to communicate it to the world.
   * Compress what you’ve learned into some key claims, something you can convey via a short series of bullet points
   * Refine the evidence that convinced you into clear, rigorous, legible experiments that provide strong evidence for the key claims
      * You may already have done this in the understanding stage, but often making them rigorous involves a bunch of further experiments - larger sample size, sanity checks, etc.
      * Refining is a lot of effort and could be considered its own stage, or a continuum with Understanding. I make it a subpart of distillation because I think it’s worth distinguishing experiments done to convince you of what’s true, and experiments done instrumentally to make proof others would believe (and to increase your confidence). Typically I’ll do refining after compressing the work into a clear narrative, so I know exactly what needs to be refined.
   * Communicate these clearly in a high quality write-up
      * The form factor doesn’t really matter: blog post, Arxiv paper, conference paper, private google doc, etc, whatever feels appropriate
      * This should not be an afterthought! If no one else understands your research it is useless
* Compress the Core Narrative: What are the most important takeaways? What's the simplest, truest story that explains your key findings and answers your initial research question? What have you learned?
   * A useful framing: “how would you explain your research to a friend?” or “how would you compress your findings into 150 words or less?” or “how would you give a lightning talk on this?”. You want something that’s a short series of bullet points.
   * It often helps to discuss your research with a range of people at this point - what are they interested in? What confuses them? What points do you keep emphasising and coming back to?
* Refine your evidence: 
   * North star: How can I build an evidence base that makes my key claims obviously correct?
      * Research is messy, so “obviously correct” is a high bar, but useful to aspire to IMO
   * Select Strongest Evidence: To start, choose the clearest, most convincing experiments, visualizations, and analyses that directly support your main claims. Ask: "What evidence best distinguishes my claims from alternatives? What would convince a knowledgeable skeptic?"
   * Red team your existing evidence: Then, red team this strongest evidence - if you were wrong, what’s the flaw in your case? What objections would an intelligent external researcher raise? If you presented this to a specific mentor what feedback do you think they’d give?
      * This is typically a mix of conceptual flaws, e.g. there are multiple hypotheses equally consistent with the data, and methodological laziness - poor baselines, low sample size, poor randomisation/cherry-picking, etc
      * Check Robustness: How general are the findings? Do they hold across different models/datasets/prompts (where applicable and feasible)? Sanity-check against known results.
   * Plan out experiments that would provide robust evidence covering the flaws in the existing evidence
      * By default, this looks like incremental improvements over the experiments done in Understanding, fixing various flaws (scaled up, across more models, higher sample size, implementing strong baselines, etc)
      * But it’s also great to include new experiment ideas, and it’s worth making time to brainstorm. Often red-teaming exposes holes in the existing evidence, and you can design new experiments to plug them
   * Actually do it (obviously)
* Communicate to the world: Produce a high quality write-up! (And actually share it)
   * Write iteratively: I recommend first writing a draft abstract, then the titles of each section, then a bullet point outline, then fleshing out the introduction into prose, then writing the entire thing in prose, then editing the abstract and intro based on insights from the writing so far.
      * Expect many rounds of refinement, both from feedback, and from you improving it, especially for concision, clarity and correctness
   * Choose the Right Medium: Don't default to an academic paper if a blog post, tweet thread, or internal report is more appropriate for your goals and audience. Find the truth first, then package it. Consider multiple communication forms for different audiences.
      * Should you try to write a conference paper? Some default to this, some would never consider it. 
         * I think this can be quite helpful and I often encourage my mentees to do it, it’s a good forcing function for rigor and clarity, and provides a deadline to actually ship something
         * But it can also be quite poisonous, because peer review is noisy and kinda BS, and incentivises a certain kind and style of paper, and it’s easy to get caught in the mindset of writing publishable papers, rather than purely seeking truth - I’ve seen this happen a fair bit. I try to only think about publishability late in the process, and sometimes put a truth-optimised paper on Arxiv and submit an academic-friendly edit.
   * Allocate time according to the number of readers: Many more people read your title > abstract > intro / figures > everything else > appendices. Accordingly, you should spend far more time per word on the title > abstract > … This often feels weird! But e.g. a good abstract can make or break a paper, in a way that screwing up a subsection doesn’t
      * Some researchers advocate for an equal time split between the 5 (excluding appendices). I have no clue how to spend 20% of my time on a badass title, but I like the spirit
   * Acknowledge limitations: Inevitably, your results will have some limitations - edge cases, ways your evidence could be wrong, etc. I strongly encourage you to discuss these clearly and prominently in a write-up, even if you don’t have good counters to it. This is a key part of doing good science.
      * Pragmatically, when I read a paper, I’ll generally notice at least some limitations anyway, and judge a paper if it ignores them and respect one that discusses them clearly even if it weakens the narrative - so if you’re optimising for experienced researchers liking your work, acknowledging limitations is generally in your interests
      * Your goal is to inform not persuade
   * Visualize Effectively: Invest time in high-quality plots and diagrams. Make them self-contained (clear axes, titles, legends). Ensure they directly illustrate the point you're making. Good visuals are often more impactful than dense text.
   * Iterate on Communication: Get feedback on drafts from peers and mentors. Pay attention to where readers get confused or unconvinced. Revise for clarity and impact. 
      * (Remember the illusion of transparency: what's clear to you might not be clear to others).
   * Research Debt is a good meditation on the costs of poor research communication
* Failure Modes:
   * Unclear or Overstated Claims: Making assertions that aren't fully supported by the evidence or failing to clearly define the scope.
   * Ignoring Limitations/Counterarguments: Undermining credibility by appearing biased or unaware of weaknesses.
   * Weak/Insufficient/Confusing Evidence: Failing to present the data in a way that clearly supports the claims.
   * Poor Communication: Obscuring valuable insights through jargon, lack of structure, or bad visualizations.
   * Trying to Persuade vs. Inform: Focusing on "selling" the result rather than objectively presenting the evidence and reasoning. Good researchers value truth-seeking over salesmanship.
   * Perfectionism/Yak Shaving: Getting lost in minor details or formatting tweaks while neglecting the core message and argument structure.
* Mentorship Role: Providing high-level feedback on the narrative structure, argument strength, and clarity. Identifying logical gaps, weak evidence, or unaddressed counterarguments. Advising on effective communication strategies, framing, and audience targeting.
* When to go back to Understanding? If you discover that your narrative no longer seems true/well supported, you should go back to Understanding
   * This is fine: It's totally natural that in the course of trying to refine your evidence and case, you discover you were wrong about something. Sometimes results from a few cherry-picked prompts don't generalize. This is the point of refining.
   * Switch mode: If you discover that you no longer think your list of key claims is true, then you should return to understanding or possibly even exploration. You may also want to pivot this into being a negative results paper if your experiments confidently show that your claims, which you thought were positive, were false. This could be of interest to others.
      * Don't get caught in the trap of thinking, "It would be inconvenient if I had to change my narrative because that would involve extra work." This easily results in producing false research, which is far worse than needing to put in extra effort. The truth is what it is, and you should strive to understand it, even if it is inconvenient.