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

One measurement so far, on [ml-bench](https://github.com/wassname/ml-bench): 12 hard machine
learning research problems from my own work, none of them in any training set, each answer graded
against my own answer by an LLM judge. A score of 1.00 means the model matched me. The test gives
the model this SKILL.md and nothing else, so the only change is the document.

| deepseek-v4-flash-0731 | bare | with SKILL.md | change |
| --- | --- | --- | --- |
| the 11 questions both runs answered | +0.563 | +0.698 | +0.135, or +24% |
| same, minus the one field that can score above 1.00 | +0.555 | +0.672 | +0.117 |
| 9 questions, dropping the two this skill is the source of | +0.501 | +0.689 | +0.188 |

For scale, changing the judge moves a score by 0.04 on average, so the effect is about three times
the noise. Two questions cite this repo as their source, and dropping them raises the effect rather
than lowering it, so the model is not just reading the answer.

Only deepseek-v4-flash-0731 reads the document. The frontier models below answer the same questions
with no document, as they normally do, and the document closes most of the distance to them:

| frontier model, no document | questions in common | flash, no document | flash, with SKILL.md | the frontier model | distance closed |
| --- | --- | --- | --- | --- | --- |
| gpt-5.6-sol | 9 | +0.540 | +0.678 | +0.774 | 59% |
| glm-5.2, the top of the table | 11 | +0.563 | +0.698 | +0.694 | 103% |

deepseek-v4-flash-0731 costs $0.036 for all 12 questions and gpt-5.6-sol costs $0.70, so this is a
20x cheaper model reading a document instead of thinking harder.

Caveats: one model, one run, one judge, at bench version v94. The gain is uneven, from +0.81 on one
question to -0.17 on another. Replication on other models is in progress.

## Citation

```bibtex
@misc{wassname2026mldebug,
  title = {ML Debugging Folklore: A Practitioner Debugging Skill for LLM Agents},
  author = {Michael J. Clark},
  year = {2026},
  url = {https://github.com/wassname/ml_debug/}
}
```
