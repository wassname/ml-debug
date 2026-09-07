# Sweeps: learning what to try, and comparing results

Appendix to the [ML Debugging skill](../SKILL.md). Choose the experiment for the
question and iteration cost. Learning which direction to try next needs less
certainty than claiming one method reliably beats another.

## Expensive exploratory runs

For cheap runs, changing one thing at a time often makes diagnosis easier. For
hours-long runs, batch changes when they have distinguishable predicted effects.
Record what each should change in the logs before running, including possible
interactions. Update the Bayesian mental model from trajectories and demos as well
as final metrics; keep unresolved explanations rather than forcing attribution.

For example, a loader change may predict less time waiting for data, while a
regularisation change predicts a different train–validation gap. Seeing both
supports those explanations, but does not prove the changes acted independently.
If both predict only a better final score, the log may not separate them. A later
isolated comparison is useful when that uncertainty changes what to do next.

## Comparing configurations or methods

Keep the evaluation data, metric definition and relevant budget comparable.
Pair runs where meaningful: reuse seeds and inputs, but check that the changed
implementation has not changed what those seeds control. Pairing can reduce
noise; it does not guarantee its cancellation.

Inspect paired differences in the original metric units, their spread, and failed
runs. A comparison of two bundles estimates the bundle difference, not each
component's contribution. Distinguish exploratory selection from confirmation on
seeds or data not used to select the winner.

Within-seed z-scores can describe response shapes, but erase effect magnitude.
With just two settings, they can give the winner the same normalized value on
every seed despite very different raw gains. Do not use that artificial lack of
variance as evidence of reliability.

Describe uncertainty in the raw differences, with a method suited to the sample
size and dependence. There is no universal “t > 2 with four seeds” guarantee.
A noisy estimate leaves the effect uncertain; it does not establish either “no
effect” or “a lucky seed.” One run can inform the next experiment without
establishing reliability across seeds.

Keep crashed or divergent runs visible and investigate them. Do not silently
exclude them from the comparison.

<!-- Pi: revised from wassname's exploratory-run direction and the reviewed
within-seed normalization counterexample. Source background: README.md sections
“Seed variance”, “Changing anything changes everything”, and “Exploration over
exploitation”. -->
