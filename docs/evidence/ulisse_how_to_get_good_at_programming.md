# How to get good at programming — Ulisse Mini

Source: https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming (5 May 2023)
Fetched-via: r.jina.ai reader, 2026-08-15 (CLAUDE agent)
Fetch-status: full post text including footnotes; LessWrong site chrome and the comment thread are trimmed. Supersedes the earlier three-quote excerpt. (CLAUDE agent)

Why it matters here: white-boxing a system shrinks the space you search when debugging, and the trigger to invest in it is noticing that you have gone into brute-force search.

---

_Epistemic status: very confident_

See also: A closely related [post](https://gwern.net/unseeing) by Gwern, another related [post](https://www.lesswrong.com/posts/nEBbw2Bc2CnN2RMxy/gears-level-models-are-capital-investments) by John, and some interesting [slides](https://www.cs.dartmouth.edu/~sergey/hc/rss-hacker-research.pdf#page=19) from a hacker's talk. None of the concepts here are new, but I've tried to lay them out in a more helpful frame.

* * *

When good programmers debug hard problems fast, it's usually because they understand the system well enough to [_track the important internal state_](https://www.lesswrong.com/posts/bhLxWTkRc8GXunFcB/what-are-you-tracking-in-your-head) in their head, letting them drastically _reduce the solution space they're searching over._

This post contains my advice from ~5yrs of linux & programming experience on one of the primary ways to getting better at programming: _white-boxing_.

## Definition and clarification

**Definition**: White-boxing, the process of taking a system you reason about purely in terms of input/output abstractions ("Autograd takes code and outputs gradients") into a system who's gears you understand ("Autograd takes code, records operations to construct a computational graph, then computes gradients via the chain rule")

There are three important things to understand about white-boxing:

First, White-boxing goes through various shades of gray. When you hit diminishing returns you want to switch to understanding another system. (Though if you find a topic fascinating then go ahead and do a deep dive!)

Second, It is higher value to white-box _leaky abstractions_. Autograd for ML is a great example of a leaky abstraction, if you mix up `permute` and `view` your gradients can be subtly wrong. See Karpathy's [great post](https://karpathy.medium.com/yes-you-should-understand-backprop-e2f06eab496b) for more on this. On the other hand, the CPU is a very good abstraction, unless you're doing something unfathomably cursed, you should never run into CPU bugs.

Third, and perhaps most important for building skill,[[1]](https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming#fn289bs9hi65b)you must **notice** when you're going into brute-force search mode, and then **take action** by investing time in understanding the underlying system, until both the problem and solution make sense.

## Absorbing the pattern

Read Gwern's [list](https://gwern.net/unseeing#atoms) and then attempt to come up with _three new examples_ of the pattern, ala [framing exercises](https://www.lesswrong.com/s/Fu7Euu3F96rKhFRWH). I used to think I had absorbed the concept, but I was still black-boxing things without realizing it. I encourage the reader do another exercise: _Come up with three examples of systems (preferably computer systems) that you've recently been partially black-boxing, and problems you ran into because of this._ Alternatively, come up with examples of you _doing black-box search, and how inefficient this was._ Try and install the [trigger-action-plan](https://www.lesswrong.com/posts/v4nNuJBZWPkMkgQRb/making-intentions-concrete-trigger-action-planning) for "notice black-box search, understand things instead"

It may seem I'm making a big deal of this, but it is _critical_ to [notice](https://agentyduck.blogspot.com/p/noticing.html) when you don't understand something, and then _take action_ by understanding it, making a note for later, or something else. Not doing this has caused me to unintentionally plateau for _years_ at certain things (like CSS).

## Conclusion

Go out there and understand systems! Watch talks, read articles, reimplement existing software. We built computers, a human wrote every line of code that's being executed. **You**_**can**_**understand it**.

**Notice** when you're doing brute-force search due to a lack of understanding, and **take action** to build that understanding. The investment will pay off, often immediately, as a black-box search for solutions can be extremely inefficient.[[2]](https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming#fnai0jcih2uug)

Finally, [here's](https://github.com/codecrafters-io/build-your-own-x) a Github megalist of **resources** around "[building your own x](https://github.com/codecrafters-io/build-your-own-x)" - one of the best ways to understand a system is to build it yourself, so go out there do that! open the black box!

![Image 1](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/LTypqBMTSmRrrhb2v/yxdxpyk9zjlk7twaxejq)

A black box being a leaky abstraction. Go out there and open it!

1.   **[^](https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming#fnref289bs9hi65b)**Me failing to follow this advice resulted in my CSS skills not improving for several years, as I would always go into the "try random stuff until it works" mode. 
2.   **[^](https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming#fnrefai0jcih2uug)**I am repeating this because it's that important.
