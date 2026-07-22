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

---

Source: arXiv abstracts (via WebFetch) + EQ-bench-site repo
Title: evaluator blind spots (Doddapaneni), criteria drift (Shankar), Judgemark v4 cost/score frontier
Fetched-via: WebFetch of arXiv abstract pages, 2026-07-22; Judgemark scores read from the checked-in judgemark-v4.js in EQ-bench/EQ-bench-site
Fetch-status: paper quotes verbatim from abstracts; Judgemark numbers copied from the repo's data rows (not the rendered site table)

## Doddapaneni et al., "Finding Blind Spots in Evaluator LLMs with Interpretable Checklists" (2024) — https://arxiv.org/abs/2406.13439

Evaluator LLMs miss most injected quality drops:

> Our findings reveal significant shortcomings in current Evaluator LLMs, which failed to identify quality drops in over 50% of cases on average.

## Shankar et al., "Who Validates the Validators?" (2024) — https://arxiv.org/abs/2404.12272

Criteria drift, and the validator-needs-validation problem:

> LLM-generated evaluators simply inherit all the problems of the LLMs they evaluate, requiring further human validation.

> users need criteria to grade outputs, but grading outputs helps users define criteria

> some criteria appears dependent on the specific LLM outputs observed (rather than independent criteria that can be defined a priori)

## Judgemark v4 cost-vs-score frontier (snapshot 2026-07)

Data rows from https://github.com/EQ-bench/EQ-bench-site/blob/main/judgemark-v4.js (columns: model, score, lower-CI, upper-CI, USD cost). Higher score = better at separating stronger from weaker creative writing. Pareto frontier (maximize score, minimize cost):

| model | score | cost | note |
|-|-|-|-|
| claude-opus-4-6 | 0.907 | $39.37 | top absolute score |
| gpt-5.5 | 0.878 | $30.44 | |
| claude-sonnet-4-6 | 0.821 | $23.36 | |
| gemini-3.1-pro-preview | 0.787 | $23.07 | |
| grok-4.5 | 0.771 | $17.11 | low refusal |
| zai-org/GLM-5.2 | 0.732 | $8.28 | Chinese, censors CN-political |
| google/gemma-4-31B-it | 0.723 | $0.82 | cheap knee; refuses many contentious tasks |
| google/gemma-4-26B-A4B-it | 0.530 | $0.61 | |
| Qwen/Qwen3.5-9B | 0.324 | $0.56 | cheapest |

Off-frontier for reference: Qwen3.5-27B 0.605 ($1.76), DeepSeek-V4-Pro 0.471 ($2.94), grok-4.3 0.496 ($9.71). So in v4, Qwen and DeepSeek are mid-pack, not frontier; grok-4.5 and gemma carry the value case.

## SpeechMap per-lab Free Speech Index (snapshot 2026-07-21) — https://speechmap.ai/labs/

Higher = answers more / refuses less (0-100), windowed to releases in the last 6 months; "Index" is the windowed score, "Peak" the best single model. This is a cross-topic aggregate and a lab average, so it does not resolve per-model or per-topic refusal (e.g. Chinese labs score mid-to-high here but still refuse on Chinese-political topics; a lab's aggregate can hide a heavily safety-tuned model like Gemma). Copied verbatim from the table wassname pasted:

| Rank | Lab | Index | Peak | Models |
|-|-|-|-|-|
| 1 | Mistral AI | 88.9 | 98.2 | 9 |
| 2 | xAI | 85.8 | 98.2 | 5 |
| 3 | IBM | 84.0 | 84.0 | 1 |
| 4 | Google DeepMind | 81.1 | 88.4 | 9 |
| 5 | Meta | 76.8 | 76.8 | 1 |
| 6 | Zhipu AI (GLM) | 71.0 | 85.9 | 12 |
| 7 | Arcee AI | 70.1 | 82.2 | 3 |
| 8 | Meituan | 63.6 | 78.2 | 2 |
| 9 | Tencent | 60.3 | 76.3 | 4 |
| 10 | DeepSeek | 59.0 | 89.1 | 7 |
| 11 | Moonshot AI | 57.6 | 65.9 | 5 |
| 13 | Anthropic | 53.8 | 71.5 | 10 |
| 16 | OpenAI | 48.0 | 66.7 | 15 |
| 19 | Alibaba (Qwen) | 45.5 | 60.8 | 13 |
| 20 | NVIDIA | 45.3 | 67.7 | 7 |
| 23 | Xiaomi | 43.9 | 62.6 | 10 |
| 24 | ByteDance | 32.1 | 34.4 | 3 |

Note the wide Peak-vs-Index gaps (DeepSeek peak 89.1 vs index 59.0; Zhipu 85.9 vs 71.0): pick the specific permissive checkpoint, not the lab.

Not fetched: SpeechMap's per-model and per-topic breakdowns (https://speechmap.ai/timeline/, /labs/<lab>/) and the eqbench4 EI benchmark data (https://github.com/EQ-bench/EQ-bench-site/blob/main/eqbench4/eqbench4_data.js) are separate from the judge data used here.
