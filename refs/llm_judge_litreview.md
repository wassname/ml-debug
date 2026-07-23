# LLM-as-a-judge: 2026 literature review (varglite)

Quote-anchored evidence for the operational rules of thumb in [llm_judges.md](llm_judges.md). Every `>` block is copy-pasteable from the cited source (ctrl-F-able); each was fetched from the raw HTML/README this turn unless flagged otherwise. Assembled 2026-07-23 (CLAUDE agent). Bare-quote cache with more sources (incl. summarizer-extracted numbers not safe to quote verbatim) lives in [../docs/evidence/llm_judge_biases.md](../docs/evidence/llm_judge_biases.md).

Verify: **current LLM judges carry large, size-dependent biases (order, self-preference) and degrade on long inputs and over-long reasoning, so read outputs, swap order, cap reasoning to the task, and keep N small.**

## Position and order bias

## Lech Mazur, position_bias benchmark — [github README](https://github.com/lechmazur/position_bias)
- last updated: not stated on the raw README; result set covers 2026-era models (GPT-5.4, Claude Opus 4.8, Kimi K2.5)

> Across the 36-model result set, the model-average first-shown pick rate is 64.3%, with a median of 65.4%. **The model-average absolute first-position lift is 15.7 percentage points.** So the aggregate pattern is not a subtle tie-breaker: the displayed order materially changes many judgments.

epistemic context: outsider-run public benchmark with a reproducible swapped-order harness (193 pairs, 36 models); no arXiv paper, the numbers are the raw output of the author's own runs. The headline order-flip figure elsewhere in the same README is "the model-average order-flip rate is 43.0%".

## "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge" — Shi et al. (Dartmouth), IJCNLP-AACL 2025 — [arXiv:2406.07791](https://arxiv.org/abs/2406.07791)
- page date: arXiv June 2024; IJCNLP-AACL 2025

> Our findings confirm that position bias is not due to random chance and varies significantly across judges and tasks. **While position bias is weakly influenced by the length of prompt components, it is strongly affected by the quality gap between solutions.** Our agreement and disagreement analysis among judges further provides insights into the distribution of judging difficulty across the dataset, and highlights the potential for dataset modifications.

epistemic context: peer-reviewed; largest-scale dedicated position-bias study (over 150,000 evaluation instances, 15 judges, 22 tasks); "quality gap" here means the closer the two answers in quality, the more the judge flips on order.

## "RLAIF vs. RLHF" — Lee et al. (Google), ICML 2024 — [arXiv:2309.00267](https://arxiv.org/abs/2309.00267)
- page date: arXiv Sept 2023; ICML 2024

> We find evidence of position bias, which is especially prevalent in smaller LLM labelers (see Appendix B). **To mitigate the effect of position bias, two inferences are made for every pair of candidates, where the order in which candidates are presented to the LLM is reversed for the second inference.** The results from both inferences are then averaged to obtain the final preference distribution.

epistemic context: peer-reviewed; the standard citation for both the "smaller = more position-biased" observation and the swap-and-average fix; per-size figures (PaLM-2 L/S/XS keep position 18/21/56% of the time) are in its Appendix B, not the quoted main text.

## Self-preference scales inversely with judge size

