# Just Know Stuff (how to achieve success in an ML PhD) — Patrick Kidger

Source: https://kidger.site/thoughts/just-know-stuff/ (2023-01-26)
Fetched-via: r.jina.ai reader, 2026-08-15 (CLAUDE agent)
Fetch-status: full post text. Supersedes the earlier "Software development" section excerpt. (CLAUDE agent)

Why it matters here: the "never accept the kludge" posture, and the claim that most ML researchers would not pass muster as junior developers.

---

_Posted on January 26, 2023_
## Introduction

So I recently completed my PhD in Mathematics from the University of Oxford. (Hurrah! It was so much fun.)

In 2-and-a-bit years I wrote 12 papers, received 4139 GitHub stars, got 3271 Twitter followers, authored 1 textbook – doing double-duty as my thesis – and got the coveted big-tech job-offer.

On Neural Differential Equations

If you’re interested in a textbook on Neural Differential Equations with a smattering of scientific computing, then [my thesis is available online.](https://arxiv.org/abs/2202.02435)

Quite a few folks seem to have looked at this, and messaged me – mostly on [Twitter](https://twitter.com/PatrickKidger) or [Mastodon](https://fosstodon.org/@PatrickKidger) – asking for advice on **how to achieve success in a machine learning PhD?**

Each time my answer is: **Just Know Stuff.**

Now, I don’t think “Just Know Stuff” is a terribly controversial opinion – undergraduate classes are largely based around imparting knowledge; the first year of a new PhD’s life is usually spent reading up on the literature – but from the number of questions I get it would seem that this is something worth restating.

Know your field inside-out. Know as much about adjacent fields (in math, statistics, …) as you can. Don’t just know how to program; know how to do software development. Know the mathematical underpinnings your work is built upon. And so on and so on. Indeed: [possessing a technical depth of knowledge is how you come up with new ideas and learn to recognise bad ones](https://kidger.site/thoughts/how-to-handle-a-hands-off-supervisor).

This does beg the follow-up question: **what is worth knowing? What is worth learning?**

And the answer to _that_ is what I started repeating to all of you folks messaging me. But then that started taking up way too much time, mostly because I write way too much. So now I’m writing this post instead – this way I’ll only have to write way too much only once!

The following is a highly personal list of the things I found to be useful during my PhD, and which I think are of a broad enough appeal that they probably represent a reasonable core of knowledge for those just starting an ML PhD. The following is by no mean exhaustive, and you should certainly expect to add a lot of domain-specific stuff on top of this. But perhaps the following is a useful starting point.

_This list is targeted towards early-stage PhD or pre-PhD students. If you’re late-stage and reading through this thinking “yeah, of course I know this stuff”, then well… that’s the point!_

## Machine learning

*   Know both forward- and reverse-mode autodifferentiation. (Nice reference: Appendix A of my thesis. ;) )
    *   Write some custom gradient operations in both PyTorch and JAX.
    *   Look up “optimal Jacobian accumulation” on the autodifferentiation page on Wikipedia.
    *   Optional: learn how JAX derives reverse-mode autoderivatives by combining partial evaluation, forward-mode-autodifferentiation, and transposition.
    *   Optional: why is the computation of a divergence computationally expensive using autodifferentiation? Learn Hutchinson’s trace estimator. (Why is that efficient?) Learn the [Hutch++ trace estimator](https://ram900.hosting.nyu.edu/hutchplusplus/). (Which is surprisingly poorly known.)

*   What is meant by Strassen’s algorithm? Learn how matrix multiplies are actually done in practice. Learn Winograd convolutions.
*   Write your own implementation of a convolutional layer. Write your own implementation of multihead attention.
*   Know the universal approximation theorem. (I recommend Leshno et al. 1993 or Pinkus 1999 as references. _Not_ the much-more-frequently cited references to older results by Cybenko or Hornik, who give much weaker results.)
    *   Optional: if you’re really keen then look up the modern line of work on [alternate universal approximation theorems](https://arxiv.org/abs/1905.08539).

*   Learn the basics of graph neural networks. (E.g. what is oversmoothing?) How do these generalise CNNs?
*   Learn modern Transformer architectures. Look up recent papers [(or implementations)](https://github.com/lucidrains) to see some of the more common architectural tricks. Build a toy implementation.
*   Learn U-Nets. Build a toy implementation.
*   Know how residual networks are discretised ordinary differential equations.
*   know how Gated Recurrent Units (GRUs) are also discretised differential equations.
*   Know how stochastic gradient descent is also a discretised differential equation too! (Yes, including the “stochastic”: that’s a Monte-Carlo discretisation of an expectation.) These are [gradient flows](https://francisbach.com/gradient-flows/).
*   Know what is meant by the manifold hypothesis.
*   Learn the basics of policy gradients. Implement PPO to solve cart-pole. ([Spinning up](https://spinningup.openai.com/en/latest/) is a great resource.)
*   Learn KL divergence, Wasserstein distance, MMD distance.
*   Learn normalising flows, VAEs, WGANs, score-based diffusion models. [Implement a basic score-based diffusion from scratch.](https://docs.kidger.site/equinox/examples/score_based_diffusion/)
*   Try the basics of distributed training of a model. (Over multiple GPUs; multiple computers.) Start with `jax.pmap`.
*   Know how to do hyperparameter optimisation via Bayesian optimisation. My favourite library for this is [Ax](https://ax.dev/).
    *   Optional: try doing this in a distributed fashion, with a main thread sending hyperparameter jobs to different machines, and receiving results back. (The “Service API” for Ax is the appropriate tool here.)

*   Learn the formulae for Adadelta, Adam, etc. What were the innovations for each optimiser? (Momentum, second moments, …) What are some of the newer ones that are now being used (Adabelief, RAdam, NAdamW, … etc. etc. – this is a flavour-of-the-month kind of field.)
*   Learn why we use first-order optimisation techniques (SGD and friends), rather than anything else. (Why not Gauss–Newton? Why not Newton–Raphson? Why not Levenberg–Marquardt?) On that note, let’s move on to…

## (Elementary) scientific computing

*   …start by learning all of those algorithms I just mentioned as well (they’re all nonlinear solvers).
*   Learn QR decompositions, LU decompositions, SVD decompositions, Cholesky decompositions.
    *   Solve linear systems via each of the above decompositions. (Recognise that this is better than inverting a matrix.) Learn the varying computational costs and stabilities of the different ways of doing this. (SVD -> Cholesky-> QR -> LU.)
    *   Reduce linear least squares to linear solves via the normal equations. Know that this squares the condition number. Recognise that this is the textbook approach to fitting a linear model.

*   Learn what is meant by the [Moore–Penrose pseudoinverse](https://en.m.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse) of a matrix.
*   Learn the basics of numerical differential equation solvers:
    *   Euler’s method
    *   Heun’s method
    *   Optional: Implicit Euler method. Know that it works provided `hL < 1`, where `h` is the step size and `L` is the Lipschitz constant of the vector field. (Know the contraction mapping theorem.)
    *   Optional: other diffeq solvers, e.g. explicit Runge–Kutta methods. [This is a nice summary of when to use each.](https://docs.kidger.site/diffrax/usage/how-to-choose-a-solver/)

*   Know Monte-Carlo sampling. Know Quasi Monte-Carlo sampling. Know the convergence rates for both.
*   Learn what is meant by quadrature.
*   Learn Chebyshev polynomials.
*   Know the quirks of floating-point arithmetic: non-associativity, catastrophic cancellation, the impossibility of representing some integers, that you should not compare floats via equality, the meaning of numerical stability.
    *   This is the reason `expm1` and `logsumexp` exist as standalone functions.

*   Optional: learn wavelets.
*   Optional: sparsity.
    *   The different kinds of sparse format (CSC, COO, …);
    *   Sparse linear solvers (e.g. iterative/Krylov methods);
    *   Linear preconditioners.

There’s (a lot) more scientific computing out there, but I’m writing for an ML audience here. The above is perhaps a minimum worth being conversant on.

## Software development.

_(Those of you deriving PAC-Bayes bounds, you might be able to skip this section. Unless you want an industry job post-PhD, that is.)_

Academic software is almost always a poorly-maintained kludge of leaky abstractions, awful formatting, and bugs that don’t cripple things only because some other bug stops them from doing so.

_This is a systemic professional failing._ As an (applied) ML researcher, the overwhelming majority of your time will be spent in front of a screen, staring at code. And yet most of you (yes, you) would not pass muster as a junior developer.

So, how to improve? First of all, never accept the kludge.

*   You’ve messed up your Git repo? Figure out the commands to fix it… don’t just delete it and clone from the remote. ([https://xkcd.com/1597](https://xkcd.com/1597))
*   You’ve written messy code? Assuming you’re using Python: learn PEP8, pre-commit, Black, flake8, isort. (Or [ruff](https://github.com/charliermarsh/ruff) if you’re ahead-of-the-curve.)
    *   Feel free to steal the configs from [one of my repositories](https://github.com/patrick-kidger/equinox).

*   Your code is too slow? Learn a more performant language (C++, Rust, Triton) and write things there.
*   Focus on writing clean code, based around orthogonal abstractions. When the code starts getting messy – and it will – be willing to refactor your code into something more legible. Avoid both spaghetti code and ravioli code.

And returning to the overall theme:

*   Learn Python to an advanced enough level that you know what descriptors, weak references, and metaclasses are.
    *   Learn what closures are.

*   Learn how to build your own Python package and push it to PyPI.
*   Learn both PyTorch and JAX.
    *   When the documentation is inadequate, look at their source code.
    *   Optional: [reimplement JAX core transforms from scratch](https://jax.readthedocs.io/en/latest/autodidax.html).

*   Learn some object oriented design patterns. At least as far as dependency inversion and factories.
*   Learn some C/C++.
    *   Pass-by-reference vs pass-by-copy. Pointers.
    *   Write some bindings for using these from Python. (In ML, this is easiest using PyTorch+LibTorch+pybind11.)
    *   Optional: learn some OpenMP.

*   Learn some Julia. Understand why multiple dispatch is so cool, and how this helps build numerical programs. Write some macros and learn what is meant by homoiconicity.
*   Learn some Haskell. Learn functional programming. Learn some type theory. (Learn the difference between a sum type and a union type.) Learn what is meant by monads. Learn what is meant by referential transparency.
    *   Optional: look up Koka and learn what is meant by algebraic effects.
    *   Optional: look up Idris or Liquid Haskell and learn what is meant by dependent types.

*   Learn some Common Lisp or Scheme. Understand why its code is the same as its abstract syntax tree (AST). Write some macros and _really_ understand homoiconicity.
*   What is meant by generic programming? What is meant by variadic generics? When are these helpful? ([Cough cough](https://github.com/google/jaxtyping).)
*   Learn big-O notation for computational complexity. Learn how a hash map is implemented. Look up how a Python dict is implemented. Look up the exponential memory allocation trick for continually appending to e.g. a Python list.
*   Know dynamic programming. (The classic example here is the Fibonacci numbers.) Learn to recognise when a problem can be solved this way. Recognise the equivalence between dynamic programming and caching (a la Python’s `functools.lru_cache`).
*   Have a read of programming blogs. (Personally, this is how I procrastinate from more serious work.)
*   Learn how to collaborate on code! Typically via GitHub-style pull-request workflows. We’re not going to hire you without evidence we can work with you.
*   Know how to write tests. Integrate them into a CI/CD system e.g. GitHub Actions. (Once again, feel free to [steal from one of my repos](https://github.com/patrick-kidger/diffrax/tree/main/.github/workflows/).)

There’s loads more I could add here: learn some compiler theory (tail call optimisation, peephole optimisation, …). Learn distributed computing. Learn different database systems. Learn a bit about how a CPU works (L1/L2/L3 caches, CPU cycles, vectorisation, branch prediction, some basic assembly, etc.). Learn other programming languages (Nim, Zig, Dex, …) Learn when to use a few mildly nontrivial data structures (heaps, btrees, ropes, …)

You don’t need to become a serious software developer. (i.e. knowing all of the above list and substantially more.) Just don’t write code that makes my eyes bleed.

In nearly every respect I’d actually recommend against the university-taught courses for much of the above list. YMMV, but these are usually pretty poor. (Perhaps because they’re taught by academics… who, as already discussed, don’t usually know what they’re doing here. E.g. C++ courses that taught the `new` and `delete` operators as good practice…) Try the internet instead.

I recommend reading programming forums, YouTube videos from programming conferences, and programming blogs.

## Mathematics

*   Some basics.
    *   Convex functions (recognise that this is a way to bound a nonlinear function by an easier-to-understand linear function).
    *   Lipschitz functions (these have already appeared several times above: in WGANs, the implicit Euler method, the contraction mapping theorem).
    *   The meaning of injectivity, surjectivity, bijectivity.

*   Please, please: learn some probability via measure theory. You’ll start reading machine learning papers wondering how people ever express themselves precisely without it. The entire field seems to be predicated around writing things like as if that’s somehow meaningful notation.
*   Likewise, learn integration through measure theory. At least as far as Fubini’s theorem, the Leibniz Integral Rule, and what is meant by absolute continuity of measures.
    *   Optional: If you’re keen then go as far as Radon–Nikodym derivatives. (Which appears in the definition of the KL divergence, for example.)
    *   Optional: the meaning of almost-everywhere. Recognise that ReLU is almost-everywhere differentiable.
    *   Optional: Alexandrov’s Theorem.

*   Topology is a great topic to learn the basics of, as this underpins nearly all of modern mathematics: open sets, closed sets, compactness, continuous functions, etc.
    *   Optional: there’s some very enjoyable “counterexamples in topology” books out there, that will melt your brain into a variety of interesting shapes.

*   Analysis. A topic close to my heart, as this was my primary field of study at university.
    *   Real analysis, at least the basics: epsilon-delta, the definition of differentiation, that continuous functions on a compact set attain their bounds, etc.
    *   Functional analysis, once again at least the basics: at least as far as the Weierstraß Approximation Theorem.
    *   Ordinary differential equations; at least as far as linearisation around equilibria. (Probably the engineers have some good not-too-dense reference texts for these.)
    *   Fourier series.
    *   Div, grad, curl and all that.

*   Optional: any number of slightly more specialised, but still very widely applicable, fields. For example:
    *   Differential geometry
    *   Optimal transport.
    *   Stochastic calculus, if you do anything to do with time series. (Or score-based diffusion models.)
    *   Statistical physics.
    *   Perturbation theory. Much of machine learning is morphing into a branch of applied mathematics. And as my old fluid dynamics lecturer commented, you can’t be a card-carrying applied mathematician without knowing perturbation theory.

## Statistics

Actually, I’m going to admit to something here: my statistics is nowhere near as strong as I’d like it to be. I think there’s probably a lot that should be added to the following list.

*   All the usual introductory stuff: log-likelihoods, BLUE, cross-validation, confidence intervals, random forests, XGBoost etc. etc.
    *   Regularisation: Tikhonov/ridge/L2 regularisation, sparsity/L1 regularisation, weight decay. The equivalence between regularised maximum likelihood and maximum a-posteriori.

*   Variance minimisation:
    *   Antithetic sampling;
    *   Importance sampling (_cough_ Radon–Nikodym derivatives again _cough_);
    *   Quasi Monte-Carlo (again);
    *   Control variates.

*   Linear-time biased Monte-Carlo approximations to MMDs. Quadratic-time unbiased Monte-Carlo approximations to MMDs.
    *   It may have gone out of fashion, but the basics of kernel theory.

*   Markov Chain Monte-Carlo. Hamiltonian Monte-Carlo.
    *   Relatedly, Gaussian “soap bubbles” in high dimensions, and “typical sets” in MCMC. Anything to build high-dimensional intuition is great. [This](https://stanislavfort.github.io/blog/sphere-spilling-out/) is a fun example. Can you figure out what’s wrong with the final picture?

## That’s a lot of stuff

That’s quite a long list.

Don’t expect to cover all of that in a few months; this is something that should happen over the next few years. To be precise, the above is more-or-less what I think deserves to be known by most people by the end of their PhD. You should naturally expect to also know your own subfield, whatever that is, inside-out.

This list is noticeably biased towards the things I happen to be more involved in, which I guess is unsurprising.

(For example I haven’t mentioned Vapnik–Chervonenkis dimensions or Gaussian processes anywhere. Some may disagree with me but I think it’s possible to get by without knowing VC dimensions these days. And I have a personal bias against Gaussian processes.)

So, season to taste. Probably a few of you are reading this wondering how it could have slipped my mind to add your favourite X, Y or Z to that list! (Object detection, scaling laws for large models, subquadratic attention mechanisms, symbolic regression, …)

It’s worth noting that “by the end of their PhD” is kind of an arbitrary deadline. One never really stops learning. I certainly look back what I’ve written a couple of years ago, and see noticeable improvements I would make if I were to do it again. And looking forward, I have a list of things I intend to learn more about. (Currently: algebraic effects, deeper knowledge of Rust, and microbiology.)

## Interesting parts of the internet to hang out in.

When it comes to Just Knowing Stuff, it’s great to get a sense of the general Zeitgeist in the ML community, and also the rest of the tech community at large. These are a few of my favourite spots:

*   Twitter;
*   Mastodon;
*   Hacker News;
*   /r/machinelearning
*   YouTube, in particular the recorded talks from programming conferences;
*   Programming/software blogs;
*   Forums for software you use regularly
    *   including the GitHub “issues” and “discussions” tabs

## Conclusion

Those of you who already have research experience, and who are reading this: what would be your personal Just Know Stuff list? Do you think mine is fair?

Write your own list and/or let me know on [Twitter](https://twitter.com/PatrickKidger) or [Mastodon](https://fosstodon.org/@PatrickKidger).
