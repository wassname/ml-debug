# nanochat: LLM Pretraining Engineering Notes

**Sources:**
- deepwiki.com/karpathy/nanochat (sections 3, 12, 13) -- AI-generated wiki from source + LOG.md
- github.com/karpathy/nanochat/blob/main/dev/LOG.md -- primary experiment log
**URLs:** https://deepwiki.com/karpathy/nanochat, https://github.com/karpathy/nanochat
**Date accessed:** 2026-03
**Context:** nanochat is Karpathy's 2026 open-source minimal LLM speedrun (GPT-2 level in ~2.5h on 8xH100, ~3500 lines). The LOG.md documents 320+ HP sweeps from Jan-Mar 2026.
**Caveat:** deepwiki pages are AI-generated from source code; treat as secondary docs. LOG.md quotes are primary (verbatim from the experiment log).

---

## 1. Dataset >> Architecture (empirical)

From LOG.md (2026-03-04):
> "This is by far the single biggest improvement to nanochat's GPT-2 speedrun time, bringing it down from **2 hours 46 minutes to 2 hours 1 minute** — a 27% reduction."

The 27% came from one dataset swap (FineWeb-EDU 100B → ClimbMix 400B). The previous 5 architecture/dataset attempts all failed:
1. Vanilla FineWeb (CORE 0.2602 → 0.2241)
2. FinePDFs mixture (0.2602 → 0.2549)
3. Dolma3_mix-6T (failed)
4-5. Two more undocumented attempts.

**Lesson:** If training is slow or CORE is low, swap datasets before tuning architecture.

---

## 2. Scale-dependent HP sensitivity: tune at target scale

From deepwiki section 12 (sourced from LOG.md sweeps):

> "Fine-tuned d12 hyperparameters actively hurt d20 performance."

- d12 → d20 HP transfer fails: improvement magnitude shrinks (~0.002 at d12 → ~0.0007 at d20)
- `x0_beta1` sweep at d20: flat plateau 0.90-0.96, **sharp cliff at 0.98** (catastrophic: +0.0033 bpb)
- "Add only changes that were validated at d20+" before production

**Sweep methodology:**
1. Quick experiment at d12 (~5 min): directional signal
2. Validate at target scale d20 (~20 min)
3. If still promising, validate at production d24+ (~1-2 hours)

---

## 3. Multi-axis validation: steps, FLOPs, wall-clock

From LOG.md (throughout):
> "Improvements must show gains across multiple axes: per-step efficiency (loss vs. step), wall-clock efficiency (loss vs. time), and compute efficiency (loss vs. FLOPs)."

**FP8 example (LOG.md 2026-02-02):**
- Microbenchmark: 1.38x speedup
- Full training: 1.17x tok/sec
- Capability-matched (accounting for precision loss): **~5% real gain**

> "torch.compile is MANDATORY. Without it, FP8 is 4x slower due to unfused scaling ops."

**MoE example (LOG.md 2026-02-19):** MFU dropped 46% → 35%; per-step improvement didn't compensate; net negative.

---

## 4. Negative results: what doesn't work at GPT-2 scale

**SwiGLU** (2026-02-05): Iso-FLOP swap, tested d12 and d24. Worse on step efficiency, wall clock, FLOPs. ReLU² remains superior.

**Mixture of Experts** (2026-02-19):
- `torch._grouped_mm` dispatch overhead: MFU 46% → 35%
- Per-step improvement doesn't compensate throughput hit
- FP8 unsupported for grouped matmul (needs separate API + custom Triton kernels)
- Verdict: "MoE is not worth the trouble for nanochat right now."

**Multi-Token Prediction:** +13GB memory, MFU −1%, no per-step improvement, wall-clock worse.

**Batch size ramping:** Small gains observed but code complexity not justified.

**Five data mixtures** all worse than FineWeb-EDU before ClimbMix (see §1).

---

## 5. MFU monitoring: primary throughput health check

> "In wandb, `train/mfu` (Model FLOPs Utilization) should be >40%"

MFU <40% suggests:
- GPU memory underutilized (device batch size too small)
- I/O bottleneck (data loading slower than compute)
- Excessive distributed synchronization overhead

MFU calculation: `(flops_per_token × batch_tokens_per_sec) / (gpu_peak_flops × n_gpus)`

Normal range 40-60% on 8xH100 for transformer training.

---

## 6. BOS alignment: loss improvement may be "fake"

From deepwiki section 12:
> "The 'lower validation loss' from BOS-alignment is misleading—it's just fewer noisy tokens, not better learning."

