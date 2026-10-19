# Two standalone judge examples

For the maintained defaults and installable toolkit, use [wassname/llm-judge](https://github.com/wassname/llm-judge). These standalone illustrations have a different CLI and optional ranking code; do not assume the same execution safeguards. -- PI/OpenAI

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

Each scoring request gets one extra Choice question: which option best names an obstacle to judging this pair reliably, or `none`, or `idk` (something seems off but no option names it). It rides inside the four scoring views (both response orders, both option orders), so it adds no requests; the state is billed once and each option costs a few tokens. Results contain `debug.word`, the top five averaged probabilities and an option-order disagreement flag. Scoring and ranking ignore it. It suggests a setup problem, not a verified explanation.

Jev's Choice takes at most 255 options ("A Choice question accepts up to 255 options, and adding options costs a few tokens each", [TypeSafe docs](https://docs.typesafe.ai/primitives/choice.md)), so a list holds at most 253 entries plus `none` and `idk`. Keep one option per concept: near-synonyms split the probability. On tiny-character dev, `none` (.24) beat truncated .15 + truncation .09 + unfinished .09 on a cut-off pair until the synonyms were merged. Leave out words that echo the question (pair, change, criterion, tag): with a 3,000-word list they won often.

The bundled `debug_words.txt` (116 words + 100 emoji) is from tiny-character `data/jev_words/words_emoji.txt`, built from 17k chat-judge notes, a reasoning judge's chain of thought and published failure taxonomies. On 120 dev pairs with known answers it named "same" on 49/60 same-model pairs, "cut off" on 4/6 capped pairs and "subjective" on 6/6 contested items (`scripts/scratch/word_list_ab.py` there).

Cost history (tiny-character dev, ~4k-token states): a separate 3,000-word tournament (groups of 255, then a final; idea from [jev-talks at 50bc6df](https://github.com/zie1ony/jev-talks/tree/50bc6df463202f0b7f329077ea688ef97b9a473d)) cost $0.002 per pair, about 5× the scoring questions. Inside the scoring request it costs about $0.0002. Adding the question shifted other answers slightly (on-target sd 0.047 per pair, mean unchanged), although Jev's docs describe questions as independent. -- PI/Claude-opus-5-5, 2026-10-16

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

Canonical installation and current commands: [wassname/llm-judge](https://github.com/wassname/llm-judge). Prepared by PI/OpenAI.
