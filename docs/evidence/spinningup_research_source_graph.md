# Spinning Up as a Deep RL Researcher - source graph and research-taste excerpts

Primary source: https://spinningup.openai.com/en/latest/spinningup/spinningup.html
Author: Joshua Achiam, OpenAI
Date: October 13th, 2018
Related local cache: docs/evidence/spinningup_researcher.md
Fetch-status: excerpted from Spinning Up HTML via browser; source graph cross-checked against existing local evidence files where present.
Use: RL research-process evidence, especially for source graph, fair comparisons, seeds, preregistration, and ablations.

## Why this matters for agents

Spinning Up is not just an RL textbook page. Its researcher page is a compact research apprenticeship guide. It points to the same battle-tested debugging and reproducibility references already cached in this repo, then adds project selection and rigorous comparison advice.

## Quotes

> If you’re an aspiring deep RL researcher, you’ve probably heard all kinds of things about deep RL by this point. You know that it’s hard and it doesn’t always work. That even when you’re following a recipe, reproducibility is a challenge. And that if you’re starting from scratch, the learning curve is incredibly steep.

> In particular, this will outline a useful curriculum for increasing raw knowledge, while interleaving it with the odds and ends that lead to better research.

> Write your own implementations. You should implement as many of the core deep RL algorithms from scratch as you can, with the aim of writing the shortest correct implementation of each.

> Simplicity is critical. You should organize your efforts so that you implement the simplest algorithms first, and only gradually introduce complexity.

> Don’t overfit to existing implementations either. Study existing implementations for inspiration, but be careful not to overfit to the engineering details of those implementations.

> Iterate fast in simple environments. To debug your implementations, try them with simple environments where learning should happen quickly.

> Your ideal experiment turnaround-time at the debug stage is <5 minutes (on your local machine) or slightly longer but not much.

> Start by exploring the literature to become aware of topics in the field.

> Use the related work section and citations to find closely-related papers and do a deep dive in the literature. You’ll start to figure out where the unsolved problems are and where you can make an impact.

> There are a many different ways to start thinking about ideas for projects, and the frame you choose influences how the project might evolve and what risks it will face.

> Avoid reinventing the wheel. When you come up with a good idea that you want to start testing, that’s great! But while you’re still in the early stages with it, do the most thorough check you can to make sure it hasn’t already been done.

> Under no circumstances handicap the baseline!

> Beware of random seeds making things look stronger or weaker than they really are, so run everything for many random seeds (at least 3, but if you want to be thorough, do 10 or more).

> This is to enforce a weak form of preregistration: you use the tuning stage to come up with your hypotheses, and you use the final runs to come up with your conclusions.

> Check each claim separately. Another critical aspect of doing research is to run an ablation analysis.

## Source graph

Spinning Up intro references, with local status:
- Alex Irpan, Deep Reinforcement Learning Doesn't Work Yet: https://www.alexirpan.com/2018/02/14/rl-hard.html. Local cache: docs/evidence/alexirpan_rl_hard.md.
- Islam et al., Reproducibility of Benchmarked Deep Reinforcement Learning Tasks for Continuous Control: https://arxiv.org/abs/1708.04133. Not separately cached; discussed/cited inside Henderson local cache.
- Henderson et al., Deep Reinforcement Learning that Matters: https://arxiv.org/abs/1709.06560. Local cache: docs/evidence/henderson_2018_deep_rl_matters.md.
- Matthew Rahtz, Lessons Learned Reproducing a Deep RL Paper: http://amid.fish/reproducing-deep-rl. Local cache: docs/evidence/amid_fish_reproducing_deep_rl.md.
- David Silver UCL RL course: http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html. Not cached.
- Berkeley Deep RL course: http://rll.berkeley.edu/deeprlcourse/. Not cached.
- Deep RL Bootcamp lectures: https://sites.google.com/view/deep-rl-bootcamp/lectures. Reddit index cache: docs/evidence/reddit_deeprl_bootcamp_2017_75m5vd.md.
- John Schulman, Nuts and Bolts of Deep RL: http://joschu.net/docs/nuts-and-bolts.pdf. Local cache: docs/evidence/joschu_nuts_and_bolts.md.
- Tim Rocktaschel et al., Advice for Short-term Machine Learning Research Projects: https://rockt.github.io/2018/08/29/msc-advice.html. Not cached.
- Catherine Olsson / 80,000 Hours, ML Engineering for AI Safety & Robustness: https://80000hours.org/articles/ml-engineering-career-transition-guide/. Not cached.

## Likely follow-up cache candidates

Priority 1:
- Chris Olah, research taste: short and directly named by Nanda.
- Jacob Steinhardt, Research as a Stochastic Decision Process: directly named by Nanda for prioritization.
- Tim Rocktaschel et al., short-term ML research projects: directly named by Spinning Up for research growth.

Priority 2:
- David Silver/UCL, Berkeley Deep RL, Deep RL Bootcamp: curriculum material, less directly research-taste except via RL mastery.
- Catherine Olsson/80k: career/field-entry framing; useful if the skill expands beyond project-level research taste.