## "Beyond the Surface: Measuring Self-Preference in LLM Judgments" — Chen et al., EMNLP 2025 main — [arXiv:2506.02592](https://arxiv.org/abs/2506.02592)
- page date: arXiv June 2025; EMNLP 2025 main conference. Data + code: [github.com/zhiyuanc2001/self-preference](https://github.com/zhiyuanc2001/self-preference)

> As observed in the figure, models larger than 7B exhibit significantly less self-preference bias compared to those of 7B or smaller. **For example, the DBG score of Qwen2.5-0.5B-Instruct is 41.7%. In contrast, the DBG score of Qwen2.5-14B-Instruct is only 2.1%.** This suggests that LLM judging tasks should utilize larger models to obtain more accurate and unbiased judgment results.

epistemic context: peer-reviewed; the DBG (Difference-based Bias Gauge) score nets out genuine quality using gold judgments, so the residual is bias not skill. The same paper reports reasoning models still self-prefer ("not necessarily less" than non-reasoning), so reasoning is not a fix.

## Reasoning judges: accuracy up, superficial bias not fixed

## "JudgeLRM: Large Reasoning Models as a Judge" — Chen et al., 2025 — [arXiv:2504.00050](https://arxiv.org/abs/2504.00050)
- page date: arXiv April 2025

> JudgeLRM, a family of judgment-oriented LLMs, trained using reinforcement learning (RL) with judge-wise, outcome-driven rewards to activate reasoning capabilities. **JudgeLRM consistently outperform SFT-tuned baselines in the same size, as well as other RL and SFT variants, and even surpass state-of-the-art reasoning models:** notably, JudgeLRM-3B/4B exceeds GPT-4, while JudgeLRM-7B/8B outperforms DeepSeek-R1.

epistemic context: single-group result, not independently replicated; the abstract's headline "+8.14% F1 over same-size SFT" figure is in the body (not re-verified verbatim here). Complementary finding from Huang et al. (arXiv:2601.03630): reasoning judges win on accuracy "particularly on reasoning-intensive tasks" but "still exhibit strong evaluation biases".

## Overthinking: the reasoning-token budget is non-monotonic

## "Does Thinking More always Help? ... Mirage of Test-Time Scaling in Reasoning Models" — Ghosal et al., 2025 — [arXiv:2506.04210](https://arxiv.org/abs/2506.04210)
- page date: arXiv June 2025

> We observe an initial increase (similar to (Muennighoff et al., 2025; Aggarwal & Welleck, 2025)) in accuracy as the average thinking budget increases. **For example, in Figure 2(a), accuracy increases from 82.2% to 87.3% as the average number of thinking tokens increases from 385 to 1100.** However, this trend does not continue indefinitely.

epistemic context: peer-review status unclear (preprint); the paper attributes the post-peak decline to output variance, not worse reasoning; the subagent-reported downstream figure (accuracy falls 87.3% -> 70.3% as tokens rise 1100 -> 15980) is in the body and not re-quoted verbatim here.

## Reasoning-effort token budgets are a config choice, not a constant

## CAIS `simple-evals` and litellm defaults — raw source, fetched 2026-07-23
- [simple-evals/.env.example](https://github.com/centerforaisafety/simple-evals/blob/main/.env.example) and [litellm/constants.py](https://github.com/BerriAI/litellm/blob/main/litellm/constants.py)

> DEFAULT_REASONING_EFFORT_HIGH_THINKING_BUDGET=24576
> DEFAULT_REASONING_EFFORT_MEDIUM_THINKING_BUDGET=8192
> DEFAULT_REASONING_EFFORT_LOW_THINKING_BUDGET=1024

epistemic context: CAIS's eval harness deliberately overrides litellm's stock defaults, whose own constants.py sets HIGH=4096, MEDIUM=2048, LOW=1024. So "effort=high" can mean 4096 or 24576 tokens depending on which mapping is live; setting effort on a judge without checking this can truncate its reasoning ~6x below what a serious harness allots.

## Self-consistency: how many samples N

## "Self-Consistency Is Losing Its Edge: Diminishing Returns and Rising Costs in Modern LLMs" — Loo, 2025 — [arXiv:2511.00751](https://arxiv.org/abs/2511.00751)
- page date: arXiv Oct 2025 (v2 May 2026)

> Self-consistency was designed for an era when base models frequently made reasoning errors; this technique has become an expensive habit mismatched to current model capabilities. **Results confirm that accuracy gains plateau early and, in some configurations, decline at high sample counts** — a pattern inconsistent with diminishing returns alone and more consistent with noise introduction on problems that were already solved. This suggests self-consistency should be reserved for genuinely difficult problems rather than applied as a default scaling strategy.

epistemic context: single-author preprint (low citation signal, flagged); its reported plateau is N~10-15 on strong 2026 models (Gemini 2.5), down from the ~40 of the original PaLM-540B-era self-consistency paper (Wang et al., arXiv:2203.11171). Sets a sane ceiling for a repeat-variance check: 4-10 passes is plenty, past ~15 buys nothing.

## Context rot: long inputs and rubrics degrade judging

## "NoLiMa: Long-Context Evaluation Beyond Literal Matching" — Modarressi et al., ICML 2025 — [arXiv:2502.05167](https://arxiv.org/abs/2502.05167)
- page date: arXiv Feb 2025; ICML 2025. Repo: [github.com/adobe-research/NoLiMa](https://github.com/adobe-research/NoLiMa)

> While they perform well in short contexts (<1K), performance degrades significantly as context length increases. **At 32K, for instance, 11 models drop below 50% of their strong short-length baselines.** Even GPT-4o, one of the top-performing exceptions, experiences a reduction from an almost-perfect baseline of 99.3% to 69.7%.

epistemic context: peer-reviewed; removes literal lexical overlap so the test measures latent-association retrieval, the closest analog to a judge matching a rubric to a semantically-distant answer. The paper defines "effective length as the maximum length at which the score remains above a threshold, set at 85% of the model's base score" -- most models fall below it by 8-16K tokens.

## "Lost in the Middle: How Language Models Use Long Contexts" — Liu et al., TACL 2024 — [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- page date: arXiv July 2023; TACL 2024

> We find that performance can degrade significantly when changing the position of relevant information, indicating that current language models do not robustly make use of information in long input contexts. **In particular, we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models.** Our analysis provides a better understanding of how language models use their input context.

epistemic context: peer-reviewed; the origin of the U-shaped/middle-penalty result, replicated across 6 model families. Operational read for judging: put the rubric and the answer-under-test at the start or end of the prompt, never buried mid-way through a long reference block.

## Machine-accessible judge benchmarks

URLs resolve (checked by subagent via WebFetch); I have not curled every dataset. Pull data programmatically from these.

| name | measures | data URL | notes |
|---|---|---|---|
| JudgeBench (2410.12784) | objective-correctness judge accuracy | [HF ScalerLab/JudgeBench](https://huggingface.co/datasets/ScalerLab/JudgeBench) | many strong judges near-random (~50%) |
| RewardBench (2403.13787) | RM accuracy chat/safety/reasoning | [HF allenai/reward-bench](https://huggingface.co/datasets/allenai/reward-bench) | dedicated results dataset |
| RewardBench 2 (2506.01937) | RM accuracy, harder unseen prompts | [HF allenai/reward-bench-2](https://huggingface.co/datasets/allenai/reward-bench-2) | ~20pt harder than v1 |
| RM-Bench (2410.16184) | RM subtlety + style-bias robustness | [THU-KEG/RM-Bench](https://github.com/THU-KEG/RM-Bench) | SOTA ~46.6% under style bias |
| PPE (2410.14872) | RM/judge vs real post-RLHF human prefs | [lmarena/PPE](https://github.com/lmarena/PPE) | 16k Arena pairs |
| LLMBar (2310.07641) | adversarial instruction-following judge | [princeton-nlp/LLMBar](https://github.com/princeton-nlp/LLMBar) | 419 expert-agreed pairs |
| CALM / Justice-or-Prejudice (2410.02736) | 12 cognitive-bias categories | [Y0oMu/LLM-Judge-Bias-Dataset](https://github.com/Y0oMu/LLM-Judge-Bias-Dataset) | mirror repo, lower provenance |
| MT-Bench (2306.05685) | judge-human agreement, chat | [HF lmsys/mt_bench_human_judgments](https://huggingface.co/datasets/lmsys/mt_bench_human_judgments) | 3,755 human judgments |
| Arena-Hard-Auto (2406.11939) | pairwise win-rate vs baseline | [lmarena/arena-hard-auto](https://github.com/lmarena/arena-hard-auto) | viewer glitchy, raw files OK |
| JudgeLM (2310.17631) | fine-tuned judge vs GPT-4 | [HF BAAI/JudgeLM-100K](https://huggingface.co/datasets/BAAI/JudgeLM-100K) | 100k pairs |
| PandaLM (2306.05087) | small judge vs GPT-3.5/4 | [WeOpenML/PandaLM](https://github.com/WeOpenML/PandaLM) | 7B recovers ~88-94% of frontier |
| Judgemark v4 | judge score-separability, writing | [judgemark-v4.js](https://github.com/EQ-bench/EQ-bench-site/blob/main/judgemark-v4.js) | JS object, no arXiv paper |
| JETTS (2504.15253) | judge for test-time scaling | [SalesforceAIResearch/jetts-benchmark](https://github.com/SalesforceAIResearch/jetts-benchmark) | rerank/beam/critique |
| RewardMATH (2410.01729) | RM math robustness | [HF RewardMATH/RewardMATH](https://huggingface.co/datasets/RewardMATH/RewardMATH) | code repo anonymized |

## Epistemic summary

- **Who says X**: the "large, size-dependent bias" claim rests on three independent chains: an outsider benchmark measuring order-flip on 2026 models (Lech Mazur), an EMNLP paper measuring self-preference vs size with a quality-netted metric (2506.02592), and a Google paper reporting position bias rising as labeler size falls (2309.00267). The "long context / long reasoning both hurt" claim rests on NoLiMa + Lost-in-the-Middle (context) and Ghosal + Loo (reasoning tokens / samples).
- **How they could know**: all direct measurement (repeated inference under swapped order, matched own-vs-other pairs, needle-retrieval at varied length, accuracy-vs-token-budget sweeps), not self-report.
- **Entanglement check**: the bias sources are independent (different teams, years 2023-2026, metrics). The context-rot sources partly share lineage (NoLiMa explicitly builds on the Lost-in-the-Middle framing), so they stack less than they appear to; treat them as ~1.5 independent observations, not 2.
- **Hard-to-vary check**: "bias is large" is hard to vary (a 43% flip rate is not reframable as noise). "Shrinks monotonically with size" is softer: 2506.02592 itself attributes the trend to capability, and a frontier reasoning model (GPT-5.4) still flips ~66% in Lech Mazur, so size alone does not guarantee low bias.
- **What would change my mind (not-claim)**: under the null I would expect near-zero order-flip after swapping, flat DBG across 0.5B->72B, no benefit from swap-and-average, and flat accuracy across context length and thinking-token budget. None of these hold. The one genuine gap: no clean same-model with/without-retrieval judge ablation exists, so RAG-as-mitigation is untested, not refuted.
- **Calibrated take**: qualitative claim (large order + self bias, mitigable by swap-and-average; long context and over-long reasoning both degrade judging) `p ≈ 0.90-0.97`. Specific "monotonically shrinks with size" `p ≈ 0.70-0.85` (capability confound). Cheapest way to be wrong: quote the 41.7%->2.1% size curve as if size is the lever when it may be capability, and assume a big judge is order-invariant. Safe rule: swap-and-average every judge regardless of size; treat "bigger/smarter judge" as a weak prior, not a fix.
