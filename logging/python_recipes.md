# Python recipes for the run log

<!-- Moved from the token-efficient-logging skill by PI/Claude, 2026-11-17; wassname's practices, Codex's and PI/OpenAI's wording. Parts that repeated SKILL.md were left out. -->

Read this when you write the logging code itself: the resolved config table, stage headings, the progress bar, failure handling, or a table that streams one row per step.

## Resolved config

Print the command and the config at the values that were used, after the file sink is attached. A dataclass dump is not enough when a field such as `layer=None` or a model name is resolved later. Use a `setting | value` table for flat values and a fenced `yaml` block for nested config. Show each field once.

```python
import dataclasses
import shlex
import sys
from tabulate import tabulate

values = {**dataclasses.asdict(cfg), "resolved_layer": cfg.resolved_layer(), "resolved_model": cfg.resolved_model()}
table = tabulate(sorted(values.items()), headers=["setting", "value"], tablefmt="pipe", disable_numparse=True)
logger.info(f"\n\n## Command\n\n```text\n{shlex.join(sys.argv)}\n```")
logger.info(f"\n\n## Resolved config\n\n{table}\n")
```

## Stage headings

Each sub-stage heading repeats the path from its parent, so a cut or grepped log still says where it is, and `grep '^#' run.md` prints the outline. Close a top-level stage before you open the next, with its elapsed time and, for GPU stages, its peak memory.

```python
logger.info("\n\n# train [mean] seed=42, steps=500")
logger.info("\n\n## train -> calibrating")
logger.info("\n\n## train -> calibrating -> demo gen +ve (C=1.4)")
logger.info("\n\n# train done: 12.3s, 41.2GB peak")
logger.info("\n\n# eval [mean] seed=42")
```

The two leading newlines make the blank lines between logger messages. Check the file that was written, because some viewers remove blank lines.

## Compose a section

Write one Markdown section as one f-string. Compute the variable parts first, then put them in. Do not make one call per blank line.

```python
table = tabulate(rows, headers=headers, tablefmt="pipe", disable_numparse=True)
logger.info(f"""\\
## evaluation

{table}
""")
```

Use `tabulate` when the project already depends on it. Do not add a template engine to print one section.

## Progress bar

Set both `tqdm` intervals: when only `mininterval` is raised, the default `maxinterval` can still redraw the line often.

```python
progress = tqdm(range(n_steps), desc=f"train {variant}", mininterval=120, maxinterval=120, ascii=True, file=sys.stderr)
for step in progress:
    loss, grad_norm = train_step(step)
    progress.set_postfix(loss=f"{loss:.3g}", grad=f"{grad_norm:.3g}", refresh=False)
```

When you run a command as an agent and do not need live progress, set `TQDM_DISABLE=1`.

## Failure

Attach the logger before anything that can fail, so that a startup error reaches `run.md`. On failure, write the traceback in a fenced block, then a result block that names the failed stage, then the path of `run.md`, and exit with a nonzero status. Do not write a second report over the live log.

## A table that streams one row per step

Use this in place of `tqdm` only when every row is a result you will read. Print a legend once, build the legend, header and rows from one column list, and repeat the header about every 50 rows so that a tail of the log can still be read.

```python
COLUMNS = [
    ("step", 4, "d", "training step"),
    ("rew↑", 6, "+.2f", "mean reward; higher is better"),
    ("hack↓", 7, "frac", "rollouts flagged as reward hacking; lower is better"),
    ("loss", 7, "+.2f", "mean training loss"),
    ("gn", 7, ".1e", "gradient norm before clipping"),
]

def cell(value, spec):
    return f"{value[0]}/{value[1]}" if spec == "frac" else format(value, spec)

def header():
    return "  ".join(f"{name:>{width}}" for name, width, _, _ in COLUMNS)

def row(metrics):
    return "  ".join(f"{cell(metrics[name], spec):>{width}}" for name, width, spec, _ in COLUMNS)

logger.info("\ncolumns:\n" + "\n".join(f"    {name:>8} = {text}" for name, _, _, text in COLUMNS))
logger.info(f"\n{header()}")
for step, metrics in enumerate(training_loop):
    if step and step % 50 == 0:
        logger.info(f"\n{header()}")
    logger.info(row(metrics))
```

Keep the raw values in the metrics mapping, so that the same rows can build the result table at the end. A column that is used only for analysis afterwards, such as detailed timing, does not need to stream.
