# wassname's ML Debugging Folklore

In an attempt to upskill the machine learning debugging on AI coding assistants (and humans), I've collected high quality sources on how to debug machine learning projects, focusing on the mindset and the "taste". When I started ML I went searching for discussions on best practices, and started a few discussions of my own and they helped me a lot, over the years I've collected good ones. I hope they can help others, as well as help in auto research setups. This intro is human written, and the below is AI written with human guidance.

## Use as a Claude skill

```
/skills add https://github.com/wassname/ml_debug
```

Or paste `SKILL.md` into your system prompt / context when debugging.

## What's here

- **[SKILL.md](SKILL.md)** -- the main artifact. Load into an LLM agent's context as a debugging skill. A short calibration note, then the folklore itself: verbatim sourced quotes from practitioners, general lessons first, modern transformers and LLM fine-tuning in their own section.

- **[PLAYBOOK.md](PLAYBOOK.md)** -- the synthesized long-form: mental models, practitioner priors, step catalogs, symptom tables, the agent debugging loop, triage, and anti-patterns. Menus of hypotheses distilled from the same sources, not quotes. Deeper one-off tricks (loss-surface analysis, stuck-metric diagnosis, sweep reliability) live in [refs/](refs/).

- **[docs/evidence/](docs/evidence/)** -- frozen local copies of source material (blog posts, talks, papers, reddit threads). Claims in SKILL.md link back to exact quotes here.

## Does it help?

Measured on [ml-bench](https://github.com/wassname/ml-bench): 12 hard machine learning research
problems from my own work, none of them in any training set, each answer graded against my own
answer by a panel of five LLM judges. A score of 1.00 means the model matched me. The test gives the
model this SKILL.md and nothing else, so the only change is the document.

No measurable gain, from three answers per question in each arm:

| deepseek-v4-flash-0731, 12 questions | bare | with SKILL.md |
| --- | --- | --- |
| mean score | +0.643 | +0.667 |
| the three runs | +0.608, +0.648, +0.674 | +0.746, +0.641, +0.614 |

The difference is +0.023 with a standard error of 0.044, so it is not distinguishable from zero.
Pairing by question rather than by run gives the same +0.023 with a standard error of 0.031, t of
0.76. The runs themselves scatter by more than the difference between the two columns.

An earlier version of this section reported +0.135, or 59% of the distance to gpt-5.6-sol. That was
one run of each arm, and it happens to be the first run in each column above. It did not survive the
other two.

Two other readings. With SKILL.md the model writes 31% more text for the same score, so any
verbosity bias in the judges makes the true effect smaller than +0.023, not larger. And only 1 answer
in 36 uses the document's own vocabulary, so the document is in the context without changing much of
what the model writes. The header does tell it not to quote the document back.

Caveats: one model, three answers per question, one judge panel, at bench version v96. The result is
that this document did not help this model on these questions. It is not evidence about a stronger
model, a longer task, or an agent that can run code.

## Citation

```bibtex
@misc{wassname2026mldebug,
  title = {ML Debugging Folklore: A Practitioner Debugging Skill for LLM Agents},
  author = {Michael J. Clark},
  year = {2026},
  url = {https://github.com/wassname/ml_debug/}
}
```
