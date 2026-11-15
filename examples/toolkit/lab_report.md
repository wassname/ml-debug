<!-- Example of one lab report: one entry in RESEARCH_JOURNAL.md. The task and every number are
illustrative, not measurements. It shows: the prediction written before the run and scored after
it; evidence quoted with its source; interpretation in the first person with a credence; an
alternative explanation and the test that separates it; no numeric threshold set in advance. -->

## 2026-03-01 12:05 -- answer-only loss mask: small gain in exact match, not yet separable from seed variance

This entry reports the first run with the loss restricted to answer tokens.

Context. Commit 3f2a91c, job 41, `train.py --mask answer --lora-r 8 --steps 600 --seed 0`,
Qwen3-0.6B, 200 held-out problems. Mode: exploring (one seed, stored baseline).

Prediction, written before the run (job label): "answer-only mask gives higher exact match than
full-sequence loss: 60%. If higher, I move to 75%; if equal or lower, to 35%."

Evidence, copied from the final lines of the run log:

| run | exact match | answer loss |
|:---|---:|---:|
| answer-only mask | 0.470 | 0.41 |
| full-sequence loss (stored run, job 37) | 0.445 | 0.48 |
| base model | 0.215 | 2.41 |

Source: `outputs/20260301T1140_answer_mask_s0/run.md`, section "Result". The step-0 check held:
the adapter scored 0.215, equal to the base model. I read 20 of the 200 replies, sampled with
seed 0: all 20 are a single number with no trailing text.

Interpretation (mine). The prediction's direction held: 0.470 against 0.445 is 5 problems of 200.
One seed cannot separate that from seed variance, which I have not measured on this task. I move
from 60% to 65%, not to 75%. Exact match was still rising at step 600, so both runs are
undertrained; the gap could grow or close.

Alternative. The gain comes from a higher effective learning rate, because the mean loss over 2
tokens has larger gradients than the mean over 31. The run log's gradient norm supports this
weakly: 1.8 at step 0 against 0.9 in the stored run. Test that separates the two: the
full-sequence run at twice the learning rate. If it also reaches 0.47, the mask is not the cause.

Next. Queued as job 42: `why: is the answer-mask gain an effect of gradient scale; resolve: keep
the mask only if full-sequence at 2x lr stays below it`.
