# Research as a Stochastic Decision Process - Jacob Steinhardt

Source: https://cs.stanford.edu/~jsteinhardt/ResearchasaStochasticDecisionProcess.html
Author: Jacob Steinhardt
Date: not visible in fetched HTML
Fetch-status: excerpted from HTML via browser.
Use: research-prioritization evidence; cited by Nanda's Key Mindsets post.

## Why this matters for agents

Steinhardt gives a crisp formal-ish rule for research prioritization: reduce uncertainty as fast as possible. This is useful for agents deciding which experiment, baseline, prototype, or sanity check to run first.

## Quotes

> Below I analyze how to approach a project that has many somewhat independent sources of uncertainty (we can often think of these as multiple "steps" or "parts" that each have some probability of success).

> We will eventually see that a good principle is to "reduce uncertainty at the fastest possible rate".

> This reveals that harder tasks should not necessarily be prioritized. Rather, we should prioritize tasks that are more likely to fail (so that we remove the risk of them failing) but also tasks that take less time.

> Do the components in order from most informative per unit time to least informative per unit time.

> De-risk all components (to the extent feasible), then execute.

> Specifically, for each task we want a cheap way to obtain high confidence about whether that task will be feasible. This is called "de-risking".

> We are often either in "de-risking mode" (determining if the problem is infeasible as quickly as possible) or "execution mode" (assuming the problem is feasible and trying to solve it quickly).

> The counterpart to ceilings are baselines--simple or off-the-shelf methods that give a quick lower bound on achievable accuracy.

> Together with ceilings, they delineate a range of possible performance, which helps us interpret our core results.

> I often think about possible approaches to a problem as an exponentially branching search tree.

> Whenever something doesn't work, I ask why it didn't work. My goal is to avoid trying similar things that will fail for the same reason.

> Compared to other people I know, I try harder and earlier to show that my ideas can't work to solve a problem.

> We often try easier tasks first, when instead we should try the most informative tasks first.

## Source graph

This is a standalone blog post. It links to concepts like Poisson arrival processes, but the skill-relevant content is the prioritization/de-risking frame above.
