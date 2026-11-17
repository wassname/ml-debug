# Minimal runbook: the order of work on one page

<!-- Moved from the repo-setup skill by PI/Claude, 2026-11-17; wassname's practices. -->


The chain every experiment follows. A script with a dataclass config computes
and saves JSON; pueue queues it on the shared GPU with a why/resolve label; a
marimo notebook renders the JSON; `just nb-html` exports judgeable HTML. Heavy
compute never runs inside the notebook (an 18-min model load in a kernel makes
the report unrenderable; a JSON artifact makes it instant and re-runnable).

### mypackage/run.py -- tyro subconfig, loguru, tqdm, jaxtyping

```python
from dataclasses import dataclass, field
from pathlib import Path
import json

import torch
import tyro
from jaxtyping import Float
from loguru import logger
from torch import Tensor
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


@dataclass
class ModelCfg:
    # tiny RANDOM model is the smoke default: real architecture, garbage
    # weights, loads in seconds on CPU. Real model comes in via CLI.
    name: str = "wassname/qwen3-5lyr-tiny-random"
    layer: int = 2


@dataclass
class Cfg:
    model: ModelCfg = field(default_factory=ModelCfg)
    out: Path = Path("outputs/dev")
    n_pairs: int = 32
    fast_dev_run: bool = False  # tiny everything; must exercise the real code path


def layer_energy(hs: Float[Tensor, "b s d"]) -> Float[Tensor, "b"]:
    # jaxtyping on function boundaries; BEARTYPE=1 makes shape bugs loud in
    # smoke. Real-world example: steering-lite variants/super_sspace.py
    # (dict[int, Float[Tensor, "n d_model"]] params, annotated hook signatures).
    return hs.float().square().mean(dim=(1, 2))


def main(cfg: Cfg) -> None:
    cfg.out.mkdir(parents=True, exist_ok=True)
    logger.add(cfg.out / "run.md")  # console AND file; no tee needed
    logger.info(f"cfg: {cfg}")

    tokenizer = AutoTokenizer.from_pretrained(cfg.model.name)
    model = AutoModelForCausalLM.from_pretrained(cfg.model.name)
    rows = []
    for i in tqdm(range(2 if cfg.fast_dev_run else cfg.n_pairs)):
        ids = tokenizer("probe", return_tensors="pt")
        hs = model(**ids, output_hidden_states=True).hidden_states[cfg.model.layer]
        rows.append({"i": i, "energy": layer_energy(hs).item()})

    artifact = cfg.out / "metrics.json"
    artifact.write_text(json.dumps({"cfg": str(cfg), "rows": rows}, indent=2))
    logger.info(
        f"SHOULD: energy is finite and stable across i; NaN or drift means a "
        f"hook or dtype bug. out: {artifact}"
    )


if __name__ == "__main__":
    main(tyro.cli(Cfg))
```

Nested override from the CLI: `--model.name Qwen/Qwen3-4B --model.layer 18`.
simple-parsing works the same way if preferred:
`from simple_parsing import parse; cfg = parse(Cfg)`.

### justfile

```just
set shell := ["bash", "-cu"]

# real pipeline, tiny random model, beartype on: catches runtime/shape/hook
# bugs in seconds. Garbage metrics are expected.
smoke *ARGS:
	BEARTYPE=1 uv run python -m mypackage.run --fast-dev-run {{ ARGS }}

# queue the real run on the shared GPU (label states why + what resolves it)
run out label *ARGS:
	pueue add -l "{{ label }}" -w "$PWD" -- \
	  uv run python -m mypackage.run --out {{ out }} {{ ARGS }}

# lint notebooks; export one headless with outputs as judgeable HTML
nb-check nb="nbs":
	uv run marimo check {{ nb }}

nb-html nb out="outputs/nb_html":
	uv run marimo check {{ nb }}
	mkdir -p {{ out }}
	uv run marimo export html {{ nb }} -o {{ out }}/$(basename {{ nb }} .py).html
```

### nbs/report.py -- marimo reads the artifact, takes no CLI args

```python
import marimo

app = marimo.App()


@app.cell
def _():
    import json
    from pathlib import Path

    import marimo as mo
    import polars as pl

    # repo-relative via notebook_dir; robust to marimo's launch cwd
    artifact = Path(mo.notebook_dir()).parent / "outputs/dev/metrics.json"
    df = pl.DataFrame(json.loads(artifact.read_text())["rows"])
    mo.ui.table(df.to_dicts(), selection=None)
    return


if __name__ == "__main__":
    app.run()
```

### The loop

```bash
just smoke 2>&1 | tee /tmp/claude-1000/smoke_run.log | tail -30   # must pass first
just run outputs/exp1 "why: test X; resolve: outputs/exp1/metrics.json shows Y" --model.name Qwen/Qwen3-4B
pqf <id>                           # run_in_background and wake on exit, with the job's exit code
just nb-html nbs/report.py         # or pueue this too: the HTML is the run artifact
```

UAT is the link to the HTML or JSON plus the SHOULD line in the log, never
"it ran". Export exits non-zero if a notebook cell errored (it may still write
the HTML with the error rendered), so check the exit code as well as the link.
