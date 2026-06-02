# How to get good at programming — Ulisse Mini

Source: https://www.lesswrong.com/posts/LTypqBMTSmRrrhb2v/how-to-get-good-at-programming . Verbatim excerpts cached for the skill.

---

> When good programmers debug hard problems fast, it's usually because they understand the system well enough to *track the important internal state* in their head, letting them drastically *reduce the solution space they're searching over.*

> you must **notice** when you're going into brute-force search mode, and then **take action** by investing time in understanding the underlying system, until both the problem and solution make sense.

> It is higher value to white-box *leaky abstractions*. Autograd for ML is a great example of a leaky abstraction, if you mix up `permute` and `view` your gradients can be subtly wrong.
