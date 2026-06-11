Source: https://arxiv.org/abs/2108.02497 (v5; updated annually since 2021)
Title: "How to avoid machine learning pitfalls: a guide for academic researchers" — Michael A. Lones (Heriot-Watt University)
Fetched-via: PDF downloaded from arxiv.org, text extracted with pdfplumber, 2026-06-11
Fetch-status: verbatim excerpts; line breaks rejoined, ligature artifacts fixed

# How to avoid machine learning pitfalls (excerpts)

Abstract:

> Mistakes in machine learning practice are commonplace, and can result in a loss of confidence in the findings and products of machine learning. This guide outlines common mistakes that occur when using machine learning, and what can be done to avoid them. Whilst it should be accessible to anyone with a basic understanding of machine learning techniques, it focuses on issues that are of particular concern within academic research, such as the need to do rigorous comparisons and reach valid conclusions. It covers five stages of the machine learning process: what to do before model building, how to reliably build models, how to robustly evaluate models, how to compare models fairly, and how to report results.

Structure (from the introduction):

> The review is divided into five sections. *Before you start to build models* covers issues that can occur early in the ML process, and focuses on the correct use of data and adequate consideration of the context in which ML is being applied. *How to reliably build models* then covers pitfalls that occur during the selection and training of models and their components. *How to robustly evaluate models* presents pitfalls that can lead to an incorrect understanding of model performance. *How to compare models fairly* then extends this to the situation where models are being compared, discussing how common pitfalls can lead to misleading findings. *How to report your results* focuses on reproducibility and factors that can lead to incomplete or deceptive reporting.

The full do/don't list (table of contents, v5) — this is the exhaustive-checklist value of the paper:

> 2.1 Do think about how and where you will use data / 2.2 Do take the time to understand your data / 2.3 Don't look at all your data / 2.4 Do clean your data / 2.5 Do make sure you have enough data / 2.6 Do talk to domain experts / 2.7 Do survey the literature / 2.8 Do think about how your model will be deployed
> 3.1 Don't allow test data to leak into the training process / 3.2 Do try out a range of different models / 3.3 Don't use inappropriate models / 3.4 Do keep up with progress in deep learning (and its pitfalls) / 3.5 Don't assume deep learning will be the best approach / 3.6 Do be careful where and how you do feature selection / 3.7 Do optimise your model's hyperparameters / 3.8 Do avoid learning spurious correlations
> 4.1 Do use an appropriate test set / 4.2 Don't do data augmentation before splitting your data / 4.3 Do avoid sequential overfitting / 4.4 Do evaluate a model multiple times / 4.5 Do save some data to evaluate your final model instance / 4.6 Do choose metrics carefully / 4.7 Do consider model fairness / 4.8 Don't ignore temporal dependencies in time series data
> 5.1 Don't assume a bigger number means a better model / 5.2 Do use meaningful baselines / 5.3 Do use statistical tests when comparing models / 5.4 Do correct for multiple comparisons / 5.5 Don't always believe results from community benchmarks / 5.6 Do combine models (carefully)
> 6.1 Do be transparent / 6.2 Do report performance in multiple ways / 6.3 Don't generalise beyond the data / 6.4 Do be careful when reporting statistical significance / 6.5 Do look at your models / 6.6 Do use a machine learning checklist

Section 3.1, "Don't allow test data to leak into the training process":

> A common problem is allowing information about this data to leak into the configuration, training or selection of models. When this happens, the data no longer provides a reliable measure of generality, and this is a common reason why published ML models often fail to generalise to real world data. There are a number of ways that information can leak from a test set. Some of these seem quite innocuous. For instance, during data preparation, using information about the means and ranges of variables within the whole data set to carry out variable scaling or imputation — in order to prevent information leakage, these statistics should be calculated using only the training data. [...] The best thing you can do to prevent these issues is to partition off a subset of your data right at the start of your project, and only use this independent test set once to measure the generality of a single model at the end.

Section 4.8, "Don't ignore temporal dependencies in time series data":

> Most notably, time series data are subject to a particular kind of data leakage known as look ahead bias. This occurs when some or all of the data points used to train the model occur later in the time series than those used to test the model. In effect, this can allow knowledge of the future to leak into training, and this can then bias the test performance. A situation where this commonly occurs is when standard cross-validation is applied to time series data, since it results in the training folds in all but one of the cross-validation iterations containing data that is in the future relative to the test fold.
