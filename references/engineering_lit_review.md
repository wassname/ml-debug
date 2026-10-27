# Engineering literature review

Use before copying a method from papers, when a method works for the authors but not for you, or when asked what the papers did that we missed.

The aim is the **boring details that decide whether a method works**: loss tweaks, masking and
EOS handling, data cleaning and filters, the exact prompts, replay ratios, what they removed from
an instruction mix. These are rarely in the abstract and often only in an appendix, a config, a
code comment or a fix commit. Authors rarely put them in the paper because they are boring,
embarrassing or seem obvious, yet they are often what makes the method work. Find them, then
**compare each one with what we do**. Rank by importance; do not write a complete summary or an
audit of other people's bugs.
<!-- PI/Claude (opus-5-5), 2026-10-27, from the constitutional_grafting paper-guide work. wassname:
"it's meant to look for most important tricks and gotchas and components, and motivating insights
and so on. in papers, ablations, code comments even commit history"; "and say evidence too"; "and who
said"; "focusing on boring details that are critical like loss tweaks, data cleaning, etc"; "or prompt
used". -->

## 1. Papers as full markdown in `docs/papers/`

- Keep a manifest `docs/papers/manifest.tsv` (`filename url title authors year`) and one fetch
  script, so anyone can refetch. File names: `<year>_<firstauthor>_<slug>.md`, with a front-matter
  header (title, authors, source URL, fetch date).
- arXiv: fetch `arxiv.org/html/<id>` and convert with `pandoc -f html -t gfm-raw_html --wrap=none`
  (r.jina.ai mangles arXiv HTML). Blogs and LessWrong: `https://r.jina.ai/<url>`. See the `arxiv` skill.
- Check every file has real body text (size > 5 kB, not a nav page). Strip inline base64 images.
  Note what is image-only (tables, prompts as figures): you cannot read it from the markdown.

## 2. Find the code or a replication, and judge it

Search in this order: links inside the paper markdown (`grep -o 'github.com/[^ )]*'`), the arXiv
abstract page, HF collections named in the paper, `gh search repos "<title>"` and by arXiv id and
author handles (see the `gh` skill), then web search for "<title> replication" / "reproduction".

Judge each repo before you trust it, and record the verdict in `VENDOR.md`:

| Question | Evidence to look at |
|:--|:--|
| Is it from the paper's authors? | owner is an author or their lab; the paper links it; CITATION file |
| Does it show it actually runs? | configs with the paper's numbers, released checkpoints or eval outputs, logs, tests or CI |
| Is it the paper's version? | a tag or commit near the paper date; README names the paper |
| Human or agent written? | many small commits over weeks vs one squashed dump; `CLAUDE.md`/`AGENTS.md`; uniform verbose comments |
| Is it sloppy? | hard-coded paths, dead branches, paper vs code mismatches, no pinned deps |

A third-party replication is not the authors' code; label it. If there is no code, say where you
searched; released generation prompts and HF dataset cards often hold the real data pipeline.

## 3. Vendor the code as git submodules

```bash
git submodule add --depth 1 <url> docs/vendor/<name>
# repo too big (data blobs)? code only:
git clone --filter=blob:limit=1m --no-checkout <url> docs/vendor/<name>
git -C docs/vendor/<name> sparse-checkout set --no-cone '/*' '!/data/'   # adjust the excluded dirs
git -C docs/vendor/<name> checkout <pinned_commit>
git submodule add <url> docs/vendor/<name>                               # reuses the clone
git -C docs/vendor/<name> fetch --unshallow --filter=blob:none           # history for step 6; pin unchanged
```

Gated HF datasets (`gated='auto'`) return 401 without a token: use the local token
(`~/.cache/huggingface/token`) for cards and `datasets-server` first-rows. Never print it.

## 4. `jargon.md`

Build the term list from the **most relevant prior paper first**, quoting its definition and section.
Fill gaps from the next papers. Only then name what is left, and think before inventing:

- Prefer the field's standard term. Do not overload a term another paper already uses for something else.
- Keep terms distinct from each other: two names should not suggest the same thing.
- Make it self-evident: a reader should guess the meaning from the name. No folksy metaphors.
- Mark each term as paper term (with source) or project term, and say how it differs when a paper's
  word is close but not the same.

## 5. Mine for the boring critical details

Lead each per-paper file with a **Top 10** across four kinds: **tricks** (deliberate techniques),
**gotchas** (failures they hit or warn about), **components** (what the ablations show carries the
effect, and what does not), **motivating insights** (why they think it works). Look hardest at:

- **Loss and format:** masking (assistant-only, document prefix tags, EOS), chat template, packing,
  sequence length, any extra loss term or reweighting.
- **Data cleaning and filters:** refusal filters, "As an AI I have no opinions" filters, other-model
  identity filters, judge models and thresholds, dedup method and threshold, length filters, fact checks.
- **Prompts:** quote the exact generation, revision and judge prompts, and the line that does the trick.
- **Generation:** seed taxonomy, diversity mechanism, candidates per kept item, revision loops, teacher model.
- **Reasoning:** how chain-of-thought is generated, kept, stripped or masked.
- **Stability and mixing:** lr, warmup, epochs, decay, clipping, LoRA targets, replay or instruction-data ratio
  and what they filtered out of it.
