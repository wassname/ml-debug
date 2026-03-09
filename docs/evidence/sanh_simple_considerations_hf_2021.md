# Simple Considerations for Simple People Building Fancy Neural Networks

**Source:** Victor Sanh, Hugging Face Blog, February 25, 2021
**URL:** https://huggingface.co/blog/simple-considerations
**Author:** Victor Sanh (Hugging Face research scientist, author of DistilBERT)

---

## Core practices (overlaps heavily with Karpathy 2019 recipe)

**Data first:**
> "the very first step of building a neural network is to put aside machine learning and simply focus on your data"

**Overfit test:**
> "it is a good habit when you think you have finished implementing to overfit a small batch of examples (16 for instance). If your implementation is (nearly) correct, your model will be able to overfit and remember these examples by displaying a 0-loss (make sure you remove any form of regularization such as weight decay)."

**Baselines:**
> "Start as simple as possible to get a sense of the difficulty of your task and how well standard baselines would perform."
> "it is sometimes hard to understand if your performance comes from a bug in your model/code or is simply limited by your model's expressiveness"

---

## NLP-specific: tokenization warning

> "when you work with language, have a serious look at the outputs of the tokenizers. I can't count the number of lost hours I spent trying to reproduce results (and sometimes my own old results) because something went wrong with the tokenization."

---

## Common implementation errors listed

- Wrong indexing ("really the worst")
- Forgetting `model.eval()` or `model.zero_grad()`
- Preprocessing errors
- Loss receiving wrong argument type (probabilities vs. logits)
- Uniform constant initialization (breaks symmetry)
- Parameters not called in forward pass (no gradients)
- Learning rate stuck at 0
- Suboptimal input truncation

---

## HP tuning advice

> "there is no point of launching 1000 runs with different hyperparameters: compare a couple of runs with different hyperparameters to get an idea of which hyperparameters have the highest impact"

> "random over a reasonably manually defined grid search is still a tough-to-beat baseline" [re: Bayesian vs random search]

---

## Embeddings freezing (NLP, pre-trained LM fine-tuning)

> "in my experience working with pre-trained language models, freezing the embeddings modules to their pre-trained values doesn't affect much the fine-tuning task performance while considerably speeding up the training."

Credence ~65-70% -- specific domain claim, lacks ablation study reference.

---

## External links from this post

- **Cecelia Shao, "Checklist for Debugging Neural Networks"** (2019, KDnuggets/Towards Data Science): 5-section checklist (start simple, confirm loss, check intermediate outputs, diagnose parameters, track work). Thin; largely overlaps with Karpathy recipe and Slavv. Not captured separately -- see those sources instead.
- **Chase Roberts, "How to unit test machine learning code"** (2017, Medium, 4 min): Focuses on software unit testing practices applied to ML models -- testing gradient flow, output shapes, that outputs change when weights change. Spawned `mltest` library. Not a full debugging guide. Main insight: "The code never crashes, the loss still goes down, it just converges to poor results."
- **Joel Grus, "Reproducibility in ML as engineering best practices"** (Google Slides): Experiment reproducibility / engineering hygiene. Not fetched.
- **A recipe for Training Neural Networks** -- Karpathy (captured in full: karpathy_recipe_training_nn_2019.md)
