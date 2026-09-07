from __future__ import annotations

import argparse
import re
from pathlib import Path

SOURCES = (
    Path("README.md"),
    Path("SKILL.md"),
    Path("rl/SKILL.md"),
    Path("pinn/SKILL.md"),
    Path("references/llm_judges.md"),
    Path("references/llm_judge_litreview.md"),
)

METADATA = re.compile(r"^(Source|Evidence|Credence|Code|Implication):")


def normalized(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def quotes(path: Path) -> list[str]:
    records: list[str] = []
    lines: list[str] = []

    def flush() -> None:
        if lines:
            text = " ".join(lines)
            records.append(f"{text} -- curated in {path}")
            lines.clear()

    for line in path.read_text().splitlines():
        if not line.startswith("> "):
            flush()
            continue
        text = line[2:].strip()
        if METADATA.match(text):
            flush()
            continue
        lines.append(text)
    flush()
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    seen: set[str] = set()
    records: list[str] = []
    for path in SOURCES:
        for record in quotes(path):
            key = normalized(record.rsplit(" -- curated in ", 1)[0])
            if key not in seen:
                seen.add(key)
                records.append(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(records) + "\n")
    print(f"{len(records)} curated quote blocks")


if __name__ == "__main__":
    main()
