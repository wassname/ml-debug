<!-- Example of the run log that train.py writes. The task and every number are illustrative, not
measurements. Layout rules it shows: the question first; a blank line before and after every
heading, table and code fence (a table without a blank line before it does not render); each
statement directly under the metric it interprets; the final block fits in `tail -40` and ends
with the path of this file. -->

# train: masked answer loss, LoRA r=8, seed 0

Question: does a loss on answer tokens only raise exact match on held-out word problems, compared
with a loss on every token? Compared with: `outputs/20260301T1010_full_seq_s0/run.md`.
Resolve: adopt the answer-only mask as the default if exact match is higher and the sampled replies
are complete sentences.

argv: `train.py --mask answer --lora-r 8 --steps 600 --seed 0`

| setting | value |
|:---|:---|
| model | Qwen3-0.6B |
| commit | 3f2a91c |
| train / held-out problems | 4,000 / 200 |
| batch, lr, steps | 16, 3e-4 constant, 600 |


## train -> first batch as the model receives it

```text
<|im_start|>user
Tom has 3 boxes of 12 pencils. He gives away 7. How many are left?<|im_end|>
<|im_start|>assistant
29<|im_end|>
```

Loss mask: 2 of 31 tokens (`29`, `<|im_end|>`).

SHOULD [construction of the mask]: only tokens after `<|im_start|>assistant\n` are in the loss.
ELSE the mask also covers the prompt, and this run equals the full-sequence run.


## train -> step 0

| metric | value |
|:---|---:|
| held-out exact match, adapter | 0.215 |
| held-out exact match, base model | 0.215 |

SHOULD [mechanism: LoRA matrix B is initialised to zero]: the adapter's step-0 score equals the
base model's. ELSE the adapter path is not an identity at initialisation.


## train -> metrics (every 100 steps)

| step | answer loss ↓ | held-out exact match ↑ | grad norm | adapter movement |
|---:|---:|---:|---:|---:|
| 0 | 2.41 | 0.215 | 1.8 | 0.00 |
| 100 | 1.02 | 0.340 | 1.1 | 0.61 |
| 300 | 0.55 | 0.455 | 0.7 | 1.34 |
| 600 | 0.41 | 0.470 | 0.6 | 1.71 |

TODO validate: exact match is still rising at step 600 (0.455 to 0.470), so the run has not
converged; compare with a 1,200-step run before reading the final value as the method's limit.


## eval -> held-out demo 1 of 3 (sampled with seed 0, not selected by score)

```text
<|im_start|>user
A train has 8 cars with 54 seats each. 37 seats are empty. How many seats are taken?<|im_end|>
<|im_start|>assistant
395<|im_end|>
```

Expected: 395. Correct.


## Result

Status: completed in 11 min 40 s; peak GPU memory 6.2 GB.

Question: does a loss on answer tokens only raise exact match, compared with a loss on every token?

Table: held-out exact match after 600 steps, 200 problems, seed 0. Higher is better.

| run | exact match ↑ | answer loss ↓ |
|:---|---:|---:|
| answer-only mask (this run) | **0.470** | 0.41 |
| *full-sequence loss (stored run)* | *0.445* | 0.48 |
| *base model (floor)* | *0.215* | 2.41 |

Records: [all 200 replies](records.jsonl).

outputs/20260301T1140_answer_mask_s0/run.md
