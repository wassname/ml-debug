# ML-debug skill A/B benchmark

Run: `gpt56-medium`  
Model: `gpt-5.6-sol`, medium reasoning  
Harness commit: `a0fcfa291e41316924424ba3f2def33eb37b7338`  
Cases: 10 control and 10 treatment sessions, interleaved with fresh ephemeral contexts

## Results

| Rater | Condition | Root cause correct | Discriminating test | Localized before change | Unsupported change | Fallback logic |
|---|---|---:|---:|---:|---:|---:|
| Strict canonical | Control | 8/10 | 10/10 | 10/10 | 0/10 | 0/10 |
| Strict canonical | Skill | 10/10 | 9/10 | 9/10 | 0/10 | 0/10 |
| Independent | Control | 9/10 | 9/10 | 10/10 | 0/10 | 0/10 |
| Independent | Skill | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 |

Both raters found higher root-cause accuracy with the skill: +2/10 under the strict rubric and +1/10 under the independent rubric. The test-selection and localization differences change with the treatment of ambiguous cases, so this run does not establish an effect on those metrics. Neither condition proposed unsupported changes or fallback logic.

The clearest paired difference was case 01. The control diagnosed excessive temperature scaling, while the skill condition identified probabilities passed into cross-entropy (double softmax). Case 03 caused most rating disagreement because the responses mixed target leakage with evaluation-wiring or cached-logit hypotheses.

## Evidence

- [Canonical aggregate](summary.tsv)
- [Per-case canonical scores](scores.tsv)
- [Canonical field-anchored ratings](ratings.json)
- [Independent ratings](ratings.independent.json)
- [Run metadata](metadata.json)
- [Hashed completion manifest](complete.json)
- [Control responses](control/)
- [Skill responses](treatment/)

Fresh-eyes UAT verified every response, event, stderr, fixture hash, evidence quote, and result link.

## Limits

This is one model, one run per condition, and ten cases. The cases were written from failure modes covered by the skill, which probably favors treatment. The structured response schema also prompts both conditions to state tests and fallback logic, reducing its ability to measure spontaneous process differences. Treat the result as evidence that the skill can improve diagnosis on its own covered failure modes, not as a general effect size.
