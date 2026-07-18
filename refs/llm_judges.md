# LLM-as-a-judge: known biases and mitigations

Appendix to the [ML Debugging skill](../SKILL.md). When an LLM-judged eval looks surprisingly good, or a ranking flips between runs, suspect the judge before the model. Each bias below has been measured; verbatim sources in [docs/evidence/llm_judge_biases.md](../docs/evidence/llm_judge_biases.md).

## The measured biases

Position bias is large enough to flip rankings outright. Wang et al. (ACL 2024):

> the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context. [...] e.g., Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator.[^wang]

Zheng et al. (the MT-Bench paper) named the wider taxonomy: "position, verbosity, and self-enhancement biases, as well as limited reasoning ability"[^zheng]. Their headline agreement number (GPT-4 matches human preference "over 80%", the same as human-human agreement) is the case *for* LLM judges; the bias list is the fine print.

Self-preference tracks self-recognition. Panickssery et al. fine-tuned models to vary self-recognition ability and found "a linear correlation between self-recognition capability and the strength of self-preference bias"[^panickssery], with controlled experiments supporting a causal reading. A judge that can tell its own outputs apart will favor them, so judging a model with itself (or a sibling checkpoint) is structurally biased.

There are also output-distribution quirks. From Haize Labs' verdict docs (practitioner notes): the gpt-4o family skews numerical scores upward and mode-collapses even with logprobs; llama-family judges give higher-entropy, more discriminative score distributions; JSON-mode constrained decoding imposes its own inductive bias on scores.[^verdict]

## Mitigation checklist

From Wang's calibration framework and verdict's best-practices page:

- Ask for an explanation or justification *before* the score, not after.
- Score both orderings and aggregate (Wang's Balanced Position Calibration); at minimum, randomize position and check the flip rate.
- Use a different model family for the judge (and for any verifier-of-the-judge) than the one being evaluated. Same-model verification produces a positive skew "that may not discriminate faithfully".[^verdict]
- Inspect the raw score distribution before trusting means: mode collapse or skew means the scale isn't being used.
- Spot-check judge verdicts against your own reading of ~20 transcripts (the [Ng error-analysis move](../SKILL.md#inspect-the-data-first), applied to the judge).
- Judge quality is benchmarkable: [JudgeBench](https://huggingface.co/spaces/ScalerLab/JudgeBench) ranks judges on objective-correctness pairs.

## Harness validity checks

The following additions are practical evaluation rules from wassname:

- Read both compared outputs for every scenario, not only the winner or aggregate. Verify that A and B are not accidentally identical and that both are coherent, on-task, non-refusing, complete, and untruncated.
- Reject or revise a scenario when every arm succeeds, every arm fails, outputs visibly struggle with the harness, or the test cannot distinguish the intended behavior. These are harness observations, not model results.
- Ask evaluated agents for an unscored exit interview about ambiguity, missing context, broken tools, unnatural constraints, and other harness problems. Save and read the feedback, but do not let self-report override task evidence.
- Save full append-only traces in JSONL or Inspect `.eval`, including prompts, responses, provider-exposed reasoning and tool events, artifacts, machine checks, both judgment orders, usage, costs, and errors. Use Inspect Scout or an equivalent transcript audit when practical.
- Before reporting a winner, make a judgeable per-scenario audit that links the A output, B output, machine result, forward and reversed judge rationales, saturation status, and the human validity decision.

[^zheng]: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023) — https://arxiv.org/abs/2306.05685
[^wang]: Wang et al., "Large Language Models are not Fair Evaluators" (ACL 2024) — https://arxiv.org/abs/2305.17926
[^panickssery]: Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations" (2024) — https://arxiv.org/abs/2404.13076
[^verdict]: Haize Labs, verdict docs: [best practices](https://verdict.haizelabs.com/docs/best-practices/), [distributional bias cookbook](https://verdict.haizelabs.com/docs/cookbook/distributional-bias/)
