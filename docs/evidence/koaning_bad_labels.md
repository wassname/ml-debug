# Bad Labels — Vincent D. Warmerdam (koaning)

Source: https://koaning.io/posts/labels/ (2021-09-02). Cached copy for the ML-debugging skill.

---

I write a lot of blogposts on why you need more than grid-search to properly judge a machine learning model. In this blogpost I want to demonstrate yet another reason; labels often seem to be wrong.

What I'll describe here is also available as a course on calmcode.io.

## Bit of Background

It turns out that bad labels are a *huge* problem in many popular benchmark datasets. To get an impression of the scale of the issue, just go to labelerrors.com. It's an impressive project that shows problems with many popular datasets; CIFAR, MNIST, Amazon Reviews, IMDB, Quickdraw and Newsgroups just to name a few. It's part of a research paper (https://arxiv.org/abs/2103.14749) that tries to quantify how big of a problem these bad labels are.

The issue here isn't just that we might have bad labels in our training set, the issue is that it appears in the validation set. If a machine learning model can become state of the art by squeezing another 0.5% out of a validation set one has to wonder. Are we really making a better model? Or are we creating a model that is better able to overfit on the bad labels?

## Quick Trick

Here's a quick trick seems worthwhile. Let's say that we train a model that is very general. That means high bias, low variance. You may have a lower capacity model this way, but it will be less prone to overfit on details.

After training such a model, it'd be interesting to see where the model disagrees with the training data. These would be valid candidates to check, but it might result in list that's a bit too long for comfort. So to save time you can can sort the data based on the `predict_proba()`-value. When the model gets it wrong, that's interesting, but when it *also* associates a very low confidence to the correct class, that's an example worth double checking.

## What does this mean?

The abstract of the [Northcutt et al.] paper certainly paints a clear picture of what this exercise means for state-of-the-art models:

> We find that lower capacity models may be practically more useful than higher capacity models in real-world datasets with high proportions of erroneously labeled data. For example, on ImageNet with corrected labels: ResNet-18 outperforms ResNet-50 if the prevalence of originally mislabeled test examples increases by just 6%. On CIFAR-10 with corrected labels: VGG-11 outperforms VGG-19 if the prevalence of originally mislabeled test examples increases by 5%. Traditionally, ML practitioners choose which model to deploy based on test accuracy -- our findings advise caution here, proposing that judging models over correctly labeled test sets may be more useful, especially for noisy real-world datasets.

## So what now?

More people should do check their labels more frequently. ... if you're looking for a simple place to start, check out the cleanlab project (https://github.com/cgnorthcutt/cleanlab). It's made by the same authors of the labelerrors-paper and is meant to help you find bad labels.

For everyone; maybe we should spend a less time tuning parameters and instead spend it trying to get a more meaningful dataset.
