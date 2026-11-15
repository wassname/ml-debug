# Diagnostic Statements

Read this when writing or auditing the lines that tell a later reader what a metric should mean.

## Preserve epistemic status

Most first-pass expectations are hypotheses. Label them honestly:

```text
TODO validate: NLL should fall below the base model after the cosine LR starts dropping; compare with the base trajectory and two prior runs.

FIXME: coeff=0 output differs from base output, so the identity sanity check is broken.

SHOULD [mechanism: coeff=0 bypasses the adapter]: output is byte-identical to base. ELSE the zero-coefficient path is not an identity.
```

Promote a claim to `SHOULD:` only when a derivation, mechanism, paper, or validated prior run supports it. Name that basis in the same line or immediately above it. A config default, conventional value, or plausible story is not a basis.

Use `FIXME:` only for behavior already observed to be wrong. An untested suspicion stays `TODO validate:`.

## Make the claim diagnostic

A useful statement predicts a direction, relation, invariant, or qualitative behavior and says what a violation distinguishes.

Useful:

```text
SHOULD [identity path]: coeff=0 output is byte-identical to base. ELSE formatting or routing changed the supposedly inactive path.

TODO validate: validation loss should track training loss after warmup; sustained divergence may indicate overfitting, but compare across seeds before diagnosing it.
```

Harmful:

```text
BAD, DO NOT EMIT: SHOULD: loss is finite.
BAD, DO NOT EMIT: SHOULD: KL < 0.05 because that is the configured default.
BAD, DO NOT EMIT: SHOULD: accuracy > 0.7; otherwise lower the learning rate.
```

The first is only a type-level fact. The second invents a limit. The third invents both a limit and a diagnosis. These lines cause later agents to debug around unsupported claims.

Use a numerical threshold only when its value follows from the experiment, such as a barrier constraint:

```text
SHOULD [constraint definition]: KL < eps_kl=2.0 nats, so the barrier remains slack. ELSE the constraint is competing with the objective.
```

## Keep interpretation beside evidence

Put the statement immediately before or after the metric, sample, or table it interprets, with blank lines around the pair.

```text
kl 0.8 nats
SHOULD [constraint definition]: below eps_kl=2.0 nats, so the barrier is slack. ELSE it competes with the objective.

mse 5.3
TODO validate: should fall across steps if the adapter is active; compare with the frozen-adapter control.
```

Do not collect a wall of statements far from their evidence. Do not repeat them in the final 40-line result block; that block reports results.

## Avoid unvalidated diagnosis

Describe what an observation discriminates before prescribing a fix. Include a diagnosis or repair only when the causal link has been validated repeatedly or the user has explicitly recorded it as institutional knowledge.

When designing a training diagnostic that you cannot justify mechanistically, do the PREDICT and CAUSES steps of [SKILL.md](../SKILL.md). If it still lacks support, leave it as `TODO validate:` instead of filling the gap with a plausible threshold.