Best-fit packing (adopted) vs greedy-crop (baseline):
- Greedy-crop: 39.4% of tokens are crops (mid-document)
- Best-fit: 34.6% crops -- still significant

Both ensure sequences start at document boundaries (BOS token). Sequences that start mid-document add confusing tokens and inflate validation loss.

**Implication:** When comparing two training runs with different dataloaders, check if the loss comparison is apples-to-apples.

---

## 7. Explicit dtype management > autocast

From LOG.md (2026-03-04):
> "autocast is 'magic we don't control' — it silently decides which ops run in which precision via internal allowlists."

Replaced autocast with:
```python
COMPUTE_DTYPE = torch.bfloat16 if sm >= 80 else torch.float32  # auto-detected
# Override: NANOCHAT_DTYPE=float32 python train.py
```

Custom `Linear` class casts weights to match input dtype: `F.linear(x, self.weight.to(dtype=x.dtype))`.

**Debugging application:** Override `NANOCHAT_DTYPE=float32` globally to debug NaN/Inf without hunting `with autocast():` blocks.

FA3 (Hopper kernels): doesn't support fp16/fp32 → automatic fallback to SDPA.

---

## 8. FP16 + distributed: inf detection must be synchronized

From deepwiki section 12:
> "If any rank's gradient contains inf, **all ranks must clip to avoid divergence**."

Pattern:
```python
grad_norm = clip_grad_norm_(model.parameters(), 1.0)
dist.all_reduce(grad_norm, op=dist.ReduceOp.MAX)  # "is any rank inf?"
if torch.isinf(grad_norm):
    optimizer.zero_grad(); continue  # skip step on ALL ranks
```

Single-GPU testing hides this bug. Always test distributed code multi-GPU.

---

## 9. Empirical scaling laws (from 320+ sweeps)

**Batch size** (sourced from Cerebras "Power Lines" paper):
```
B_opt ∝ D^0.383  (D = target training tokens)
```
Reference: d12 at B=2^19. 10× more tokens → only ~2.4× bigger batch (sublinear).

| Depth | Target Tokens | Auto Batch |
|-------|--------------|------------|
| d8    | 0.44B        | 2^18 = 262K |
| d12-16| 0.7B-2.5B   | 2^19 = 524K |
| d18-26| 3.4B-9.6B   | 2^20 = 1.05M |

**Weight decay** (empirically derived, LOG.md):

| Depth | Width | Optimal WD |
|-------|-------|-----------|
| d8    | 512   | ~0.40 |
| d12   | 768   | ~0.22 |
| d16   | 1024  | ~0.10 |
| d20   | 1280  | ~0.08 |

Power law fit: `WD ∝ 1/width²`. Scale from reference: `WD_target = WD_ref × (width_ref/width_target)²`.

---

## 10. Python GC overhead: disable after warmup

From deepwiki section 3:
> "GC is disabled after step 1 to prevent 500ms overhead from cycle detection."

500ms × 880 steps ≈ 7 minutes lost to GC on a 2.76h run (4.4% overhead). Disable safely after step 1 when allocation patterns stabilize.

---

## 11. Cautious weight decay + torch.compile gotcha

From deepwiki section 12:
> "Must inline logic in optimizer step. Passing `weight_decay` as function argument triggers torch.compile recompilation on schedule changes."

```python
# Good: read at step time from group dict
for group in param_groups:
    wd = group["weight_decay"]  # no recompile on schedule change

# Bad: pass as argument (recompiles when wd changes)
def step(self, wd):  # triggers recompile every step if wd schedule varies
```

---

## 12. Compute-optimal ratio: 10.5 (Kaplan-style counting)

From LOG.md sweeps across parameter-counting methods:
- Kaplan-style (projections including lm_head, no embeddings): stable 10.5 ratio across scales
- Chinchilla-style (all params): varies 3.0-4.0

For speedrun: deliberately undertrain to ratio ~9.5 (saves ~2-3h) to hit GPT-2 CORE threshold.

---

## 13. FP8 summary

- Effective speedup at d24 scale: ~5% (capability-matched), not the microbenchmark 1.38x
- Memory saving: ~9GB activations stored as FP8 vs BF16
- `torch.compile` mandatory: without it, FP8 is 4× slower
- Only works on Hopper (H100, SM 90+)
- During evaluation: **disable FP8** (use BF16/FP32) -- FP8 introduces ~5% accuracy variance

---

## 14. Key gap this fills

The existing ml_debug skill sources (2017-2021) predate modern LLM pretraining at scale. nanochat is one of the few open-source codebases that publicly documents the empirical decisions behind training a transformer from scratch in 2026, with quantified results: 320+ sweeps, negative results, scaling laws, and specific failure modes.
