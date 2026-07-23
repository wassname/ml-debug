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

## Reasoning-token budget: Epoch AI + DeepSeek-R1

Epoch AI, "Output length" — https://epoch.ai/data-insights/output-length (via WebFetch, 2026-07-22):

> Reasoning models also exhibit longer response lengths overall - currently, around 8x more tokens on average, compared to non-reasoning models.

> Reasoning models' responses are growing considerably faster (5x per year) than those from non-reasoning models (2.2x per year).

> moving from 'medium' to 'high' effort resulted in a 1.6x increase in output tokens

DeepSeek-AI, "DeepSeek-R1" (arXiv:2501.12948), abstract quotes:

> The reasoning abilities of LLMs can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories.

> emergent development of advanced reasoning patterns, such as self-reflection, verification, and dynamic strategy adaptation

(The response-length-grows-over-training result is R1's headline figure in the body; not re-quoted verbatim here.) Also unverified: the per-model Artificial Analysis token-use splits (https://artificialanalysis.ai/models/qwen3-6-27b#intelligence-index-token-use-tabs) that wassname read as ~5k Gemma-4-31b to ~30k Qwen3.6-35B-A3B; the dashboard is JS-rendered and WebFetch only returned aggregate totals.

---

# 2026 lit-search batch (added 2026-07-23, CLAUDE agent)

Verification legend for this batch:
- [FT] full-text verified: I curled the paper HTML or raw source this turn and the quote below is copied from that fetch.
- [ID] arXiv id + title resolved this turn (real paper, topic matches); the in-body number was extracted by a research subagent via WebFetch's summarizer, NOT copied from raw PDF. Trust the direction; re-pull the exact figure before quoting as gospel.

## Reasoning-effort token budgets: CAIS simple-evals + litellm defaults — [FT]

CAIS `simple-evals/.env.example` (curled from raw github, 2026-07-23), the effort->token map a serious eval harness ships:

> DEFAULT_REASONING_EFFORT_HIGH_THINKING_BUDGET=24576
> DEFAULT_REASONING_EFFORT_MEDIUM_THINKING_BUDGET=8192
> DEFAULT_REASONING_EFFORT_LOW_THINKING_BUDGET=1024

litellm's OWN stock defaults (`litellm/constants.py`, curled same day) are ~6x lower at the top end:

> DEFAULT_REASONING_EFFORT_DISABLE_THINKING_BUDGET = ... 0
> DEFAULT_REASONING_EFFORT_MINIMAL_THINKING_BUDGET = ... 128
> DEFAULT_REASONING_EFFORT_LOW_THINKING_BUDGET = ... 1024
> DEFAULT_REASONING_EFFORT_MEDIUM_THINKING_BUDGET = ... 2048
> DEFAULT_REASONING_EFFORT_HIGH_THINKING_BUDGET = ... 4096

Takeaway: "high effort" is not a fixed token count. litellm stock caps high at 4096; CAIS deliberately overrides to 24576 (6x). So when you set effort=high on a judge you must know which mapping is live, or you may be truncating reasoning at 4k without meaning to. Sources: https://github.com/centerforaisafety/simple-evals/blob/main/.env.example , https://github.com/BerriAI/litellm/blob/main/litellm/constants.py

## Position bias, headline flip rates

## Lech Mazur, position_bias benchmark — https://github.com/lechmazur/position_bias — [FT]
Independent, outsider-run, continuously-updated public harness (strong trust). Method: same story pair shown in both orders, 193 verified pairs, 36 models, 386 prompts/model. Numbers copied from raw README this turn:

> The benchmark finds a large position effect in the current results. The model-average order-flip rate is 43.0%, and the median model flips in 41.3% of decisive two-view cases.

> the model-average first-shown pick rate is 64.3%

> The model-average first-position rating bonus is +0.271 on the 1-to-7 rating scale.

> Mistral Medium 3.5 is the most position-sensitive model in this run: 82.8% first-shown pick rate, +32.8 pp first lift, 72.5% order flip

Rule of thumb: even in 2026, judges flip ~43% of decisive verdicts on order swap alone; the worst flip >70%. Direction is not universal (Mistral Large 3 goes second-position). Always judge both orders. (Note: an earlier subagent draft misattributed 27.4% to Claude Opus; the raw table puts 27.4% first-shown pick on Mistral Large 3, so I dropped the per-model attributions except the verified worst-case.)

## "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge" — Shi et al. (Dartmouth), IJCNLP-AACL 2025 — https://arxiv.org/abs/2406.07791 — [ID]
Most-cited dedicated position-bias study, largest scale (150k+ instances, 15 judges, 22 tasks).

> Our experiments, involving 15 LLM judges across MTBench and DevBench with 22 tasks and approximately 40 solution-generating models, result in over 150,000 evaluation instances.

> While position bias is weakly influenced by the length of prompt components, it is strongly affected by the quality gap between solutions.

Rule of thumb: position bias is systematic, not random noise, and it gets WORSE as the two answers converge in quality (exactly when you most need the judge). Metrics introduced: repetition stability, position consistency, preference fairness.

## "Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models" — Norman, Rivera, Hughes (UC Berkeley), 2026 — https://arxiv.org/abs/2606.19544 — [ID]
2026 audit of 21 judges. Title confirmed via arxiv abs this turn; in-body numbers via subagent WebFetch (re-fetched HTML mirror after PDF parse failed).

> High test-retest reliability (>0.95) coexists with severe position bias (>0.10) in two production-deployed judges (instantiating a consistency-bias paradox).

> Across a range of judge models, flip rates range from 25% to 50%

> All 21 judges evaluated under the bias-audit protocol register a verbosity bias below 0.011 on MT-Bench, with the largest value being GPT-4o-mini at 0.010

Two rules of thumb: (1) a judge being REPRODUCIBLE (same verdict on re-run) does not make it VALID (right, or order-invariant); measure both. (2) Verbosity bias in current-gen judges is ~10x smaller than 2023-era studies reported, so don't over-correct for length on modern judges. Contested-direction flag lives with the self-preference entries below.

## Self-preference / self-enhancement scales inversely with size

## "Beyond the Surface: Measuring Self-Preference in LLM Judgments" — Chen et al., EMNLP 2025 main — https://arxiv.org/abs/2506.02592 — [FT]
Machine-accessible: https://github.com/zhiyuanc2001/self-preference . Its DBG score uses gold judgments to separate bias from genuine quality. Quotes copied from arxiv HTML full-text this turn:

> the DBG score of Qwen2.5-0.5B-Instruct is 41.7%. In contrast, the DBG score of Qwen2.5-14B-Instruct is only 2.1%.

> the DBG score of Llama-3.1-70B is 0.4%, whereas that of Llama-3.1-8B is 21.6%, which is much higher than the score of Llama-3.1-70B.

> Larger models exhibit less self-preference bias compared to smaller models.

> the self-preference bias in reasoning models is not necessarily less significant than the bias found in language models. For instance, the DBG score of DS-R1-Distill-Qwen-32B is 4.8%, whereas the DBG score of Qwen2.5-72B-Instruct is only 2.6%.

Rule of thumb: self-preference is inversely proportional to size. Tiny judges (<1B) can inflate their own scores ~40%; strong large judges drop to low single digits. Reasoning does NOT reliably remove it. Do not use a small model to judge its own family's outputs.

## "Do LLM Evaluators Prefer Themselves for a Reason?" — Chen et al., 2025 — https://arxiv.org/abs/2504.03846 — [ID]
The counter-intuitive one: CoT REDUCES self-preference (contradicts naive "more thinking = more bias"). Title confirmed this turn; HSPP numbers via subagent WebFetch.

> generating reasoning traces substantially reduces harmful self-preference across all models

> For MATH500, harmful self-preference propensity (HSPP) dropped from 56.9% (no reasoning) to 19.3% (standard CoT) to 17.0% (long CoT)

Tension to flag: this paper says CoT roughly halves self-preference; 2506.02592 (above) says LRMs "not necessarily less" biased. Different metrics (HSPP vs DBG), so the direction of "does reasoning fix self-preference" is contested. State it as open, not settled.

## Reasoning judges: accuracy up, superficial bias not fixed

## "JudgeLRM: Large Reasoning Models as a Judge" — Chen et al., 2025 — https://arxiv.org/abs/2504.00050 — [ID]
RL-trained reasoning judge. Title confirmed; F1 numbers via subagent WebFetch.

> JudgeLRM achieves an average improvement of 8.14% in F1 score [vs same-size SFT judges]

> On the human-annotated PandaLM benchmark, JudgeLRM-3B surpasses GPT-4 [F1 72.12% vs 61.80%]

## "Reasoning Model Is Superior LLM-Judge, Yet Suffers from Biases" — Huang et al., Jan 2026 — https://arxiv.org/abs/2601.03630 — [ID]

> LRMs outperform non-reasoning LLMs in terms of judgment accuracy, particularly on reasoning-intensive tasks

> [LRMs] still exhibit strong evaluation biases

Rule of thumb across these two: prefer a reasoning judge for reasoning-heavy grading (~5-8 F1 gain), but it does not remove length/position/style bias. "Use a reasoning judge" is defensible; "reasoning fixes bias" is not.

## "Explicit Reasoning Makes Better Judges" — 2025 — https://arxiv.org/abs/2509.13332 — [ID]
Directly tests small judges (Qwen3 0.6B/1.7B/4B). (Subagent first mislabeled the title as "Thinking Small Models..."; corrected to the real arxiv title this turn.)

> thinking models achieve approximately 10% points higher accuracy with little overhead (under 2x), in contrast to augmentation strategies like few-shot learning, which deliver modest gains at a higher cost (>8x).

> The smallest model in our study (Qwen 3 0.6B) fails to surpass 50% accuracy on difficult 'Chat Hard' and 'Safety' tasks, in some cases performing worse than random selection.

> when subjected to verbosity bias, the thinking model exhibits a higher consistency (83.48 vs 73.86)

Rule of thumb: sub-1B judges fall to random on hard/safety pairs; turning on reasoning buys ~+10 accuracy and higher bias-consistency far cheaper than few-shot ICL (<2x cost vs >8x).

## "RLAIF vs. RLHF" — Lee et al. (Google), ICML 2024 — https://arxiv.org/abs/2309.00267 — [FT]
The canonical "smaller = more position-biased" source. Main-text quotes copied from arxiv HTML this turn; the 18/21/56% per-size figures are in its Appendix B (table, not captured by my main-text grep).

> We find evidence of position bias, which is especially prevalent in smaller LLM labelers

> two inferences are made for every pair of candidates, where the order in which candidates are presented to the LLM is reversed for the second inference. The results from both inferences are then averaged to obtain the final preference distribution.

> Alignment decreases by 4% when substituting PaLM 2 L with PaLM 2 S, and decreases another 11% when using PaLM 2 XS

Reported (Appendix B, via subagent): PaLM 2 L/S/XS keep the same position after swap 18% / 21% / 56% of the time; for L, 94% of same-position cases favor the first candidate. Rule of thumb: the order-swap-and-average mitigation is standard and it comes from here; smaller judges need it most.

## Overthinking: token budget vs task difficulty is non-monotonic

## "Does Thinking More always Help? Mirage of Test-Time Scaling in Reasoning Models" — Ghosal et al., 2025 — https://arxiv.org/abs/2506.04210 — [ID]
Cleanest non-monotonic curve. Title confirmed this turn; numbers via subagent WebFetch.

> accuracy increases from 82.2% to 87.3% as the average number of thinking tokens increases from 385 to 1100. However... pushing the average thinking token count from 1100 to 15980 reduces accuracy from 87.3% to 70.3%

Rule of thumb: return on thinking tokens peaks then declines. In their setup peak was ~1.1k tokens; 14x more tokens (16k) cost ~17 accuracy points. Past the peak, extra tokens add variance, not reasoning.

## "OptimalThinkingBench: Evaluating Over and Underthinking in LLMs" — Aggarwal et al., 2025 — https://arxiv.org/abs/2508.13141 — [ID]

> Thinking models often overthink for hundreds of tokens on the simplest user queries without improving performance. In contrast, large non-thinking models underthink, often falling short of much smaller thinking models.

Rule of thumb: easy items hit negative marginal utility of thinking earlier than hard items; no current model budgets thinking optimally, so difficulty-aware caps beat a fixed cap. This is the evidence base for "cap reasoning low on easy tasks, spend the savings on N passes."

## Self-consistency convergence: how many samples N

## "Self-Consistency Improves Chain of Thought Reasoning" — Wang et al., 2022 — https://arxiv.org/abs/2203.11171 — [ID]
Foundational (several-thousand citations), PaLM-540B era.

> GSM8K (+17.9%) [self-consistency over CoT; 56.5% -> 74.4% at N=40]

Widely-reproduced pattern: gain is monotonic in N with diminishing returns; bulk arrives by N=5-10, saturates ~N=40 for that era's models.

## "Self-Consistency Is Losing Its Edge: Diminishing Returns and Rising Costs in Modern LLMs" — Loo, 2025 — https://arxiv.org/abs/2511.00751 — [ID]
Single-author preprint (low citation signal, flagged), but directly answers "how has N moved." Numbers via subagent WebFetch.

> [MATH-500, Gemini-2.5-Flash-Lite] accuracy improved through approximately 10 sampled paths before plateauing... declining slightly beyond 15

> [MATH-500, Gemini-2.5-Pro] ... improved to 99.2% at 3 paths and 99.6% at 15... a total gain of 1.6% at approximately 15x the single-sample token cost

Rule of thumb for N: on strong 2026 models the self-consistency plateau moved in to N~10-15 (from ~40), total gain shrank to <2 points, and accuracy can DECLINE past the plateau. Reserve repeats for genuinely hard items where the base model is well below ceiling. This also sets the sane N for your N=4 repeat-variance check: 4-10 is plenty to see instability; going past ~15 buys nothing.

## "Inference-Time Scaling for Generalist Reward Modeling" (DeepSeek-GRM) — Liu et al., 2025 — https://arxiv.org/abs/2504.02495 — [ID]
Vendor paper (mild caution). Numbers via subagent WebFetch.

> Direct voting with 32 samples of DeepSeek-GRM-27B could achieve comparable performance to the 671B MoE model

> [ReaLMistake] inference-time scaling with 32 samples improved from 67.9 (voting@1) to 72.8 (voting@32 with meta RM)

Rule of thumb: sampling+voting a small generative judge 32x can match a ~25x-larger single-shot judge, and a learned meta-verifier over the votes beats plain majority vote. Scaling judge COMPUTE can substitute for judge SIZE.

## Context rot: long inputs/rubrics degrade judging

## Chroma, "Context Rot: How Increasing Input Tokens Impacts LLM Performance" — Hong, Troynikov, Huber, July 2025 — https://research.trychroma.com/context-rot — [ID]
Industry report (not peer-reviewed), 18-model controlled study. Numbers via subagent WebFetch.

> Even a single distractor reduces performance relative to the baseline (needle only), and adding four distractors compounds this degradation further.

> as needle-question similarity decreases, model performance degrades more significantly with increasing input length

Rule of thumb: degradation is continuous and starts well before the window fills; a 1M-token window does not reliably reason over 1M tokens. Accuracy is highest when the key info sits near the START of the sequence.

## "NoLiMa: Long-Context Evaluation Beyond Literal Matching" — Modarressi et al., ICML 2025 — https://arxiv.org/abs/2502.05167 — [ID]
Repo: https://github.com/adobe-research/NoLiMa . Removes literal lexical overlap, so it measures latent-association retrieval (closest analog to a judge matching a rubric to a semantically-distant answer). Numbers via subagent WebFetch.

> The effective length is defined as the longest context where a model maintains at least 85% of its base score.

> At 32K, for instance, 10 models drop below 50% of their strong short-length baselines.

> GPT-4o: ... a reduction from an almost-perfect baseline of 99.3% to 69.7% [at 32K]

Rule of thumb: once literal cues are gone, even top models fall below their 85%-effective-length by ~8-16K tokens; by 32K most are below half their short-context score.

## "Lost in the Middle" — Liu et al., TACL 2024 — https://arxiv.org/abs/2307.03172 — [ID]
Origin of the U-shaped/middle-penalty result, replicated across 6 model families.

> performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models.

Rule of thumb for judge prompts: put the rubric and the answer-under-test at the START or END of the prompt, never buried mid-way through a long reference block. (Exact "%drop when moved to middle" varies by model, ~15-25 pts in secondary summaries; direction robust, magnitude approximate.)

## Machine-accessible judge benchmark index (URLs resolve; pull data programmatically)

| name | measures | data URL | machine-accessible |
|---|---|---|---|
| JudgeBench (2410.12784) | objective-correctness judge accuracy (near-random for many strong judges) | https://huggingface.co/datasets/ScalerLab/JudgeBench | yes (Parquet) |
| RewardBench (2403.13787) | RM accuracy chat/safety/reasoning | https://huggingface.co/datasets/allenai/reward-bench | yes (+ results dataset) |
| RewardBench 2 (2506.01937) | RM accuracy, harder unseen prompts (~20pt harder) | https://huggingface.co/datasets/allenai/reward-bench-2 | yes (Parquet) |
| RM-Bench (2410.16184) | RM subtlety + style-bias robustness (SOTA ~46.6% under style bias) | https://github.com/THU-KEG/RM-Bench | yes (JSON/HF) |
| PPE (2410.14872) | RM/judge vs real post-RLHF human prefs | https://github.com/lmarena/PPE | yes (HF+JSON) |
| LLMBar (2310.07641) | adversarial instruction-following judge | https://github.com/princeton-nlp/LLMBar | yes (JSON) |
| CALM / Justice-or-Prejudice (2410.02736) | 12 cognitive-bias categories, robustness+consistency rate | https://github.com/Y0oMu/LLM-Judge-Bias-Dataset | yes (JSON; mirror repo) |
| MT-Bench (2306.05685) | judge-human agreement, chat | https://huggingface.co/datasets/lmsys/mt_bench_human_judgments | yes (Parquet) |
| Arena-Hard-Auto (2406.11939) | pairwise win-rate vs baseline | https://github.com/lmarena/arena-hard-auto | yes (JSON; viewer glitchy) |
| JudgeLM (2310.17631) | fine-tuned 7-33B judge vs GPT-4 | https://huggingface.co/datasets/BAAI/JudgeLM-100K | yes (JSON) |
| PandaLM (2306.05087) | small fine-tuned judge vs GPT-3.5/4 | https://github.com/WeOpenML/PandaLM | yes (JSON in-repo) |
| Judgemark v4 | judge score-separability, creative writing | https://github.com/EQ-bench/EQ-bench-site/blob/main/judgemark-v4.js | yes but nonstandard (JS object) |
| JETTS (2504.15253) | judge usefulness for test-time scaling (rerank/beam/critique) | https://github.com/SalesforceAIResearch/jetts-benchmark | yes (JSONL) |
| RewardMATH (2410.01729) | RM math robustness (1 correct vs 9 wrong) | https://huggingface.co/datasets/RewardMATH/RewardMATH | yes (Parquet; code anon) |

URL provenance: subagent reported all resolve via WebFetch; I have NOT independently curled every dataset. JudgeBench near-random headline and RM-Bench 46.6% are subagent WebFetch quotes. Lower-provenance: CALM data is a mirror repo (Y0oMu, not the main org); RewardMATH code lives on anonymous.4open.science; Judgemark has no arXiv paper (independent practitioner benchmark by Sam Paech).

## Honesty flags for this batch
- [FT] entries (Lech Mazur 43%, self-preference DBG 41.7/2.1, RLAIF position-bias direction + averaging mitigation, CAIS/litellm budgets) are copied from raw source I fetched this turn.
- [ID] entries: arXiv id + title confirmed real and on-topic this turn, but the specific in-body number was pulled by a research subagent through WebFetch's summarizer, not from raw PDF. Re-pull before quoting a figure as exact.
- Discarded as hallucinated by subagents: arXiv IDs with impossible month codes (e.g. 2602.08028, 2606.13603 from search autocomplete); not included.
- Contested / do-not-state-as-settled: whether reasoning fixes self-preference (2504.03846 says CoT halves HSPP; 2506.02592 says LRMs "not necessarily less" on DBG). Different metrics.
