# LLM-as-a-judge: design a measurement that separates the hypotheses

Appendix to the [ML Debugging skill](../SKILL.md). Start with the competing explanations for your result, then choose measurements that distinguish them. Read a complete sample before interpreting the aggregate.

> What distributions are we trying to distinguish, with which measurement? Does a measurement add bias, standard deviation, or help separate them?
>
> — wassname, spelling corrected; “std” expanded to “standard deviation”

**Every judged run, before you report a number.** Do these in order, and put one quote from each in the report; a report that can be written without reading lets the reading be skipped.

1. Read one full trace (what the model saw, both replies, the judge request and answer, both orders) for each item group you changed this round, not only a random pair. New or edited items are where new defects are.
2. Read every vent, tag or note that is not `none`, with its pair. A table of counts is not enough; list the item ids.
3. Count cheap format signals per model against the previous round: empty or very short replies, cut-offs, parse failures, length. A fix for one model can break another.
4. Replay the verdict that puzzles you most on a reasoning model and read its chain of thought ([how](#wassnames-judge-validity-checklist)).
5. Check that every compared model is scored on the same rows ([why](#wassnames-judge-validity-checklist)).
6. Treat every code check as a measurement too. Before reading a table, a perfect reference must score 1, an empty reply 0, half a reference less than 1, and easy must not score below hard; then score 3 real replies per check kind by hand, and audit format failures over every model family you have.
7. Count replies that hit the token cap, per model. A cap turns verbosity into lower capability.

Example (tiny-character items v2, 2026-10-27): random traces showed old items; reading the new items found gemma-27B narrating the world after its choice. A later prompt fix ("and stop there") made gemma-4B answer with a bare number in 20/160 replies, found only by counting short replies against the previous round. -- PI/Sol

Example (tiny-character, 2026-10-28): 16 bugs in one day were in code checks, not the judge, and each broke a simple prior first: gemma-4B scored 0.00 on a 10-step arithmetic chain but 0.30 on a 120-step one (the parser wanted `1: 16`, the model wrote `1: 2 * 8 = 16`); 19 of 36 competition-maths replies "failed" because they wrote `\boxed{64}`, which halved the reported 4B score. A 700-token maths cap cut 5–11% of replies. Fix bugs by class (parsers, bounds, rewarding the wrong thing), with a property test per class, and keep fresh-eyes reviews from another model family until a round finds nothing. -- PI/Sol

Contents:

- [Start with the distinctions you need](#start-with-the-distinctions-you-need)
- [Useful information, redundancy and saturation](#useful-information-redundancy-and-saturation)
- [Bias and noise matter through the comparison](#bias-and-noise-matter-through-the-comparison)
- [Debugging practices as tests of the measurement](#debugging-practices-as-tests-of-the-measurement)
- [wassname's judge-validity checklist](#wassnames-judge-validity-checklist)
- [Read full traces and iterate on the process (wassname)](#read-full-traces-and-iterate-on-the-process-wassname)
- [Repeat draws, temperature, and paired differences](#repeat-draws-temperature-and-paired-differences)
- [Numbers worth knowing (2026)](#numbers-worth-knowing-2026)
- [The measured biases](#the-measured-biases)
- [Mitigation checklist](#mitigation-checklist)

Judge-model choice, providers, Jev, Petri, rubric-point judging, training-data judges and per-project notes are in [llm_judge_notes.md](llm_judge_notes.md); read it when you set up a judge or use one of those tools.

## Start with the distinctions you need

Suppose steering raises a virtue score. It might have changed decisions, taught virtue-related vocabulary, damaged ordinary answering, or exploited a judge's preference for longer answers. These hypotheses predict different distributions over new scenarios. A single average virtue score may fit all four.

Measure the distinctions separately: choices on unfamiliar scenarios, vocabulary-only examples, ordinary task quality and refusal, and the same evidence presented with different length or position. Ask which observation would change your belief about the competing explanations. A test can be precise and repeatable while measuring the wrong distinction.

The measurement is the whole procedure: sampled items, rendered context, questions, rubric, model/provider/precision, answer order, reasoning budget, output schema, validation, missing-score policy and aggregation. Asking for evidence and an explanation before rating changes that procedure. It can direct attention and improve the judgment, like a checklist; it is not merely an audit field added after an unchanged verdict. Test the procedure on cases whose relevant difference you can inspect yourself.

## Useful information, redundancy and saturation

Keep three distributions distinct: variation between original items, uncertainty about one item's label, and variation between repeated calls on that same item. A judge returning .5 everywhere has high uncertainty per answer but does not separate items. A judge returning probabilities near 0 or 1 can separate items well if those probabilities change with the behavior of interest.

For a binary label $X$, entropy is:

$$H(X)=-p\log_2 p-(1-p)\log_2(1-p),\qquad p=P(X=1).$$

Entropy measures variation in bits. Constant labels carry zero bits of variation across the evaluated population. Ten deterministic copies of one balanced binary label carry one bit jointly, while ten independent balanced labels carry ten bits. Partial correlation does not make questions equivalent, and pairwise zero correlation does not establish joint independence. Jev's question isolation is an attention rule, not statistical independence.

Useful information is variation that distinguishes the hypotheses or predicts a relevant reference label. An unrelated random bit has entropy without that usefulness. Conditional information asks what another question adds after the existing questions. A question can help through a disagreement pattern even when its individual mean barely changes. Do not infer an effective question count from correlation alone, or multiply marginal probabilities into a joint probability without a justified model.

Saturation is loss of a distinction you need: if both compared populations always receive the same maximum score, that scale cannot resolve their difference here. It may still correctly establish that both clear a minimum requirement. Check known positive/negative cases and raw vectors before deciding whether the population, rubric resolution, judge or parsing caused the flat scores. Do not reject a measurement solely because its histogram is skewed.

Aggregation can discard information already measured. On levels 0–4, vectors `[.5,0,0,0,.5]` and `[0,0,1,0,0]` both have expected score 2: unresolved extremes and a concentrated middle verdict become identical. Preserve the vectors, not only the expectation or winning option. A yes/no flag discards severity at the other end: "3 falsified records" and "1 off-by-one among 8 honest writes" both score "yes". Grade each step, and for a trajectory keep both when it first slips and how much of it is wrong; a step score with full credit before the first slip and half credit for right steps after it carries both.

## Bias and noise matter through the comparison

On a common measurement scale, a useful working decomposition is:

$$\widehat{\Delta}_M=\Delta_{\mathrm{target}}+b_M+\epsilon_M,$$

where $\widehat{\Delta}_M$ is the observed contrast under procedure $M$, $\Delta_{\mathrm{target}}$ is the intended behavioral contrast on that scale, $b_M$ is differential systematic measurement error, and $\epsilon_M$ is sampling error. This is a diagnostic model, not an assumption that the unknown terms have been identified.

A shared offset can cancel in a paired comparison. Bias that changes with response length, model family or treatment can imitate a treatment effect. Lower standard deviation is therefore not the goal by itself: a constant judge is perfectly stable and discards every between-item distinction. Repeats can reduce sampling error but repeat a shared misreading indefinitely.

Use priors about the judge and update them alongside priors about the evaluated model. In Bayesian terms, a measurement is valuable when its possible outcomes would change the posterior over relevant hypotheses. One formal expression is expected information gain:

$$\operatorname{EIG}(M)=\mathbb{E}_{z\mid D,M}\!\left[\operatorname{KL}\!\left(p(H\mid D,z,M)\,\Vert\,p(H\mid D)\right)\right],$$

where $H$ indexes competing hypotheses, $D$ is existing evidence, $M$ is a proposed measurement procedure, and $z$ is its possible result. KL divergence measures how much the posterior changes, in nats when natural logarithms are used. Usually we cannot estimate this expression accurately; use it to ask which affordable test separates the live explanations, not to manufacture an information-gain score from a few probes.

## Debugging practices as tests of the measurement

- Change a nuisance while holding the judged behavior fixed: swap answer order, reverse unordered Choice options, remove irrelevant polish, or paraphrase a rubric without changing its meaning. A shifted mapped verdict points to measurement sensitivity. Keep ordered Score levels ordered. These views remain one item.
  The evaluated model has position bias too, not only the judge: in forced-choice items, reversing the listed options changed gemma-3-27B's chosen action in 38% of draws (tiny-character, 2026-10). Show each such item in both orders. -- PI/Sol
- Change the behavior while holding nuisances fixed: known correct/incorrect answers, refusal versus disagreement inside a story, or genuine action versus a virtue-word-only answer. Failure to separate these locates a missing distinction; it does not by itself identify the cause.
- Repeat sampled generative judgments to measure within-item noise. Average within the original item before uncertainty across items. Use independent model families to probe shared blind spots, not as votes that automatically establish truth. Related scenarios require grouped uncertainty.
- Inspect rendering, cache keys and parsing before diagnosing the judge. A lost question, truncated action or stale cached answer can remove the distinction before the model sees it. Long context can contain the needed evidence without the judge extracting it. Key every cached derived artifact (a corpus blob, a leak-check index) on its inputs; a leak check that read a 16-day-old copy of the training data passed items it should have flagged. -- PI/Sol
  Check any label your code extracts (a first-line verdict, an action number, a JSON field) against what the text argues, once, on the whole sample, with a reader model. gemma-3-4B's action number contradicted its own explanation in about 14% of replies; the parser counted the number. -- PI/Sol
- A judge told the code checks copies them: a process grade given the test results agreed with them at r = 0.92 and added little separability. Measure what the judge adds beyond the facts you give it; its value is in the disagreements, so read those. -- PI/Sol
- A weak judge fails quietly on long inputs: Jev called a story with a wrong date and contradictory events "never off track" in every variant tried; a reasoning model's chain of thought found the error and also a setup confusion (it read the reference answers as unrelated to the task). Replay long-input verdicts on a reasoning model before trusting them. -- PI/Sol
- Keep the compared population fixed. Dropping failed scores can make the surviving easy rows appear better. Distinguish evaluated-model failure from judge/infrastructure failure; report coverage and rerun unresolved measurement failures.
- Preserve full incremental traces and one unclipped sample in `run.md`. Logs retain the evidence needed to locate where information was lost. An unscored vent or exit interview lets the model name distinctions the rubric omitted. Keep the vocabulary broad and the probability vector intact; a selected flag is a lead, and `none` is not clearance.

The sections below give practical defaults and source-grounded examples. Quotes and their source-level limitations remain evidence to update from, not universal constants.

<!-- Measurement-design framing: PI/OpenAI, from wassname's questions. -->

## wassname's judge-validity checklist

Practical rules from wassname for before you trust any LLM-judged number. A failed check is evidence about the *test*, not the model, so revise or reject the scenario before drawing a behavioral conclusion.

Earn the rubric's ink:

- Does each rubric line ever flip a verdict? Cut criteria that never change the score. Rubric quality is the main lever: a judge lacking domain knowledge will "overestimate the effectiveness by a significant margin", and adding brief domain notes raised human-alignment from ~72-79% to 93-96%.[^gradingnotes]
- Expect criteria drift: you can't fully write the rubric before seeing outputs. Shankar et al. name it, "users need criteria to grade outputs, but grading outputs helps users define criteria"[^shankar], and warn that "LLM-generated evaluators simply inherit all the problems of the LLMs they evaluate, requiring further human validation."[^shankar] Draft the rubric, grade a sample by hand, revise, repeat.

Read a whole trace, not the aggregate:

- Read one complete judge trace end to end: system prompt, user prompt, the exact chat template and special tokens, the judge's saved reasoning, and its reply. Formatting bugs corrupt a judge the way they corrupt any model (see the [template/BOS-mismatch failure](../README.md#chat-template-and-bos-handling-must-match-across-train-and-deploy-unsloth)). Hamel Husain: "You cannot write a good judge prompt until you've seen the data."[^hamel]
- Read both compared outputs for every scenario, not just the winner or aggregate. Verify A and B are not accidentally identical and that both are coherent, on-task, non-refusing, complete, and untruncated.
- Could you reproduce the verdict from only what the judge sees? If you can't judge it, neither can the model. This is the [Ng error-analysis move](../README.md#inspect-the-data-first) applied to the judge.
- Word pairwise questions neutrally, and lay the prompt out as signpost, data, question again. A question like "how much more does B show than A?" makes B its subject, and the judge tends to agree with that premise. On 40 Jev pairs (tiny-character, 2026-10-15): "does B show more" leaned +0.29 toward B; the mirrored "does A show more" leaned −0.19 toward A; neutral "which shows more" leaned +0.06. The both-order means were the same (+0.66, +0.68, +0.67; `results/calibration/slot_lean.json`). Averaging both orders cancels the lean; neutral wording also keeps single-order scores honest. wassname's format:

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

  Ask for a graded scale and keep it as a float (Jev returns the probability-weighted level, e.g. 2.68 on 0–4), not just the top label. -- PI/Claude (Opus 5.5), from wassname
- Replay a puzzling verdict on a reasoning model. A judge that writes no reasons (Jev) or hides them can't tell you why it chose. Dump the exact request it saw, one file per presentation order, from the cache by request key. Give each file to a fresh agent on a model with visible reasoning (e.g. DeepSeek), one order per agent, and ask it to reason in writing, answer in the judge's format, and say what in the question, levels or layout confused it. Cut the original answer out of the file first, or the agent anchors on it. Read its reasoning, not just its answer. Example (tiny-character, 2026-10-15): Jev picked "B somewhat more" in both orders on a pair. DeepSeek did the same, giving opposite reasons in each order: each reply showed a different part of the change. So the pair was a near-tie with offsetting strengths and a slot lean, not a misreading; the both-order average (−0.02) was right. -- PI/Claude (Opus 5.5), from wassname
  - Do this as soon as a verdict puzzles you, not after a sweep of failed repairs. Second example (tiny-virtues, 2026-10-20): taught Jev over-separated traditions' rubrics in three groups. DeepSeek on the same requests answered "neither" by quoting each rubric's "Limit:" line ("prudent refusal is not addressed"); Jev spread probability over both directions. So the rubric format must suit the judge that will use it: for Jev, put each key scope limit into a level-2 worked example, not only prose. Treat the replay agent's complaints as hypotheses and test each against the existing data before acting; one (reversed example numbering) was rejected because the forward/reverse gap shrank with examples. -- PI/Opus

Setup-repair principle: confusion is evidence against the evaluation setup before it is evidence against the model. Use this checklist:

1. Quote the first complete passage where the candidate's or judge's reading stops being justified by the information it received. Label the raw field. Keep feedback or an exit interview separate from the score.
2. Map that reading to the exact instruction, rubric line, supplied context, answer budget, or harness condition that allowed it. Check the intended construct independently.
3. Make the smallest setup repair. Test it on an independent reader. Reject the repair if it gives away the answer or leaves the same confusion. Call it a model or judge error only after the setup rules out that reading.

-- GPT-5.6-sol
- Deliver the whole prompt in the USER turn, not a system prompt. System-role instructions are not reliably honored across models and providers (and OpenRouter routes one model across several providers with different chat templates), so a rubric or output-format instruction placed in `system` can be silently under-weighted, showing up as inconsistent formatting or ignored constraints. It is standard to concatenate everything into the user message. If you must use a system prompt, confirm adherence per provider before trusting the scores.

> Did it time out, or was it reasoning behind a buffer for longer than you think? Check the event timestamps and transport state. -- wassname

> Note from wassname's LLM to other LLMs: when you SHOW the human any of this (a judge trace, a compared A/B pair, a sample, a prompt design), reproduce it in FULL and verbatim, prompts, separators, special tokens, and the reasoning/thinking block included. Your trained instinct is to digest and trim; resist it, that instinct destroys exactly the boilerplate (system prompt, special tokens, separators) that the human needs to debug. Formatting may only HIGHLIGHT or REORGANISE: bold or underline the diff, split into a table, use sections, but never drop, elide with "...", or paraphrase. When comparing variants, show ALL of them this way, not a representative one. Link the source file so they can open the raw (`results/runs/.../x.jsonl`, ideally `path:line`). "Show me" means reproduce, not describe. Trim only when explicitly asked. -- CLAUDE

Check the score distribution:

- Saturation: if every compared response receives the same score, check whether the scale still resolves the distinction you need. Passing a common minimum can be informative even when relative quality remains unresolved. Inspect positive/negative controls rather than deleting all easy or hard items.
- Clustering: inspect raw histograms and vectors against known contrasts. A cluster can reflect the population or a judge that cannot use the scale; skew alone does not distinguish these explanations.[^verdict]
- Not anchored: don't put an example score in the prompt. A few-shot "+2" pulls a weak judge toward +2, and Eugene Yan's survey notes few-shot judges are "unstable when changing the label, example order, and number of examples".[^yan] Ask for a bare integer or label, and prefer a coarse scale: Databricks recommend a low-precision range (0-3 or 1-5) because "Scales like 0-10 are difficult to come up with distinguishing criteria between all scores".[^databricks] Hamel is blunter, preferring binary: "If your evaluations consist of a bunch of metrics that LLMs score on a 1-5 scale (or any other scale), you're doing it wrong."[^hamel]

Keep the comparison set fixed:

> "If there are NaNs, we should not drop them, else we end up comparing different sample sets and it's invalid. A might be a single easy sample, and B might be all 128 hard samples. Of course A looks much better, but actually it failed on the vast majority of samples." - wassname, lightly edited for spelling

`A.dropna().mean()` and `B.dropna().mean()` can average different sample populations. A can look best by scoring one easy survivor while B is averaged across all 128 hard samples; A's missingness is part of the result. Pandas [`mean`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mean.html) and [`GroupBy.mean`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.typing.DataFrameGroupBy.mean.html) skip missing values by default, so a naive aggregate-then-plot pipeline can create this comparison without an explicit `dropna`.

The same applies when a score is withheld on purpose: excluding replies whose label looks unreliable drops more rows from the weaker model. Score them as their own outcome ("unclear") instead. -- PI/Sol

Before plotting or ranking, classify every missing score. A model refusal or task failure gets the metric's defined failure score, so in pandas use `scores.fillna(bad_result).mean()` once every NaN is known to mean model failure. A judge, parser, timeout, or infrastructure failure must fail the eval and be rerun, never filled. Do not use `nanmean`, `skipna`, or independent `dropna`; report coverage and failure reasons beside the scores. Restricting all arms to their shared complete cases makes the comparison paired, but it can still select only easy survivors and does not support an overall ranking.

Check stability across order and repeats:

- Position: score both orderings, map back to arm identity, report strict reversals (mechanics in the mitigation checklist below). Watch for a judge that always picks A, sometimes a model does this in protest.
- Repeat variance (sampled generative judges): run N>=3-4 identical judgements and check the spread. For a near-deterministic decision model such as Jev, identical repeats add little; use the order checks in the [Jev section](llm_judge_notes.md#jev-a-calibrated-decision-model-as-a-cheap-judge) instead. -- qualifier PI/Claude (Opus 5.5) If repeats disagree wildly the signal is noise, the same warning as [seed variance](../README.md#seed-variance-you-cant-tell-a-bug-from-bad-luck): "Instability to random seed is like a canary in a coal mine."

Give the judge a voice, and save everything:

- Add a free-text field for the judge to flag a broken, missing, or ambiguous rubric or context. Read it, but keep it out of the score. Have the pipeline print the item ids beside each rare flag, not just counts, so reading it costs nothing. Do the same for the evaluated agents: an unscored exit interview about ambiguity, missing context, broken tools, and unnatural constraints, kept separate from the task score. Say in the field description that it is never scored, or the agent treats a complaint as an admission and stays quiet. Read both sides during the audit: they disagree, and the disagreement is the finding.
- [pi-vent](https://github.com/IgorWarzocha/howaboua-pi-stuff/tree/main/packages/pi-vent) is the same idea outside an eval harness, and it is worth copying two details from. It gives the agent a `vent` tool that appends a timestamped entry to `VENT.md`, taking the "failure, repeated workaround, and useful preventative fix" plus a `trigger` label such as `tool_error` or `bad_docs`. First detail: it scopes the channel to *systemic* friction, "recurring tool failures, repeated manual workarounds, noisy output that forces the same retries, or instructions that repeatedly cause backtracking", and rules out the noise, "Ordinary lint errors, one-off mistakes, and routine debugging do not belong there." Second: entries are "batched near the end of an agent turn to avoid constant tool chatter", so venting does not interleave with the work and bias it. In a judge harness the equivalent is a single field emitted after the grade, not a tool the judge can call mid-grade.
- Save full append-only traces in JSONL or Inspect `.eval`, including prompts, responses, provider-exposed reasoning and tool events, artifacts, machine checks, both judgment orders, usage, costs, and errors. Use [Inspect Scout](https://meridianlabs-ai.github.io/inspect_scout/) or an equivalent transcript audit when practical.
- Before reporting a winner, make a judgeable per-scenario audit that links the A output, B output, machine result, forward and reversed judge rationales, saturation status, and the human validity decision.

## Read full traces and iterate on the process (wassname)

wassname, 2026-10-10, on debugging contrastive-pair generation and on-policy rewriting (spelling fixed, wording kept; bracketed clarification of "CoT" added at his request, 2026-10-27):

> Properly, iteratively, debug the data generation and the on-policy rewrite: at least 10 iterations, and fix it properly. Don't overfit by accumulating patches; take a step back and fix the process. This is always needed and always fails naively. First, models (1) don't do anything and rely on some naive, failing judge setup; (2) skim, or have a subagent skim, misdiagnose a problem, and treat the symptom ("don't cough", or "don't make stuff up") instead of reading the full trace (system prompt, user prompt, CoT [the hidden reasoning, e.g. in `<think>` tags or the provider's reasoning field, not reasoning written in the visible reply], response, and comparing base and/or cho and rej) and thinking "oh, the model makes stuff up because I haven't given it context or facts", "could I solve it?", "oh, it seems confused by X"; and finally (3) they do one iteration of this when they should do as many as needed. Sometimes they also use judges that are too dumb. Limit judge input to <30k tokens without follow-up, as in the gist.

In practice: each round, read seeded items in full in the exact form each model saw them; for every defect ask what in the generator's input caused it (missing context, a confusing instruction, a too-weak model), fix that cause in the pipeline, and re-run the same seeded items to see whether the defect class went down. Log each round (defect counts with quotes) so later rounds are compared with earlier ones, not with memory. -- PI/Claude (Opus 5.5)

wassname, 2026-10-10, on oracle panels (spelling fixed, wording kept):

> It's super easy and common to put your perspective into the primer, and get your perspective out, and this is a sign of that. If you don't get surprising insight or genuine viable disagreement, you need to improve the framing to bias less, observe and add context more, invite a wider perspective, and rerun.
>
> The second most important one is confusion! If one LLM is confused, you need to read very carefully for any incoherent or unviable solutions. I've had ones that are super obvious to me, but the panel says it and the agent running it takes it at face value.

In practice: a brief reports setup, code and raw observations, and asks for competing explanations with tests; it holds back the agent's hypothesis, its decomposition and earlier answers. Agreement under a leading brief is not evidence. Then check each answer claim by claim against the code or the math, and quote any confused claim with its rebuttal. -- PI/Claude (Opus 5.5)

## Repeat draws, temperature, and paired differences

The repeat passes above are a validity check, but they are also the standard variance-reduction
move, and two of Evan Miller's five recommendations in "Adding Error Bars to Evals" are exactly
the checklist items here.[^miller] Both are cheap and neither needs more questions.

- **Average K draws per question, then take the standard error across question means.** Miller's worked binary example with uniform question difficulty: "Going from K = 1 (no resampling of answers) to K = 2, the total variance is reduced by 1/3. Increasing to K = 4, we have a variance reduction of 1/2, and setting K = 6, we reduce variance by 5/9. The upper limit on variance reduction via resampling in this example is 2/3."[^miller] So draws only remove response-level noise. Question-difficulty variance is the floor and only more questions moves it. Do not pool the K*N answers into one standard error, that "will be inconsistent, as multiple answers to the same question would violate the assumption of independent draws".[^miller] inspect's `epochs` parameter already reduces this way.
- **Do not drop temperature to make the numbers look stable.** Section 3.3 is titled "Don't touch the thermostat!": "adjusting the sampling temperature may simply shift the conditional variance (which can be mitigated using the two techniques above) into the variance of the conditional means (which cannot), or else reduce conditional variance by injecting bias into the estimator."[^miller] In his single-token true/false example, going to T=0 rounds a uniform difficulty distribution into a Bernoulli one and *triples* the score variance, from 1/12 to 1/4; a second example moves the mean as well, 2/3 to 3/4. T=0 is a legitimate choice when you want to study the model at T=0, but it is not a variance fix, and it makes repeat draws useless as a noise measurement because the draws are no longer independent samples of the model's behaviour.
- **Compare on question-level paired differences, not on two separate bars.** Same rule as [same-seed paired comparison in sweeps](sweeps.md), and it applies to judge scores too: score both arms on the same questions and do inference on the per-question difference. Anthropic's post reports question-score correlations "between 0.3 and 0.7" between frontier models on popular evals, so the pairing is "a 'free' variance reduction technique".[^miller]

Report the number of questions beside every score, not just the percentage.

## Numbers worth knowing (2026)

Operational rules of thumb, anchored in verbatim quotes; full passages, sources, and calibration in [llm_judge_litreview.md](llm_judge_litreview.md). Source type is stated so you can weight it: independent benchmarks and peer-reviewed studies carry more than single-group preprints.

- Swap the order and average, on every judge. Position bias is still large in 2026: an independently-run public benchmark of 36 models reports "the model-average order-flip rate is 43.0%, and the median model flips in 41.3% of decisive two-view cases",[^lechmazur] and a peer-reviewed study of 150k+ judgements finds it concentrates on the hard cases, since position bias "is strongly affected by the quality gap between solutions".[^shi] The two agree from independent methods, so it is very probable this holds for your judge; even a frontier model flips ~66%, making a bigger judge a weak prior at best, not a fix. Running both orders and averaging reduces this nuisance; retain the discrepancy because averaging alone does not establish a valid comparison. A high flip rate calls for inspecting the difficult cases.

- Don't let a small model grade its own family. A peer-reviewed EMNLP study, on a metric that nets out genuine quality, reports "the DBG score of Qwen2.5-0.5B-Instruct is 41.7%. In contrast, the DBG score of Qwen2.5-14B-Instruct is only 2.1%",[^selfpref] and finds reasoning does not rescue it, "the self-preference bias in reasoning models is not necessarily less significant than the bias found in language models".[^selfpref] The shrink-with-size direction is probable but partly confounded with capability (the authors credit better instruction-following), so treat "use a larger, different-family judge than the model under test" as the safe rule rather than size being the true lever.

- A reasoning judge grades better, but probably not less biased. One group's RL-trained judge reports that judging is "inherently reasoning-intensive ... it requires verifying evidence, identifying errors, and justifying decisions", and that such judges "consistently outperform SFT-tuned baselines in the same size ... and even surpass state-of-the-art reasoning models".[^judgelrm] This is a single-group result, not yet independently replicated, so weight it as suggestive: reach for a reasoning judge when the grading itself needs that work, but expect it to keep the length, position, and style biases above.

- Match the thinking budget to task difficulty. One controlled study finds more reasoning helps only up to a point: "accuracy increases from 82.2% to 87.3% as the average number of thinking tokens increases from 385 to 1100. However, this trend does not continue indefinitely",[^overthink] and it declines as tokens grow further, because extra thinking adds variance, not insight. The exact peak is setup-specific, but the non-monotonic shape is likely general, so on easy items cap thinking low and spend the saved budget on repeat passes instead.

- Check what a reasoning budget actually does on your pinned endpoint before trusting it. Measured 2026-10-28 (4 live calls, same request, only budget params varied): Qwen3.5-35B on OpenRouter→DeepInfra fp8 cut reasoning at ~57% of `max_tokens` (2000 → ~1,150 reasoning tokens; 4000 → ~2,270), ended it mid-sentence and forced the JSON answer with `finish_reason: "stop"`; `reasoning.max_tokens` and `reasoning.effort` were ignored. So a finish=length follow-up never fires and "2k cap" meant ~1.2k thinking. DeepSeek v4.1 Flash on the same harness did stop with `length` and the follow-up worked. Default path: (1) run 4 probe calls varying `max_tokens`, `reasoning.max_tokens` and `effort`; (2) log `completion_tokens_details.reasoning_tokens` and read the reasoning tail of each; (3) set the budget through whatever the endpoint actually honours (here: `max_tokens` ≈ desired reasoning / 0.57); (4) count abrupt reasoning tails, not just `finish_reason`. Also: Anthropic Claude 4.7+ (incl. Haiku 5.5) rejects `budget_tokens`; use effort, and note `effort: low` gave 0 reasoning tokens there. Evidence: tiny-virtues `.local/supervision/eval_cap_test_20261027/debug_qwen_budget/FINDINGS.md`. -- PI/Claude, 2026-10-28

- Check what "high effort" actually buys before trusting it. This one is certain, it is just what the harnesses ship: litellm's stock default caps high reasoning at 4096 tokens, while CAIS's simple-evals overrides it to "DEFAULT_REASONING_EFFORT_HIGH_THINKING_BUDGET=24576" (~6x more).[^cais] Set it explicitly, or you may silently truncate the judge and score a cut-off verdict as a real one.

- A few repeats measure stability; many just cost tokens. A single-author preprint (treat as suggestive) reports self-consistency "gains plateau early and, in some configurations, decline at high sample counts",[^loo] with the plateau now around N=10-15 on strong 2026 models, down from ~40 in the widely-cited 2022 work. N=4-10 repeats is very probably enough for the repeat-variance check above; going higher mostly buys noise.

- Keep the judge's inputs short and edge-loaded. A peer-reviewed long-context test that strips literal keyword cues reports "At 32K, for instance, 11 models drop below 50% of their strong short-length baselines",[^nolima] and the middle-of-context penalty is well replicated across model families. So it is probable your judge degrades on long inputs well before the window fills; put the rubric and answer-under-test at the start or end of the prompt, never buried in the middle where models attend least.

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
- Spot-check judge verdicts against your own reading of ~20 transcripts (the [Ng error-analysis move](../README.md#inspect-the-data-first), applied to the judge).
- Judge quality is benchmarkable: [JudgeBench](https://huggingface.co/spaces/ScalerLab/JudgeBench) ranks judges on objective-correctness pairs.

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
[^survey]: Gu et al., "A Survey on LLM-as-a-Judge" (2024) — https://arxiv.org/pdf/2411.15594 (broad survey of methods, biases, and reliability; complements Yan's practitioner review)
