"""Diagnostics for model components that require no design choice: copy this file next to train.py.

For every new part, three questions have a mechanical answer:
  is it learning?        movement(): how far each parameter group moved from its start
  who shapes it?         grad_share(): each loss term's gradient norm, share and cosine at each group
  is each input in use?  input_swap(): the metric with one named input permuted across the batch

Each function returns rows; table() prints them as Markdown with the statement that says how to
read them. Call them at evaluation steps and write the result into run.md beside the other numbers.
Demo and self-test: python3 scripts/parts.py
"""
from __future__ import annotations

from typing import Callable

import torch
from torch import Tensor, nn

Groups = dict[str, list[nn.Parameter]]


def snapshot(groups: Groups) -> dict[str, list[Tensor]]:
    """Copy of every parameter at the start of training, for movement()."""
    return {name: [p.detach().clone() for p in ps] for name, ps in groups.items()}


def movement(groups: Groups, start: dict[str, list[Tensor]]) -> list[dict]:
    rows = []
    for name, ps in groups.items():
        moved = torch.sqrt(sum(((p.detach() - p0) ** 2).sum() for p, p0 in zip(ps, start[name])))
        norm0 = torch.sqrt(sum((p0**2).sum() for p0 in start[name]))
        rows.append({"part": name, "moved": moved.item(), "start norm": norm0.item()})
    return rows


def _flat_grad(loss: Tensor, ps: list[nn.Parameter]) -> Tensor:
    gs = torch.autograd.grad(loss, ps, retain_graph=True, allow_unused=True)
    return torch.cat([(g if g is not None else torch.zeros_like(p)).flatten() for g, p in zip(gs, ps)])


def grad_share(losses: dict[str, Tensor], groups: Groups) -> list[dict]:
    """Each loss term's gradient alone at each group: norm, share of the summed norms, and for two
    terms their cosine. Call before backward() of the total, on the same graph."""
    rows = []
    for part, ps in groups.items():
        grads = {term: _flat_grad(loss, ps) for term, loss in losses.items()}
        total = sum(g.norm() for g in grads.values())
        row = {"part": part}
        for term, g in grads.items():
            row[f"{term} norm"] = g.norm().item()
            row[f"{term} share"] = (g.norm() / total).item() if total > 0 else float("nan")
        if len(grads) == 2:
            a, b = grads.values()
            row["cosine"] = torch.nn.functional.cosine_similarity(a, b, dim=0).item() if a.norm() * b.norm() > 0 else float("nan")
        rows.append(row)
    return rows


@torch.no_grad()
def input_swap(metric: Callable[..., Tensor], inputs: dict[str, Tensor], seed: int = 0) -> list[dict]:
    """metric(**inputs) -> scalar error on a held-out batch. Each named input is permuted across the
    batch (dim 0) in turn, the others kept."""
    gen = torch.Generator().manual_seed(seed)
    intact = metric(**inputs).item()
    rows = [{"input": "(intact)", "error": intact, "change": 0.0}]
    for name, x in inputs.items():
        perm = torch.randperm(x.shape[0], generator=gen).to(x.device)
        swapped = metric(**{**inputs, name: x[perm]}).item()
        rows.append({"input": f"{name} swapped", "error": swapped, "change": swapped - intact})
    return rows


STATEMENTS = {
    "movement": "TODO validate: every part that should learn has moved; a part with movement 0, or movement far below its start norm, receives no gradient or a very small one.",
    "grad_share": "TODO validate: every term that should shape a part has a visible share there. A share near 0 with cosine near 0 is a difference in size, not a conflict: PCGrad or UPGrad then return the plain sum and do not help.",
    "input_swap": "SHOULD [mechanism: a part that uses an input gives a different output when that input comes from another example]: the error with an input swapped is above the intact error. ELSE that input has no effect: not connected, or entering at a scale far below the other inputs.",
}


def table(rows: list[dict], kind: str) -> str:
    cols = list(dict.fromkeys(k for r in rows for k in r))
    fmt = lambda v: f"{v:.4g}" if isinstance(v, float) else str(v)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(":---" if i == 0 else "---:" for i in range(len(cols))) + "|"]
    lines += ["| " + " | ".join(fmt(r.get(c, "")) for c in cols) + " |" for r in rows]
    return "\n".join(lines) + "\n\n" + STATEMENTS[kind] + "\n"


def _demo() -> None:
    """A toy with two properties that hold by construction: the second loss reaches the encoder only
    through U, which starts at zero, and one input is accepted and never used."""
    torch.manual_seed(0)
    d, n = 16, 256
    enc, dec, U = nn.Linear(d, d), nn.Linear(2 * d, d), nn.Parameter(torch.zeros(d, d))
    groups: Groups = {"encoder": list(enc.parameters()), "decoder": list(dec.parameters()), "U": [U]}
    start = snapshot(groups)
    x, tok, unused = torch.randn(n, d), torch.randn(n, d), torch.randn(n, d)
    y1, y2 = x.roll(1, 1), (x + tok).roll(2, 1)

    def terms(x: Tensor, tok: Tensor, unused: Tensor) -> dict[str, Tensor]:
        z = enc(x)
        out = dec(torch.cat([z, tok], -1)) @ U
        return {"forecast": ((z - y1) ** 2).mean() / (y1**2).mean(), "slope": ((out - y2) ** 2).mean() / (y2**2).mean()}

    opt = torch.optim.Adam([p for ps in groups.values() for p in ps], lr=1e-2)
    shares = {}
    for step in range(201):
        losses = terms(x, tok, unused)
        if step in (0, 10, 200):
            shares[step] = grad_share(losses, groups)
            print(f"\n### step {step}\n\n" + table(shares[step], "grad_share"))
        opt.zero_grad()
        sum(losses.values()).backward()
        opt.step()
    moved = movement(groups, start)
    print(table(moved, "movement"))
    swap = input_swap(lambda **kw: terms(**kw)["slope"], {"x": x, "tok": tok, "unused": unused})
    print(table(swap, "input_swap"))
    # self-test, each line true by construction of the toy
    assert shares[0][0]["slope share"] == 0, "U = 0: the slope term cannot reach the encoder at step 0"
    assert shares[200][0]["slope share"] > 0, "U has moved: the slope term reaches the encoder"
    assert swap[3]["change"] == 0, "an input the function ignores changes nothing when swapped"
    assert swap[1]["change"] > 0 and swap[2]["change"] > 0, "inputs in use change the error when swapped"
    assert all(r["moved"] > 0 for r in moved)
    print("parts.py self-test: PASS")


if __name__ == "__main__":
    _demo()
