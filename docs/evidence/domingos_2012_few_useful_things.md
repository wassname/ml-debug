Source: https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf (author's copy; CACM doi:10.1145/2347736.2347755)
Title: "A Few Useful Things to Know About Machine Learning" — Pedro Domingos, Communications of the ACM, Oct 2012, vol. 55 no. 10
Fetched-via: PDF downloaded from Domingos' UW page, pages transcribed by hand from the rendered pages (3-column CACM layout defeats text extraction)
Fetch-status: verbatim excerpts

# A Few Useful Things to Know About Machine Learning (excerpts)

Standfirst and intro (p. 78) — the paper's stated purpose is writing down ML folk knowledge:

> Tapping into the "folk knowledge" needed to advance machine learning applications.

> Several fine textbooks are available to interested practitioners and researchers (for example, Mitchell and Witten et al.). However, much of the "folk knowledge" that is needed to successfully develop machine learning applications is not readily available in them. As a result, many machine learning projects take much longer than necessary or wind up producing less-than-ideal results. Yet much of this folk knowledge is fairly easy to communicate. This is the purpose of this article.

Key-insights box (p. 78):

> developing successful machine learning applications requires a substantial amount of "black art" that is difficult to find in textbooks.

"It's Generalization that Counts" (p. 80):

> The fundamental goal of machine learning is to generalize beyond the examples in the training set. [...] Doing well on the training set is easy (just memorize the examples). The most common mistake among machine learning beginners is to test on the training data and have the illusion of success.

> Contamination of your classifier by test data can occur in insidious ways, for example, if you use test data to tune parameters and do a lot of tuning. (Machine learning algorithms have lots of knobs, and success often comes from twiddling them a lot, so this is a real concern.)

"Overfitting Has Many Faces" (p. 81):

> What if the knowledge and data we have are not sufficient to completely determine the correct classifier? Then we run the risk of just hallucinating a classifier (or parts of it) that is not grounded in reality, and is simply encoding random quirks in the data. This problem is called *overfitting*, and is the bugbear of machine learning. When your learner outputs a classifier that is 100% accurate on the training data but only 50% accurate on test data, when in fact it could have output one that is 75% accurate on both, it has overfit.

> Everyone in machine learning knows about overfitting, but it comes in many forms that are not immediately obvious.

"Feature Engineering Is The Key" (p. 84):

> At the end of the day, some machine learning projects succeed and some fail. What makes the difference? Easily the most important factor is the features used.

> First-timers are often surprised by how little time in a machine learning project is spent actually doing machine learning. But it makes sense if you consider how time-consuming it is to gather data, integrate it, clean it and preprocess it, and how much trial and error can go into feature design. Also, machine learning is not a one-shot process of building a dataset and running a learner, but rather an iterative process of running the learner, analyzing the results, modifying the data and/or the learner, and repeating.

"More Data Beats a Cleverer Algorithm" pull quote (p. 84):

> A dumb algorithm with lots and lots of data beats a clever one with modest amounts of it.
