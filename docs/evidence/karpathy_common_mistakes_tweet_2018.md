Source: https://x.com/karpathy/status/1013244313327681536 (thread, 1 Jul 2018)
Title: Andrej Karpathy, "most common neural net mistakes" tweet thread
Fetched-via: x.com blocked (HTTP 451 via jina reader); tweet 1 verbatim from x.com page title in web search results; tweets 2-3 verbatim from https://threadreaderapp.com/thread/1013244313327681536.html ; thread also indexed on Karpathy's own https://karpathy.ai/tweets.html
Fetch-status: verbatim, cross-checked across the two mirrors

# most common neural net mistakes (tweet thread)

Tweet 1 (1 Jul 2018):

> most common neural net mistakes: 1) you didn't try to overfit a single batch first. 2) you forgot to toggle train/eval mode for the net. 3) you forgot to .zero_grad() (in pytorch) before .backward(). 4) you passed softmaxed outputs to a loss that expects raw logits. ; others? :)

Tweet 2 (same thread, 1 Jul 2018):

> oh: 5) you didn't use bias=False for your Linear/Conv2d layer when using BatchNorm, or conversely forget to include it for the output layer .This one won't make you silently fail, but they are spurious parameters

Tweet 3 (same thread, 1 Jul 2018):

> 6) thinking view() and permute() are the same thing (& incorrectly using view)

Context: this thread is the seed of Karpathy's 2019 "A Recipe for Training Neural Networks" post (see karpathy_recipe_training_nn_2019.md), which opens by referencing it.
