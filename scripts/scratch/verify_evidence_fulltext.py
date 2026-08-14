"""Check a cached evidence file is the full source, not a summary of it.

Refetches the URL in the file header and measures what fraction of the source's
5-word n-grams (shingles, Broder 1997) survive in the cache. Reproducing 5 words
in a row is what copying does and what summarising does not: a verbatim copy
scores ~1.0, a rewrite collapses toward 0, however confident its author was.

n=5 measured, not guessed. Sweeping n on a known-good file against synthetic
copy-with-noise / paraphrase / summary variants: a summary scores 0% for any
n>=3 and an unrelated paper on the same topic scores 0.05% at n=5, so shared
vocabulary is not the risk. Larger n separates paraphrase better but punishes
honest extraction noise (a copy missing 1 word in 40 scores 88% at n=5, 70% at
n=12), which would trip the 0.8 threshold on real PDF text.

    uv run scripts/scratch/verify_evidence_fulltext.py docs/evidence/*.md
"""

import re
import subprocess
import sys
from pathlib import Path

SHINGLE = 5
URL_RE = re.compile(r"https?://[^\s)>\"']+")


def norm(text: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split()


def shingles(words: list[str], n: int = SHINGLE) -> set[tuple[str, ...]]:
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def source_url(head: str) -> str | None:
    for line in head.splitlines():
        if re.match(r"(?i)\s*[-*]?\s*\**(source|url|urls)\**\s*:", line):
            m = URL_RE.search(line)
            if m:
                return m.group(0).rstrip(".,")
    m = URL_RE.search(head)
    return m.group(0).rstrip(".,") if m else None


# landing pages that serve an abstract or a citation stub, never the full text
STUB_HOSTS = re.compile(
    r"(?i)arxiv\.org/abs/|semanticscholar\.org|doi\.org/|dx\.doi\.org|researchgate\.net"
    r"|paperswithcode\.com|scholar\.google|ieeexplore\.ieee\.org/document/|dl\.acm\.org/doi/(?!pdf)"
    r"|link\.springer\.com/(article|chapter)/|sciencedirect\.com/science/article/(?!pii/[^/]+/pdf)"
    r"|openreview\.net/forum|papers\.nips\.cc/paper[^/]*/hash/|proceedings\.mlr\.press/[^/]+/?$"
)


def curl_raw(url: str) -> str:
    return subprocess.run(
        ["curl", "-sL", "--max-time", "180", url], capture_output=True, text=True, check=True
    ).stdout


def curl(url: str) -> str:
    return subprocess.run(
        ["curl", "-s", "--max-time", "180", f"https://r.jina.ai/{url}"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def fetch(url: str) -> str:
    # sites that serve a JS shell to a scraper need their own API
    m = re.search(r"(?:lesswrong\.com|alignmentforum\.org|forum\.effectivealtruism\.org)/(?:posts|s/[^/]+/p)/([^/?#]+)", url)
    if m:  # graphql sits behind a bot check, the markdown api does not
        return subprocess.run(
            ["curl", "-s", "--max-time", "120", "-H", "Accept: text/markdown",
             f"https://www.lesswrong.com/api/post/{m.group(1)}?compact=1"],
            capture_output=True, text=True, check=True,
        ).stdout
    m = re.search(r"huggingface\.co/blog/([\w-]+)", url)  # jina gets 403 here
    if m:
        return curl_raw(f"https://raw.githubusercontent.com/huggingface/blog/main/{m.group(1)}.md")
    # an /abs/ page is the abstract, we want the paper
    url = re.sub(r"arxiv\.org/abs/", "arxiv.org/pdf/", url)
    if re.fullmatch(r"https?://github\.com/[^/]+/[^/#?]+/?", url):  # bare repo -> its README
        slug = url.rstrip("/").split("github.com/")[1]
        for branch in ("main", "master"):
            out = curl(f"https://raw.githubusercontent.com/{slug}/{branch}/README.md")
            if len(out.split()) > 100:
                return out
        return out
    url = url.replace("github.com/", "raw.githubusercontent.com/").replace("/blob/", "/")
    if url.lower().endswith(".pdf"):
        pdf = Path("/tmp/_verify.pdf")
        subprocess.run(["curl", "-sL", "--max-time", "180", url, "-o", str(pdf)], check=True)
        # no -layout: it clips multi-column text
        return subprocess.run(
            ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
        ).stdout
    out = subprocess.run(
        ["curl", "-s", "--max-time", "180", f"https://r.jina.ai/{url}"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return out


def main(paths: list[str]) -> int:
    bad = 0
    print(f"{'file':<58} {'cache_w':>8} {'src_w':>8} {'covered':>8}  verdict")
    for p in paths:
        path = Path(p)
        text = path.read_text(encoding="utf-8", errors="replace")
        url = source_url("\n".join(text.splitlines()[:12]))
        if not url:
            print(f"{path.name:<58} {'':>8} {'':>8} {'':>8}  NO_URL_IN_HEADER")
            bad += 1
            continue
        if STUB_HOSTS.search(url):
            # cite the document, not a landing page: an /abs/ or Semantic Scholar
            # link means nobody can check the quote without a second lookup
            print(f"{path.name:<58} {'':>8} {'':>8} {'':>8}  STUB_LINK {url}")
            bad += 1
        src = fetch(url)
        sw, cw = norm(src), norm(text)
        if len(sw) < SHINGLE * 3:
            print(f"{path.name:<58} {len(cw):>8} {len(sw):>8} {'':>8}  FETCH_EMPTY {url}")
            continue
        s_src, s_cache = shingles(sw), shingles(cw)
        cov = len(s_src & s_cache) / len(s_src)
        ratio = len(cw) / len(sw)
        # high coverage of a stub proves nothing: an abstract, a landing page or a
        # paywall snippet is a subset of any honest cache, and of a summary too
        if cov > 0.8 and ratio > 1.6:
            verdict = f"SRC_STUB x{ratio:.1f}, cannot verify"
        elif cov > 0.8 and ratio < 0.7:
            verdict = "CACHE_TRUNCATED"
        elif cov > 0.8:
            verdict = "ok"
        elif cov > 0.3:
            verdict = "PARTIAL"
        else:
            verdict = "SUMMARY?"
        bad += verdict != "ok"
        print(f"{path.name:<58} {len(cw):>8} {len(sw):>8} {cov:>7.1%}  {verdict}")
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
