# Engineering literature review: tricks, gotchas, components, insights

Use this before you copy a method from papers, when you want to know "what did they do that we
missed", or when a method works for the authors but not for you. The aim is the **most important**
things the authors learned, not a complete summary and not a list of defects in their code.
<!-- PI/Claude (opus-5-5), 2026-10-27, from the constitutional_grafting paper-guide work. wassname's
words: "it's meant to look for most important tricks and gotchas and components, and motivating
insights and so on. in papers, ablations, code comments even commit history", "and say evidence
too", "and who said". -->

## What to look for

Rank by importance. Lead with a **Top 10** across four kinds:

| Kind | Question | Typical places |
|:--|:--|:--|
| Trick | What did they do on purpose that is not in the method summary? | appendices, configs, code comments, prompts |
| Gotcha | Which failure did they hit or warn about? | limitations, footnotes, fix/revert commits, `# NOTE` comments |
| Component | Which ingredient do the ablations show carries the effect, and which does not? | ablation tables, "surprisingly", "did not matter" |
| Motivating insight | Why do the authors think the method works? | introduction, discussion, "we hypothesize" |

Categories that are easy to miss: data cleaning and filters (refusal filters, "As an AI I have no
opinions" filters, other-model identity filters, judge thresholds, dedup method), generation
(seed taxonomy, diversity mechanism, revision loops, candidates per kept item), reasoning and think
blocks (generated how, kept, stripped, masked), loss and format (masking, EOS, chat template,
packing, document prefix tokens), stability (lr, warmup, epochs, decay, clip, LoRA targets, replay
ratio), mixing (instruction data added to SFT and what was filtered out of it), and evaluation
(how they separate deep from shallow effects).

## Evidence and attribution

Every item needs **evidence** and **who said it**. Use `varglight` / `quote-with-provenance`: a
blockquote with a sentence before and after, the main sentence in bold, and the exact location
(paper section or line, `file:line`, or commit hash). Who said it is one of: the paper authors,
the code author (`git blame`), the commit author and date, a third-party replicator (not the
paper's authors), or "inferred by me". An inference must never read like an author claim.

## Sources, all four

1. **Paper**, including appendices and footnotes. Ablations often hide in the appendix.
2. **Ablation results**: what was varied, what mattered, effect size.
3. **Code comments.** Dump every comment longer than 40 characters or spanning several lines,
   plus docstrings, and read them all; grep alone misses most. Script:
   `uv run --no-project python ~/.pi/agent/skills/ml-debug/scripts/dump_comments.py <vendor_dir> <out_dir>`.
4. **Commit history.** Where the authors spent many commits is where the hard problems were.
   ```bash
   git -C <repo> fetch --unshallow --filter=blob:none   # history without big blobs; pin unchanged
   git -C <repo> log --format= --name-only | sort | uniq -c | sort -rn | head -30   # churn
   git -C <repo> log --format='%h %ad %an %s' --date=short | grep -i -E 'fix|bug|revert|nan|oom|collapse|mask|eos|refus|filter|dedup'
   git -C <repo> show <hash> -- <file>
   ```

## Getting the code

- Vendor official code as git submodules: `git submodule add --depth 1 <url> docs/vendor/<name>`.
  Shallow clones have one commit, so fetch history as above before mining it.
- Repos too big because of data: clone code only with `git clone --filter=blob:limit=1m
  --no-checkout`, check out with a sparse pattern that skips data directories, then
  `git submodule add <url> <path>` reuses the existing clone.
- Gated Hugging Face datasets (`gated='auto'`) return 401 without a token; use the local token
  (`~/.cache/huggingface/token`) for card and first-rows reads. Agents should not print it.
- No public code? Say where you searched. Released generation prompts or HF dataset cards often
  hold the real data pipeline.
- Label replications: a third-party replication is not the authors' code.

## Process that worked

1. One reader per paper (plus its code), all with the same short brief file. Bigger models for the
   core papers. The brief states the goal in the user's words.
2. Each reader writes `<paper>.md`: Top 10 first, then recipe table (starting checkpoint, data,
   tokens, LoRA or full FT, lr, epochs, masking, post-training, evaluation; "not stated" where
   absent), ablations and notes, effort map, comparison with our pipeline (our `file:line`), and
   read coverage.
3. A synthesis reader builds the index: what the papers say matters most, tricks worth stealing,
   things we forgot (deliberate or not), gotchas in one line each. It must verify each claim against
   the source and move unverifiable ones to an "Unverified" list.
4. Read the synthesis yourself, and check its claims against **your own repo**.

## Gotchas in doing this

- A brief that asks for "gotchas" and "compare with our code" gets an audit of other people's bugs,
  not the authors' lessons. Ask for tricks, components and insights explicitly.
- Readers make stale claims about your project (observed: "we only test GSM8K" when the eval also had
  ordinary-help tasks; "check truncation" when lengths were measured a week earlier). Check every
  "we don't do X" against your repo and journal before you act on it.
- Readers report what they read. Ask for a coverage section (read in full, skimmed, skipped) and
  distrust any finding from a skipped file.
- Context compaction can wipe a long-running reader's task. Keep the brief in a file so you can resend it.
- Without effect sizes, a recipe table cannot tell you which settings matter. Ablations and author notes
  are the main payload, and the hyperparameter table is background.
