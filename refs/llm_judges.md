# LLM-as-a-judge: known biases and mitigations

Appendix to the [ML Debugging skill](../SKILL.md). When an LLM-judged eval looks surprisingly good, or a ranking flips between runs, suspect the judge before the model. Each bias below has been measured; verbatim sources in [docs/evidence/llm_judge_biases.md](../docs/evidence/llm_judge_biases.md).

## The measured biases

Position bias is large enough to flip rankings outright. Wang et al. (ACL 2024):

> the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context. [...] e.g., Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator.[^wang]

Zheng et al. (the MT-Bench paper) named the wider taxonomy: "position, verbosity, and self-enhancement biases, as well as limited reasoning ability"[^zheng]. Their headline agreement number (GPT-4 matches human preference "over 80%", the same as human-human agreement) is the case *for* LLM judges; the bias list is the fine print.

Self-preference tracks self-recognition. Panickssery et al. fine-tuned models to vary self-recognition ability and found "a linear correlation between self-recognition capability and the strength of self-preference bias"[^panickssery], with controlled experiments supporting a causal reading. A judge that can tell its own outputs apart will favor them, so judging a model with itself (or a sibling checkpoint) is structurally biased.

There are also output-distribution quirks. From Haize Labs' verdict docs (practitioner notes): the gpt-4o family skews numerical scores upward and mode-collapses even with logprobs; llama-family judges give higher-entropy, more discriminative score distributions; JSON-mode constrained decoding imposes its own inductive bias on scores.[^verdict]

And the judge misses more than you'd think. Doddapaneni et al. probed evaluator LLMs with deliberately degraded answers and found they "failed to identify quality drops in over 50% of cases on average"[^doddapaneni]. A judge that silently passes half the injected regressions is not a safety net.

## Mitigation checklist

From Wang's calibration framework and verdict's best-practices page:

