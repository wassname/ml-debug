Source: arXiv abstracts via export.arxiv.org API + https://verdict.haizelabs.com/docs/best-practices/ and /docs/cookbook/distributional-bias/ (via jina reader)
Title: LLM-as-a-judge biases — Zheng et al. 2023 (MT-Bench), Wang et al. 2023 (positional bias), Panickssery et al. 2024 (self-preference), plus Haize Labs' verdict practitioner notes
Fetched-via: arXiv API abstracts verbatim; verdict docs verbatim via r.jina.ai, 2026-06-11
Fetch-status: verbatim (abstracts in full or near-full; verdict pages are short and quoted nearly whole)

# LLM judge biases (excerpts)

## "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" — Zheng et al. (LMSYS), NeurIPS 2023 — https://arxiv.org/abs/2306.05685

The canonical paper naming the bias taxonomy:

> We examine the usage and limitations of LLM-as-a-judge, including position, verbosity, and self-enhancement biases, as well as limited reasoning ability, and propose solutions to mitigate some of them. [...] Our results reveal that strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans.

## "Large Language Models are not Fair Evaluators" — Wang et al., ACL 2024 — https://arxiv.org/abs/2305.17926

Positional bias is large enough to flip rankings outright:

> We find that the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context. This manipulation allows us to skew the evaluation result, making one model appear considerably superior to the other, e.g., Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator. To address this issue, we propose a calibration framework with three simple yet effective strategies: 1) Multiple Evidence Calibration, which requires the evaluator model to generate multiple evaluation evidence before assigning ratings; 2) Balanced Position Calibration, which aggregates results across various orders to determine the final score; 3) Human-in-the-Loop Calibration [...]

## "LLM Evaluators Recognize and Favor Their Own Generations" — Panickssery, Bowman, Feng (NYU/MATS), 2024 — https://arxiv.org/abs/2404.13076

Self-preference is causally linked to self-recognition:

> One such bias is self-preference, where an LLM evaluator scores its own outputs higher than others' while human annotators consider them of equal quality. [...] We discover that, out of the box, LLMs such as GPT-4 and Llama 2 have non-trivial accuracy at distinguishing themselves from other LLMs and humans. By fine-tuning LLMs, we discover a linear correlation between self-recognition capability and the strength of self-preference bias; using controlled experiments, we show that the causal explanation resists straightforward confounders.

## Haize Labs, verdict docs — practitioner mitigation notes

"Best Practices / Learnings" (https://verdict.haizelabs.com/docs/best-practices/), quoted nearly whole:

> - ask for an explanation/justification (**before** the score)
> - hierarchical verifier is a must — try a different model for the verifier to avoid self-preference bias
> - study the output distribution of provider models carefully — for example, we find that the gpt-4o family of models has an upward skew for numerical scales and exhibit mode collapse even when using logprobs — likely due to their user-facing alignment tuning. llama models exhibit higher-entropy distributions (more filled out) — this provides more expressiveness and discriminative power
> - watch for any positional bias -- flip scales, shuffle positions, etc.

"Distributional Bias in LLM-as-a-Judge" cookbook (https://verdict.haizelabs.com/docs/cookbook/distributional-bias/):

> Note that using the same model for the initial judge and verification judge will result in a positive-skew that may not discriminate faithfully between good and bad explanations.

> Constrained decoding methods for structured outputs (e.g., JSON-mode) impose an inductive bias on the model's output distribution.

Related: JudgeBench leaderboard for judge quality — https://huggingface.co/spaces/ScalerLab/JudgeBench
