# Justfile with sweep recipes

<!-- Moved from the repo-setup skill by PI/Claude, 2026-11-17; wassname's practices. -->


```just
set shell := ["bash", "-cu"]

SEEDS_3 := "41 43 44"
BASE := "uv run python -m mypackage.run"

# List available recipes
default:
    @just --list

# Queue all sweeps. Comment out completed sections; `just results` to check.
queue:
    #!/usr/bin/env bash
    set -x
    # -- round 1: one-factor sweeps --
    # just sweep-lr    # done: lr=3e-4 best
    just sweep-lr

# One-factor sweep: learning rate
# H: 3e-4 is a typical Adam learning rate; confirm on this task
sweep-lr:
    #!/usr/bin/env bash
    set -x
    export WANDB_RUN_GROUP="sweep-lr-$(date +%Y%m%d-%H%M)"
    for seed in {{ SEEDS_3 }}; do
        for lr in 1e-5 1e-4 3e-4 1e-3; do
            echo "=== lr=$lr seed=$seed ==="
            {{ BASE }} --lr=$lr --seed=$seed
        done
    done

# smoke: one end-to-end run of the real pipeline on tiny inputs.
# Real model calls, real evaluation, real I/O; only the scale changes. Not a unit test.
smoke *ARGS:
    BEARTYPE=1 {{ BASE }} --fast-dev-run {{ ARGS }}

# Download wandb runs to cache
download:
    uv run python scripts/download_wandb.py

# Analyze cached results
analyze *ARGS:
    uv run python scripts/analyze_results.py {{ ARGS }}

# Download + analyze
results *ARGS:
    just download
    just analyze {{ ARGS }}
```

Rules for sweep recipes:
- Comment starts with `# H:` hypothesis
- Group sweeps with `WANDB_RUN_GROUP` including timestamp
- Loop seeds innermost (so all conditions run before any seed repeats)
- Comment out completed sweeps with outcome in the `queue` recipe

The smoke recipe uses the same entry point and the same code as the real run, at the smallest
config that executes every code path of the real run: tiny random model, GPU, `BEARTYPE=1`, about
1 minute. Run enough steps to reach each periodic action (checkpoint save, scheduler step), and
run it twice when there is a disk cache. Do not write a second, smaller harness. The GPU is used
so that the real dtype (for example bf16) is tested; a tiny model uses a small fraction of it, so
the smoke test does not need the queue.