- Ask for an explanation or justification *before* the score, not after.
- Score both orderings and aggregate (Wang's Balanced Position Calibration); at minimum, randomize position and check the flip rate.
- Use a different model family for the judge (and for any verifier-of-the-judge) than the one being evaluated. Same-model verification produces a positive skew "that may not discriminate faithfully".[^verdict]
- Inspect the raw score distribution before trusting means: mode collapse or skew means the scale isn't being used.
- Spot-check judge verdicts against your own reading of ~20 transcripts (the [Ng error-analysis move](../SKILL.md#inspect-the-data-first), applied to the judge).
- Judge quality is benchmarkable: [JudgeBench](https://huggingface.co/spaces/ScalerLab/JudgeBench) ranks judges on objective-correctness pairs.

## Choosing the judge model

Pick from the cost-vs-score Pareto frontier of a judging leaderboard, and prefer a well-known model so your setup is reproducible. [Judgemark v4](https://eqbench.com/judgemark-v4.html) is "a meta-evaluation of LLM judging ability. The model being tested is the judge, not the writer",[^judgemark] scoring how well a judge's ratings separate stronger from weaker writing, and it lists a cost per model. Its lesson (wassname's read): the smartest models are the best judges, so the value frontier is the capable-but-cheap models, not the single top scorer. Caveat: Judgemark scores creative-writing discrimination, so a judge that tops it may not transfer to code- or fact-correctness judging.

From the checked-in v4 scores (snapshot 2026-07, [source](https://github.com/EQ-bench/EQ-bench-site/blob/main/judgemark-v4.js)) the cost-vs-score frontier runs from the top absolute scorers, claude-opus-4-6 (0.91, ~$39) and gpt-5.5 (0.88, ~$30), down through claude-sonnet-4-6 and gemini-3.1-pro (~0.8, ~$23), grok-4.5 (0.77, $17) and GLM-5.2 (0.73, $8), to the cheap knee google/gemma-4-31b (0.72 at $0.82), which nearly matches models 20-40x its price.

But a frontier score isn't sufficient: refusals wreck ambiguous or red-teaming evals, and refusal is topic-conditional. Check refusal rates on [speechmap.ai](https://speechmap.ai/), which "publish[es] refusal rates for every model release from every major provider".[^speechmap] The cheap-and-capable Gemma refuses many contentious tasks; Chinese models (GLM, Qwen, DeepSeek) tend to refuse on Chinese political topics; US models on corporate or left-coded topics, with Grok among the exceptions. So check refusal on *your* eval's subject matter, not in the abstract, and re-read the live leaderboards rather than trusting these names, they date fast.

## wassname's judge-validity checklist

Practical rules from wassname for before you trust any LLM-judged number. A failed check is evidence about the *test*, not the model, so revise or reject the scenario before drawing a behavioral conclusion.

Earn the rubric's ink:

- Does each rubric line ever flip a verdict? Cut criteria that never change the score. Rubric quality is the main lever: a judge lacking domain knowledge will "overestimate the effectiveness by a significant margin", and adding brief domain notes raised human-alignment from ~72-79% to 93-96%.[^gradingnotes]
- Expect criteria drift: you can't fully write the rubric before seeing outputs. Shankar et al. name it, "users need criteria to grade outputs, but grading outputs helps users define criteria"[^shankar], and warn that "LLM-generated evaluators simply inherit all the problems of the LLMs they evaluate, requiring further human validation."[^shankar] Draft the rubric, grade a sample by hand, revise, repeat.

Read a whole trace, not the aggregate:

- Read one complete judge trace end to end: system prompt, user prompt, the exact chat template and special tokens, the judge's saved reasoning, and its reply. Formatting bugs corrupt a judge the way they corrupt any model (see the [template/BOS-mismatch failure](../SKILL.md#chat-template-and-bos-handling-must-match-across-train-and-deploy-unsloth)). Hamel Husain: "You cannot write a good judge prompt until you've seen the data."[^hamel]
- Read both compared outputs for every scenario, not just the winner or aggregate. Verify A and B are not accidentally identical and that both are coherent, on-task, non-refusing, complete, and untruncated.
- Could you reproduce the verdict from only what the judge sees? If you can't judge it, neither can the model. This is the [Ng error-analysis move](../SKILL.md#inspect-the-data-first) applied to the judge.
- Chase confusion: if the judge hedges, asks for missing context, or self-contradicts, that is a harness fault, not a result ([investigate confusion](../SKILL.md#pursue-anomalies-investigate-confusion)).

Check the score distribution:

- Not saturated: reject scenarios where every arm passes or every arm fails (too easy or too hard leaves nothing to discriminate).
- Not clustered: plot the raw histogram. Mode collapse or skew means the scale isn't being used.[^verdict]
- Not anchored: don't put an example score in the prompt. A few-shot "+2" pulls a weak judge toward +2, and Eugene Yan's survey notes few-shot judges are "unstable when changing the label, example order, and number of examples".[^yan] Ask for a bare integer or label, and prefer a coarse scale: Databricks recommend a low-precision range (0-3 or 1-5) because "Scales like 0-10 are difficult to come up with distinguishing criteria between all scores".[^databricks] Hamel is blunter, preferring binary: "If your evaluations consist of a bunch of metrics that LLMs score on a 1-5 scale (or any other scale), you're doing it wrong."[^hamel]

Check stability across order and repeats:

- Position: score both orderings, map back to arm identity, report strict reversals (mechanics in the mitigation checklist above). Watch for a judge that always picks A, sometimes a model does this in protest.
- Repeat variance: run N>=3-4 identical judgements and check the spread. If repeats disagree wildly the signal is noise, the same canary as [seed variance](../SKILL.md#seed-variance-you-cant-tell-a-bug-from-bad-luck): "Instability to random seed is like a canary in a coal mine."

Give the judge a voice, and save everything:

- Add a free-text field for the judge to flag a broken, missing, or ambiguous rubric or context. Read it, but keep it out of the score. Do the same for the evaluated agents: an unscored exit interview about ambiguity, missing context, broken tools, and unnatural constraints, kept separate from the task score.
- Save full append-only traces in JSONL or Inspect `.eval`, including prompts, responses, provider-exposed reasoning and tool events, artifacts, machine checks, both judgment orders, usage, costs, and errors. Use [Inspect Scout](https://meridianlabs-ai.github.io/inspect_scout/) or an equivalent transcript audit when practical.
- Before reporting a winner, make a judgeable per-scenario audit that links the A output, B output, machine result, forward and reversed judge rationales, saturation status, and the human validity decision.

For a worked example, wassname has a ~300-line async OpenRouter judge (WIP) that implements many of these: bounded thinking, pinned quantisation, a versioned eval, JSON-schema output, JSONL of everything, OpenRouter error handling, and position-bias swapping: [gist](https://gist.github.com/wassname/b7f76e42de131887c02d9e9835be80ef).

[^zheng]: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023) — https://arxiv.org/abs/2306.05685
[^wang]: Wang et al., "Large Language Models are not Fair Evaluators" (ACL 2024) — https://arxiv.org/abs/2305.17926
[^panickssery]: Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations" (2024) — https://arxiv.org/abs/2404.13076
[^verdict]: Haize Labs, verdict docs: [best practices](https://verdict.haizelabs.com/docs/best-practices/), [distributional bias cookbook](https://verdict.haizelabs.com/docs/cookbook/distributional-bias/)
[^hamel]: Hamel Husain, "Creating a LLM-as-a-Judge That Drives Business Results" (2024) — https://hamel.dev/blog/posts/llm-judge/ (critique-shadowing workflow: look at the data first, iterate the prompt with a domain expert, prefer binary pass/fail) ([cache](../docs/evidence/llm_judge_biases.md))
[^databricks]: Databricks, "Best Practices for LLM Evaluation of RAG Applications" (2023) — https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG (use a low-precision 0-3 / 1-5 scale; few-shot examples help weak judges but shift the score distribution) ([cache](../docs/evidence/llm_judge_biases.md))
[^gradingnotes]: Databricks, "Enhancing LLM-as-a-Judge with Grading Notes" (2024) — https://www.databricks.com/blog/enhancing-llm-as-a-judge-with-grading-notes (per-question domain rubrics lifted human-alignment to 93-96%) ([cache](../docs/evidence/llm_judge_biases.md))
[^yan]: Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)" — https://eugeneyan.com/writing/llm-evaluators/ (survey of position, verbosity, and few-shot-instability biases; argues for binary over Likert; collects G-Eval, Doddapaneni blind-spots, Shankar "Who Validates the Validators?") ([cache](../docs/evidence/llm_judge_biases.md))
[^judgemark]: EQ-Bench, "Judgemark v4" — https://eqbench.com/judgemark-v4.html (meta-eval of a model's judging ability, scored by how well its ratings separate stronger from weaker writing; leaderboard shows cost per model)
[^speechmap]: SpeechMap.ai — https://speechmap.ai/ (refusal / completion rates across providers on contentious prompts; useful for spotting a judge that will refuse ambiguous or red-teaming scenarios)
[^doddapaneni]: Doddapaneni, Khan, Verma, Khapra, "Finding Blind Spots in Evaluator LLMs with Interpretable Checklists" (2024) — https://arxiv.org/abs/2406.13439 (evaluator LLMs missed injected quality drops in >50% of cases) ([cache](../docs/evidence/llm_judge_biases.md))
[^shankar]: Shankar, Zamfirescu-Pereira, Hartmann, Parameswaran, Arawjo, "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences" (2024) — https://arxiv.org/abs/2404.12272 (criteria drift; LLM evaluators need human validation) ([cache](../docs/evidence/llm_judge_biases.md))
