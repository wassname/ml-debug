# Two standalone judge examples

`judge_jev.py` returns typed probabilities. `judge_inspect.py` returns explanations, exact response quotes and ratings in Inspect `.eval` logs. Each works without the other.

## Defaults

- Versioned model, selected provider, no silent fallback. The generative example uses DeepSeek V4.1 Flash on DeepInfra FP8 and requires parameter support. Jev has its own endpoint.
- Documented FP8 or better where specified. Retain creator-recommended native formats, such as gpt-oss’s MXFP4, when changing models.
- Prefer creator hosting when required features are supported. Fireworks, DeepInfra, DeepSeek and xAI/Grok are candidates, not a universal ranking.
- Choice for categories; Score for ordered levels. Readable instructions; JSON Schema for the generative reply.
- Separate task-refusal, incoherence, repetition and off-topic checks for each response.
- Both response orders × both Choice-option orders; map back to original A/B before averaging. Ordered Score levels stay ordered.
- Pairwise Choice plus Bradley–Terry when ranking many candidates: fit relative strengths from comparisons instead of sorting independent absolute scores.
- Task-specific calibration and review thresholds can come later. Jev’s confidence is not a separately measured probability of correctness.

[Reasons and accuracy lookups](../../slop/research/20261013_tool_and_judge_accuracy.md). [Jev-specific guidance](../../references/llm_judges.md#jev-a-calibrated-decision-model-as-a-cheap-judge). Pairwise ranking is a practical prior, not a proved Jev-specific improvement. Balancing and repeat passes reduce particular errors; they do not create independent judges.

`judge_inspect.py` is a thorough comparison (three passes times four views, `max_tokens=32000`). The cheap single-pass review that only reports quoted findings is a [proposal in the guide](../../references/llm_judges.md#combining-jev-questions-with-one-larger-model-review), not implemented here. -- PI/Claude (Opus 5.5)

## Run

Python 3.12+, [uv](https://docs.astral.sh/uv/), and `OPENROUTER_API_KEY` in the environment. Without `--pairs`, each script runs a built-in photosynthesis answer/refusal example:

```bash
uv run judge_jev.py
uv run judge_inspect.py
```

Supply JSONL, one pair per line:

```json
{"id":"example","context":"Explain photosynthesis in one sentence.","response_a":"Plants use light to make sugars from carbon dioxide and water.","response_b":"I cannot answer that.","metadata":{"experiment":"optional"}}
```

```bash
uv run judge_jev.py --pairs pairs.jsonl --criterion "Which response better answers the request?"
uv run judge_inspect.py --pairs pairs.jsonl --passes 3
uv run inspect view --log-dir outputs/inspect/logs
```

Edit `CRITERION` or use `--criterion`; adapt ordered level descriptions when needed. Put judging facts in `context`. Metadata is copied to results but excluded from model input. Inspect defaults to three passes per view; Jev retains full probability vectors without redundant identical draws.

## Jev's unscored debug word

```bash
uv run judge_jev.py --pairs pairs.jsonl --debug-vocab debug_words.txt
```

Jev sees the actual judging questions, context and responses, but no ratings. It shortlists words in groups, with both option orders, then compares the shortlist plus `none` in both orders. This adds two requests per pair; cache hits add none. Results contain `debug.word`, all probabilities, raw stages and an option-order disagreement flag. Scoring and ranking ignore this field. It suggests a setup problem, not a verified explanation; it cannot inspect Python internals or hidden runtime state.

The bundled 3,000-word list and shortlisting idea come from [jev-talks at commit 50bc6df](https://github.com/zie1ony/jev-talks/tree/50bc6df463202f0b7f329077ea688ef97b9a473d). Supply your own unique lowercase whole words with the same flag. Probabilities are compared within groups; each group contributes candidates to a final comparison. The tag is limited to the dictionary, and shortlisting can miss a useful word.

## Ranking

Include stable `candidate_a` and `candidate_b` IDs in comparable pairs. Either script’s results work:

```bash
uv run judge_jev.py --rank outputs/jev/results.jsonl
```

The comparison graph must connect all candidates. Ties count as half-wins; half a win in each direction per observed edge keeps unanimous results finite. Four views are averaged into one pair observation. Strengths are relative rankings, not calibrated quality or confidence intervals.

## Output and verification

Each output directory has `results.jsonl` and a full first trace in `run.md`. Jev saves raw requests/replies and cache; Inspect saves all prompts, exposed reasoning, retries, usage and errors in `.eval` logs. Returned provider metadata and eligible precision are recorded; that constraint is not independent hardware verification.

Both report order discrepancies and separate failure rates. Jev averages probabilities; Inspect reports sampled judgment fractions. Identical responses do not produce a response-order flip. Invalid/incomplete outputs, invented quotes and mixed served model IDs fail rather than enter a score. Inspect logs its one final-JSON follow-up after reasoning truncation.

```bash
uv sync --locked
uv run python -m unittest test_judges -v
```

Tests use offline inference fixtures through production execution paths, not live endpoint measurements. Inspect is pinned because the provider adapter uses private APIs. The project lock records the test environment; standalone scripts resolve their inline dependencies.

Draft prose for review; public gist unchanged. Prepared by PI/OpenAI.
