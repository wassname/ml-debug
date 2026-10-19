# Model-guided research: planning check

Fresh `reviewer-openai` response to three hypothetical research cases after reading the edited
skill. These are recommendations, not executed GPU experiments. The cases were supplied with
the skill path, so this does not test automatic skill discovery. No old-skill comparison was run.

Parent assessment: the response chose targeted architecture tests over a broad sweep and an
unmotivated probe (A), observation-led exploration without a fixed theory (B), and an ablation
for a working method's attribution claim (C). This checks those examples, not general uplift.

Static checks passed: `git diff --check` for both edited repositories; all `SKILL.md` relative
links resolve; the Bayesian reference anchor exists; all three new quotations match the
LessWrong markdown API verbatim (ignoring added bold emphasis).

Assessment and static checks: PI/OpenAI. Case responses below: reviewer-openai.

### A. Test the gate intervention, not a broad sweep

Recommend two paired 45-minute runs: gate removed versus nonsaturating gate, using the same seed, data order, adapter initialization, and existing optimizer settings. Smoke-test both through the real pipeline first. Preserve initial adapter-output scale where feasible; document any unavoidable difference.

The repeated zero gate and tiny gradients make blocked adapter learning a plausible explanation, not a proven cause. LR insensitivity weakens the case for an LR-first search but does not exclude optimizer effects. These architectural tests cost approximately 1.5 GPU-hours; a 24-point sweep at current duration costs 18.

Inspect inline gate values and derivatives, adapter gradients **and actual parameter updates**, adapter-output norms, training loss, validation performance, and representative predictions.

- Both variants restore updates and improve validation: favor the simpler gate-free method; replicate across seeds.
- Only the nonsaturating variant improves: retain adaptive scaling; investigate whether gate removal destabilizes output magnitude.
- Updates recover without task gains: saturation was a bottleneck, not the whole explanation. Next compare low-rank capacity/insertion choices against the learning dense reference.
- Neither restores updates: inspect optimizer membership, detachments, initialization, and the backward path before further training.

Allocate the remaining approximately 4.5 hours adaptively to replication or the indicated repair. Defer full ablations. Reject the offline similarity probe unless someone specifies a decision its outcomes would change that these inline measurements cannot answer.

### B. Discover structure before choosing a mechanism

Recommend inspecting a small random sample plus high-, low-, and unexpectedly changing-loss examples, showing both raw inputs and their actual model-consumed representations. Then run two short baseline continuations from the same checkpoint with different data orders, capped at 25 GPU-minutes each, evaluating a fixed example panel.

This buys direct familiarity and separates repeatable example difficulty from unstable learning without inventing an explanation. Inspect labels, truncation/masks, source/domain, length, predictions, and per-example loss trajectories. Compare against untouched random examples to avoid conclusions based only on extremes.

- Stable groups emerge: formulate a tentative explanation and select a matched comparison next.
- Corrupt labels or preprocessing emerge: repair that specific defect and rerun affected examples alongside unaffected controls.
- Difficulty rankings change substantially across continuations: prioritize batch composition, stochasticity, and gradient interference.
- No structure emerges: broaden qualitative sampling and record what remains unknown; do not launch an arbitrary architecture search.

### C. Test the attribution to X

Recommend retraining without X, paired to the three existing seeds, keeping data, training budget, evaluation, and other settings fixed. Cap this targeted comparison at four GPU-hours. Reuse full-method results only if their provenance matches.

Inspect paired held-out score differences, seed spread, learning curves, and subgroup effects.

- Removing X consistently eliminates the gain: supports X’s contribution **within this configuration**, not its sufficiency or the claimed internal mechanism.
- Gains persist with narrow uncertainty: withdraw the claim that X is necessary; prefer the simpler method.
- Partial degradation: attribute only that portion conditionally to X.
- Noisy differences: attribution remains unresolved; spend remaining budget on precision.
- Ablation destabilizes training: distinguish optimization dependence from the proposed mechanism through a matched replacement/rescue test.