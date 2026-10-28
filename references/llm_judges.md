# LLM-as-a-judge runbook

Appendix to the [ML Debugging skill](../SKILL.md). Use it for any number that an LLM judge or a code check produced. Work through it in order: design the measurement, check the code checks, read every run, then report. Tools, providers, Jev, Petri and project lessons are in [llm_judge_notes.md](llm_judge_notes.md). The papers behind the numbers are in [llm_judge_litreview.md](llm_judge_litreview.md).

> What distributions are we trying to distinguish, with which measurement? Does a measurement add bias, standard deviation, or help separate them?
>
> — wassname, spelling corrected; "std" expanded to "standard deviation"

Contents:

- [Design the measurement](#design-the-measurement)
- [Check the code checks before the judge](#check-the-code-checks-before-the-judge)
- [Every judged run, before you report a number](#every-judged-run-before-you-report-a-number)
- [If you see this, check that](#if-you-see-this-check-that)
- [Replay a puzzling verdict on a reasoning model](#replay-a-puzzling-verdict-on-a-reasoning-model)
- [When a reader is confused, repair the setup first](#when-a-reader-is-confused-repair-the-setup-first)
- [Missing scores](#missing-scores)
- [Repeats, temperature and paired differences](#repeats-temperature-and-paired-differences)
- [What a measurement can separate](#what-a-measurement-can-separate)
- [Numbers worth knowing (2026)](#numbers-worth-knowing-2026)
- [The measured biases](#the-measured-biases)

## Design the measurement

Start from the competing explanations for the result. Suppose steering raises a virtue score. Steering might have changed decisions, taught virtue words, damaged ordinary answering, or exploited a judge's preference for long answers. One average score fits all four. Measure each one separately: choices on unfamiliar scenarios, vocabulary-only examples, ordinary task quality and refusal, and the same evidence presented at a different length or position. For each test, ask which result would change your belief.

The measurement is the whole procedure: items, rendered context, question, rubric, judge model, provider and precision, answer order, reasoning budget, output schema, code checks and parsing, missing-score policy and aggregation. A change to any of these is a different measurement.

Defaults:

- Use a larger judge from a different model family than the model under test. A judge favours outputs it can recognise as its own, and small judges do this most.[^selfpref][^panickssery] How to choose: [notes](llm_judge_notes.md#choosing-the-judge-model).
- Put the whole prompt in the user turn. System prompts are not followed reliably across models and providers, and OpenRouter can route one model to providers with different chat templates.
- Word pairwise questions neutrally. "Does B show more?" makes B the subject, and the judge leans toward agreeing; "which shows more?" does not. Averaging both orders cancels the lean, and neutral wording keeps single-order scores usable. Lay the prompt out as signpost, data, then the question again. wassname's format:

  ```text
  Here are two answers to the same prompt. I will ask which has more or less of <the thing>.   # 1. signpost: what to look for
  ### Prompt
  ...
  ### Answer A
  ...
  ### Answer B
  ...                                                                                         # 2. data
  Which answer shows more of <the thing>, and by how much? Rubric: A much more / A more /
  same / B more / B much more. Reply as JSON: {"reasoning": "...", "verdict": "..."}      # 3. ask again, fresh in context
  ```

- Use a coarse scale (0–3, 1–5, or binary). If the judge gives a probability per level (a decision model such as Jev, or token logprobs), keep the vector and its expected level $\sum_k k\,p_k$, not only the top label. A judge that writes one label gives no distribution; repeat it to get one. Databricks: "Scales like 0-10 are difficult to come up with distinguishing criteria between all scores".[^databricks] Do not put an example score in the prompt: few-shot judges are "unstable when changing the label, example order, and number of examples".[^yan]
- Ask for evidence and reasons before the verdict. This changes the judgment, because it directs attention, and it gives you something to read.
- Earn each rubric line: cut lines that never change a verdict. Short domain notes per question raised human agreement from ~72–79% to 93–96%.[^gradingnotes] Expect the rubric to change after you grade outputs: "users need criteria to grade outputs, but grading outputs helps users define criteria".[^shankar] Draft, grade a sample by hand, revise, repeat.
- Score both answer orders, map back to arm identity, and keep the disagreement. Forced-choice items given to the evaluated model need both option orders too, because the evaluated model also has position bias.
- Add an unscored free-text field where the judge can flag a broken rubric, missing context or a confusing setup. Give the evaluated model the same: an unscored exit interview about ambiguity, missing context and broken tools. Say in the field description that it is never scored, or the model treats a complaint as an admission and stays quiet. Emit it after the grade, not during it. [pi-vent](https://github.com/IgorWarzocha/howaboua-pi-stuff/tree/main/packages/pi-vent) is the same idea for agents.
- Keep judge input under ~30k tokens, with the rubric and the answer at the start or end, not in the middle.[^nolima]
- Probe what the reasoning budget does on your pinned endpoint: 4 calls that vary `max_tokens`, `reasoning.max_tokens` and effort, then read the reasoning tail of each. Some providers cut reasoning early and still return `finish_reason: "stop"`. Set "high effort" explicitly; harness defaults differ about 6x.[^cais] [Measured example](llm_judge_notes.md#reasoning-budgets-on-a-pinned-endpoint).
- Set token caps far above healthy reply length, so that any cap hit means a broken reply for every model.
- Key every cache on a hash of its exact inputs, including derived files (a corpus copy, a leak-check index). An item id is not a cache key: a changed option wording or an old copy of the training data is then silently reused.
- Save append-only traces in JSONL or Inspect `.eval`: prompts, replies, provider reasoning, tool events, code-check results, both orders, usage, cost and errors. [Inspect Scout](https://meridianlabs-ai.github.io/inspect_scout/) can audit them.

## Check the code checks before the judge

Parsers, scorers and test harnesses are measurements too, and they fail without an error. In practice more bugs are found here than in the judge. Before you read any table:

1. A perfect reference scores 1, an empty reply 0, and half a reference less than 1.
2. For the same model, easy items do not score below hard ones.
3. Score 3 real replies per check kind by hand and compare with the code.
4. Count format failures for every model family you have. A model can write a right answer in a form the parser rejects.
5. Fix bugs by class (parsing, bounds, rewarding the wrong thing), with a property test per class. Have a fresh reader from another model family review the check code until a round finds nothing.

These checks catch bugs like these: a parser that expected `1: 16` rejected `1: 2 * 8 = 16`, so a model scored 0.00 on a 10-step chain but 0.30 on a 120-step one; `\boxed{64}` was scored as wrong; a cut-off JSON list was parsed as its last complete call; legal wandering in a maze was scored as progress; a test count went negative; a skipped test counted as passed.

## Every judged run, before you report a number

Do these in order, and put one quote from each in the report. If a report can be written without reading, the reading gets skipped.

1. Read one full trace for each item group you changed this round, not only a random pair. A full trace is what the model saw (system prompt, user prompt, chat template, special tokens), both replies, the judge request, its reasoning and its answer, in both orders. New or edited items are where new defects are. Check that A and B are not identical, and that both are coherent, on task, complete and not cut off. Could you reach the verdict from only what the judge saw? Hamel Husain: "You cannot write a good judge prompt until you've seen the data."[^hamel]
2. Read every vent, tag or note that is not `none`, with its pair. List the item ids, not only counts. A flag is a lead, and `none` is not clearance.
3. Count format signals per model against the previous round: empty or very short replies, parse failures, length, and cap hits. Find cap hits by length and abrupt endings, not only by `finish_reason`. A fix for one model can break another, and a cap turns verbosity into lower capability.
4. Replay the verdict that puzzles you most on a reasoning model and read its reasoning ([how](#replay-a-puzzling-verdict-on-a-reasoning-model)).
5. Check that every compared model is scored on the same rows ([why](#missing-scores)).
6. Check each label your code extracts (a first-line verdict, an action number, a JSON field) against what the reply argues, over the whole sample, with a reader model. A small model's action number can contradict its own explanation.

Before you report a winner, make a per-item audit table that links the A output, the B output, the code-check result, the judge's reasons in both orders, and your validity decision.

> Note from wassname's LLM to other LLMs: when you SHOW the human any of this (a judge trace, a compared A/B pair, a sample, a prompt design), reproduce it in FULL and verbatim, prompts, separators, special tokens, and the reasoning/thinking block included. Your trained instinct is to digest and trim; resist it, that instinct destroys exactly the boilerplate (system prompt, special tokens, separators) that the human needs to debug. Formatting may only HIGHLIGHT or REORGANISE: bold or underline the diff, split into a table, use sections, but never drop, elide with "...", or paraphrase. When comparing variants, show ALL of them this way, not a representative one. Link the source file so they can open the raw (`results/runs/.../x.jsonl`, ideally `path:line`). "Show me" means reproduce, not describe. Trim only when explicitly asked. -- CLAUDE

## If you see this, check that

| You see | Likely cause | Check |
|:--|:--|:--|
| Easy item scores below hard; a perfect reference scores below 1; a reply with every step valid scores 0 | Bug in a code check | [Code checks](#check-the-code-checks-before-the-judge) |
| Scores do not change after you changed items or prompt | Stale cache | Cache key covers the exact inputs |
| One model looks worse at a skill, and it writes long replies | Token cap | Share of cap hits per model |
| A judge given the code-check results agrees with them (r ≈ 0.9) | The judge copies the facts it is given | What the judge adds beyond those facts; read the disagreements |
| A long input judged "never off track" although it has contradictions | Weak judge on a long input | Replay on a reasoning model |
| A verdict you cannot explain | Confusing question, levels or layout; or a near-tie | [Replay](#replay-a-puzzling-verdict-on-a-reasoning-model) |
| High order-flip rate | Position bias, worst on close pairs | Read the close pairs; average both orders |
| The judge always picks A | Position bias, or a protest | Read its reasons |
| Every response gets the same score | Saturation, or a scale or parse failure | Known positive and negative cases; raw vectors |
| Scores cluster on one level | The population, or a judge that cannot use the scale | Histogram against known contrasts |
| A model improves after failed rows were dropped | Different rows compared | [Missing scores](#missing-scores) |
| A yes/no flag is the same for very different failures | A binary flag hides severity | Grade each step |
| An extracted label contradicts the reply's text | Extraction bug, or model inconsistency | Reader-model check (step 6 above) |
| Repeats disagree widely | Noise dominates | More items; do not lower the temperature |
| A call "timed out" | It may have been reasoning behind a buffer | Event timestamps and transport state |

> Did it time out, or was it reasoning behind a buffer for longer than you think? Check the event timestamps and transport state. -- wassname

## Replay a puzzling verdict on a reasoning model

A judge that writes no reasons (Jev), or hides them, can't tell you why it chose. Replay as soon as a verdict puzzles you, not after several failed repairs.

1. Dump the exact request the judge saw from the cache by request key, one file per answer order.
2. Remove the original verdict from each file, or the replay anchors on it.
3. Give each file to a fresh agent on a model with visible reasoning (e.g. DeepSeek), one order per agent. Ask it to reason in writing, answer in the judge's format, and say what in the question, levels or layout confused it.
4. Read its reasoning, not only its answer.
5. Treat its complaints as hypotheses. Test each against existing data before you act on it.

Possible readings, each a hypothesis to test: the same verdict for opposite reasons in each order can be a near-tie with offsetting strengths, or a judge that follows position; check the close pairs. A replay that applies a rubric limit the judge ignored can mean the rubric format does not suit that judge, or that the judge cannot do the task; test by moving the limit into a worked example.

## When a reader is confused, repair the setup first

Confusion is evidence against the evaluation setup before it is evidence against the model:

1. Quote the first complete passage where the candidate's or judge's reading stops being justified by the information it received. Label the raw field. Keep feedback or an exit interview separate from the score.
2. Map that reading to the exact instruction, rubric line, supplied context, answer budget, or harness condition that allowed it. Check the intended construct independently.
3. Make the smallest setup repair. Test it on an independent reader. Reject the repair if it gives away the answer or leaves the same confusion. Call it a model or judge error only after the setup rules out that reading.

-- GPT-5.6-sol

wassname, 2026-10-10, on debugging contrastive-pair generation and on-policy rewriting (spelling fixed, wording kept; bracketed clarification added at his request):

> Properly, iteratively, debug the data generation and the on-policy rewrite: at least 10 iterations, and fix it properly. Don't overfit by accumulating patches; take a step back and fix the process. This is always needed and always fails naively. First, models (1) don't do anything and rely on some naive, failing judge setup; (2) skim, or have a subagent skim, misdiagnose a problem, and treat the symptom ("don't cough", or "don't make stuff up") instead of reading the full trace (system prompt, user prompt, CoT [the hidden reasoning, e.g. in `<think>` tags or the provider's reasoning field, not reasoning written in the visible reply], response, and comparing base and/or cho and rej) and thinking "oh, the model makes stuff up because I haven't given it context or facts", "could I solve it?", "oh, it seems confused by X"; and finally (3) they do one iteration of this when they should do as many as needed. Sometimes they also use judges that are too dumb. Limit judge input to <30k tokens without follow-up, as in the gist.

In practice: fix each defect's cause in the generator's input, re-run the same seeded items, and log defect counts with quotes per round, so rounds are compared with each other, not with memory.

wassname, 2026-10-10, on oracle panels (spelling fixed, wording kept):

> It's super easy and common to put your perspective into the primer, and get your perspective out, and this is a sign of that. If you don't get surprising insight or genuine viable disagreement, you need to improve the framing to bias less, observe and add context more, invite a wider perspective, and rerun.
>
> The second most important one is confusion! If one LLM is confused, you need to read very carefully for any incoherent or unviable solutions. I've had ones that are super obvious to me, but the panel says it and the agent running it takes it at face value.

In practice: a brief gives setup, code and raw observations, and asks for competing explanations with tests. It holds back your hypothesis and earlier answers. Agreement under a leading brief is not evidence. Check each answer claim by claim against the code or the math.

## Missing scores

> "If there are NaNs, we should not drop them, else we end up comparing different sample sets and it's invalid. A might be a single easy sample, and B might be all 128 hard samples. Of course A looks much better, but actually it failed on the vast majority of samples." - wassname, lightly edited for spelling

Pandas [`mean`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mean.html) and [`GroupBy.mean`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.typing.DataFrameGroupBy.mean.html) skip missing values by default, so a plain aggregate-then-plot pipeline makes this error without an explicit `dropna`.

Classify every missing score before you plot or rank:

- A model refusal or task failure gets the metric's defined failure score: `scores.fillna(bad_result).mean()`, once every NaN is known to mean model failure.
- A judge, parser, timeout or infrastructure failure fails the eval and is rerun, never filled.
- A reply whose label looks unreliable is scored as its own outcome ("unclear"), not excluded. Exclusion drops more rows from the weaker model.

Do not use `nanmean`, `skipna` or independent `dropna`. Report coverage and failure reasons beside the scores. Restricting all arms to their shared complete rows makes the comparison paired, but can still keep only the easy rows and does not support an overall ranking.

## Repeats, temperature and paired differences

Evan Miller's "Adding Error Bars to Evals" gives three cheap rules.[^miller]

- Average K draws per question, then take the standard error across question means. In his uniform-difficulty example: "Going from K = 1 (no resampling of answers) to K = 2, the total variance is reduced by 1/3. Increasing to K = 4, we have a variance reduction of 1/2 [...] The upper limit on variance reduction via resampling in this example is 2/3." Draws remove only reply-level noise; only more questions reduce question-difficulty variance. Do not pool K×N answers into one standard error. inspect's `epochs` already reduces this way.
- Do not lower the temperature to make numbers look stable: "adjusting the sampling temperature may simply shift the conditional variance [...] into the variance of the conditional means (which cannot [be mitigated]), or else reduce conditional variance by injecting bias into the estimator." T=0 is fine when you want to study the model at T=0, but then repeats no longer measure noise.
- Compare per-question paired differences, not two separate bars (same rule as [sweeps](sweeps.md)). Question scores of frontier models correlate "between 0.3 and 0.7", so pairing is "a 'free' variance reduction technique".
- The unit of uncertainty is the original item. Both answer orders, reversed options and repeat draws of one item are one item: average them first. Related items (variants of one scenario) need grouped or clustered standard errors, or the error bars are too narrow.

For sampled generative judges, run 3–10 identical judgments on a few items and check the spread. More than ~10 mostly costs tokens.[^loo] For a near-deterministic decision model such as Jev, repeats add little; use the order checks in the [Jev section](llm_judge_notes.md#jev-a-calibrated-decision-model-as-a-cheap-judge). Report the number of questions beside every score.

## What a measurement can separate

Keep three distributions apart: variation between items, uncertainty about one item's label, and variation between repeated calls on one item. A judge that returns .5 everywhere is uncertain per answer and separates no items. A judge near 0 or 1 can separate items well, if its answers change with the behaviour of interest.

For a binary label $X$ with $p = P(X=1)$, entropy in bits is

$$H(X)=-p\log_2 p-(1-p)\log_2(1-p).$$

Constant labels carry zero bits. Ten deterministic copies of one balanced label carry one bit; ten independent balanced labels carry ten. Useful information is variation that separates the hypotheses or predicts a reference label; a random bit has entropy but no use. A question can add information through its disagreements even when its mean barely moves. Do not infer an effective question count from correlation alone. Jev's question isolation is an attention rule, not statistical independence.

Saturation is the loss of a distinction you need: if both compared populations always get the top score, the scale cannot separate them, though it can still show that both pass a minimum. Check known positive and negative cases and raw vectors before you blame the population, the rubric, the judge or the parser. A skewed histogram alone is not a reason to reject a measurement.

Aggregation discards information. On levels 0–4, `[.5,0,0,0,.5]` and `[0,0,1,0,0]` both have expected score 2. Keep the vectors. A yes/no flag discards severity: "3 falsified records" and "1 off-by-one among 8 honest writes" both score "yes". Grade each step. For a trajectory, keep both when it first slips and how much of it is wrong. A combined step score (full credit before the first slip, half credit for right steps after it) is more informative than either number alone, but keep the two raw numbers too.

Bias and noise matter only through the comparison. A useful working decomposition:

$$\widehat{\Delta}_M=\Delta_{\mathrm{target}}+b_M+\epsilon_M,$$

where $\widehat{\Delta}_M$ is the observed contrast under procedure $M$, $\Delta_{\mathrm{target}}$ is the intended behavioural contrast, $b_M$ is differential systematic measurement error, and $\epsilon_M$ is sampling error. A shared offset cancels in a paired comparison. Bias that changes with length, model family or treatment can look like a treatment effect. Low standard deviation is not the goal: a constant judge is perfectly stable and separates nothing. Repeats reduce sampling error but repeat a shared misreading.

A measurement is worth running when its possible results would change your belief about the live hypotheses. Formally, expected information gain:

$$\operatorname{EIG}(M)=\mathbb{E}_{z\mid D,M}\!\left[\operatorname{KL}\!\left(p(H\mid D,z,M)\,\Vert\,p(H\mid D)\right)\right],$$

where $H$ indexes hypotheses, $D$ is existing evidence and $z$ is a possible result of $M$. You usually cannot estimate it; use it to ask which affordable test separates the live explanations.

## Numbers worth knowing (2026)

Rules of thumb with verbatim quotes. Full passages and calibration are in [llm_judge_litreview.md](llm_judge_litreview.md).

- Swap the order and average, on every judge. An independently run benchmark of 36 models: "the model-average order-flip rate is 43.0%, and the median model flips in 41.3% of decisive two-view cases".[^lechmazur] A peer-reviewed study of 150k+ judgments finds position bias "is strongly affected by the quality gap between solutions",[^shi] so it is worst on close pairs. Even a frontier model flips ~66%; a bigger judge is not a fix.
- Don't let a small model grade its own family: "the DBG score of Qwen2.5-0.5B-Instruct is 41.7%. In contrast, the DBG score of Qwen2.5-14B-Instruct is only 2.1%", and "the self-preference bias in reasoning models is not necessarily less significant".[^selfpref] The size effect is partly confounded with capability.
- A reasoning judge probably grades better but is not less biased. Single-group result: RL-trained judges "consistently outperform SFT-tuned baselines in the same size".[^judgelrm] Use one when grading needs verification work; expect the length, position and style biases to remain.
- Match the thinking budget to difficulty: "accuracy increases from 82.2% to 87.3% as the average number of thinking tokens increases from 385 to 1100. However, this trend does not continue indefinitely".[^overthink] On easy items cap thinking low and spend the savings on repeats. On hard items a low cap scores a cut-off verdict as a real one.
- Set "high effort" explicitly. litellm's default caps it at 4096 tokens; CAIS simple-evals uses "DEFAULT_REASONING_EFFORT_HIGH_THINKING_BUDGET=24576".[^cais]
- Self-consistency "gains plateau early and, in some configurations, decline at high sample counts" (single-author preprint), around N=10–15 on strong 2026 models.[^loo]
- Keep inputs short and edge-loaded: "At 32K, for instance, 11 models drop below 50% of their strong short-length baselines".[^nolima]

## The measured biases

Position bias can flip rankings. Wang et al.: "the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context. [...] e.g., Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator."[^wang]

Zheng et al. list "position, verbosity, and self-enhancement biases, as well as limited reasoning ability".[^zheng] They also report GPT-4 agreement with human preference "over 80%", the same as human-human agreement.

Self-preference tracks self-recognition: "a linear correlation between self-recognition capability and the strength of self-preference bias".[^panickssery] Judging a model with itself or a sibling checkpoint is biased by design.

Score distributions have quirks (practitioner notes): the gpt-4o family skews scores upward and mode-collapses even with logprobs; llama-family judges give more spread; JSON-mode decoding shifts scores. Same-model verification gives a positive skew "that may not discriminate faithfully".[^verdict]

Judges miss injected regressions: evaluators "failed to identify quality drops in over 50% of cases on average".[^doddapaneni] Judge quality can be benchmarked on [JudgeBench](https://huggingface.co/spaces/ScalerLab/JudgeBench).

<!-- Agent-written (PI/OpenAI, PI/Sol, PI/Claude; see git log) from wassname's guidance. Quoted passages are attributed inline. Project evidence for the examples: llm_judge_notes.md#evidence-behind-the-llm_judgesmd-examples -->

[^zheng]: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023) — https://arxiv.org/pdf/2306.05685
[^wang]: Wang et al., "Large Language Models are not Fair Evaluators" (ACL 2024) — https://arxiv.org/pdf/2305.17926
[^panickssery]: Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations" (2024) — https://arxiv.org/pdf/2404.13076
[^verdict]: Haize Labs, verdict docs: [best practices](https://verdict.haizelabs.com/docs/best-practices/), [distributional bias cookbook](https://verdict.haizelabs.com/docs/cookbook/distributional-bias/)
[^hamel]: Hamel Husain, "Creating a LLM-as-a-Judge That Drives Business Results" (2024) — https://hamel.dev/blog/posts/llm-judge/ (critique-shadowing workflow: look at the data first, iterate the prompt with a domain expert, prefer binary pass/fail) ([cache](../docs/evidence/llm_judge_biases.md))
[^databricks]: Databricks, "Best Practices for LLM Evaluation of RAG Applications" (2023) — https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG (use a low-precision 0-3 / 1-5 scale; few-shot examples help weak judges but shift the score distribution) ([cache](../docs/evidence/llm_judge_biases.md))
[^gradingnotes]: Databricks, "Enhancing LLM-as-a-Judge with Grading Notes" (2024) — https://www.databricks.com/blog/enhancing-llm-as-a-judge-with-grading-notes (per-question domain rubrics lifted human-alignment to 93-96%) ([cache](../docs/evidence/llm_judge_biases.md))
[^yan]: Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)" — https://eugeneyan.com/writing/llm-evaluators/ (survey of position, verbosity, and few-shot-instability biases; argues for binary over Likert; collects G-Eval, Doddapaneni blind-spots, Shankar "Who Validates the Validators?") ([cache](../docs/evidence/llm_judge_biases.md))
[^doddapaneni]: Doddapaneni, Khan, Verma, Khapra, "Finding Blind Spots in Evaluator LLMs with Interpretable Checklists" (2024) — https://arxiv.org/pdf/2406.13439 (evaluator LLMs missed injected quality drops in >50% of cases) ([cache](../docs/evidence/llm_judge_biases.md))
[^shankar]: Shankar, Zamfirescu-Pereira, Hartmann, Parameswaran, Arawjo, "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences" (2024) — https://arxiv.org/pdf/2404.12272 (criteria drift; LLM evaluators need human validation) ([cache](../docs/evidence/llm_judge_biases.md))
[^lechmazur]: Lech Mazur, position_bias benchmark — https://github.com/lechmazur/position_bias (independent, outsider-run swapped-order harness; 193 pairs, 36 models, 2026-era; strong trust signal, but a solo-run leaderboard not a paper) ([litreview](llm_judge_litreview.md))
[^shi]: Shi et al., "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge" (IJCNLP-AACL 2025) — https://arxiv.org/pdf/2406.07791 (peer-reviewed; 150k+ instances, 15 judges; bias worsens as the answer quality gap shrinks) ([litreview](llm_judge_litreview.md))
[^selfpref]: Chen et al., "Beyond the Surface: Measuring Self-Preference in LLM Judgments" (EMNLP 2025 main) — https://arxiv.org/pdf/2506.02592 (peer-reviewed; DBG nets out quality; larger judges less self-biased, though authors credit capability; reasoning models still biased) ([litreview](llm_judge_litreview.md))
[^judgelrm]: Chen et al., "JudgeLRM: Large Reasoning Models as a Judge" (2025) — https://arxiv.org/pdf/2504.00050 (single-group preprint, not independently replicated; RL-trained reasoning judges beat same-size SFT, ~+8 F1 headline in body) ([litreview](llm_judge_litreview.md))
[^overthink]: Ghosal et al., "Does Thinking More always Help? ... Mirage of Test-Time Scaling in Reasoning Models" (2025) — https://arxiv.org/pdf/2506.04210 (preprint; one controlled study, accuracy-vs-thinking-token curve is non-monotonic, peak setup-specific) ([litreview](llm_judge_litreview.md))
[^cais]: CAIS simple-evals .env.example vs litellm constants.py (fetched 2026-07, directly verifiable config) — https://github.com/centerforaisafety/simple-evals/blob/main/.env.example (effort high=24576/med=8192/low=1024, overriding litellm stock 4096/2048/1024)
[^loo]: Loo, "Self-Consistency Is Losing Its Edge: Diminishing Returns and Rising Costs in Modern LLMs" (2025) — https://arxiv.org/pdf/2511.00751 (single-author preprint, low citation signal; plateau ~N=10-15 on modern models, can decline past it) ([litreview](llm_judge_litreview.md))
[^miller]: Evan Miller (Anthropic), "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations" (2024) — https://arxiv.org/pdf/2411.00640, short version https://www.anthropic.com/research/statistical-approach-to-model-evals ([cache](../docs/evidence/miller_2024_error_bars_evals.md)). arXiv stat.AP preprint, not peer reviewed, but the statistics are textbook and the recommendations show up in tooling (inspect `epochs`). The variance fractions come from one uniform-difficulty toy example, so treat the direction as general and the numbers as illustrative.
[^nolima]: Modarressi et al., "NoLiMa: Long-Context Evaluation Beyond Literal Matching" (ICML 2025) — https://arxiv.org/pdf/2502.05167 (peer-reviewed; effective length = length holding 85% of base score; most models below half by 32K once literal cues removed) ([litreview](llm_judge_litreview.md))
