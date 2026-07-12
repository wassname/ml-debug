#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FOOTNOTE_RE = re.compile(r"\[\^([^\]]+)\]")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.MULTILINE)
FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")
YAML_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):", re.MULTILINE)
LINE_ANCHOR_RE = re.compile(r"\bL(\d+)(?:-(\d+))?")


def is_frozen_evidence(path: Path, root: Path) -> bool:
    relative = "/" + path.relative_to(root).as_posix() + "/"
    return "/docs/evidence/" in relative


def authored_markdown(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.md"))
        if ".git" not in path.parts and not is_frozen_evidence(path, root)
    ]


def prose_lines(path: Path, errors: list[str]) -> list[tuple[int, str]]:
    lines = path.read_text(errors="replace").splitlines()
    prose: list[tuple[int, str]] = []
    opened: tuple[str, int, int] | None = None
    for line_number, line in enumerate(lines, 1):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(2)
            remainder = match.group(3)
            if opened is None:
                if marker[0] == "`" and "`" in remainder:
                    errors.append(f"{path}:{line_number}: backtick fence info contains a backtick")
                opened = (marker[0], len(marker), line_number)
            elif marker[0] == opened[0] and len(marker) >= opened[1]:
                if remainder.strip():
                    errors.append(f"{path}:{line_number}: closing fence has trailing text")
                opened = None
            continue
        if opened is None:
            prose.append((line_number, line))
    if opened is not None:
        errors.append(f"{path}: unclosed {opened[0] * opened[1]} fence from line {opened[2]}")
    return prose


def local_target(raw_target: str, source: Path) -> tuple[Path, str] | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    path_text, _, fragment = target.partition("#")
    path_text = unquote(path_text)
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", path_text):
        return None
    path = source if not path_text else (source.parent / path_text).resolve()
    return path, unquote(fragment)


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(errors="replace").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = re.sub(r"<[^>]+>", "", match.group(1))
        explicit = re.search(r"\{#([A-Za-z0-9_.:-]+)\}\s*$", heading)
        if explicit:
            anchors.add(explicit.group(1))
            heading = heading[: explicit.start()].rstrip()
        slug = re.sub(r"[^\w\s-]", "", heading.lower())
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        duplicate = counts.get(slug, 0)
        counts[slug] = duplicate + 1
        anchors.add(slug if duplicate == 0 else f"{slug}-{duplicate}")
    return anchors


def check_frontmatter(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("SKILL.md")):
        if ".git" in path.parts:
            continue
        lines = path.read_text(errors="replace").splitlines()
        if not lines or lines[0] != "---":
            errors.append(f"{path}: missing YAML frontmatter")
            continue
        try:
            closing = lines.index("---", 1)
        except ValueError:
            errors.append(f"{path}: unclosed YAML frontmatter")
            continue
        keys = YAML_KEY_RE.findall("\n".join(lines[1:closing]))
        if sorted(keys) != ["description", "name"]:
            errors.append(f"{path}: frontmatter keys must be name and description, got {keys}")
        values = {}
        for line in lines[1:closing]:
            if ":" not in line:
                errors.append(f"{path}: invalid frontmatter line {line!r}")
                continue
            key, raw_value = line.split(":", 1)
            value = raw_value.strip()
            if value[:1] in {"\"", "'"} and (len(value) < 2 or value[-1] != value[0]):
                errors.append(f"{path}: unterminated quoted frontmatter value for {key}")
            values[key] = value.strip("'\"")
        if not values.get("name") or not values.get("description"):
            errors.append(f"{path}: name and description must be nonempty")
        elif not re.fullmatch(r"[a-z0-9-]+", values["name"]):
            errors.append(f"{path}: invalid skill name {values['name']!r}")


