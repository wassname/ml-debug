Source: https://old.reddit.com/r/MachineLearning/comments/6pfsyk/p_37_reasons_why_your_nn_is_not_working/
Title: "[P] 37 Reasons why your Neural Network is not working" - r/MachineLearning discussion thread, 2017
Fetched-via: reddit blocks scrapers now, so via the Wayback Machine snapshot https://web.archive.org/web/2020/https://old.reddit.com/r/MachineLearning/comments/6pfsyk/p_37_reasons_why_your_nn_is_not_working/ , 2026-08-15 (CLAUDE agent)
Fetch-status: all 22 comments, verbatim. Nesting is flattened; scores not captured.

# [P] 37 Reasons why your NN is not working

Companion thread to [slavv_37_reasons_nn.md](slavv_37_reasons_nn.md). It matters because a commenter posted 13 extra checks here, the author replied "Do you mind if I add them to the article?", and the article never did add them: checking the 2025 archived copy, only the batch-size point overlaps. So this thread, not the article, is the source for those checks.


## u/slavivanov

You know what, I see the car kinda

## u/antiquechrono

If you look at the site that was referenced it's fairly obvious why the feature detector classified that as a car. The paper itself is pretty interesting too.

[not a car](http://carlvondrick.com/ihog/results/teaser_vis.png)

## u/fimari

I see a sports car, maybe cabriolet with closed roof - I blame it on my youth, I'm definitely over-fitting on cars...

## u/Molag_Balls

Whoosh 

( it was a joke )

## u/villasv

It actually looks like a car.

## u/Molag_Balls

Am I wrong in thinking the comment itself was a joke? Or at least just a funny observation?

## u/villasv

Hang on, sorry. [/u/Sillychina](/web/20230610050333/https://old.reddit.com/u/Sillychina) was almost certainly joking. I failed to notice the context fork from from [/u/antiquechrono](/web/20230610050333/https://old.reddit.com/u/antiquechrono), where it's shown that in the "eyes" of the model that's indeed not far from a car.

## u/aysz88

almost certainly joking

I dunno... Personally, I really could see the "car" (the general shape of one) in the same orientation as shown in the diagnostics.

## u/tinkerWithoutSink

Really nice post. A while back I scoured the internet and couldn't find anything quite like this so I made my own, but never shared. Yours is better though, I especially appreciated the citations.

Here's a few you might not have considered:

- I.  Sample size: you can work out the minimum sample size by graphing the cumulative mean or std and seeing when it stabilized. It it converges on 256, then that's probably a good batch (not sure about this and batches). And the minimum size for your training data.

- 8. Loss for unbalanced data. I'll add that when you can't balance the dataset KLD and Dice loss help to get convergence on unbalanced data

- 11. Small batches. You don't want batches that are too small either right (serious question)? I figure that if they are a decent sample of your data then that will help, but I'm not sure

- 12.  How much data augmentation is too much, I use simple hypterparam optimization and a scikit learn model to test this. You can look at the standard deviation of a data feature and try not to exceed that for risk of drowning out signal with noise.

- III architecture mistakes

- [have dropout after pooling](https://www.reddit.com/r/MachineLearning/comments/46b8dz/what_does_debugging_a_deep_net_look_like/d04qyqm/)

- 17. I Use dummy metrics too, [http://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html](http://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)

- 21. 

- If your validation loss is jumping around, then your validation set is too small

- If your validation accuracy is higher than you training accuracy... actually this one has me stumped?

- . 22. Test frameworks. Too many DL and RL frameworks are broken, so it might be worth testing frameworks too

- . 33. You didn't mentioned different activations. 

- I've noticed that if your loss if fluctuating up and down try using Elu instead of ReLU. This is because ReLU masks half the data, and so the model might be flipping between masking one of two modes

- sigmoidal (sigmoid, tanh) activation units, which can saturate/have regions of near flat curvature and thus very little gradient gets propagated backwards, so learning is incredibly slow if not completely halted [src](http://stats.stackexchange.com/questions/163600/pre-training-in-deep-convolutional-neural-network)

- you can always try linear activations as a sanity check

- loss curves. This has been done but you might want to think about diagnosing differen't loss curves e.g.

- 1) a sharp drop in loss at the start (bad init?) 

- 2) fluctuating loss (bad activation?) 

- 3) increasing loss (high learning rate?)

## u/johnQuincyLadams

+1 for dummy estimators they are a great tool. and great rule-of-thumb re: std dev of a feature as bounds for augmentation params, I always wondered how to choose that.

Validation acc > training acc might have to do with over-regularization, if regularizers/dropout/batchnorm are turned off in the evaluation phase ?? idk

## u/tinkerWithoutSink

if regularizers/dropout/batchnorm are turned off in the evaluation phase ?? idk

Ah that must be it! I had a look at the [keras code](https://github.com/fchollet/keras/blob/master/keras/engine/training.py#L1871), and it uses test mode to evaluate the validation data. So this probably turns off dropout/reg and increases accuracy. Nice thinking!

## u/slavivanov

These are great points. Do you mind if I add them to the article?

## u/tinkerWithoutSink

Yeah please do!

## u/serge_cell

Small batches. 

For obvious reason small batches are better if you don't use batch normalization and don't care about gpu performance. Have nothing to do with data variation (assuming there is no precision problems)

## u/ambodi

I am not sure if this is a debugging lesson/checkpoint or a lesson on multi-layer perceptron summarized and bullet numbered.

## u/grrrgrrr

Nice article, I have a [book cover](http://imgur.com/a/dQ7Q0) for you

## u/schmook

Reason 5 will shake-shake your gradients!!

## u/Dutchcheesehead

I don't get step 2: 2. Try random input. By feeding garbage my network should not learn anything, right? Then how should I conclude my network is turning my data into garbage?

## u/Pfohlol

The point is that if you don't see a change in behavior after feeding noise, your network wasn't working properly in the first place and you should investigate why

## u/mlaway

I'm trying to build a GAN and I've been rather unsuccessful. If someone could make a similar guide on how to train and debug them, that'd be cool:)

## u/slavivanov

This might help you: [https://github.com/soumith/ganhacks](https://github.com/soumith/ganhacks)

## u/mlaway

It does, but it doesn't really explain how to debug these types of models. My point is that if I came up with the idea of GANs, they wouldn't be recognized because I can't make the idea work in practice. I want to learn the tools I need to find out what is wrong with my current implementation. I'm looking at gradients (they look fine/are not zero, but after some time neither the generator nor discriminator updates anymore, even though it seems like the gradients aren't 0) and I've tried a variety of different hyperparameters, but the generated images still only resemble random noise.
