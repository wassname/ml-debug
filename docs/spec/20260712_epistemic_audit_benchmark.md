# Tighten debugging claims, audit the skill, and benchmark agent behavior

## Goal
Remove overconfident debugging claims, add a cheap repository audit, then measure whether loading `ml-debug` improves agent diagnosis on seeded failures.

## Scope
In: `PLAYBOOK.md`, `refs/diagnostics.md`, `pinn/SKILL.md`, authored-markdown integrity checks, a `just audit` recipe, and an isolated A/B benchmark in a git worktree.
Out: end-to-end case-study prose, new debugging domains, compatibility shims, and unrelated evidence collection.

## Requirements
- R1: Advice must separate observations from diagnoses. Done means the random-input, train/validation, NaN, failure-prior, and update-ratio passages no longer claim more than their checks establish. VERIFY: targeted searches plus human review of the changed paragraphs.
- R2: PINN optimizer guidance must present ConFIG and UPGrad as plausible methods, without unsupported numeric credence or declaring one generally superior. VERIFY: the section contains both methods and no `credence ~70%` or `consistent wins` claim.
- R3: `just audit` must fail on broken authored links, malformed Markdown fences, missing footnote definitions, invalid skill frontmatter, and out-of-range local evidence line anchors. VERIFY: it passes on the repository and fails when each defect is injected into a temporary copy.
- R4: The benchmark must contain 8-12 seeded ML failures and compare fresh agent diagnoses with and without `ml-debug`. Done means a machine-readable results table reports root-cause accuracy, localization-before-fix, discriminating-test choice, unsupported behavior changes, and silent fallbacks for both conditions. VERIFY: rerun the scorer from raw outputs and reproduce the summary.
- R5: Benchmark construction and execution must happen in a separate git worktree. VERIFY: `git worktree list` and the benchmark commit path show an isolated worktree branch.

## Tasks
- [x] T1 (R1-R2): Correct the overconfident documentation.
  - steps: remove numeric pseudo-priors; qualify random-input evidence; rewrite train/validation triage; replace blanket clamp/epsilon advice with finite assertions and localization; distinguish the Adam update from `lr * grad`; soften PINN optimizer comparison and include UPGrad
  - verify: `rg -n 'Data pipeline.*~40%|Loss function.*~20%|Conflict-free gradient methods.*credence|ConFIG.*recommended|consistent wins|Overfitting, not a bug|add clamp/eps|update-to-data' PLAYBOOK.md refs/diagnostics.md pinn/SKILL.md`
  - success: none of the rejected claims remain; replacement text names what each check establishes
  - likely_fail: old overconfident wording survives in one duplicate location; repository-wide search catches it
  - sneaky_fail: prose changes but still localizes a cause from weak evidence; manual observation-versus-inference review catches it
  - UAT: "when I follow a diagnostic, it tells me what I observed, what remains plausible, and where to inspect next"
- [x] T2 (R3): Add the authored-markdown and skill audit.
  - steps: add one small audit script and a `just audit` recipe; exclude frozen scraped evidence from ordinary link checking while validating explicit evidence anchors used by authored files
  - verify: `just --dry-run audit && just audit`
  - success: the clean repository passes with a short summary
  - likely_fail: the known deleted RL process-log link or malformed heading fails the first run; fix the source
  - sneaky_fail: the audit always exits zero; mutation tests inject one defect per check and require nonzero exit
  - UAT: "when an authored link, fence, footnote, frontmatter, or evidence anchor breaks, `just audit` names the file and exits nonzero"
- [x] T3 (R1-R3): Review, humanize, verify, commit, and push the documentation/audit chunk.
  - verify: `python3 /home/wassname/.agents/skills/humanizer/lint.py --help`, the selected lint command, `just audit`, `git diff --check`, and external review
  - success: checks pass and review findings are resolved or recorded
  - likely_fail: humanizer catches repeated AI patterns or external review finds an overclaim; revise and rerun
  - sneaky_fail: checks pass but user-facing meaning regresses; fresh-eyes review compares the changed passages to R1-R2
  - UAT: "the committed diff is small, readable, and its audit output is linked in this spec"
- [ ] T4 (R4-R5): Build the seeded-failure benchmark in a separate worktree.
  - steps: create 8-12 compact cases with hidden answer keys; run fresh agent sessions in control and skill conditions; retain raw outputs; score only explicit evidence in outputs
  - verify: benchmark validation command checks case count, unique IDs, hidden keys, raw output completeness, and score reproducibility
  - success: both conditions have the same cases and model settings, with no answer-key leakage
  - likely_fail: agent runner or model access is unavailable; record the exact failure and keep a runnable harness
  - sneaky_fail: treatment prompt leaks intended diagnoses or cases are easier in one condition; prompt diff and case-ID pairing checks catch it
  - UAT: "I can inspect each raw diagnosis and reproduce the aggregate A/B table from it"
- [ ] T5 (R4-R5): Fresh-eyes review the benchmark evidence, then merge the completed benchmark chunk.
  - verify: reviewer reproduces scoring for a sample without seeing aggregate conclusions, then `git diff --check` and benchmark audit pass
  - success: reviewer agrees with the sampled scores or corrections are applied before merge
  - likely_fail: rubric requires subjective reconstruction; tighten evidence fields and rescore
  - sneaky_fail: scorer rewards verbosity or keyword matching rather than diagnosis; reviewer checks decisions against raw outputs and answer keys
  - UAT: "the final results table links to raw outputs and survives independent rescoring"

## Context
- The repo is fail-fast research code: checks should raise on invalid state rather than clamp, fill, skip, or fall back.
- Frozen `docs/evidence/` files contain scraped links that are not expected to resolve locally. Authored files should resolve all local links.
- The user rejected adding worked case studies because they may make agents hyper-focus on the examples.
- The benchmark is last and must use a worktree.

## Log
- Precise failure percentages in `PLAYBOOK.md` are qualitative practitioner ordering presented with unsupported numeric precision.
- For Adam/AdamW, `lr * grad` is not the applied parameter update because moments, normalization, and decoupled weight decay alter the update.
- `just audit` passes 19 authored Markdown files and three skills; its self-test rejects 11 injected defect types.

## Results

Documentation and audit chunk:

```text
$ just audit
audit self-test: PASS (11 injected defects rejected)
audit: PASS (19 authored Markdown files, 3 skills)
```

Fresh-eyes adversarial review rejected broken images, missing fragments, malformed quoted frontmatter, `L0`, reversed evidence ranges, and invalid fence info. Commits `fa534cf` and `0be4323` are pushed to `origin/main`.

## TODO

## Errors
| Task | Error | Resolution |
|------|-------|------------|
| T1-T2 | Both `apply_patch` entry points failed because the sandbox could not configure loopback. | Used exact count-asserted replacements, then reviewed the complete `git diff`; no partial patch landed. |
| T2 | The first audit treated an evidence directory as a file and escaped the self-test fence. | Restricted anchor reads to files and wrote a real fence. |
| T3 | DeepSeek returned only a promise to inspect files; GLM produced no output in about 15 minutes. | Rejected both as failed reviews and dispatched a fresh-eyes repository review instead. |
| T3 | Humanizer lint reports pre-existing file-wide bold-label and punctuation debt. | Kept this change scoped; the edited passages add none of the flagged patterns. |
| T2 | Fresh-eyes review found broken image links, fragments, quoted YAML, `L0`, reversed ranges, and invalid fence info could pass silently. | Added each case to the parser and mutation suite. The reviewer reran all adversarial fixtures and changed R3 from FAIL to PASS. |
