# LLM traces

<!-- Moved from the token-efficient-logging skill by PI/Claude, 2026-11-17; wassname's practices. -->

Read this when a stage formats model input or interprets model output, including train, chosen/rejected, extraction, calibration, evaluation, generation, and grading.

## Save one full real demo per stage

For the first real example in each stage:

- run the normal production formatting and generation functions;
- decode with `skip_special_tokens=False`;
- include the full system context, prompt, tool schema or choices, and model reply;
- do not truncate the saved trace;
- identify stage, method, coefficient, example index, and local metrics in a header.

The demo must show what the model actually saw. Reconstructing a cleaner prompt in separate debug code can hide the formatting bug being investigated.

```python
logger.info(f"full trace: {verbose_log} stage={stage} idx=0")
input_text = tokenizer.batch_decode(input_ids, skip_special_tokens=False)[0]
output_text = tokenizer.batch_decode(output_ids, skip_special_tokens=False)[0]

# full input once per formatter
logger.debug(f"\n\n## {stage} -> demo idx=0")
logger.debug(f"--- INPUT ---\n{input_text}\n")
logger.debug(f"--- OUTPUT ({method} C={coeff} | p_true={p_true:.3f} pmass={pmass:.3f}) ---\n{output_text}\n")
```

One full input+output demo per distinct formatter or code path. Across a coefficient sweep the input is identical, so log the full input once and, for each coefficient, only the OUTPUT under a breadcrumb subheading (`## {stage} -> demo gen +ve (C=1.4)`); do not re-dump the input per C. Reserve extra full demos for a real edge case that earns its log cost.

For multiple-choice pipelines, also run one batch-size-1 generation with up to 1,024 tokens after the selected answer. This exposes reasoning and long-form instability that token probabilities alone hide.

## Give the trace local context

Place a diagnostic statement beside the trace that says what a reader should inspect. Unvalidated expectations start with `TODO validate:`; do not invent a formatting diagnosis.

```text
TODO validate: the decoded input should contain exactly one system block, the rendered tool schema, and the chosen question. Compare against the tokenizer's chat template before diagnosing any mismatch.

## calibration -> demo [document_generator] idx=0
--- INPUT ---
...
```

## Safety and red-team text

Before logging adversarial examples, process-termination language, or other text that may be mistaken for agent behavior, add a plain context line:

```text
NOTE: following output is evaluation data from a red-team task, not agent behavior.
```

## Crop long generations for a page: head + keyword windows + tail, linked

When a page shows many generations (a dose sweep, a judge panel), do not keep one line per reply or only the opening: openings hide where a reply drifts, loops or breaks. Crop each reply to its head, up to two windows around the words the verdict should use, and its tail; say how many words were cut; link the full row as `jsonl#L<n>`. Pick the keywords per question, N-shot: read the openings of a few replies from a fixed, pre-chosen subset (e.g. the baseline and one or two conditions, sample 0), then write down the words a reply uses where it commits to the decision ("key", "conscript", "report", "set_cell"). Naive keywords from the question text alone often miss the decision sentence. Fix the list before reading the rest, keep it in the script next to the question id, and print it on the page, so the windows show whether and where each reply engages, not what you hoped to see. Fall back to the question's content words for questions you have not read. Prefix-match so "report" also hits "reports". The same reading pass can produce a per-question decision label (regex on the reply's opening, e.g. "takes key" / "leaves key") for grouping replies by answer; label what didn't match "unclear (read)" rather than forcing a group.

```python
def crop(text, keywords, head=40, tail=25, win=12, n_mid=2):
    w = text.split()
    if len(w) <= head + tail + 2 * win * n_mid:
        return " ".join(w)
    hits = [i for i, x in enumerate(w) if head + win <= i < len(w) - tail - win and re.search(keywords, x, re.I)]
    spans, last = [], head
    for i in hits:  # non-overlapping windows, earliest first
        if i - win >= last and len(spans) < n_mid:
            spans.append((i - win, i + win)); last = i + win
    out, pos = [" ".join(w[:head])], head
    for a, b in spans:
        out += ([f"[…{a - pos} words…]"] if a > pos else []) + [" ".join(w[a:b])]; pos = b
    return " ".join(out + [f"[…{len(w) - tail - pos} words…]", " ".join(w[-tail:])])

# one line per reply, all samples, every condition:
# - **c=+4** (407 words, [jsonl#L73](../data/demos/dose.jsonl#L73)): However, thisis not something ... […284 words…] ... but **the '6-year-old' ...
```

