Source: https://github.com/google-research/tuning_playbook (README.md, fetched from raw.githubusercontent.com main branch)
Title: "Deep Learning Tuning Playbook" — Varun Godbole, George E. Dahl, Justin Gilmer, Christopher J. Shallue, Zachary Nado (Google Research / Harvard), 2023
Fetched-via: curl of raw README.md, 2026-06-11
Fetch-status: verbatim excerpts; bullet indentation flattened in places, content unchanged

# Deep Learning Tuning Playbook (excerpts)

From "Why a tuning playbook?":

> Currently, there is an astonishing amount of toil and guesswork involved in actually getting deep neural networks to work well in practice. Even worse, the actual recipes people use to get good results with deep learning are rarely documented. Papers gloss over the process that led to their final results in order to present a cleaner story, and machine learning engineers working on commercial problems rarely have time to take a step back and generalize their process. [...] There is a vast gulf between the results achieved by deep learning experts and less skilled practitioners using superficially similar methods. At the same time, these very experts readily admit some of what they do might not be well-justified.

From "The incremental tuning strategy":

> ***Summary:*** *Start with a simple configuration and incrementally make improvements while building up insight into the problem. Make sure that any improvement is based on strong evidence to avoid adding unnecessary complexity.*

> The most effective way to maximize performance is to start with a simple configuration and incrementally add features and make improvements while building up insight into the problem.

> For each launch, we must make sure that the change is based on strong evidence – not just random chance based on a lucky configuration – so that we don't add unnecessary complexity to the training pipeline.

From "Exploration vs exploitation":

> ***Summary:*** *Most of the time, our primary goal is to gain insight into the problem.*

> Although one might think we would spend most of our time trying to maximize performance on the validation set, in practice we spend the majority of our time trying to gain insight into the problem, and comparatively little time greedily focused on the validation error. In other words, we spend most of our time on "exploration" and only a small amount on "exploitation".

> Prioritizing insight over short term gains can help us: Avoid launching unnecessary changes that happened to be present in well-performing runs merely through historical accident. Identify which hyperparameters the validation error is most sensitive to, which hyperparameters interact the most and therefore need to be re-tuned together, and which hyperparameters are relatively insensitive to other changes and can therefore be fixed in future experiments.

From "Choosing the goal for the next round of experiments":

> Each round of experiments should have a clear goal and be sufficiently narrow in scope that the experiments can actually make progress towards the goal: if we try to add multiple features or answer multiple questions at once, we may not be able to disentangle the separate effects on the results.

From "Identifying scientific, nuisance, and fixed hyperparameters":

> For a given goal, all hyperparameters will be either **scientific hyperparameters**, **nuisance hyperparameters**, or **fixed hyperparameters**. Scientific hyperparameters are those whose effect on the model's performance we're trying to measure. Nuisance hyperparameters are those that need to be optimized over in order to fairly compare different values of the scientific hyperparameters. This is similar to the statistical concept of nuisance parameters. Fixed hyperparameters will have their values fixed in the current round of experiments.

> The learning rate is a nuisance hyperparameter because we can only fairly compare models with different numbers of hidden layers if the learning rate is tuned separately for each number of layers (the optimal learning rate generally depends on the model architecture).

> By fixing certain hyperparameters for a set of experiments, we must accept that conclusions derived from the experiments might not be valid for other settings of the fixed hyperparameters. In other words, fixed hyperparameters create caveats for any conclusions we draw from the experiments.
