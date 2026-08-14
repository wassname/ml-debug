# Gears-Level Models are Capital Investments — John Wentworth

Source: https://www.lesswrong.com/posts/nEBbw2Bc2CnN2RMxy/gears-level-models-are-capital-investments
Author: John Wentworth (johnswentworth)
Date: 22nd Nov 2019
Fetch-status: full post text, fetched 2026-08-15 from the LessWrong markdown API (`/api/post/nEBbw2Bc2CnN2RMxy`), comments and site navigation stripped. (CLAUDE agent)
Use: evidence for preferring mechanism-level understanding over black-box tuning.

## Full post

Mazes
-----

The usual method to solve a maze is some variant of [babble-and-prune](/api/post/i42Dfoh4HtsCAfXxL): try a path, if it seems to get closer to the exit then keep going, if it hits a dead end then go back and try another path. It's a black-box method that works reasonably well on most mazes.

However, there are [other methods](/api/post/CPBmbgYZpsGqkiz2R). For instance, you could start by looking for a chain of walls with only one opening, like this:

![](https://lh5.googleusercontent.com/slc6ady6AokKORztEuKCY8B0Z12uf9BMxNyTkS9oaCqyibKF-Qb1yMFnhLbOGST7x-TpuI5ay4_vYPaLTJkhPgG4Mo1DMeX2T7kDfCBKr44qOreOUEU4j0G8AL7wlvJzwZiTbDJI)

This chain of walls is a [gears-level insight](/api/post/B7P97C27rvHPz3s9B) into the maze - a piece of the internal structure which lets us better understand “how the maze works” on a low level. It’s not specific to any particular path, or to any particular start/end points - it’s a property of the maze itself. Every shortest path between two points in the maze either starts and ends on the same side of that line, or passes through the gap.

If we only need to solve the maze once, then looking for a chain of walls is not very useful - it could easily take as long as solving the maze! But if we need to solve the *same* maze more than once, with different start and end points… then we can spend the time finding that chain of walls just once, and re-use our knowledge over and over again. It’s a capital investment: we do some extra work up-front, and it pays out in lower costs every time we look for a path through the maze in the future.

This is a general feature of gears-level models: figuring out a system’s gears takes extra work up-front, but yields dividends forever. The alternative, typically, is a black-box strategy: use a method which works without needing to understand the internals of the system. The black-box approach is cheaper for one-off tasks, but usually doesn’t yield any insights which will generalize to new tasks using the same system - it’s context-dependent.

Marketing
---------

Suppose we work with the marketing team at an online car loan refinance company, and we're tasked with optimizing the company's marketing to maximize the number of car loans the company refinances. Here's two different approaches we might take:

*   We [a/b test](https://en.wikipedia.org/wiki/A/B_testing) hundreds of different ad spend strategies, marketing copy permutations, banner images, landing page layouts, etc. Ideally, we find a particular combination works especially well.
*   We obtain some anonymized data from a credit agency on people with car loans. Ideally, we learn something about the market - e.g. maybe subprime borrowers usually either declare bankruptcy or dramatically increase their credit score within two years of taking a loan.

The first strategy is black-box: we don't need to know anything about who our potential customers are, what they want, the psychology of clicking on ads, etc. We can treat our marketing pipeline as a black box and fiddle with its inputs to see what works. The second strategy is gears-level, the exact opposite of black-box: the whole point is to learn who our potential customers are, breaking open the black box and looking at the internal gears.

These aren't mutually exclusive, and they have different relative advantages. Some upsides of black-box:

*   Black-box is usually cheaper and easier, since the code involved is pretty standard and we don't need to track down external data. Gears-level strategies require more custom work and finding particular data.
*   Black-box yields direct benefits when it works, whereas gears-level requires an extra step to translate whatever insights we find into actual improvements.

On the other hand:

*   Gears-level insights can highlight ideas we wouldn't even have thought to try, whereas black-box just tests the things we think to test.
*   When some tests are expensive (e.g. integrating with a new ad channel), gears-level knowledge can tell us which tests are most likely to be worthwhile.
*   Black-box optimization is subject to [Goodhart](/api/post/YtvZxRpZjcFNwJecS), while gears-level insights usually are not (at least in-and-of themselves)
*   Gears-level insights are less likely subject to distribution shift. For instance, if we change ad channels, then the distribution of people seeing our ads will shift. Different ad copy will perform well, and we'd need to restart our black-box a/b testing, whereas general insights about subprime borrowers are more likely to remain valid.
*   Conversely, black-box optimizations depreciate over time. Audiences and ad channels evolve, and ads need to change with them, requiring constant re-optimization to check that old choices are still optimal.
*   By extension, gears-level insights tend to be permanent and broadly applicable, and have the potential for compound returns, whereas black-box improvements are much more context-specific and likely to shift with time.

In short, the black-box approach is easier, cheaper, and more directly useful - but its benefits are ephemeral and it can't find unknown unknowns. Gears-level understanding is more difficult, expensive, and risky, but it offers permanent, generalizable insights and can suggest new questions we wouldn't have thought to ask.

With this in mind, consider the world through the eyes of an ancient lich or [thousand-year-old vampire](/api/post/kXSETKZ3X9oidMozA). It's a worldview in which ephemeral gains are irrelevant. All that matters is permanent, generalizable knowledge - everything else will fade in time, and usually not even very much time. In this worldview, gears-level understanding is everything.

On the other end of the spectrum, consider the world through the eyes of a startup with six months of runway which needs to show rapid growth in order to close another round of funding. For them, black-box optimization is everything - they want fast, cheap results which don’t need to last forever.

Wheel with Weights
------------------

There’s a [neat experiment](/api/post/gZP8t9BAg37bqxDzZ) where people are given a wheel with some weights on it, each of which can be shifted closer to/further from the center. Groups of subjects have to cooperatively find settings for the weights which minimize the time for the wheel to roll down a ramp.

![](https://lh5.googleusercontent.com/3rzHoBUFab1R_FqE1xdLVa_p5IUkcvdOjuOwi-XRo6J56rsRjFo6E6a2yso5rGgiYxMqtucdOC0WeZ2K48XrbRItBINBLy3Ym-m-2lPl7VSrmwuZCaEFTm2uUByuifSIPhfYNZUv)

Given the opportunity to test things out, subjects would often iterate their way to optimal settings - but they didn’t iterate their way to correct theories. When asked to predict how hypothetical settings would perform, subjects’ predictions didn’t improve much as they iterated. This is black-box optimization: optimization was achieved, but insight into the system was not.

If the problem had changed significantly - e.g. changing weight ratios/angles, ramp length/angle, etc - the optimal settings could easily change enough that subjects would need to re-optimize from scratch. On the other hand, the system is simple enough that just doing all the math is tractable - and that math would remain essentially the same if weights, angles, and lengths changed. A gears-level understanding is possible, and would reduce the cost of optimizing for new system parameters. It’s a capital investment: it only makes sense to make the investment in gears-level understanding if it will pay off on many different future problems.

In the experiment, subjects were under no pressure to achieve gears-level understanding - they only needed to optimize for one set of parameters. I’d predict that people would be more likely to gain understanding if they needed to find optimal weight-settings quickly for many different wheel/ramp parameters. (A close analogy is [evolution of modularity](/api/post/JBFHzfPkXHB2XfDGj): changing objectives incentivize learning general structure.)

Metis
-----

Let’s bring in the [manioc example](/api/post/TMFNQoRZxM4CuRCY6):

> There's this plant, manioc, that grows easily in some places and has a lot of calories in it, so it was a staple for some indigenous South Americans since before the Europeans showed up. Traditional handling of the manioc involved some elaborate time-consuming steps that had no apparent purpose, so when the Portuguese introduced it to Africa, they didn't bother with those steps - just, grow it, cook it, eat it.

> The problem is that manioc's got cyanide in it, so if you eat too much too often over a lifetime, you get sick, in a way that's not easily traceable to the plant. Somehow, over probably hundreds of years, the people living in manioc's original range figured out a way to leach out the poison, without understanding the underlying chemistry - so if you asked them why they did it that way, they wouldn't necessarily have a good answer.

The techniques for processing manioc are a [stock](/api/post/TMFNQoRZxM4CuRCY6) [example](/api/post/Zm7WAJMTaFvuh2Wc7) of metis: traditional knowledge accumulated over generations, which doesn’t seem like it has any basis in reason or any reason to be useful. It’s black-box knowledge, where the black-box optimizer is cultural transmission and evolution. Manioc is a cautionary tale about the dangers of throwing away or ignoring black-box knowledge just because it doesn’t contain any gears.

In this case, building a gears-level model was *very* expensive - people had to get sick on a large scale in order to figure out that any knowledge was missing at all, and even after that it presumably took a while for scientists to come along and link the problem to cyanide content. On the other hand, now that we have that gears-level model in hand, we can quickly and easily test new cooking methods to see whether they eliminate the cyanide - our gears-level model provides generalizable insights. We can even check whether any particular dish of manioc is safe before eating it, or breed new manioc strains which contain less cyanide. Metic knowledge would have no way to do any of that - it doesn’t generalize.

More Examples
-------------

(Note: in each of these examples, there are many other ways to formulate a black-box/gears-level approach. I just provide one possible approach for each.)

Pharma

*   Black box approach: run a high-throughput assay to test the effect thousands of chemicals against low-level markers of some disease.
*   Gears-level approach: comb the literature for factors related to some disease. Run experiments holding various subsets of the factors constant while varying others, to figure out which factors mediate the effect of which others, and ultimately build up a causal graph of their interactions.

The black-box approach is a lot cheaper and faster, but it’s subject to Goodhart problems, won’t suggest compounds that nobody thought to test, and won’t provide any knowledge which generalizes to related diseases. If none of the chemicals tested are effective, then the black-box approach leaves no foundation to build on. The gears-level approach is much slower and more expensive, but eventually yields reliable, generalizable knowledge.

Financial Trading

*   Black box approach: build a very thorough backtester, then try out every algorithm or indicator we can think of to see if any of them achieve statistically significant improvement over market performance.
*   Gears-level approach: research the trading algorithms and indicators actually used by others, then simulate markets with traders using those algorithms/indicators. Compare results against real price behavior and whatever side data can be found in order to identify missing pieces.

The gears-level approach is far more work, and likely won’t produce anything profitable until very late in development. On the other hand, the gears-level approach will likely generalize far better to new markets, new market conditions, etc.

Data Science

*   Black box approach: train a neural network, random forest, support vector machine, or whatever generic black-box learning algorithm you like.
*   Gears-level approach: build a [probabilistic graphical model](/api/post/hzuSDMx7pd2uxFc5w). Research the subject matter to hypothesize model structure, and [statistically compare](/api/post/5mr8Qcqi6xWa6HCHw) different model structures to see which match the data best. Look for side information to confirm that the structure is correct.

The black box approach is subject to Goodhart and often fails to generalize. The gears-level approach is far more work, requiring domain expertise and side data and probably lots of custom code (although the recent surge of [probabilistic programming languages](https://pyro.ai/examples/svi_part_i.html) helps a lot in that department), but gears-level models ultimately give us human-understandable explanations of how the system actually works. Their internal parameters have physical meaning.

Takeaway
--------

Building gears-level models is expensive - often prohibitively expensive. Black-box approaches are usually much cheaper and faster. But black-box approaches rarely generalize - they’re subject to Goodhart, need to be rebuilt when conditions change, don’t identify unknown unknowns, and are hard to build on top of. Gears-level models, on the other hand, offer permanent, generalizable knowledge which can be applied to many problems in the future, even if conditions shift.

The upfront cost of gears-level knowledge makes it an investment, and the payoff of that investment is the ability to re-use the model many times in the future.
