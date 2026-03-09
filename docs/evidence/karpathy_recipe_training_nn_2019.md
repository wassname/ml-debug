# A Recipe for Training Neural Networks

**Source:** Andrej Karpathy blog post, April 25, 2019
**URL:** https://karpathy.github.io/2019/04/25/recipe/
**Author:** Andrej Karpathy (then Stanford/OpenAI/Tesla)

---

## Core thesis: silent failure problem

> "The 'possible error surface' is large, logical (as opposed to syntactic), and very tricky to unit test... a 'fast and furious' approach to training neural networks does not work and only leads to suffering."

Examples of silent failures listed:
- Forgetting to flip labels during left-right augmentation (network learns to detect flipped images internally)
- Off-by-one bugs in autoregressive models
- Clipping loss instead of gradients
- Using wrong mean from pretrained checkpoint
- Misconfigured regularization / LR / decay

> "The qualities that in my experience correlate most strongly to success in deep learning are patience and attention to detail."

---

## Stage 1: Become one with the data

> "The first step to training a neural net is to not touch any neural net code at all and instead begin by thoroughly inspecting your data."

**Manual inspection:**
> "Scan through thousands of examples manually... understand distribution patterns. Look for: duplicates, corrupted images/labels, imbalances, biases. Pay attention to own classification process -- hints at needed architecture."

**Programmatic search for outliers:**
> "The outliers especially almost always uncover some bugs in data quality or preprocessing."

---

## Stage 2: End-to-end pipeline & dumb baselines

**Fix random seed:**
> "Always use a fixed random seed to guarantee that when you run the code twice you will get the same outcome. This removes a factor of variation and will help keep you sane."

**Disable complexity early:**
- Turn off data augmentation initially -- "it is just another opportunity to introduce some dumb bug"

**Verify loss at initialization:**
> "Verify that your loss starts at the correct loss value. E.g. if you initialize your final layer correctly you should measure -log(1/n_classes) on a softmax at initialization."

**Initialize final layer bias correctly:**
> "Regression with mean 50? Initialize bias to 50. Imbalanced dataset (1:10)? Set logit bias to predict 0.1 probability at init. Setting these correctly will speed up convergence and eliminate 'hockey stick' loss curves."

**Overfit a single batch:**
> "Overfit a single batch of only a few examples (e.g. as little as two). To do so we increase the capacity of our model and verify that we can reach the lowest achievable loss (e.g. zero)... If they do not, there is a bug somewhere and we cannot continue to the next stage."

**Visualize immediately before model input:**
> "The unambiguously correct place to visualize your data is immediately before your y_hat = model(x)... This is the only 'source of truth'. I can't count the number of times this has saved me and revealed problems in data preprocessing and augmentation."

**Visualize prediction dynamics:**
> "The 'dynamics' of how these predictions move will give you incredibly good intuition for how the training progresses. Many times it is possible to feel the network 'struggle' to fit your data if it wiggles too much in some way, revealing instabilities."

**Backprop-to-input dependency check:**
> "A relatively common bug I've come across... people use view instead of transpose/permute somewhere and inadvertently mix information across the batch dimension... set the loss to be something trivial like the sum of all outputs of example i, run the backward pass all the way to the input, and ensure that you get a non-zero gradient only on the i-th input."

**Input-independent baseline:**
> Train model with all inputs zeroed. "Does your model learn to extract any information out of the input at all? If not, something is wrong."

---

## Stage 3: Overfit

**Don't be a hero:**
> "I've seen a lot of people who are eager to get crazy and creative in stacking up the lego blocks of the neural net toolbox in various exotic architectures... Resist this temptation strongly in the early stages of your project. I always advise people to simply find the most related paper and copy paste their simplest architecture that achieves good performance."

**Adam as safe starting point:**
> "In the early stages of setting baselines I like to use Adam with a learning rate of 3e-4. In my experience Adam is much more forgiving to hyperparameters, including a bad learning rate."

> "For ConvNets a well-tuned SGD will almost always slightly outperform Adam, but the optimal learning rate region is much more narrow and problem-specific."

**Build complexity incrementally:**
> "If you have multiple signals to plug into your classifier I would advise that you plug them in one by one and every time ensure that you get a performance boost you'd expect. Don't throw the kitchen sink at your model at the start."

**Learning rate decay warning:**
> "If you are re-purposing code from some other domain always be very careful with learning rate decay... your code could secretly be driving your learning rate to zero too early, not allowing your model to converge."

> "In my own work I always disable learning rate decays entirely (I use a constant LR) and tune this all the way at the very end."

**First layer sanity check:**
> "To gain additional confidence that your network is a reasonable classifier, I like to visualize the network's first-layer weights and ensure you get nice edges that make sense. If your first layer filters look like noise then something could be off."

---

## Stage 4: Regularize

**Primary advice: get more real data**
> "It is a very common mistake to spend a lot engineering cycles trying to squeeze juice out of a small dataset when you could instead be collecting more data. As far as I'm aware adding more data is pretty much the only guaranteed way to monotonically improve the performance of a well-configured neural network almost indefinitely."

**Smaller batch size = more regularization (via batch norm):**
> "Due to the normalization inside batch norm smaller batch sizes somewhat correspond to stronger regularization. This is because the batch empirical mean/std are more approximate versions of the full mean/std so the scale & offset 'wiggles' your batch around more."

**Dropout + batchnorm warning:**
> "Use this [dropout] sparingly/carefully because dropout does not seem to play nice with batch normalization."

**Larger model + early stopping:**
> "I've found a few times in the past that larger models will of course overfit much more eventually, but their 'early stopped' performance can often be much better than that of smaller models."

---

## Stage 5: Hyperparameter tuning

**Random search over grid:**
> "It is best to use random search instead [of grid search]. Intuitively, this is because neural nets are often much more sensitive to some parameters than others. In the limit, if a parameter a matters but changing b has no effect then you'd rather sample a more thoroughly than at a few fixed points multiple times."

---

## Stage 6: Squeeze performance

**Don't stop early:**
> "I've often seen people tempted to stop the model training when the validation loss seems to be leveling off. In my experience networks keep training for unintuitively long time. One time I accidentally left a model training during the winter break and when I got back in January it was SOTA."

**Ensembles:**
> "Model ensembles are a pretty much guaranteed way to gain 2% of accuracy on anything."
