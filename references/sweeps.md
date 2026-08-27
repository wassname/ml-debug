# Sweeps: same-seed comparison and cross-seed reliability

Appendix to the [ML Debugging skill](../SKILL.md). The general idea behind a trustworthy hyperparameter sweep, tool-agnostic. The point is the difference between "I tried it and it seemed better" and "it's reliably better across seeds." Irpan's 30% seed-failure result and Henderson's "seeds alone create statistically different distributions" (see the main skill's folklore section) are why this matters: a single lucky run proves nothing.

## The core move: pair on seed, normalize within group, test across seeds

1. Run the same set of seeds for every value of the parameter you're varying. Same seeds across values turns this into a paired comparison and cancels seed-level baseline differences.
2. Vary one parameter per sweep when you can (all-else-equal). If you vary two, effects confound and you can't attribute the result.
3. Within each (group, seed), z-score the metric across the parameter values. This removes the per-seed baseline offset so you compare *shapes*, not absolute levels.
4. Aggregate the z-scores across seeds per value, then take a t-stat: `mean_z / (std_z / sqrt(n_seeds))`. `|t| > 2` with 4+ seeds is a real, reliable effect; `t ~ 0` is no consistent effect.
5. For numeric parameters, also fit a linear trend (Pearson r) and t-test it: a clean dose-response is `r` near +/-1 with a significant t-stat.

```py
for group in groups:
    for seed in seeds_in_group:
        vals = {param_value: metric for runs matching (group, seed, param)}
        z[seed] = (vals - mean(vals)) / std(vals)   # within-(group,seed) normalization
    for value in param_values:
        mean_z, std_z = mean(z[:, value]), std(z[:, value])
        t_stat = mean_z / (std_z / sqrt(n_seeds))    # >>2 reliably better, <<-2 reliably worse
```

## What you're looking for

High effect size *and* a strong t-stat. A value with a big mean but `t=0.5` is a lucky seed; a value with a modest mean but `t=4.0` is a real (if small) effect.

## Common pitfalls

- `n_seeds = 1`: t-stat is undefined. One data point. Replicate before concluding anything.
- Cross-group comparisons: different groups often have different base configs, so "group A's best value vs group B's best" is apples-to-oranges. Compare within groups.
- Too many parameters varied at once: split into separate sweeps.
- Crashed / diverged runs showing as missing or NaN metrics: investigate the run, don't silently drop it; a divergence is itself a finding.
