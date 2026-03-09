# ML Debugging Folklore

Practitioner knowledge for debugging ML systems, curated and synthesized by [wassname](https://github.com/wassname). Opinionated by source selection -- I picked sources I trust (Schulman, Goodfellow, CS231n, ...) and had an LLM extract the most relevant information for debugging ML systems.

## Use as a Claude skill

```
/skills add https://github.com/wassname/ml_debug
```

Or paste `SKILL.md` into your system prompt / context when debugging.

## What's here

- **[SKILL.md](SKILL.md)** -- the main artifact. Load into an LLM agent's context as a debugging skill. Parts 1-5 are reference knowledge; Part 6 is a runnable triage protocol (grep patterns, diagnostic snippets, decision tree); Part 7 is debugging mental models and practitioner priors.

- **[docs/evidence/](docs/evidence/)** -- frozen local copies of source material (blog posts, talks, papers, reddit threads). Claims in SKILL.md link back to exact quotes here.
