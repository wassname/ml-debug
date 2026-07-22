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

---

Source: Hamel Husain, Databricks (x2), Eugene Yan blog posts (via WebFetch)
Title: practitioner rules on scale precision, rubric quality, and reading judge traces
Fetched-via: WebFetch summarizer model, 2026-07-22; short quotes cross-checked by re-fetching
Fetch-status: quotes below reproduced twice identically EXCEPT the Databricks scale range, where two fetches disagreed (0-3 or 0-4 vs 0-3 or 1-5) so it is paraphrased, not quoted, in the ref

## Hamel Husain, "Creating a LLM-as-a-Judge That Drives Business Results" — https://hamel.dev/blog/posts/llm-judge/

Critique-shadowing workflow; look at the data before writing the judge, prefer binary:

> You cannot write a good judge prompt until you've seen the data.

> If your evaluations consist of a bunch of metrics that LLMs score on a 1-5 scale (or any other scale), you're doing it wrong.

Onward links from this post: Shankar et al., "Who Validates the Validators?" (arXiv:2404.12272); Yan, "ALIGN Eval" (https://aligneval.com/); OpenAI Cookbook, "Custom LLM as a Judge to Detect Hallucinations with Braintrust" (https://cookbook.openai.com/examples/custom-llm-as-a-judge); "What We've Learned From A Year of Building with LLMs" (https://applied-llms.org/).

## Databricks, "Best Practices for LLM Evaluation of RAG Applications" — https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG

Use a low-precision integer scale:

> Scales like 0-10 are difficult to come up with distinguishing criteria between all scores.

The recommended range paraphrased (fetches disagreed on 0-4 vs 1-5): a coarse 0-3 or 1-5 Likert scale, with an example for each score in the range. Onward links: LMSYS MT-Bench (arXiv:2306.05685) and its FastChat judge prompts (https://github.com/lm-sys/FastChat/blob/main/fastchat/llm_judge/data/judge_prompts.jsonl).

## Databricks, "Enhancing LLM-as-a-Judge with Grading Notes" — https://www.databricks.com/blog/enhancing-llm-as-a-judge-with-grading-notes

Per-question domain rubrics fix the domain-knowledge gap:

> Without Grading Notes, both judge-LLMs overestimate the effectiveness by a significant margin, likely indicating the gap in domain knowledge to criticize.

> With Grading Notes introducing brief domain knowledge, both judge LLMs showed significant improvement in the alignment rate with humans, especially in the case of GPT-4: alignment rate increased to 96.3% for Llama3 and 93.1% for GPT-4o, which corresponds to 85% and 67.5% reduction in misalignment rate, respectively.

## Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)" — https://eugeneyan.com/writing/llm-evaluators/

A survey; the few-shot-instability line is attributed to Luo et al., "ChatGPT as a Factual Inconsistency Evaluator" (arXiv:2303.15621):

> performance unstable when changing the label, example order, and number of examples

Key papers the survey collects (worth reading past this file):
- Zheng et al., MT-Bench — position/verbosity/self-enhancement bias — arXiv:2306.05685
- Liu et al., G-Eval — CoT scoring with GPT-4 — arXiv:2303.16634
- Doddapaneni et al., "Finding Blind Spots in Evaluator LLMs with Interpretable Checklists" — GPT-4 misses >50% of quality drops on several axes — arXiv:2406.13439
- Huang et al., "On the Limitations of Fine-Tuned Judge Models" — finetuned judges fail out-of-domain — arXiv:2403.02839
- Shankar et al., "Who Validates the Validators?" — aligning LLM eval with human preferences — arXiv:2404.12272

Judge leaderboards (live, not cached): Judgemark v4 (https://eqbench.com/judgemark-v4.html), SpeechMap refusal rates (https://speechmap.ai/).
