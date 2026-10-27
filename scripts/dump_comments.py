# Dump every comment >40 chars or multi-line block (and docstrings) from each vendored repo, with file:line, for reading.
# Usage: uv run --no-project python dump_comments.py <vendor_dir> <out_dir>  -> <out_dir>/<repo>.md per subdirectory
# See references/engineering_lit_review.md. -- PI/Claude (opus-5-5), 2026-10-27
import ast, io, json, re, sys, tokenize
from pathlib import Path

VENDOR, OUT = Path(sys.argv[1]), Path(sys.argv[2])
HASH = {".sh", ".yaml", ".yml", ".toml", ".cfg", ".r", ".jl", ".mk", ""}
SLASH = {".js", ".ts", ".tsx", ".rs", ".go", ".c", ".cpp", ".h", ".java"}
MIN = 40


def blocks_from_lines(lines, marker):
    """Group consecutive comment lines into blocks: (start_line, text)."""
    out, cur, start = [], [], None
    for i, line in enumerate(lines, 1):
        m = re.search(r"(?:^|\s)" + re.escape(marker) + r"\s?(.*)$", line) if marker in line else None
        if m and not line.lstrip().startswith(("#!",)):
            if not cur:
                start = i
            cur.append(m.group(1).rstrip())
        elif cur:
            out.append((start, cur)); cur = []
    if cur:
        out.append((start, cur))
    return out


def py_blocks(src):
    lines = src.splitlines()
    out = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return blocks_from_lines(lines, "#")
    cur, start, last = [], None, -2
    for t in toks:
        if t.type == tokenize.COMMENT:
            ln = t.start[0]
            if cur and ln != last + 1:
                out.append((start, cur)); cur = []
            if not cur:
                start = ln
            cur.append(t.string.lstrip("#").strip()); last = ln
    if cur:
        out.append((start, cur))
    try:
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                d = ast.get_docstring(node, clean=True)
                if d:
                    out.append((getattr(node, "lineno", 1), ["[docstring] " + d]))
    except (SyntaxError, ValueError):
        pass
    return sorted(out)


def ipynb_src(path):
    nb = json.loads(path.read_text(errors="replace"))
    return "\n".join("".join(c.get("source", [])) for c in nb.get("cells", []) if c.get("cell_type") == "code")


def keep(block):
    text = "\n".join(block)
    return len(block) > 1 or len(text) > MIN


for repo in sorted(p for p in VENDOR.iterdir() if p.is_dir()):
    rows, nfiles = [], 0
    for f in sorted(repo.rglob("*")):
        if not f.is_file() or ".git" in f.parts or f.stat().st_size > 2_000_000:
            continue
        ext = f.suffix.lower()
        try:
            if ext == ".py":
                bl = py_blocks(f.read_text(errors="replace"))
            elif ext == ".ipynb":
                bl = py_blocks(ipynb_src(f))
            elif ext in SLASH:
                bl = blocks_from_lines(f.read_text(errors="replace").splitlines(), "//")
            elif ext in HASH and (ext or f.name in {"Makefile", "Dockerfile", "justfile"}):
                bl = blocks_from_lines(f.read_text(errors="replace").splitlines(), "#")
            else:
                continue
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        bl = [b for b in bl if keep(b[1])]
        if bl:
            nfiles += 1
            rel = f.relative_to(repo)
            rows += [f"\n### {rel}:{ln}\n" + "\n".join(b) for ln, b in bl]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{repo.name}.md").write_text(f"# Comments >{MIN} chars or multi-line, {repo.name} ({nfiles} files, {len(rows)} blocks)\n" + "\n".join(rows))
    print(f"{repo.name:28s} files={nfiles:4d} blocks={len(rows):5d} bytes={(OUT / f'{repo.name}.md').stat().st_size:>9,}")
