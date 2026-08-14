# How to avoid machine learning pitfalls: checklist

Appendix to the [ML Debugging skill](../SKILL.md).

This is the full do/don't list from Michael A. Lones, ["How to avoid machine learning pitfalls: a guide for academic researchers"](https://arxiv.org/pdf/2108.02497) (v5, updated annually). Read the paper for the reasoning and examples behind each item; the local evidence excerpt is [here](../docs/evidence/lones_2021_ml_pitfalls.md).

> Mistakes in machine learning practice are commonplace, and can result in a loss of confidence in the findings and products of machine learning.

## Before you start to build models

> 2.1 Do think about how and where you will use data  
> 2.2 Do take the time to understand your data  
> 2.3 Don't look at all your data  
> 2.4 Do clean your data  
> 2.5 Do make sure you have enough data  
> 2.6 Do talk to domain experts  
> 2.7 Do survey the literature  
> 2.8 Do think about how your model will be deployed

## How to reliably build models

> 3.1 Don't allow test data to leak into the training process  
> 3.2 Do try out a range of different models  
> 3.3 Don't use inappropriate models  
> 3.4 Do keep up with progress in deep learning (and its pitfalls)  
> 3.5 Don't assume deep learning will be the best approach  
> 3.6 Do be careful where and how you do feature selection  
> 3.7 Do optimise your model's hyperparameters  
> 3.8 Do avoid learning spurious correlations

## How to robustly evaluate models

> 4.1 Do use an appropriate test set  
> 4.2 Don't do data augmentation before splitting your data  
> 4.3 Do avoid sequential overfitting  
> 4.4 Do evaluate a model multiple times  
> 4.5 Do save some data to evaluate your final model instance  
> 4.6 Do choose metrics carefully  
> 4.7 Do consider model fairness  
> 4.8 Don't ignore temporal dependencies in time series data

## How to compare models fairly

> 5.1 Don't assume a bigger number means a better model  
> 5.2 Do use meaningful baselines  
> 5.3 Do use statistical tests when comparing models  
> 5.4 Do correct for multiple comparisons  
> 5.5 Don't always believe results from community benchmarks  
> 5.6 Do combine models (carefully)

## How to report your results

> 6.1 Do be transparent  
> 6.2 Do report performance in multiple ways  
> 6.3 Don't generalise beyond the data  
> 6.4 Do be careful when reporting statistical significance  
> 6.5 Do look at your models  
> 6.6 Do use a machine learning checklist

Two especially common leak routes:

> The best thing you can do to prevent these issues is to partition off a subset of your data right at the start of your project, and only use this independent test set once to measure the generality of a single model at the end.

> Most notably, time series data are subject to a particular kind of data leakage known as look ahead bias.


## Extra checks from the 37-reasons thread (wassname, 2017)

Slav Ivanov's "37 Reasons why your Neural Network is not working" drew a reply from
wassname (u/tinkerWithoutSink) with further checks. Ivanov asked "Do you mind if I add
them to the article?" and never did, so this is the only place they live. Quoted from
[the thread cache](../docs/evidence/reddit_37_reasons_nn_6pfsyk.md); the numbers refer
to items in the original article.

> - I. Sample size: you can work out the minimum sample size by graphing the cumulative mean or std and seeing when it stabilized. It it converges on 256, then that's probably a good batch (not sure about this and batches). And the minimum size for your training data.
> - 8. Loss for unbalanced data. I'll add that when you can't balance the dataset KLD and Dice loss help to get convergence on unbalanced data
> - 11. Small batches. You don't want batches that are too small either right (serious question)? I figure that if they are a decent sample of your data then that will help, but I'm not sure
> - 12. How much data augmentation is too much, I use simple hypterparam optimization and a scikit learn model to test this. You can look at the standard deviation of a data feature and try not to exceed that for risk of drowning out signal with noise.
> - III architecture mistakes
>   - [have dropout *after* pooling](https://www.reddit.com/r/MachineLearning/comments/46b8dz/what_does_debugging_a_deep_net_look_like/d04qyqm/)
> - 17. I Use dummy metrics too, http://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html
> - 21.
>   - If your validation loss is jumping around, then your validation set is too small
>   - If your validation accuracy is higher than you training accuracy... actually this one has me stumped?
> - 22. Test frameworks. Too many DL and RL frameworks are broken, so it might be worth testing frameworks too
> - 33. You didn't mentioned different activations.
>   - I've noticed that if your loss if fluctuating up and down try using Elu instead of ReLU. This is because ReLU masks half the data, and so the model might be flipping between masking one of two modes
>   - sigmoidal (sigmoid, tanh) activation units, which can saturate/have regions of near flat curvature and thus very little gradient gets propagated backwards, so learning is incredibly slow if not completely halted [src](http://stats.stackexchange.com/questions/163600/pre-training-in-deep-convolutional-neural-network)
>   - you can always try linear activations as a sanity check
>   - loss curves. This has been done but you might want to think about diagnosing differen't loss curves e.g.
>     - 1) a sharp drop in loss at the start (bad init?)
>     - 2) fluctuating loss (bad activation?)
>     - 3) increasing loss (high learning rate?)

The validation-accuracy question was answered in the same thread: it happens when
regularizers, dropout and batch norm are active in training and switched off at
evaluation, so the training number is measured on a handicapped model.
