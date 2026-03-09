# nn-zero-to-hero Lecture 4: Activations, Gradients, BatchNorm

**Source:** Andrej Karpathy, nn-zero-to-hero lecture series
**Notebook:** lectures/makemore/makemore_part3_bn.ipynb
**URL:** https://github.com/karpathy/nn-zero-to-hero
**Lecture description:** "We dive into some of the internals of MLPs with multiple layers and scrutinize the statistics of the forward pass activations, backward pass gradients, and some of the typical diagnostic tools and visualizations you'd want to use to understand the health of your deep network."

---

## Incremental improvements documented (from notebook markdown)

```
original:            train 2.1245  val 2.1682
fix softmax wrong:   train 2.07    val 2.13     (overconfident init)
fix tanh saturated:  train 2.0356  val 2.1027   (init scale too large)
use kaiming init:    train 2.0377  val 2.1070   (semi-principled)
add batch norm:      train 2.0668  val 2.1048   (stable across random seeds)
```

Each row = one targeted fix. The ordering demonstrates the hierarchy: data/loss first, then init, then architecture.

---

## Activation saturation check (tanh)

```python
for i, layer in enumerate(layers[:-1]):
    if isinstance(layer, Tanh):
        t = layer.out
        print('layer %d (%10s): mean %+.2f, std %.2f, saturated: %.2f%%' %
              (i, layer.__class__.__name__, t.mean(), t.std(),
               (t.abs() > 0.97).float().mean() * 100))
        hy, hx = torch.histogram(t, density=True)
        plt.plot(hx[:-1].detach(), hy.detach())
# Healthy: distributions roughly Gaussian, saturation <5%.
# Bad: bimodal at +/-1 = too saturated (weights too large at init, or missing BN).
# Bad: all near 0 = dead layer (weights too small or gain 0).
```

---

## Gradient distribution check (per-layer)

```python
for i, layer in enumerate(layers[:-1]):
    if isinstance(layer, Tanh):
        t = layer.out.grad  # requires retain_grad() in training loop
        print('layer %d (%10s): mean %+f, std %e' %
              (i, layer.__class__.__name__, t.mean(), t.std()))
        hy, hx = torch.histogram(t, density=True)
        plt.plot(hx[:-1].detach(), hy.detach())
# Healthy: similar gradient std across layers (no vanishing/exploding gradient).
# Bad: gradient std shrinks toward earlier layers = vanishing gradient.
# Bad: gradient std explodes = need BN, gradient clipping, or better init.
```

---

## Grad:data ratio check (weight matrices)

```python
for i, p in enumerate(parameters):
    t = p.grad
    if p.ndim == 2:
        print('weight %10s | mean %+f | std %e | grad:data ratio %e' %
              (tuple(p.shape), t.mean(), t.std(), t.std() / p.std()))
        hy, hx = torch.histogram(t, density=True)
        plt.plot(hx[:-1].detach(), hy.detach())
# grad:data ratio ~ 1e-3 is healthy.
# Much higher: gradients dominate weights, learning rate too large.
# Much lower: weights barely moving, potentially dead layer.
```

---

## Update-to-data ratio tracker (training loop)

```python
ud = []

# Inside training loop:
for p in parameters:
    p.data += -lr * p.grad

with torch.no_grad():
    ud.append([((lr * p.grad).std() / p.data.std()).log10().item()
                for p in parameters])

# After training, plot:
plt.figure(figsize=(20, 4))
legends = []
for i, p in enumerate(parameters):
    if p.ndim == 2:
        plt.plot([ud[j][i] for j in range(len(ud))])
        legends.append('param %d' % i)
plt.plot([0, len(ud)], [-3, -3], 'k')  # target ~1e-3
plt.legend(legends)
# Each line should stay near -3.
# Rising above -3: LR too large, may diverge.
# Sinking below -3: LR too small, near-zero updates.
# Diverging between layers: need better initialization or BN.
```

---

## Key pedagogical insight from the notebook

The notebook demonstrates by construction (not just assertion) that:
1. Saturated tanh at init → slow learning (gradient vanishes through tanh)
2. Kaiming init → ~same scale activations throughout depth
3. BatchNorm → robust to poor init; normalization forces healthy activation stats

The incremental improvement log (above) makes this concrete: each targeted fix yields measurable improvement. This is the same pattern as the recipe blog post but with code and measured results.
