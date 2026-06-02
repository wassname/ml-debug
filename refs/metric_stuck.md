# Why won't this metric move?

Appendix to the [ML Debugging skill](../SKILL.md). When a quantity you're optimizing plateaus, these are ideas for telling *why*, not a flowchart to obey. They apply to most training setups, but they're suggestions; your project may not fit them.

The useful split is three questions, cheapest first.

## 1. Is the gradient nonzero at the metric level?

```py
metric_val = torch.tensor(current_value, requires_grad=True)
loss = loss_fn(metric_val)
loss.backward()
print(f"d(loss)/d(metric) = {metric_val.grad}")
```

- ~0: the loss doesn't care about this metric at the current operating point. Maybe saturated (log1p of a huge value), in a dead zone, or the metric is disconnected from the loss.
- large: the loss is trying to move it. The problem is downstream.

## 2. Can the parameter even change the metric?

Trace the chain `loss -> metric -> ... -> parameter`. The metric is a function of intermediate quantities, which are functions of learned parameters. Look at `d(metric)/d(parameter)`:

- Analytically: is there a structural reason this derivative is ~0? (e.g. a rotation of V can't change span(U).)
- Empirically: disable the loss term (set its coefficient to 0). Does the metric reach the same value anyway? If yes, the optimization never moved it; it's a structural ceiling, and you need a different parameterization, not a different loss weight.

## 3. Is something else fighting it?

If the gradient is nonzero and the parameter *can* change the metric:

- Competing loss terms: compute each component's gradient on the shared parameter separately. Opposite-sign gradients cancel.
- Optimizer state: AdamW momentum from earlier training can resist a direction change. Try resetting optimizer state or a warmup.
- Conditioning: if the metric needs coordinated changes across many parameters (rotating several layers at once), the per-parameter gradient may be too small even when the aggregate signal is large.

## A rough map (a guide, not a verdict)

| d(loss)/d(metric) | d(metric)/d(param) | Same value with the term off? | Reading |
|---|---|---|---|
| ~0 | any | any | Loss saturated or disconnected; reconsider the loss formula. |
| large | ~0 | yes | Structural ceiling; reconsider the parameterization. |
| large | large | no | Competing losses or optimizer inertia; isolate them. |
| large | large | yes | The term helps but converges to the same basin; weak effect or coincidence. |

## Structural-ceiling check, concretely

```py
# 1. Is d(loss)/d(metric) large? If so, the optimizer IS trying.
metric = torch.tensor(0.5, requires_grad=True)
loss = loss_fn(metric); loss.backward()
print(metric.grad)   # large (e.g. 350x the other grads) => it's trying

# 2. Can the parameter change the metric? Trace loss -> metric -> intermediate -> parameter.
#    If d(metric)/d(parameter) ~ 0, the parameter structurally cannot move it.
#    (e.g. a V-rotation can't change the output basis when U is fixed.)

# 3. Confirm empirically: set the term's coefficient to 0.
#    If the metric reaches the SAME value, it was never learned; it's structural.
```