def audit(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    check_frontmatter(root, errors)
    for path in authored_markdown(root):
        prose = prose_lines(path, errors)
        prose_text = "\n".join(line for _, line in prose)
        definitions = set(FOOTNOTE_DEF_RE.findall(prose_text))
        uses = set(FOOTNOTE_RE.findall(prose_text))
        for missing in sorted(uses - definitions):
            errors.append(f"{path}: missing footnote definition [^{missing}]")
        for line_number, line in prose:
            if line.count("[") != line.count("]"):
                errors.append(f"{path}:{line_number}: unbalanced square brackets")
            for match in LINK_RE.finditer(line):
                resolved = local_target(match.group(1), path)
                if resolved is None:
                    continue
                target, fragment = resolved
                if not target.exists():
                    errors.append(f"{path}:{line_number}: missing local link {match.group(1)!r}")
                    continue
                if fragment and target.is_file() and target.suffix.lower() == ".md":
                    if fragment not in markdown_anchors(target):
                        errors.append(f"{path}:{line_number}: missing Markdown fragment #{fragment}")
                relative = "/" + target.as_posix() + "/"
                if "/docs/evidence/" not in relative or not target.is_file():
                    continue
                line_count = len(target.read_text(errors="replace").splitlines())
                for anchor in LINE_ANCHOR_RE.finditer(line[match.end():]):
                    start = int(anchor.group(1))
                    end = int(anchor.group(2) or anchor.group(1))
                    if start < 1 or end < start or end > line_count:
                        errors.append(
                            f"{path}:{line_number}: invalid evidence anchor L{start}-{end} for "
                            f"{target} ({line_count} lines)"
                        )
    return errors


def write_fixture(root: Path) -> None:
    (root / "docs/evidence").mkdir(parents=True)
    (root / "docs/evidence/source.md").write_text("one\ntwo\nthree\n")
    (root / "SKILL.md").write_text(
        "---\nname: fixture\ndescription: fixture skill\n---\n\n# Fixture\n"
    )
    (root / "guide.md").write_text(
        "# Fixture section\n"
        "[skill](SKILL.md)\n"
        "[section](guide.md#fixture-section)\n"
        "![image](docs/evidence/source.md)\n"
        "[cache](docs/evidence/source.md): L2-3\n"
        "Claim.[^source]\n\n"
        "[^source]: Evidence.\n"
    )


def self_test() -> None:
    mutations = [
        (
            "missing local link",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text() + "\n[broken](missing.md)\n"
            ),
        ),
        (
            "missing local link",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text().replace(
                    "docs/evidence/source.md)", "missing-image.png)", 1
                )
            ),
        ),
        (
            "unclosed",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text() + "\n```python\n"
            ),
        ),
        (
            "backtick fence info",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text() + "\n```py`thon\n```\n"
            ),
        ),
        (
            "missing footnote",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text() + "\nMissing.[^absent]\n"
            ),
        ),
        (
            "frontmatter keys",
            lambda root: (root / "SKILL.md").write_text(
                (root / "SKILL.md").read_text().replace("name:", "title:")
            ),
        ),
        (
            "unterminated quoted frontmatter",
            lambda root: (root / "SKILL.md").write_text(
                (root / "SKILL.md").read_text().replace(
                    "description: fixture skill", 'description: "fixture skill'
                )
            ),
        ),
        (
            "invalid evidence anchor",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text().replace("L2-3", "L0")
            ),
        ),
        (
            "invalid evidence anchor",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text().replace("L2-3", "L3-2")
            ),
        ),
        (
            "missing Markdown fragment",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text().replace(
                    "#fixture-section", "#missing-section"
                )
            ),
        ),
        (
            "unbalanced square brackets",
            lambda root: (root / "guide.md").write_text(
                (root / "guide.md").read_text() + "\n**Broken** [label\n"
            ),
        ),
    ]
    with tempfile.TemporaryDirectory() as directory:
        clean = Path(directory) / "clean"
        write_fixture(clean)
        assert not audit(clean), audit(clean)
    for expected, mutate in mutations:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            mutate(root)
            errors = audit(root)
            assert any(expected in error for error in errors), (expected, errors)
    print(f"audit self-test: PASS ({len(mutations)} injected defects rejected)")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = audit(args.root)
    if errors:
        print("\n".join(errors))
        return 1
    if args.self_test:
        self_test()
    print(
        f"audit: PASS ({len(authored_markdown(args.root.resolve()))} authored Markdown files, "
        f"{len(list(args.root.resolve().rglob('SKILL.md')))} skills)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
