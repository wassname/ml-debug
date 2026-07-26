# Time-series evaluation and problem properties

Appendix to the [ML Debugging skill](../SKILL.md).

Use this for two separate questions:

1. Does the evaluation reproduce deployment across time?
2. What properties make the forecasting problem intrinsically easier or harder?

## Temporal evaluation should emulate deployment

> Holdout testing should emulate deployment. When you deploy, you deploy into the unknown. Hold out a future month, because people do not like it when testing is hard, but deploying to the real world is hard and we want to test it faithfully.
>
> - wassname, lightly edited for spelling

"A future month" is an example. Use the forecast horizon, prediction frequency,
label delay, and retraining cadence of the real deployment. A model retrained
daily for next-day forecasts and a frozen model used for the next quarter are
different systems and need different backtests.

Hyndman and Athanasopoulos give the basic information boundary:

> It is important to evaluate forecast accuracy using genuine forecasts. Consequently, the size of the residuals is not a reliable indication of how large true forecast errors are likely to be. The accuracy of forecasts can only be determined by considering how well a model performs on new data that were not used when fitting the model.
>
> When choosing models, it is common practice to separate the available data into two portions, **training** and **test** data, where the training data is used to estimate any parameters of a forecasting method and the test data is used to evaluate its accuracy. Because the test data is not used in determining the forecasts, it should provide a reliable indication of how well the model is likely to forecast on new data.[^fpp3-accuracy]

They also make the temporal constraint explicit:

> A more sophisticated version of training/test sets is time series cross-validation. In this procedure, there are a series of test sets, each consisting of a single observation. The corresponding training set consists only of observations that occurred *prior* to the observation that forms the test set. Thus, no future observations can be used in constructing the forecast.
>
> The forecast accuracy is computed by averaging over the test sets. This procedure is sometimes known as "evaluation on a rolling forecasting origin" because the "origin" at which the forecast is based rolls forward in time.
>
> With time series forecasting, one-step forecasts may not be as relevant as multi-step forecasts. In this case, the cross-validation procedure based on a rolling forecasting origin can be modified to allow multi-step errors to be used.[^fpp3-tscv]

Practical rule:

- Keep the final test interval later than every training observation.
- Match the tested forecast horizon to the deployed horizon.
- Refit at each rolling origin only if deployment will refit at that cadence.
- At each origin, construct features using only values that would have arrived by
  prediction time. Event time alone is insufficient when labels or covariates
  arrive late.
- Fit scaling, feature selection, decomposition, imputation, and threshold choices
  inside each training window. Applying them to the full series before splitting
  leaks future information.
- Use rolling origins for model selection or for estimating variation across
  deployment dates. Keep a final later interval untouched if it will be used as
  the final performance claim.

A random split estimates an exchangeable interpolation problem. It does not
estimate future deployment performance when observations are dependent or the
data-generating process changes over time. Cerqueira, Torgo, and Mozetic's
experiments found that blocked cross-validation can work for stationary series,
while nonstationary settings were best estimated by out-of-sample procedures
that preserve temporal order.[^cerqueira]

### Missing values can cross the information boundary

Sort by entity and time before any temporal fill.

- Forward fill can be causal when the last observation really was available at
  prediction time. It can still be wrong if it crosses entities, known reset
  boundaries, or gaps where stale values would not be used in production.
- Backward fill normally leaks a later-timestamp observation into an earlier
  prediction. It is causal only if that value was already available at prediction
  time, such as a published schedule, or if prediction is deliberately delayed
  until the value arrives.
- Bidirectional interpolation or smoothing can be useful for repairing a
  historical record, but it is future leakage in a forecasting backtest unless
  it is recomputed at each origin from past data only.
- Missingness may itself be informative. Preserve a missingness indicator when
  the production system can observe it, and reproduce the same data delay in the
  backtest.

FPP3 explicitly warns that missingness can induce context-dependent bias and
then demonstrates ARIMA interpolation.[^fpp3-missing] That interpolation uses a
different information set from an online forecast. Do not copy a retrospective
data-cleaning recipe into a deployment evaluation without checking causality.

## Properties of time-series forecasting problems

These are overlapping properties, not mutually exclusive classes. A financial
series may have changing relationships, sparse extremes, a short predictability
horizon, and strategic feedback at the same time.

FPP3 provides a compact source-backed frame:

> Some things are easier to forecast than others. The time of the sunrise tomorrow morning can be forecast precisely. On the other hand, tomorrow's lotto numbers cannot be forecast with any accuracy. The predictability of an event or a quantity depends on several factors including:
>
> 1. how well we understand the factors that contribute to it;
> 2. how much data is available;
> 3. how similar the future is to the past;
> 4. whether the forecasts can affect the thing we are trying to forecast.[^fpp3-predictability]

The following properties restate wassname's proposed categories as questions
that can all apply to one problem.

| Property | Easier case | Harder case | Canonical example | Main consequence |
| --- | --- | --- | --- | --- |
| Repeating structure | Stable level, persistent mean reversion, or fixed seasonal effects | Weak, irregular, or changing recurrence | Seasonal electricity demand | Compare against naive and seasonal-naive baselines; test whether the recurrence persists in later periods |
| Relevant data support | Many examples from the regime and horizon being forecast | Short history, a new regime, or rare extremes | Financial crashes and tail risk | Uncertainty is driven by lack of relevant examples; aggregate sample count can be misleading |
| Stability of the evolution law | Level and trend may move, but their dynamics persist | Concept drift, structural breaks, changing seasonality, or changing feature-target relationships | A crisis or policy regime change | Older data may become harmful and performance can decay after deployment |
| Predictability horizon | Errors grow slowly relative to the required horizon | Noise or sensitive dependence makes nearby trajectories diverge rapidly | Weather | Report accuracy by horizon; a useful short-range forecast need not support a long-range claim |
| Availability of future drivers | Required covariates are known at prediction time | Future covariates must themselves be forecast or arrive late | Demand forecasting from a weather forecast | Backtest the full chained system with the same information delays |
| Feedback and adaptation | The forecast does not change the target | Publication or action changes behavior, prices, policy, or competitors' responses | Financial markets | Historical relationships can weaken specifically because the model is deployed |

