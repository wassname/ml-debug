# ML Engineering for AI Safety & Robustness - Catherine Olsson and 80,000 Hours (2018-11)

Source: https://80000hours.org/articles/ml-engineering-career-transition-guide/
Authors: Catherine Olsson and the 80,000 Hours team
Date: Published November 2018; update note visible Feb 2022
Fetch-status: full article text, fetched 2026-08-15 via `curl https://r.jina.ai/https://80000hours.org/articles/ml-engineering-career-transition-guide/`. (CLAUDE agent)
Use: source-graph evidence from Spinning Up's "Other Resources" section; useful for research-engineer skill acquisition, less central to research taste.

## Why this matters for agents

This source is more about becoming useful on ML research teams than choosing research ideas. Its most relevant claim is that implementing and debugging foundational algorithms is a high-value learning path, with easy environments, metrics, and reference-code scrutiny.

## Source graph

This page was linked from Spinning Up's "Other Resources" section. It points to Josh Achiam's Key Papers in Deep RL list and a Daniel Ziegler self-study path. It is useful background for training agents to value implementation and debugging practice, but probably secondary for a dedicated research-taste skill.

## Full article

Technical AI safety is a multifaceted area of research, with many sub-questions in areas such as reward learning, robustness, and interpretability. These will all need to be answered in order to [make sure AI development will go well for humanity](https://80000hours.org/problem-profiles/positively-shaping-artificial-intelligence/) as systems become more and more powerful.

Not all of these questions are best tackled with abstract mathematics research; some can be approached with concrete coding experiments and machine learning (ML) prototypes. As a result, some AI safety research teams are looking to hire a growing number of Software Engineers and ML Research Engineers.

Additionally, some research teams that may not think of themselves as focussed on ‘AI Safety’ per se, nonetheless work on related problems like verification of neural nets or learning from human feedback, and are often hiring engineers.

> _Note that this guide was written in November 2018 to complement [**an in-depth conversation on the 80,000 Hours Podcast with Catherine Olsson and Daniel Ziegler**](https://80000hours.org/podcast/episodes/olsson-and-ziegler-ml-engineering-and-safety/) on how to transition from computer science and software engineering in general into ML engineering, with a focus on alignment and safety. If you like this guide, we’d strongly encourage you to check out the podcast episode where we discuss some of the instructions here, and other relevant advice._

_Update Feb 2022: The need for software engineers in AI safety seems even greater today than when this post was written (e.g. see [this post](https://forum.effectivealtruism.org/posts/DDDyTvuZxoKStm92M/ai-safety-needs-great-engineers) by Andy Jones). You also don’t need as much knowledge of AI safety to enter the field as this guide implies._

Table of Contents

*   [1 What are the necessary qualifications for these positions?](https://80000hours.org/articles/ml-engineering-career-transition-guide/#what-are-the-necessary-qualifications-for-these-positions)
*   [2 How can I best learn Machine Learning engineering skills if I don’t yet have the necessary experience?](https://80000hours.org/articles/ml-engineering-career-transition-guide/#how-can-i-best-learn-machine-learning-engineering-skills-if-i-dont-yet-have-the-necessary-experience)
    *   [2.1 Initial investigation](https://80000hours.org/articles/ml-engineering-career-transition-guide/#initial-investigation)
    *   [2.2 ML basics](https://80000hours.org/articles/ml-engineering-career-transition-guide/#ml-basics)
    *   [2.3 Learn ML implementation and debugging, and speak with the team you want to join](https://80000hours.org/articles/ml-engineering-career-transition-guide/#learn-ml-implementation-and-debugging-and-speak-with-the-team-you-want-to-join)
    *   [2.4 Case study: Daniel Ziegler’s ML self-study experience](https://80000hours.org/articles/ml-engineering-career-transition-guide/#case-study-daniel-zieglers-ml-self-study-experience)

*   [3 Now apply for jobs](https://80000hours.org/articles/ml-engineering-career-transition-guide/#now-apply-for-jobs)
*   [4 Learn more](https://80000hours.org/articles/ml-engineering-career-transition-guide/#learn-more)

## What are the necessary qualifications for these positions?

**Software Engineering:** Some engineering roles on AI safety teams do _not_ require ML experience. You might already be prepared to apply to these positions if you have the following qualifications:

*   BSc/BEng degree in computer science or another technical field (or comparable experience)
*   Strong knowledge of software engineering (as a benchmark: could pass a Google software engineering interview)
*   Interest in working on AI safety
*   (usually) Willingness to move to London or the San Francisco Bay Area

If you’re a software engineer with an interest in these roles, you may not need any additional preparation, and may be ready to _[apply right away](https://jobs.80000hours.org/?refinementList%5Btags\_area%5D%5B0%5D=AI+safety+%26+policy&refinementList%5Btags\_skill%5D%5B0%5D=Software+engineering&jb\_source=articles\_\_ml-engineering-career-transition-guide)_.

**ML Engineering and/or Research Engineering**: Some roles require experience implementing and debugging machine learning algorithms. If you don’t yet have ML implementation experience, you may be able to learn the necessary skills quickly, so long as you’re willing to spend a few months studying. Before deciding to do this, you should check that you meet all the following criteria:

*   BSc/BEng degree in computer science or another technical field (or comparable experience)
*   Strong knowledge of software engineering (as a benchmark: could pass a Google software engineering interview)
*   Interest in working on AI safety
*   (usually) Willingness to move to London or the San Francisco Bay Area

## How can I best learn Machine Learning engineering skills if I don’t yet have the necessary experience?

### Initial investigation

Implementing and debugging ML algorithms is different from traditional software engineering. The following can help you determine whether you’ll like the day-to-day work:

*   Matthew Rahtz’s blog post [Lessons Learned Reproducing a Deep Reinforcement Learning Paper](http://amid.fish/reproducing-deep-rl)
*   S. Zayd Enam’s blog post [Why is machine learning “hard”?](http://ai.stanford.edu/~zayd/why-is-machine-learning-hard.html)

### ML basics

If you don’t have any experience in machine learning, start by familiarizing yourself with the basics. If you have _some_ experience, but haven’t done a hands-on machine learning project recently, it’s also probably a good idea to brush up on the latest tools (writing TensorFlow, starting a virtual machine with a GPU, etc).

Although it can be difficult to find time for self-study if you’re already employed full-time or have other responsibilities, it’s far from impossible. Here are some ideas of how you might get started:

*   Consider spending a few hours a week on an online course. We recommend either of these two:
    *   The [fast.ai](http://course.fast.ai/) online course, “Practical Deep Learning For Coders, Part 1”
    *   Google’s [ML Crash Course](https://developers.google.com/machine-learning/crash-course/ml-intro)

*   If you’re employed full-time in a software engineering role, you might be able to learn ML basics without leaving your current job:
    *   If you’re at a large tech company, take advantage of internal trainings, including full-time ML rotation programs.
    *   Ask your manager if you can incorporate machine learning into your current role: for example, to spend 20% of your time learning ML, to see if it could improve one of the projects you work on.

For simple ML problems, you can get pretty far just on CPU on your laptop, but for larger problems it’s useful to buy a GPU and/or rent some cloud GPUs. You can often get some cloud computing credits through a [free trial](https://cloud.google.com/free/), [educational credits](https://aws.amazon.com/education/awseducate/) for students, or asking a friend with a startup.

### Learn ML implementation and debugging, and speak with the team you want to join

Once you know the 101-level basics of ML, the next thing to learn is how to _implement_ and _debug_ ML algorithms. (Based on the experiences of others in the community who have taken this path, we expect this to take at minimum 200 hours of focused work, and likely more if you are starting out with less experience).

Breadth of experience is not important here: you don’t need to read all the latest papers, or master an extensive reading list. You also don’t need to do novel research or come up with new algorithms. Nor do you need to focus on safety at this stage; in fact, focusing on well-known and established ML algorithms is probably better for your learning.

What you _do_ need is to get your hands dirty implementing and debugging ML algorithms, and to build evidence for job interviews that you have some experience doing this.

You should strongly consider _contacting the teams you’re interested in_ at this stage. Send them an email with the specifics of what you’re planning on spending your time on to get feedback on it. The manager of the team may suggest specific resources to use, and can help you avoid wasting time on extraneous skills you don’t need for the role.

The most straightforward way to gain this experience is to choose a subfield of ML relevant to a lab you’re interested in. Then read a few dozen of the subfield’s key papers, and reimplement a few of the foundational algorithms that the papers are based on or reference most frequently. Potential sub-fields include the following:

*   Deep reinforcement learning
*   Defenses against adversarial examples
*   Verification and robustness proofs for neural nets
*   Interpretability & visualization

If it isn’t clear how to get started – for example, if you don’t have access to a GPU, or don’t know how to write TensorFlow – many of the resources in the “basics” section above have useful tips.

If you need to quit your job to make time for learning in this phase, but don’t have enough runway to self-fund your studies, consider applying for an [EA grant](https://www.effectivealtruism.org/grants/) when it next opens – they are open to funding career transitions such as this one.

### Case study: Daniel Ziegler’s ML self-study experience

In January 2018, Daniel had strong software engineering skills but only basic ML knowledge. He decided that he wanted to work on an AI safety team as a research engineer, so he talked to Dario Amodei (the OpenAI Safety team lead). Based on Dario’s advice, Daniel spent around six full-time weeks diving into deep reinforcement learning together with a housemate. He also spent a little time reviewing basic ML and doing supervised learning on images and text. Daniel then interviewed and became an ML engineer on the safety team.

Daniel and his housemate used Josh Achiam’s [Key Papers in Deep RL](https://docs.google.com/document/d/1t55CCHabmHmrJ1VRoOSmQmR9lHkClAPxOlYGuvmof2Q/edit) list to guide their efforts. They got through about 20-30 of those papers, spending maybe 1.5 hours independently reading and half an hour discussing each paper.

More importantly, they implemented a handful of the key algorithms in TensorFlow:

*   Q-learning: DQN and some of its extensions, including prioritized replay and double DQN
*   Policy gradients: A2C, PPO, DDPG

They applied these algorithms to try to solve various [OpenAI Gym](https://github.com/openai/gym) environments, from the simple ‘Cartpole-v0’ to Atari games like ‘Breakout-v4’.

They spent 2-10 days on each algorithm (in parallel as experiments ran), depending on how in-depth they wanted to go. For some, they only got far enough to have a more-or-less-working implementation. For one (PPO), they tried to fix bugs and tune things for long enough to come close to the performance of the OpenAI Baselines implementation.

For each algorithm, they would first test on very easy environments, and then move to more difficult environments. Note that an easy environment for one algorithm may not be easy for another: for example, despite its simplicity, the Cartpole environment has a long time horizon, which can be challenging for some algorithms.

Once the algorithm was partially working, they would attain higher performance by looking for remaining bugs, both by reviewing the code carefully, and by collecting metrics such as average policy entropy to perform sanity-checks, rather than just tune hyperparameters. Finally, when they wanted to match the performance of Baselines, they scrutinized the Baselines implementations for small important details, such as exactly how to preprocess and normalize observations.

By the end of six weeks, Daniel was able to talk fluently about the key ideas in RL and the tradeoffs between different algorithms. Most importantly, he was able to implement and debug ML algorithms, going from math in a paper to running code. In retrospect, Daniel reports wishing he had spent a little more time on ML conceptual & mathematical fundamentals, but that overall this process prepared Daniel well for the interview and the role, and was particularly well-suited for OpenAI’s focus on reinforcement learning.

## Now apply for jobs

_These positions will eventually be filled, but you can find a constantly updated list of some of the most promising positions on the [80,000 Hours job board](https://80000hours.org/job-board/ai-ml-safety-research/?role-type=engineering)._

The following example job postings for software engineers on AI safety research teams specify that machine learning experience is _not_ required:

*   OpenAI’s safety team is currently hiring a [software engineer](https://openai.com/jobs/#open) for a range of projects, including interfaces for human-in-the-loop AI training and collecting data for larger language models. (_Update: this job posting is now closed._)
*   MIRI is hiring [software engineers](https://intelligence.org/careers/software-engineer/).
*   Ought is hiring [research engineers](https://ought.org/careers/research-engineer?utm_campaign=80000+Hours+Job+Board&utm_source=80000+Hours+Job+Board) with a focus on candidates who are excited by functional programming, compilers, program analysis, and related topics.

The following example job postings _do_ expect experience with machine learning implementation:

*   DeepMind is hiring [research engineers](https://deepmind.com/careers/jobs/1433588?utm_campaign=80000%20Hours%20Job%20Board&utm_source=80000%20Hours%20Job%20Board) for their _Technical AGI Safety_ team, _Safe and Robust AI_ team – which works on neural net verification and robustness – and potentially others as well.
*   Google AI is hiring [research software engineers](https://careers.google.com/jobs#t=sq&q=j&li=20&l=false&jlo=en-US&jcoid=7c8c6665-81cf-4e11-8fc9-ec1d6a69120c&jcoid=e43afd0d-d215-45db-a154-5386c9036525&j=research+engineer&) in locations worldwide. Although Google AI does not have an “AI Safety” team, there are research efforts focused on robustness, security, interpretability, and learning from human feedback.
*   OpenAI’s safety team is hiring [machine learning engineers](https://jobs.lever.co/openai/a0d3b158-14a0-48db-b38c-1c94bb18f69b) to work on alignment and interpretability.
*   The Center for Human Compatible AI at Berkeley is hiring [machine learning research engineers](https://humancompatible.ai/jobs#engineer) for 1-2 year visiting scholar positions to test alignment ideas for deep reinforcement learning systems.

When you apply to a larger organization that has multiple areas of research, specify in your application which of them you are most interested in working on. Investigate the company’s research areas in advance, in order to make sure that the areas you list are in fact ones that the company works on. For example, don’t specify “value alignment” on an application to a company that does not have any researchers working on value alignment.

If you find that you cannot get a role contributing to safety research right now, you might look for a role in which you can gain relevant experience, and transition to a safety position later.

Non-safety-related research engineering positions are also available at [other industry AI labs](https://www.google.com/search?q=machine+learning+research+engineer&ibp=htl;jobs#fpstate=tldetail&htidocid=t1jN4MUgXkPZajmvAAAAAA%3D%3D&htivrt=jobs) though these are likely to be more competitive than roles on AGI safety teams.

Finally, you could consider applying to a 1-year fellowship/residency program at [Google](https://careers.google.com/stories/edu-resources-programs//), [OpenAI](https://blog.openai.com/openai-fellows-interns-2019/), [Facebook](https://research.fb.com/programs/facebook-ai-research-residency-program/), [Uber](https://eng.uber.com/uber-ai-residency/), or [Microsoft](https://www.microsoft.com/en-us/research/academic-program/microsoft-ai-residency-program/).

## Learn more

*   Working at a leading AI lab might cause harm. [Read more on whether it might still be a high-impact career step.](https://80000hours.org/career-reviews/working-at-an-ai-lab/)
*   This [curriculum on AI safety](https://www.eacambridge.org/technical-alignment-curriculum) (or, for something shorter, [this sequence of posts](https://www.alignmentforum.org/s/mzgtmmTKKn5MuCzFJ) by Richard Ngo)
*   Our [in-depth conversation on the 80,000 Hours Podcast with Catherine Olsson and Daniel Ziegler](https://80000hours.org/podcast/episodes/olsson-and-ziegler-ml-engineering-and-safety/), on which this guide is based.
*   Our guide to [positively shaping the development of advanced artificial intelligence](https://80000hours.org/problem-profiles/positively-shaping-artificial-intelligence/)
*   Our [career review of an ML PhD](https://80000hours.org/career-reviews/machine-learning-phd/)
*   Our podcasts with Chris Olah on [what the hell is going on inside neural networks](https://80000hours.org/podcast/episodes/chris-olah-interpretability-research/) and [working at top AI labs without an undergrad degree](https://80000hours.org/podcast/episodes/chris-olah-unconventional-career-path/)
