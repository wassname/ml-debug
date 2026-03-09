# nanochat: LLM Pretraining Engineering Notes

**Source:** deepwiki.com/karpathy/nanochat (AI-generated wiki from karpathy/nanochat repo)
**URLs:** https://deepwiki.com/karpathy/nanochat, https://github.com/karpathy/nanochat
**Date accessed:** 2026-03
**Context:** nanochat is Karpathy's 2026 open-source minimal LLM speedrun (GPT-2 level in ~2.5h on 8xH100, ~3500 lines, ~$48).
**Caveat:** The deepwiki page is AI-generated from source code; treat as secondary documentation, not direct quotes.

---

## Design principle: explicit over implicit

> Explicit over implicit: No `torch.amp.autocast` magic; precision managed via `COMPUTE_DTYPE` global

Auto-detected at runtime: bfloat16 on SM 80+ (A100/H100), float32 on older GPUs.

**Debugging application:** Override globally for numerical stability debugging:
```bash
NANOCHAT_DTYPE=float32 python -m scripts.chat_cli -p "hello"
```
Avoids hunting through scattered `with autocast():` blocks when debugging NaN/Inf.

---

## Monitoring: MFU target

> When performance is unexpectedly low: Check `train/mfu` (Model FLOPs Utilization) should be >40%

MFU <40% suggests: GPU memory underutilized (batch size too small), I/O bottleneck (data loading slower than compute), or excessive distributed-training synchronization overhead.

---

## Data pipeline: BOS-aligned dataloader

> BOS-aligned best-fit dataloader ensuring every sequence starts with document boundary

Sequences must start at document boundaries (BOS token), not mid-document. Prevents loss spikes from predicting the start of an unrelated document as if it were a continuation.

---

## Systematic HP development: 320+ sweeps

> The dev/LOG.md experiment log documents 320+ hyperparameter sweeps and design decisions made since January 2026.

**Principled generalization criterion:** Changes must work across model depths (d8 to d50+), not just the target size. Improvements that only help at one scale are artifacts, not general algorithmic improvements.

---

## Four-axis improvement validation

When implementing an optimization, validate across:
1. Loss per training step (convergence speed)
2. Loss per wall-clock time (helps despite potentially slower per-step?)
3. Loss per FLOP (better hardware utilization vs. better algorithm?)

Prevents optimizations that appear good on one metric but regress on others.

---

## Scaling laws (empirical, from 320+ sweeps)

- Batch size: `B ∝ D^0.383` where D = target training tokens (sublinear, not linear scaling)
- Learning rate: per-component scaling with `√(768/n_embd)` factors
- Weight decay: `WD ∝ 1/width²`

Credence ~60-65%: stated as empirical, derivation not provided.

---

## OOM debugging: reduce device batch, keep effective batch

> Reducing device-batch-size from 32 to 16 triggers 2× gradient accumulation

Gradient accumulation maintains effective batch size. OOM errors often solvable without changing the training recipe.

---

## FP8 caveat

FP8 only works on Hopper architecture (H100). Remove `--fp8` on A100 or older.

---

## Key gap this fills

The existing ml_debug skill sources (2017-2021) predate modern LLM pretraining at scale. nanochat is one of the few open-source codebases that publicly documents the empirical decisions behind training a transformer from scratch in 2026, including 320+ sweep results. It covers:
- Loss spike prevention (BOS alignment)
- Distributed training OOM (gradient accumulation)
- Precision management (explicit dtype, FP8 caveat)
- MFU monitoring
- Cross-scale generalization testing