- **Ablations and author notes:** what was varied, what mattered, effect size; every "surprisingly",
  "we found", "did not matter".

## 6. State our point of departure

Take a Bayesian view. The closest prior work is our prior: its evidence tells us how likely the method is to work in its setting. Each way we depart from it adds uncertainty, because their evidence no longer covers that part. So be very clear on ours versus theirs, and on where our departures add research uncertainty: those are the things our own experiments must test first, in order of how much uncertainty they add and how much the result depends on them. A departure that copies their setting adds little; a new stage, model family, scale or objective adds a lot.
<!-- wassname, 2026-10-27: "it's a bayesian view of science and this is the closest prior and we need to be clear on ours vs theirs and where we will add research uncertainty" (spelling corrected). -->

For each idea in our method, write:

- **Closest prior work**: what the authors did that comes nearest to our idea, quoted with its location. Say how it differs (different checkpoint, data, scale, objective, evaluation).
- **Confidence in that evidence**: how strong is the result for our question? Consider seeds and repeats, effect size, held-out vs near-training evaluation, whether the code shows it ran, author claim vs independent replication, and how far their setting is from ours. Use words of estimative probability.
- **What we add on top**: the part no paper has tested. That part needs its own evidence; it does not inherit theirs.

A plain table works: `our idea | closest prior (quote, §) | difference | confidence | what we add | uncertainty added (low/med/high) | our test`. Readers then know which claims rest on published evidence and which are ours to show.

Test of the write-up: a superforecaster who reads only this section should have the information they need to bet on whether our experiment will work. They may lose the bet, since uncertainty is high, but they should not have to guess what the evidence is. So give them: a reference class and its base rate (how often results like the closest prior replicate or transfer to a new setting, if known), the strength of the closest evidence, each departure and which way it should move the estimate, the cruxes the outcome depends on, and which early observation would move the estimate most. Give your own estimate too, labelled as yours.
<!-- wassname, 2026-10-27: "if a super forecaster read it they should be able to use this to estimate experiment success"; "they should have info they need to make a bet. might not win. uncertainty is high" (spelling corrected). -->

## 7. Compare with ours, detail by detail

Compare against the **closest prior work first and most thoroughly**: it is our point of departure, so every difference from it is either a deliberate change we must justify or an omission we must fix. Do the full detail-by-detail table for that paper (one per idea, if different ideas have different closest papers). For other papers, add rows only where they do something important that the closest paper does not.

For every detail found, one row: `detail | theirs (quote + file:line or §) | ours (file:line, or "none") | same / different / unknown | matters? (their ablation, or inferred)`. Read our executed config and launcher, not only the template YAML: overrides hide there. "Unknown" is a finding: it means neither the paper nor the code says, so ask the authors or test it.

## 8. Code comments and commit history

- Dump every comment longer than 40 characters or spanning several lines, plus docstrings, and read
  them all; grep for `NOTE|IMPORTANT|HACK` misses most:
  `uv run --no-project python ~/.pi/agent/skills/ml-debug/scripts/dump_comments.py docs/vendor .local/comment_dumps`
- Where the authors spent many commits is where the hard problems were:
  ```bash
  git -C <repo> log --format= --name-only | sort | uniq -c | sort -rn | head -30
  git -C <repo> log --format='%h %ad %an %s' --date=short | grep -i -E 'fix|bug|revert|nan|oom|collapse|mask|eos|loss|refus|filter|dedup|prompt'
  git -C <repo> show <hash> -- <file>
  ```

## 9. Evidence and attribution

Use `varglight` / `quote-with-provenance` for every item: a blockquote with a sentence before and
after, the main sentence in bold, the exact location (paper section or line, `file:line`, commit
hash), and **who said it**: paper authors, code author (`git blame`), commit author and date,
third-party replicator, or "inferred by me". An inference must never read like an author claim.
For code, quote the comment and the line it explains.

## 10. Process that worked

1. One brief file, quoting the user's goal. One reader per paper and its code; stronger models for
   the core papers. Keep the brief in a file: context compaction can wipe a reader's task.
2. Per paper: Top 10, recipe table ("not stated" where absent), exact prompts, ablations and notes,
   effort map, the point-of-departure table, the theirs-vs-ours comparison table, read coverage.
3. A synthesis index: what the papers say matters most, tricks worth taking, things we skipped
   (deliberate or not), gotchas in one line each. It verifies claims against the source and lists
   unverifiable ones separately.
4. Read the synthesis yourself and check its claims against your own repo.

## Gotchas in doing this

- A brief that asks for "gotchas" and "compare with our code" gets an audit of other people's bugs,
  not the authors' lessons. Ask for tricks, components, insights and prompts explicitly.
- Readers make stale claims about your project (observed: "we only test GSM8K" when the eval also had
  ordinary-help tasks; "check truncation" when lengths had been measured a week earlier). Check every
  "we don't do X" against your repo and journal before acting.
- Readers report what they read. Require a coverage section, and distrust findings from skipped files.
- A hyperparameter table without effect sizes does not tell you which settings matter. Ablations,
  prompts and author notes are the main payload.