### Clarifications to the rough easy-to-hard progression

**Stable, mean-reverting, seasonal, and cyclical are not synonyms.** A raw series
with fixed seasonality is nonstationary because its distribution depends on the
season. Conversely, FPP3 notes that cyclic behavior can occur in a stationary
series when cycle lengths are not fixed, so its peaks and troughs remain hard to
time.[^fpp3-stationarity] "Persistent repeating structure" is the useful easy
property.

**Change is not sufficient for model decay.** FPP3 pushes back on the common
claim that a changing environment cannot be forecast:

> Many people wrongly assume that forecasts are not possible in a changing environment. Every environment is changing, and a good forecasting model captures the way in which things are changing. Forecasts rarely assume that the environment is unchanging. What is normally assumed is that *the way in which the environment is changing* will continue into the future.[^fpp3-predictability]

The difficult case is a change in that evolution law. FPP3 later recommends
allowing the model to evolve or fitting recent observations when relationships
cannot plausibly remain fixed over a long history.[^fpp3-long]

**Chaos and nonstationarity are different.** Chaos concerns sensitive dependence
on initial conditions in a deterministic system. It limits the useful forecast
horizon because small state-estimation errors grow. A chaotic process can still
have stable long-run statistical properties. Weather combines predictable
seasonal structure with horizon-limited atmospheric dynamics, so "weather is
chaotic" does not mean all weather quantities are unpredictable.[^lorenz]

**Non-mean-reversion and sparse extremes are different.** A random walk is
non-mean-reverting, yet its optimal point forecast is the last observed value.
Its level uncertainty grows with horizon. Forecasting rare extremes is hard for
another reason: the relevant tail contains few observations and requires
extrapolation. Treat extremes as a data-support and loss-design problem, not as
a synonym for a unit root.[^rare]

**Finance is adaptive, and sometimes adversarial.** FPP3's exchange-rate example
combines weak causal understanding, possible crises, and forecast feedback. It
notes that public forecasts can directly affect the rate.[^fpp3-predictability]
"Adversarial" is accurate when other agents observe or infer the deployed
strategy and respond against it, or when the strategy's own trades move the
market. For a small unobserved actor, "adaptive and highly competitive" is
usually more precise than saying the market personally moves against the model.

## Sources

[^fpp3-predictability]: Rob J. Hyndman and George Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., ["What can be forecast?"](https://otexts.com/fpp3/what-can-be-forecast.html) ([local book](../docs/evidence/fpp3/01-getting-started.md#11-what-can-be-forecast)). This is the authors' own organizing framework, with residential electricity demand and currency exchange rates as contrasting examples.
[^fpp3-accuracy]: Hyndman and Athanasopoulos, ["Evaluating point forecast accuracy"](https://otexts.com/fpp3/accuracy.html) ([local book](../docs/evidence/fpp3/05-forecasters-toolbox.md#58-evaluating-point-forecast-accuracy)).
[^fpp3-tscv]: Hyndman and Athanasopoulos, ["Time series cross-validation"](https://otexts.com/fpp3/tscv.html) ([local book](../docs/evidence/fpp3/05-forecasters-toolbox.md#510-time-series-cross-validation)).
[^cerqueira]: Vitor Cerqueira, Luis Torgo, and Igor Mozetic, ["Evaluating time series forecasting models: an empirical study on performance estimation methods"](https://arxiv.org/abs/1905.11744), *Machine Learning* 109 (2020), 1997-2028. This is empirical evidence across real and synthetic series, not a universal proof that one split is always best.
[^fpp3-missing]: Hyndman and Athanasopoulos, ["Dealing with outliers and missing values"](https://otexts.com/fpp3/missing-outliers.html) ([local book](../docs/evidence/fpp3/13-practical-issues.md#139-dealing-with-outliers-and-missing-values)).
[^fpp3-stationarity]: Hyndman and Athanasopoulos, ["Stationarity and differencing"](https://otexts.com/fpp3/stationarity.html) ([local book](../docs/evidence/fpp3/09-arima-models.md#91-stationarity-and-differencing)).
[^fpp3-long]: Hyndman and Athanasopoulos, ["Very long and very short time series"](https://otexts.com/fpp3/long-short-ts.html) ([local book](../docs/evidence/fpp3/13-practical-issues.md#137-very-long-and-very-short-time-series)).
[^lorenz]: Edward N. Lorenz, ["Deterministic Nonperiodic Flow"](https://doi.org/10.1175/1520-0469(1963)020%3C0130:DNF%3E2.0.CO;2), *Journal of the Atmospheric Sciences* 20.2 (1963), 130-141. Primary paper behind the weather/chaos example; the finite-horizon interpretation is the synthesis here.
[^rare]: Paul Embrechts, Marius Hofert, and Valerie Chavez-Demoulin, ["The Modeling of Extreme Events"](https://doi.org/10.1017/9781009299794.011), in *Risk Revealed* (Cambridge University Press, 2024). The chapter frames rare events as the target of extreme-value methods; the sparse-support implication is statistical reasoning rather than a direct quote.
