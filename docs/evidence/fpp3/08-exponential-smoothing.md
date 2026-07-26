Source: https://otexts.com/fpp3/expsmooth.html (chapter expsmooth, 10 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - 08-exponential-smoothing
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Chapter 8 Exponential smoothing

Exponential smoothing was proposed in the late 1950s ([Brown, 1959](#ref-Brown59); [Holt, 1957](#ref-Holt57); [Winters, 1960](#ref-Winters60)), and has motivated some of the most successful forecasting methods. Forecasts produced using exponential smoothing methods are weighted averages of past observations, with the weights decaying exponentially as the observations get older. In other words, the more recent the observation the higher the associated weight. This framework generates reliable forecasts quickly and for a wide range of time series, which is a great advantage and of major importance to applications in industry.

This chapter is divided into two parts. In the first part (Sections [8.1](https://otexts.com/fpp3/ses.html#ses)–[8.4](https://otexts.com/fpp3/taxonomy.html#taxonomy)) we present the mechanics of the most important exponential smoothing methods, and their application in forecasting time series with various characteristics. This helps us develop an intuition to how these methods work. In this setting, selecting and using a forecasting method may appear to be somewhat ad hoc. The selection of the method is generally based on recognising key components of the time series (trend and seasonal) and the way in which these enter the smoothing method (e.g., in an additive, damped or multiplicative manner).

In the second part of the chapter (Sections [8.5](https://otexts.com/fpp3/ets.html#ets)–[8.7](https://otexts.com/fpp3/ets-forecasting.html#ets-forecasting)) we present the statistical models that underlie exponential smoothing methods. These models generate identical point forecasts to the methods discussed in the first part of the chapter, but also generate prediction intervals. Furthermore, this statistical framework allows for genuine model selection between competing models.

### Bibliography

Brown, R. G. (1959). *Statistical forecasting for inventory control*. McGraw/Hill.

Holt, C. C. (1957). *Forecasting seasonals and trends by exponentially weighted averages* (ONR Memorandum No. 52). Carnegie Institute of Technology, Pittsburgh USA. Reprinted in the *International Journal of Forecasting*, 2004.

Winters, P. R. (1960). Forecasting sales by exponentially weighted moving averages. *Management Science*, *6*(3), 324–342.

## 8.1 Simple exponential smoothing

The simplest of the exponentially smoothing methods is naturally called **simple exponential smoothing** (SES)[16](#fn16). This method is suitable for forecasting data with no clear trend or seasonal pattern. For example, the data in Figure [8.1](https://otexts.com/fpp3/ses.html#fig:7-oil) do not display any clear trending behaviour or any seasonality. (There is a decline in the last few years, which might suggest a trend. We will consider whether a trended method would be better for this series later in this chapter.) We have already considered the naïve and the average as possible methods for forecasting such data (Section [5.2](https://otexts.com/fpp3/simple-methods.html#simple-methods)).

```
algeria_economy <- global_economy |>
  filter(Country == "Algeria")
algeria_economy |>
  autoplot(Exports) +
  labs(y = "% of GDP", title = "Exports: Algeria")
```

![Exports of goods and services from Algeria from 1960 to 2017.](https://otexts.com/fpp3/fpp_files/figure-html/7-oil-1.png)

Figure 8.1: Exports of goods and services from Algeria from 1960 to 2017.

Using the naïve method, all forecasts for the future are equal to the last observed value of the series,
\[
\hat{y}_{T+h|T} = y_{T},
\]
for \(h=1,2,\dots\). Hence, the naïve method assumes that the most recent observation is the only important one, and all previous observations provide no information for the future. This can be thought of as a weighted average where all of the weight is given to the last observation.

Using the average method, all future forecasts are equal to a simple average of the observed data,
\[
\hat{y}_{T+h|T} = \frac1T \sum_{t=1}^T y_t,
\]
for \(h=1,2,\dots\). Hence, the average method assumes that all observations are of equal importance, and gives them equal weights when generating forecasts.

We often want something between these two extremes. For example, it may be sensible to attach larger weights to more recent observations than to observations from the distant past. This is exactly the concept behind simple exponential smoothing. Forecasts are calculated using weighted averages, where the weights decrease exponentially as observations come from further in the past — the smallest weights are associated with the oldest observations:
\[\begin{equation}
\hat{y}_{T+1|T} = \alpha y_T + \alpha(1-\alpha) y_{T-1} + \alpha(1-\alpha)^2 y_{T-2}+ \cdots, \tag{8.1}
\end{equation}\]
where \(0 \le \alpha \le 1\) is the smoothing parameter. The one-step-ahead forecast for time \(T+1\) is a weighted average of all of the observations in the series \(y_1,\dots,y_T\). The rate at which the weights decrease is controlled by the parameter \(\alpha\).

The table below shows the weights attached to observations for four different values of \(\alpha\) when forecasting using simple exponential smoothing. Note that the sum of the weights even for a small value of \(\alpha\) will be approximately one for any reasonable sample size.

|  | \(\alpha=0.2\) | \(\alpha=0.4\) | \(\alpha=0.6\) | \(\alpha=0.8\) |
| --- | --- | --- | --- | --- |
| \(y_{T}\) | 0.2000 | 0.4000 | 0.6000 | 0.8000 |
| \(y_{T-1}\) | 0.1600 | 0.2400 | 0.2400 | 0.1600 |
| \(y_{T-2}\) | 0.1280 | 0.1440 | 0.0960 | 0.0320 |
| \(y_{T-3}\) | 0.1024 | 0.0864 | 0.0384 | 0.0064 |
| \(y_{T-4}\) | 0.0819 | 0.0518 | 0.0154 | 0.0013 |
| \(y_{T-5}\) | 0.0655 | 0.0311 | 0.0061 | 0.0003 |

For any \(\alpha\) between 0 and 1, the weights attached to the observations decrease exponentially as we go back in time, hence the name “exponential smoothing”. If \(\alpha\) is small (i.e., close to 0), more weight is given to observations from the more distant past. If \(\alpha\) is large (i.e., close to 1), more weight is given to the more recent observations. For the extreme case where \(\alpha=1\), \(\hat{y}_{T+1|T}=y_T\), so the forecasts are equal to the naïve forecasts.

We present two equivalent forms of simple exponential smoothing, each of which leads to the forecast Equation [(8.1)](https://otexts.com/fpp3/ses.html#eq:7-ses).

### Weighted average form

The forecast at time \(T+1\) is equal to a weighted average between the most recent observation \(y_T\) and the previous forecast \(\hat{y}_{T|T-1}\):
\[
\hat{y}_{T+1|T} = \alpha y_T + (1-\alpha) \hat{y}_{T|T-1},
\]
where \(0 \le \alpha \le 1\) is the smoothing parameter.
Similarly, we can write the fitted values as
\[
\hat{y}_{t+1|t} = \alpha y_t + (1-\alpha) \hat{y}_{t|t-1},
\]
for \(t=1,\dots,T\). (Recall that fitted values are simply one-step forecasts of the training data.)

The process has to start somewhere, so we let the first fitted value at time 1 be denoted by \(\ell_0\) (which we will have to estimate). Then
\[\begin{align\*}
\hat{y}_{2|1} &= \alpha y_1 + (1-\alpha) \ell_0\\
\hat{y}_{3|2} &= \alpha y_2 + (1-\alpha) \hat{y}_{2|1}\\
\hat{y}_{4|3} &= \alpha y_3 + (1-\alpha) \hat{y}_{3|2}\\
\vdots\\
\hat{y}_{T|T-1} &= \alpha y_{T-1} + (1-\alpha) \hat{y}_{T-1|T-2}\\
\hat{y}_{T+1|T} &= \alpha y_T + (1-\alpha) \hat{y}_{T|T-1}.
\end{align\*}\]
Substituting each equation into the following equation, we obtain
\[\begin{align\*}
\hat{y}_{3|2} & = \alpha y_2 + (1-\alpha) \left[\alpha y_1 + (1-\alpha) \ell_0\right] \\
& = \alpha y_2 + \alpha(1-\alpha) y_1 + (1-\alpha)^2 \ell_0 \\
\hat{y}_{4|3} & = \alpha y_3 + (1-\alpha) [\alpha y_2 + \alpha(1-\alpha) y_1 + (1-\alpha)^2 \ell_0]\\
& = \alpha y_3 + \alpha(1-\alpha) y_2 + \alpha(1-\alpha)^2 y_1 + (1-\alpha)^3 \ell_0 \\
& ~~\vdots \\
\hat{y}_{T+1|T} & = \sum_{j=0}^{T-1} \alpha(1-\alpha)^j y_{T-j} + (1-\alpha)^T \ell_{0}.
\end{align\*}\]
The last term becomes tiny for large \(T\). So, the weighted average form leads to the same forecast Equation [(8.1)](https://otexts.com/fpp3/ses.html#eq:7-ses).

### Component form

An alternative representation is the component form. For simple exponential smoothing, the only component included is the level, \(\ell_t\). (Other methods which are considered later in this chapter may also include a trend \(b_t\) and a seasonal component \(s_t\).) Component form representations of exponential smoothing methods comprise a forecast equation and a smoothing equation for each of the components included in the method. The component form of simple exponential smoothing is given by:
\[\begin{align\*}
\text{Forecast equation} && \hat{y}_{t+h|t} & = \ell_{t}\\
\text{Smoothing equation} && \ell_{t} & = \alpha y_{t} + (1 - \alpha)\ell_{t-1},
\end{align\*}\]
where \(\ell_{t}\) is the level (or the smoothed value) of the series at time \(t\). Setting \(h=1\) gives the fitted values, while setting \(t=T\) gives the true forecasts beyond the training data.

The forecast equation shows that the forecast value at time \(t+1\) is the estimated level at time \(t\). The smoothing equation for the level (usually referred to as the level equation) gives the estimated level of the series at each period \(t\).

If we replace \(\ell_t\) with \(\hat{y}_{t+1|t}\) and \(\ell_{t-1}\) with \(\hat{y}_{t|t-1}\) in the smoothing equation, we will recover the weighted average form of simple exponential smoothing.

The component form of simple exponential smoothing is not particularly useful on its own, but it will be the easiest form to use when we start adding other components.

### Flat forecasts

Simple exponential smoothing has a “flat” forecast function:
\[
\hat{y}_{T+h|T} = \hat{y}_{T+1|T}=\ell_T, \qquad h=2,3,\dots.
\]
That is, all forecasts take the same value, equal to the last level component. Remember that these forecasts will only be suitable if the time series has no trend or seasonal component.

### Optimisation

The application of every exponential smoothing method requires the smoothing parameters and the initial values to be chosen. In particular, for simple exponential smoothing, we need to select the values of \(\alpha\) and \(\ell_0\). All forecasts can be computed from the data once we know those values. For the methods that follow there is usually more than one smoothing parameter and more than one initial component to be chosen.

In some cases, the smoothing parameters may be chosen in a subjective manner — the forecaster specifies the value of the smoothing parameters based on previous experience. However, a more reliable and objective way to obtain values for the unknown parameters is to estimate them from the observed data.

In Section [7.2](https://otexts.com/fpp3/least-squares.html#least-squares), we estimated the coefficients of a regression model by minimising the sum of the squared residuals (usually known as SSE or “sum of squared errors”). Similarly, the unknown parameters and the initial values for any exponential smoothing method can be estimated by minimising the SSE. The residuals are specified as \(e_t=y_t - \hat{y}_{t|t-1}\) for \(t=1,\dots,T\). Hence, we find the values of the unknown parameters and the initial values that minimise
\[\begin{equation}
\text{SSE}=\sum_{t=1}^T(y_t - \hat{y}_{t|t-1})^2=\sum_{t=1}^Te_t^2. \tag{8.2}
\end{equation}\]

Unlike the regression case (where we have formulas which return the values of the regression coefficients that minimise the SSE), this involves a non-linear minimisation problem, and we need to use an optimisation tool to solve it.

### Example: Algerian exports

In this example, simple exponential smoothing is applied to forecast exports of goods and services from Algeria.

```
# Estimate parameters
fit <- algeria_economy |>
  model(ETS(Exports ~ error("A") + trend("N") + season("N")))
fc <- fit |>
  forecast(h = 5)
```

This gives parameter estimates \(\hat\alpha=0.84\) and \(\hat\ell_0=39.5\), obtained by minimising SSE over periods \(t=1,2,\dots,58\), subject to the restriction that \(0\le\alpha\le1\).

In Table [8.1](https://otexts.com/fpp3/ses.html#tab:export-ses) we demonstrate the calculation using these parameters. The second last column shows the estimated level for times \(t=0\) to \(t=58\); the last few rows of the last column show the forecasts for \(h=1\) to \(5\)-steps ahead.

Table 8.1: Forecasting goods and services exports from Algeria using simple exponential smoothing.

| Year | Time | Observation | Level | Forecast |
| --- | --- | --- | --- | --- |
|  | \(t\) | \(y_t\) | \(\ell_t\) | \(\hat{y}_{t\vert t-1}\) |
| 1959 | 0 |  | 39.54 |  |
| 1960 | 1 | 39.04 | 39.12 | 39.54 |
| 1961 | 2 | 46.24 | 45.10 | 39.12 |
| 1962 | 3 | 19.79 | 23.84 | 45.10 |
| 1963 | 4 | 24.68 | 24.55 | 23.84 |
| 1964 | 5 | 25.08 | 25.00 | 24.55 |
| 1965 | 6 | 22.60 | 22.99 | 25.00 |
| 1966 | 7 | 25.99 | 25.51 | 22.99 |
| 1967 | 8 | 23.43 | 23.77 | 25.51 |
|  | ⋮ | ⋮ | ⋮ | ⋮ |
| 2014 | 55 | 30.22 | 30.80 | 33.85 |
| 2015 | 56 | 23.17 | 24.39 | 30.80 |
| 2016 | 57 | 20.86 | 21.43 | 24.39 |
| 2017 | 58 | 22.64 | 22.44 | 21.43 |
|  | \(h\) |  |  | \(\hat{y}_{T+h\vert T}\) |
| 2018 | 1 |  |  | 22.44 |
| 2019 | 2 |  |  | 22.44 |
| 2020 | 3 |  |  | 22.44 |
| 2021 | 4 |  |  | 22.44 |
| 2022 | 5 |  |  | 22.44 |

The black line in Figure [8.2](https://otexts.com/fpp3/ses.html#fig:ses) shows the data, which has a changing level over time.

```
fc |>
  autoplot(algeria_economy) +
  geom_line(aes(y = .fitted), col="#D55E00",
            data = augment(fit)) +
  labs(y="% of GDP", title="Exports: Algeria") +
  guides(colour = "none")
```

![Simple exponential smoothing applied to exports from Algeria (1960--2017). The orange curve shows the one-step-ahead fitted values.](https://otexts.com/fpp3/fpp_files/figure-html/ses-1.png)

Figure 8.2: Simple exponential smoothing applied to exports from Algeria (1960–2017). The orange curve shows the one-step-ahead fitted values.

The forecasts for the period 2018–2022 are plotted in Figure [8.2](https://otexts.com/fpp3/ses.html#fig:ses). Also plotted are one-step-ahead fitted values alongside the data over the period 1960–2017. The large value of \(\alpha\) in this example is reflected in the large adjustment that takes place in the estimated level \(\ell_t\) at each time. A smaller value of \(\alpha\) would lead to smaller changes over time, and so the series of fitted values would be smoother.

The prediction intervals shown here are calculated using the methods described in Section [8.7](https://otexts.com/fpp3/ets-forecasting.html#ets-forecasting). The prediction intervals show that there is considerable uncertainty in the future exports over the five-year forecast period. So interpreting the point forecasts without accounting for the large uncertainty can be very misleading.

---

16. In some books it is called “single exponential smoothing”.[↩︎](https://otexts.com/fpp3/ses.html#fnref16)

## 8.2 Methods with trend

### Holt’s linear trend method

Holt ([1957](#ref-Holt57)) extended simple exponential smoothing to allow the forecasting of data with a trend. This method involves a forecast equation and two smoothing equations (one for the level and one for the trend):
\[\begin{align\*}
\text{Forecast equation}&& \hat{y}_{t+h|t} &= \ell_{t} + hb_{t} \\
\text{Level equation} && \ell_{t} &= \alpha y_{t} + (1 - \alpha)(\ell_{t-1} + b_{t-1})\\
\text{Trend equation} && b_{t} &= \beta^\*(\ell_{t} - \ell_{t-1}) + (1 -\beta^\*)b_{t-1},
\end{align\*}\]
where \(\ell_t\) denotes an estimate of the level of the series at time \(t\), \(b_t\) denotes an estimate of the trend (slope) of the series at time \(t\), \(\alpha\) is the smoothing parameter for the level, \(0\le\alpha\le1\), and \(\beta^\*\) is the smoothing parameter for the trend, \(0\le\beta^\*\le1\). (We denote this as \(\beta^\*\) instead of \(\beta\) for reasons that will be explained in Section [8.5](https://otexts.com/fpp3/ets.html#ets).)

As with simple exponential smoothing, the level equation here shows that \(\ell_t\) is a weighted average of observation \(y_t\) and the one-step-ahead training forecast for time \(t\), here given by \(\ell_{t-1} + b_{t-1}\). The trend equation shows that \(b_t\) is a weighted average of the estimated trend at time \(t\) based on \(\ell_{t} - \ell_{t-1}\) and \(b_{t-1}\), the previous estimate of the trend.

The forecast function is no longer flat but trending. The \(h\)-step-ahead forecast is equal to the last estimated level plus \(h\) times the last estimated trend value. Hence the forecasts are a linear function of \(h\).

### Example: Australian population

```
aus_economy <- global_economy |>
  filter(Code == "AUS") |>
  mutate(Pop = Population / 1e6)
autoplot(aus_economy, Pop) +
  labs(y = "Millions", title = "Australian population")
```

![Australia's population, 1960-2017.](https://otexts.com/fpp3/fpp_files/figure-html/auspop-1.png)

Figure 8.3: Australia’s population, 1960-2017.

Figure [8.3](https://otexts.com/fpp3/holt.html#fig:auspop) shows Australia’s annual population from 1960 to 2017. We will apply Holt’s method to this series. The smoothing parameters, \(\alpha\) and \(\beta^\*\), and the initial values \(\ell_0\) and \(b_0\) are estimated by minimising the SSE for the one-step training errors as in Section [8.1](https://otexts.com/fpp3/ses.html#ses).

```
fit <- aus_economy |>
  model(
    AAN = ETS(Pop ~ error("A") + trend("A") + season("N"))
  )
fc <- fit |> forecast(h = 10)
```

The estimated smoothing coefficient for the level is \(\hat{\alpha} = 0.9999\). The very high value shows that the level changes rapidly in order to capture the highly trended series. The estimated smoothing coefficient for the slope is \(\hat{\beta}^\* = 0.3267\). This is relatively large suggesting that the trend also changes often (even if the changes are slight).

In Table [8.2](https://otexts.com/fpp3/holt.html#tab:popholt) we use these values to demonstrate the application of Holt’s method.

Table 8.2: Forecasting Australian annual population using Holt’s linear trend method.

| Year | Time | Observation | Level | Slope | Forecast |
| --- | --- | --- | --- | --- | --- |
|  | \(t\) | \(y_t\) | \(\ell_t\) |  | \(\hat{y}_{t+1\mid t}\) |
| 1959 | 0 |  | 10.05 | 0.22 |  |
| 1960 | 1 | 10.28 | 10.28 | 0.22 | 10.28 |
| 1961 | 2 | 10.48 | 10.48 | 0.22 | 10.50 |
| 1962 | 3 | 10.74 | 10.74 | 0.23 | 10.70 |
| 1963 | 4 | 10.95 | 10.95 | 0.22 | 10.97 |
| 1964 | 5 | 11.17 | 11.17 | 0.22 | 11.17 |
| 1965 | 6 | 11.39 | 11.39 | 0.22 | 11.39 |
| 1966 | 7 | 11.65 | 11.65 | 0.23 | 11.61 |
|  | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ |
| 2014 | 55 | 23.50 | 23.50 | 0.37 | 23.52 |
| 2015 | 56 | 23.85 | 23.85 | 0.36 | 23.87 |
| 2016 | 57 | 24.21 | 24.21 | 0.36 | 24.21 |
| 2017 | 58 | 24.60 | 24.60 | 0.37 | 24.57 |
|  | \(h\) |  |  |  | \(\hat{y}_{T+h\mid T}\) |
| 2018 | 1 |  |  |  | 24.97 |
| 2019 | 2 |  |  |  | 25.34 |
| 2020 | 3 |  |  |  | 25.71 |
| 2021 | 4 |  |  |  | 26.07 |
| 2022 | 5 |  |  |  | 26.44 |
| 2023 | 6 |  |  |  | 26.81 |
| 2024 | 7 |  |  |  | 27.18 |
| 2025 | 8 |  |  |  | 27.55 |
| 2026 | 9 |  |  |  | 27.92 |
| 2027 | 10 |  |  |  | 28.29 |

### Damped trend methods

The forecasts generated by Holt’s linear method display a constant trend (increasing or decreasing) indefinitely into the future. Empirical evidence indicates that these methods tend to over-forecast, especially for longer forecast horizons. Motivated by this observation, Gardner & McKenzie ([1985](#ref-GarMacK1985)) introduced a parameter that “dampens” the trend to a flat line some time in the future. Methods that include a damped trend have proven to be very successful, and are arguably the most popular individual methods when forecasts are required automatically for many series.

In conjunction with the smoothing parameters \(\alpha\) and \(\beta^\*\) (with values between 0 and 1 as in Holt’s method), this method also includes a damping parameter \(0<\phi<1\):
\[\begin{align\*}
\hat{y}_{t+h|t} &= \ell_{t} + (\phi+\phi^2 + \dots + \phi^{h})b_{t} \\
\ell_{t} &= \alpha y_{t} + (1 - \alpha)(\ell_{t-1} + \phi b_{t-1})\\
b_{t} &= \beta^\*(\ell_{t} - \ell_{t-1}) + (1 -\beta^\*)\phi b_{t-1}.
\end{align\*}\]
If \(\phi=1\), the method is identical to Holt’s linear method. For values between \(0\) and \(1\), \(\phi\) dampens the trend so that it approaches a constant some time in the future. In fact, the forecasts converge to \(\ell_T+\phi b_T/(1-\phi)\) as \(h\rightarrow\infty\) for any value \(0<\phi<1\). This means that short-run forecasts are trended while long-run forecasts are constant.

In practice, \(\phi\) is rarely less than 0.8 as the damping has a very strong effect for smaller values. Values of \(\phi\) close to 1 will mean that a damped model is not able to be distinguished from a non-damped model. For these reasons, we usually restrict \(\phi\) to a minimum of 0.8 and a maximum of 0.98.

### Example: Australian Population (continued)

Figure [8.4](https://otexts.com/fpp3/holt.html#fig:dampedtrend) shows the forecasts for years 2018–2032 generated from Holt’s linear trend method and the damped trend method.

```
aus_economy |>
  model(
    `Holt's method` = ETS(Pop ~ error("A") +
                       trend("A") + season("N")),
    `Damped Holt's method` = ETS(Pop ~ error("A") +
                       trend("Ad", phi = 0.9) + season("N"))
  ) |>
  forecast(h = 15) |>
  autoplot(aus_economy, level = NULL) +
  labs(title = "Australian population",
       y = "Millions") +
  guides(colour = guide_legend(title = "Forecast"))
```

![Forecasting annual Australian population (millions) over 2018-2032. For the damped trend method, $\phi=0.90$.](https://otexts.com/fpp3/fpp_files/figure-html/dampedtrend-1.png)

Figure 8.4: Forecasting annual Australian population (millions) over 2018-2032. For the damped trend method, \(\phi=0.90\).

We have set the damping parameter to a relatively low number \((\phi=0.90)\) to exaggerate the effect of damping for comparison. Usually, we would estimate \(\phi\) along with the other parameters. We have also used a rather large forecast horizon (\(h=15\)) to highlight the difference between a damped trend and a linear trend.

### Example: Internet usage

In this example, we compare the forecasting performance of the three exponential smoothing methods that we have considered so far in forecasting the number of users connected to the internet via a server. The data is observed over 100 minutes and is shown in Figure [8.5](https://otexts.com/fpp3/holt.html#fig:www-usage).

```
www_usage <- as_tsibble(WWWusage)
www_usage |> autoplot(value) +
  labs(x="Minute", y="Number of users",
       title = "Internet usage per minute")
```

![Users connected to the internet through a server](https://otexts.com/fpp3/fpp_files/figure-html/www-usage-1.png)

Figure 8.5: Users connected to the internet through a server

We will use time series cross-validation to compare the one-step forecast accuracy of the three methods.

```
www_usage |>
  stretch_tsibble(.init = 10) |>
  model(
    SES = ETS(value ~ error("A") + trend("N") + season("N")),
    Holt = ETS(value ~ error("A") + trend("A") + season("N")),
    Damped = ETS(value ~ error("A") + trend("Ad") +
                   season("N"))
  ) |>
  forecast(h = 1) |>
  accuracy(www_usage)
#> # A tibble: 3 × 10
#>   .model .type     ME  RMSE   MAE   MPE  MAPE  MASE RMSSE  ACF1
#>   <chr>  <chr>  <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
#> 1 Damped Test  0.288   3.69  3.00 0.347  2.26 0.663 0.636 0.336
#> 2 Holt   Test  0.0610  3.87  3.17 0.244  2.38 0.701 0.668 0.296
#> 3 SES    Test  1.46    6.05  4.81 0.904  3.55 1.06  1.04  0.803
```

Damped Holt’s method is best whether you compare MAE or RMSE values. So we will proceed with using the damped Holt’s method and apply it to the whole data set to get forecasts for future minutes.

```
fit <- www_usage |>
  model(
    Damped = ETS(value ~ error("A") + trend("Ad") +
                   season("N"))
  )
# Estimated parameters:
tidy(fit)
#> # A tibble: 5 × 3
#>   .model term  estimate
#>   <chr>  <chr>    <dbl>
#> 1 Damped alpha   1.000
#> 2 Damped beta    0.997
#> 3 Damped phi     0.815
#> 4 Damped l[0]   90.4
#> 5 Damped b[0]   -0.0173
```

The smoothing parameter for the slope is estimated to be almost one, indicating that the trend changes to mostly reflect the slope between the last two minutes of internet usage. The value of \(\alpha\) is very close to one, showing that the level reacts strongly to each new observation.

```
fit |>
  forecast(h = 10) |>
  autoplot(www_usage) +
  labs(x="Minute", y="Number of users",
       title = "Internet usage per minute")
```

![Forecasting internet usage: comparing forecasting performance of non-seasonal methods.](https://otexts.com/fpp3/fpp_files/figure-html/fig-7-comp-1.png)

Figure 8.6: Forecasting internet usage: comparing forecasting performance of non-seasonal methods.

The resulting forecasts look sensible with decreasing trend, which flattens out due to the low value of the damping parameter (0.815), and relatively wide prediction intervals reflecting the variation in the historical data. The prediction intervals are calculated using the methods described in Section [8.7](https://otexts.com/fpp3/ets-forecasting.html#ets-forecasting).

In this example, the process of selecting a method was relatively easy as both MSE and MAE comparisons suggested the same method (damped Holt’s). However, sometimes different accuracy measures will suggest different forecasting methods, and then a decision is required as to which forecasting method we prefer to use. As forecasting tasks can vary by many dimensions (length of forecast horizon, size of test set, forecast error measures, frequency of data, etc.), it is unlikely that one method will be better than all others for all forecasting scenarios. What we require from a forecasting method are consistently sensible forecasts, and these should be frequently evaluated against the task at hand.

### Bibliography

Gardner, E. S., & McKenzie, E. (1985). Forecasting trends in time series. *Management Science*, *31*(10), 1237–1246.

Holt, C. C. (1957). *Forecasting seasonals and trends by exponentially weighted averages* (ONR Memorandum No. 52). Carnegie Institute of Technology, Pittsburgh USA. Reprinted in the *International Journal of Forecasting*, 2004.

## 8.3 Methods with seasonality

Holt ([1957](#ref-Holt57)) and Winters ([1960](#ref-Winters60)) extended Holt’s method to capture seasonality. The Holt-Winters seasonal method comprises the forecast equation and three smoothing equations — one for the level \(\ell_t\), one for the trend \(b_t\), and one for the seasonal component \(s_t\), with corresponding smoothing parameters \(\alpha\), \(\beta^\*\) and \(\gamma\). We use \(m\) to denote the period of the seasonality, i.e., the number of seasons in a year. For example, for quarterly data \(m=4\), and for monthly data \(m=12\).

There are two variations to this method that differ in the nature of the seasonal component. The additive method is preferred when the seasonal variations are roughly constant through the series, while the multiplicative method is preferred when the seasonal variations are changing proportional to the level of the series. With the additive method, the seasonal component is expressed in absolute terms in the scale of the observed series, and in the level equation the series is seasonally adjusted by subtracting the seasonal component. Within each year, the seasonal component will add up to approximately zero. With the multiplicative method, the seasonal component is expressed in relative terms (percentages), and the series is seasonally adjusted by dividing through by the seasonal component. Within each year, the seasonal component will sum up to approximately \(m\).

### Holt-Winters’ additive method

The component form for the additive method is:
\[\begin{align\*}
\hat{y}_{t+h|t} &= \ell_{t} + hb_{t} + s_{t+h-m(k+1)} \\
\ell_{t} &= \alpha(y_{t} - s_{t-m}) + (1 - \alpha)(\ell_{t-1} + b_{t-1})\\
b_{t} &= \beta^\*(\ell_{t} - \ell_{t-1}) + (1 - \beta^\*)b_{t-1}\\
s_{t} &= \gamma (y_{t}-\ell_{t-1}-b_{t-1}) + (1-\gamma)s_{t-m},
\end{align\*}\]
where \(k\) is the integer part of \((h-1)/m\), which ensures that the estimates of the seasonal indices used for forecasting come from the final year of the sample. The level equation shows a weighted average between the seasonally adjusted observation \((y_{t} - s_{t-m})\) and the non-seasonal forecast \((\ell_{t-1}+b_{t-1})\) for time \(t\). The trend equation is identical to Holt’s linear method. The seasonal equation shows a weighted average between the current seasonal index, \((y_{t}-\ell_{t-1}-b_{t-1})\), and the seasonal index of the same season last year (i.e., \(m\) time periods ago).

The equation for the seasonal component is often expressed as
\[
s_{t} = \gamma^\* (y_{t}-\ell_{t})+ (1-\gamma^\*)s_{t-m}.
\]
If we substitute \(\ell_t\) from the smoothing equation for the level of the component form above, we get
\[
s_{t} = \gamma^\*(1-\alpha) (y_{t}-\ell_{t-1}-b_{t-1})+ [1-\gamma^\*(1-\alpha)]s_{t-m},
\]
which is identical to the smoothing equation for the seasonal component we specify here, with \(\gamma=\gamma^\*(1-\alpha)\). The usual parameter restriction is \(0\le\gamma^\*\le1\), which translates to \(0\le\gamma\le 1-\alpha\).

### Holt-Winters’ multiplicative method

The component form for the multiplicative method is:
\[\begin{align\*}
\hat{y}_{t+h|t} &= (\ell_{t} + hb_{t})s_{t+h-m(k+1)} \\
\ell_{t} &= \alpha \frac{y_{t}}{s_{t-m}} + (1 - \alpha)(\ell_{t-1} + b_{t-1})\\
b_{t} &= \beta^\*(\ell_{t}-\ell_{t-1}) + (1 - \beta^\*)b_{t-1} \\
s_{t} &= \gamma \frac{y_{t}}{(\ell_{t-1} + b_{t-1})} + (1 - \gamma)s_{t-m}.
\end{align\*}\]

### Example: Domestic overnight trips in Australia

We apply Holt-Winters’ method with both additive and multiplicative seasonality[17](#fn17) to forecast quarterly visitor nights in Australia spent by domestic tourists. Figure [8.7](https://otexts.com/fpp3/holt-winters.html#fig:7-HW) shows the data from 1998–2017, and the forecasts for 2018–2020. The data show an obvious seasonal pattern, with peaks observed in the March quarter of each year, corresponding to the Australian summer.

```
aus_holidays <- tourism |>
  filter(Purpose == "Holiday") |>
  summarise(Trips = sum(Trips)/1e3)
fit <- aus_holidays |>
  model(
    additive = ETS(Trips ~ error("A") + trend("A") +
                                                season("A")),
    multiplicative = ETS(Trips ~ error("M") + trend("A") +
                                                season("M"))
  )
fc <- fit |> forecast(h = "3 years")
fc |>
  autoplot(aus_holidays, level = NULL) +
  labs(title="Australian domestic tourism",
       y="Overnight trips (millions)") +
  guides(colour = guide_legend(title = "Forecast"))
```

![Forecasting domestic overnight trips in Australia using the Holt-Winters method with both additive and multiplicative seasonality.](https://otexts.com/fpp3/fpp_files/figure-html/7-HW-1.png)

Figure 8.7: Forecasting domestic overnight trips in Australia using the Holt-Winters method with both additive and multiplicative seasonality.

Table 8.3: Applying Holt-Winters’ method with additive seasonality for forecasting domestic tourism in Australia. Notice that the additive seasonal component sums to approximately zero. The smoothing parameters are \(\alpha = 0.2620\), \(\beta^\* = 0.1646\), \(\gamma = 0.0001\) and RMSE \(=0.4169\).

| Quarter | Time | Observation | Level | Slope | Season | Forecast |
| --- | --- | --- | --- | --- | --- | --- |
|  | \(t\) | \(y_t\) | \(\ell_t\) | \(b_t\) | \(s_t\) | \(\hat{y}_{t+1\vert t}\) |
| 1997 Q1 | 0 |  |  |  | 1.5 |  |
| 1997 Q2 | 1 |  |  |  | -0.3 |  |
| 1997 Q3 | 2 |  |  |  | -0.7 |  |
| 1997 Q4 | 3 |  | 9.8 | 0.0 | -0.5 |  |
| 1998 Q1 | 4 | 11.8 | 9.9 | 0.0 | 1.5 | 11.3 |
| 1998 Q2 | 5 | 9.3 | 9.9 | 0.0 | -0.3 | 9.7 |
| 1998 Q3 | 6 | 8.6 | 9.7 | -0.0 | -0.7 | 9.2 |
| 1998 Q4 | 7 | 9.3 | 9.8 | 0.0 | -0.5 | 9.2 |
|  | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ |
| 2017 Q1 | 80 | 12.4 | 10.9 | 0.1 | 1.5 | 12.3 |
| 2017 Q2 | 81 | 10.5 | 10.9 | 0.1 | -0.3 | 10.7 |
| 2017 Q3 | 82 | 10.5 | 11.0 | 0.1 | -0.7 | 10.3 |
| 2017 Q4 | 83 | 11.2 | 11.3 | 0.1 | -0.5 | 10.6 |
|  | \(h\) |  |  |  |  | \(\hat{y}_{T+h\vert T}\) |
| 2018 Q1 | 1 |  |  |  |  | 12.9 |
| 2018 Q2 | 2 |  |  |  |  | 11.2 |
| 2018 Q3 | 3 |  |  |  |  | 11.0 |
| 2018 Q4 | 4 |  |  |  |  | 11.2 |
| 2019 Q1 | 5 |  |  |  |  | 13.4 |
| 2019 Q2 | 6 |  |  |  |  | 11.7 |
| 2019 Q3 | 7 |  |  |  |  | 11.5 |
| 2019 Q4 | 8 |  |  |  |  | 11.7 |
| 2020 Q1 | 9 |  |  |  |  | 13.9 |
| 2020 Q2 | 10 |  |  |  |  | 12.2 |
| 2020 Q3 | 11 |  |  |  |  | 11.9 |
| 2020 Q4 | 12 |  |  |  |  | 12.2 |

Table 8.4: Applying Holt-Winters’ method with multiplicative seasonality for forecasting domestic tourism in Australia. Notice that the multiplicative seasonal component sums to approximately \(m=4\). The smoothing parameters are \(\alpha = 0.2237\), \(\beta^\* = 0.1360\), \(\gamma = 0.0001\) and RMSE \(=0.4122\).

| Quarter | Time | Observation | Level | Slope | Season | Forecast |
| --- | --- | --- | --- | --- | --- | --- |
|  | \(t\) | \(y_t\) | \(\ell_t\) | \(b_t\) | \(s_t\) | \(\hat{y}_{t+1\vert t}\) |
| 1997 Q1 | 0 |  |  |  | 1.2 |  |
| 1997 Q2 | 1 |  |  |  | 1.0 |  |
| 1997 Q3 | 2 |  |  |  | 0.9 |  |
| 1997 Q4 | 3 |  | 10.0 | -0.0 | 0.9 |  |
| 1998 Q1 | 4 | 11.8 | 10.0 | -0.0 | 1.2 | 11.6 |
| 1998 Q2 | 5 | 9.3 | 9.9 | -0.0 | 1.0 | 9.7 |
| 1998 Q3 | 6 | 8.6 | 9.8 | -0.0 | 0.9 | 9.2 |
| 1998 Q4 | 7 | 9.3 | 9.8 | -0.0 | 0.9 | 9.2 |
|  | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ | ⋮ |
| 2017 Q1 | 80 | 12.4 | 10.8 | 0.1 | 1.2 | 12.6 |
| 2017 Q2 | 81 | 10.5 | 10.9 | 0.1 | 1.0 | 10.6 |
| 2017 Q3 | 82 | 10.5 | 11.1 | 0.1 | 0.9 | 10.2 |
| 2017 Q4 | 83 | 11.2 | 11.3 | 0.1 | 0.9 | 10.5 |
|  | \(h\) |  |  |  |  | \(\hat{y}_{T+h\vert T}\) |
| 2018 Q1 | 1 |  |  |  |  | 13.3 |
| 2018 Q2 | 2 |  |  |  |  | 11.2 |
| 2018 Q3 | 3 |  |  |  |  | 10.8 |
| 2018 Q4 | 4 |  |  |  |  | 11.1 |
| 2019 Q1 | 5 |  |  |  |  | 13.8 |
| 2019 Q2 | 6 |  |  |  |  | 11.7 |
| 2019 Q3 | 7 |  |  |  |  | 11.3 |
| 2019 Q4 | 8 |  |  |  |  | 11.6 |
| 2020 Q1 | 9 |  |  |  |  | 14.4 |
| 2020 Q2 | 10 |  |  |  |  | 12.2 |
| 2020 Q3 | 11 |  |  |  |  | 11.7 |
| 2020 Q4 | 12 |  |  |  |  | 12.1 |

The applications of both methods (with additive and multiplicative seasonality) are presented in Tables [8.3](https://otexts.com/fpp3/holt-winters.html#tab:tab75) and [8.4](https://otexts.com/fpp3/holt-winters.html#tab:tab76) respectively. Because both methods have exactly the same number of parameters to estimate, we can compare the training RMSE from both models. In this case, the method with multiplicative seasonality fits the data slightly better.

The estimated components for both models are plotted in Figure [8.8](https://otexts.com/fpp3/holt-winters.html#fig:fig-7-LevelTrendSeas). The small value of \(\gamma\) for the multiplicative model means that the seasonal component hardly changes over time. The small value of \(\beta^{\*}\) means the slope component hardly changes over time (compare the vertical scales of the slope and level components).

![Estimated components for the Holt-Winters method with additive and multiplicative seasonal components.](https://otexts.com/fpp3/fpp_files/figure-html/fig-7-LevelTrendSeas-1.png)

Figure 8.8: Estimated components for the Holt-Winters method with additive and multiplicative seasonal components.

### Holt-Winters’ damped method

Damping is possible with both additive and multiplicative Holt-Winters’ methods. A method that often provides accurate and robust forecasts for seasonal data is the Holt-Winters method with a damped trend and multiplicative seasonality:
\[\begin{align\*}
\hat{y}_{t+h|t} &= \left[\ell_{t} + (\phi+\phi^2 + \dots + \phi^{h})b_{t}\right]s_{t+h-m(k+1)} \\
\ell_{t} &= \alpha(y_{t} / s_{t-m}) + (1 - \alpha)(\ell_{t-1} + \phi b_{t-1})\\
b_{t} &= \beta^\*(\ell_{t} - \ell_{t-1}) + (1 - \beta^\*)\phi b_{t-1} \\
s_{t} &= \gamma \frac{y_{t}}{(\ell_{t-1} + \phi b_{t-1})} + (1 - \gamma)s_{t-m}.
\end{align\*}\]

### Example: Holt-Winters method with daily data

The Holt-Winters method can also be used for daily type of data, where the seasonal period is \(m=7\), and the appropriate unit of time for \(h\) is in days. Here we forecast pedestrian traffic at a busy Melbourne train station in July 2016.

```
sth_cross_ped <- pedestrian |>
  filter(Date >= "2016-07-01",
         Sensor == "Southern Cross Station") |>
  index_by(Date) |>
  summarise(Count = sum(Count)/1000)
sth_cross_ped |>
  filter(Date <= "2016-07-31") |>
  model(
    hw = ETS(Count ~ error("M") + trend("Ad") + season("M"))
  ) |>
  forecast(h = "2 weeks") |>
  autoplot(sth_cross_ped |> filter(Date <= "2016-08-14")) +
  labs(title = "Daily traffic: Southern Cross",
       y="Pedestrians ('000)")
```

![Forecasts of daily pedestrian traffic at the Southern Cross railway station, Melbourne.](https://otexts.com/fpp3/fpp_files/figure-html/hyndsight-1.png)

Figure 8.9: Forecasts of daily pedestrian traffic at the Southern Cross railway station, Melbourne.

Clearly the model has identified the weekly seasonal pattern and the increasing trend at the end of the data, and the forecasts are a close match to the test data.

### Bibliography

Holt, C. C. (1957). *Forecasting seasonals and trends by exponentially weighted averages* (ONR Memorandum No. 52). Carnegie Institute of Technology, Pittsburgh USA. Reprinted in the *International Journal of Forecasting*, 2004.

Winters, P. R. (1960). Forecasting sales by exponentially weighted moving averages. *Management Science*, *6*(3), 324–342.

---

17. Our implementation uses maximum likelihood estimation as described in Section [8.6](https://otexts.com/fpp3/ets-estimation.html#ets-estimation) while Holt and Winters originally minimized the sum of squared errors. For multiplicative seasonality, this will lead to slightly different parameter estimates. Optimizing the sum of squared errors can be obtained by setting `opt_crit="mse"` in `ETS()`.[↩︎](https://otexts.com/fpp3/holt-winters.html#fnref17)

## 8.4 A taxonomy of exponential smoothing methods

Exponential smoothing methods are not restricted to those we have presented so far. By considering variations in the combinations of the trend and seasonal components, nine exponential smoothing methods are possible, listed in Table [8.5](https://otexts.com/fpp3/taxonomy.html#tab:taxonomy). Each method is labelled by a pair of letters (T,S) defining the type of ‘Trend’ and ‘Seasonal’ components. For example, (A,M) is the method with an additive trend and multiplicative seasonality; (A\(_d\),N) is the method with damped trend and no seasonality; and so on.

Table 8.5: A two-way classification of exponential smoothing methods.

| Trend Component | Seasonal Component | | |
| --- | --- | --- | --- |
|  | N | A | M |
|  | (None) | (Additive) | (Multiplicative) |
| N (None) | (N,N) | (N,A) | (N,M) |
| A (Additive) | (A,N) | (A,A) | (A,M) |
| A\(_d\) (Additive damped) | (A\(_d\),N) | (A\(_d\),A) | (A\(_d\),M) |

Some of these methods we have already seen using other names:

| Short hand | Method |
| --- | --- |
| (N,N) | Simple exponential smoothing |
| (A,N) | Holt’s linear method |
| (A\(_d\),N) | Additive damped trend method |
| (A,A) | Additive Holt-Winters’ method |
| (A,M) | Multiplicative Holt-Winters’ method |
| (A\(_d\),M) | Holt-Winters’ damped method |

This type of classification was first proposed by Pegels ([1969](#ref-Pegels1969)), who also included a method with a multiplicative trend. It was later extended by Gardner ([1985](#ref-Gar1985)) to include methods with an additive damped trend and by J. W. Taylor ([2003](#ref-Taylor2003)) to include methods with a multiplicative damped trend. We do not consider the multiplicative trend methods in this book as they tend to produce poor forecasts. See Hyndman et al. ([2008](#ref-expsmooth08)) for a more thorough discussion of all exponential smoothing methods.

Table [8.6](https://otexts.com/fpp3/taxonomy.html#tab:pegels) gives the recursive formulas for applying the nine exponential smoothing methods in Table [8.5](https://otexts.com/fpp3/taxonomy.html#tab:taxonomy). Each cell includes the forecast equation for generating \(h\)-step-ahead forecasts, and the smoothing equations for applying the method.

Table 8.6:  Formulas for recursive calculations and point forecasts. In each case, \(\ell_t\) denotes the series level at time \(t\), \(b_t\) denotes the slope at time \(t\), \(s_t\) denotes the seasonal component of the series at time \(t\), and \(m\) denotes the number of seasons in a year; \(\alpha\), \(\beta^\*\), \(\gamma\) and \(\phi\) are smoothing parameters, \(\phi_h = \phi+\phi^2+\dots+\phi^{h}\), and \(k\) is the integer part of \((h-1)/m\).

|  |
| --- |
| ![](https://otexts.com/fpp3/figs/pegelstable-1.png) |

### Bibliography

Gardner, E. S. (1985). Exponential smoothing: The state of the art. *Journal of Forecasting*, *4*(1), 1–28.

Hyndman, R. J., Koehler, A. B., Ord, J. K., & Snyder, R. D. (2008). *Forecasting with exponential smoothing: The state space approach*. Springer-Verlag.

Pegels, C. C. (1969). Exponential forecasting: Some new variations. *Management Science*, *15*(5), 311–315.

Taylor, J. W. (2003). Exponential smoothing with a damped multiplicative trend. *International Journal of Forecasting*, *19*(4), 715–725.

## 8.5 Innovations state space models for exponential smoothing

In the rest of this chapter, we study the statistical models that underlie the exponential smoothing methods we have considered so far. The exponential smoothing methods presented in Table [8.6](https://otexts.com/fpp3/taxonomy.html#tab:pegels) are algorithms which generate point forecasts. The statistical models in this section generate the same point forecasts, but can also generate prediction (or forecast) intervals. A statistical model is a stochastic (or random) data generating process that can produce an entire forecast distribution. We will also describe how to use the model selection criteria introduced in Chapter [7](https://otexts.com/fpp3/regression.html#regression) to choose the model in an objective manner.

Each model consists of a measurement equation that describes the observed data, and some state equations that describe how the unobserved components or states (level, trend, seasonal) change over time. Hence, these are referred to as **state space models**.

For each method there exist two models: one with additive errors and one with multiplicative errors. The point forecasts produced by the models are identical if they use the same smoothing parameter values. They will, however, generate different prediction intervals.

To distinguish between a model with additive errors and one with multiplicative errors (and also to distinguish the models from the methods), we add a third letter to the classification of Table [8.5](https://otexts.com/fpp3/taxonomy.html#tab:taxonomy). We label each state space model as ETS(\(\cdot,\cdot,\cdot\)) for (Error, Trend, Seasonal). This label can also be thought of as ExponenTial Smoothing. Using the same notation as in Table [8.5](https://otexts.com/fpp3/taxonomy.html#tab:taxonomy), the possibilities for each component (or state) are: Error \(=\{\)A,M\(\}\), Trend \(=\{\)N,A,A\(_d\}\) and Seasonal \(=\{\)N,A,M\(\}\).

### ETS(A,N,N): simple exponential smoothing with additive errors

Recall the component form of simple exponential smoothing:
\[\begin{align\*}
\text{Forecast equation} && \hat{y}_{t+1|t} & = \ell_{t}\\
\text{Smoothing equation} && \ell_{t} & = \alpha y_{t} + (1 - \alpha)\ell_{t-1}.
\end{align\*}\]
If we re-arrange the smoothing equation for the level, we get the “error correction” form,
\[\begin{align\*}
\ell_{t} %&= \alpha y_{t}+\ell_{t-1}-\alpha\ell_{t-1}\\
&= \ell_{t-1}+\alpha( y_{t}-\ell_{t-1})\\
&= \ell_{t-1}+\alpha e_{t},
\end{align\*}\]
where \(e_{t}=y_{t}-\ell_{t-1}=y_{t}-\hat{y}_{t|t-1}\) is the residual at time \(t\).

The training data errors lead to the adjustment of the estimated level throughout the smoothing process for \(t=1,\dots,T\). For example, if the error at time \(t\) is negative, then \(y_t < \hat{y}_{t|t-1}\) and so the level at time \(t-1\) has been over-estimated. The new level \(\ell_t\) is then the previous level \(\ell_{t-1}\) adjusted downwards. The closer \(\alpha\) is to one, the “rougher” the estimate of the level (large adjustments take place). The smaller the \(\alpha\), the “smoother” the level (small adjustments take place).

We can also write \(y_t = \ell_{t-1} + e_t\), so that each observation can be represented by the previous level plus an error. To make this into an innovations state space model, all we need to do is specify the probability distribution for \(e_t\). For a model with additive errors, we assume that residuals (the one-step training errors) \(e_t\) are normally distributed white noise with mean 0 and variance \(\sigma^2\). A short-hand notation for this is \(e_t = \varepsilon_t\sim\text{NID}(0,\sigma^2)\); NID stands for “normally and independently distributed”.

Then the equations of the model can be written as
\[\begin{align}
y_t &= \ell_{t-1} + \varepsilon_t \tag{8.3}\\
\ell_t&=\ell_{t-1}+\alpha \varepsilon_t. \tag{8.4}
\end{align}\]
We refer to [(8.3)](https://otexts.com/fpp3/ets.html#eq:ann-1a) as the *measurement* (or observation) equation and [(8.4)](https://otexts.com/fpp3/ets.html#eq:ann-2a) as the *state* (or transition) equation. These two equations, together with the statistical distribution of the errors, form a fully specified statistical model. Specifically, these constitute an innovations state space model underlying simple exponential smoothing.

The term “innovations” comes from the fact that all equations use the same random error process, \(\varepsilon_t\). For the same reason, this formulation is also referred to as a “single source of error” model. There are alternative multiple source of error formulations which we do not present here.

The measurement equation shows the relationship between the observations and the unobserved states. In this case, observation \(y_t\) is a linear function of the level \(\ell_{t-1}\), the predictable part of \(y_t\), and the error \(\varepsilon_t\), the unpredictable part of \(y_t\). For other innovations state space models, this relationship may be nonlinear.

The state equation shows the evolution of the state through time. The influence of the smoothing parameter \(\alpha\) is the same as for the methods discussed earlier. For example, \(\alpha\) governs the amount of change in successive levels: high values of \(\alpha\) allow rapid changes in the level; low values of \(\alpha\) lead to smooth changes. If \(\alpha=0\), the level of the series does not change over time; if \(\alpha=1\), the model reduces to a random walk model, \(y_t=y_{t-1}+\varepsilon_t\). (See Section [9.1](https://otexts.com/fpp3/stationarity.html#stationarity) for a discussion of this model.)

### ETS(M,N,N): simple exponential smoothing with multiplicative errors

In a similar fashion, we can specify models with multiplicative errors by writing the one-step-ahead training errors as relative errors
\[
\varepsilon_t = \frac{y_t-\hat{y}_{t|t-1}}{\hat{y}_{t|t-1}}
\]
where \(\varepsilon_t \sim \text{NID}(0,\sigma^2)\). Substituting \(\hat{y}_{t|t-1}=\ell_{t-1}\) gives \(y_t = \ell_{t-1}+\ell_{t-1}\varepsilon_t\) and \(e_t = y_t - \hat{y}_{t|t-1} = \ell_{t-1}\varepsilon_t\).

Then we can write the multiplicative form of the state space model as
\[\begin{align\*}
y_t&=\ell_{t-1}(1+\varepsilon_t)\\
\ell_t&=\ell_{t-1}(1+\alpha \varepsilon_t).
\end{align\*}\]

### ETS(A,A,N): Holt’s linear method with additive errors

For this model, we assume that the one-step-ahead training errors are given by \(\varepsilon_t=y_t-\ell_{t-1}-b_{t-1} \sim \text{NID}(0,\sigma^2)\). Substituting this into the error correction equations for Holt’s linear method we obtain
\[\begin{align\*}
y_t&=\ell_{t-1}+b_{t-1}+\varepsilon_t\\
\ell_t&=\ell_{t-1}+b_{t-1}+\alpha \varepsilon_t\\
b_t&=b_{t-1}+\beta \varepsilon_t,
\end{align\*}\]
where for simplicity we have set \(\beta=\alpha \beta^\*\).

### ETS(M,A,N): Holt’s linear method with multiplicative errors

Specifying one-step-ahead training errors as relative errors such that
\[
\varepsilon_t=\frac{y_t-(\ell_{t-1}+b_{t-1})}{(\ell_{t-1}+b_{t-1})}
\]
and following an approach similar to that used above, the innovations state space model underlying Holt’s linear method with multiplicative errors is specified as
\[\begin{align\*}
y_t&=(\ell_{t-1}+b_{t-1})(1+\varepsilon_t)\\
\ell_t&=(\ell_{t-1}+b_{t-1})(1+\alpha \varepsilon_t)\\
b_t&=b_{t-1}+\beta(\ell_{t-1}+b_{t-1}) \varepsilon_t,
\end{align\*}\]

where again \(\beta=\alpha \beta^\*\) and \(\varepsilon_t \sim \text{NID}(0,\sigma^2)\).

### Other ETS models

In a similar fashion, we can write an innovations state space model for each of the exponential smoothing methods of Table [8.6](https://otexts.com/fpp3/taxonomy.html#tab:pegels). Table [8.7](https://otexts.com/fpp3/ets.html#tab:ssm) presents the equations for all of the models in the ETS framework.

Table 8.7:  State space equations for each of the models in the ETS framework.

|  |
| --- |
| ![](https://otexts.com/fpp3/figs/statespacemodels-1.png) |

## 8.6 Estimation and model selection

### Estimating ETS models

An alternative to estimating the parameters by minimising the sum of squared errors is to maximise the “likelihood”. The likelihood is the probability of the data arising from the specified model. Thus, a large likelihood is associated with a good model. For an additive error model, maximising the likelihood (assuming normally distributed errors) gives the same results as minimising the sum of squared errors. However, different results will be obtained for multiplicative error models. In this section, we will estimate the smoothing parameters \(\alpha\), \(\beta\), \(\gamma\) and \(\phi\), and the initial states \(\ell_0\), \(b_0\), \(s_0,s_{-1},\dots,s_{-m+1}\), by maximising the likelihood.

The possible values that the smoothing parameters can take are restricted. Traditionally, the parameters have been constrained to lie between 0 and 1 so that the equations can be interpreted as weighted averages. That is, \(0< \alpha,\beta^\*,\gamma^\*,\phi<1\). For the state space models, we have set \(\beta=\alpha\beta^\*\) and \(\gamma=(1-\alpha)\gamma^\*\). Therefore, the traditional restrictions translate to \(0< \alpha <1\), \(0 < \beta < \alpha\) and \(0< \gamma < 1-\alpha\). In practice, the damping parameter \(\phi\) is usually constrained further to prevent numerical difficulties in estimating the model. In the `fable` package, it is restricted so that \(0.8<\phi<0.98\).

Another way to view the parameters is through a consideration of the mathematical properties of the state space models. The parameters are constrained in order to prevent observations in the distant past having a continuing effect on current forecasts. This leads to some *admissibility* constraints on the parameters, which are usually (but not always) less restrictive than the traditional constraints region ([Hyndman et al., 2008, pp. 149–161](#ref-expsmooth08)). For example, for the ETS(A,N,N) model, the traditional parameter region is \(0< \alpha <1\) but the admissible region is \(0< \alpha <2\). For the ETS(A,A,N) model, the traditional parameter region is \(0<\alpha<1\) and \(0<\beta<\alpha\) but the admissible region is \(0<\alpha<2\) and \(0<\beta<4-2\alpha\).

### Model selection

A great advantage of the ETS statistical framework is that information criteria can be used for model selection. The AIC, AIC\(_{\text{c}}\) and BIC, introduced in Section [7.5](https://otexts.com/fpp3/selecting-predictors.html#selecting-predictors), can be used here to determine which of the ETS models is most appropriate for a given time series.

For ETS models, Akaike’s Information Criterion (AIC) is defined as
\[
\text{AIC} = -2\log(L) + 2k,
\]
where \(L\) is the likelihood of the model and \(k\) is the total number of parameters and initial states that have been estimated (including the residual variance).

The AIC corrected for small sample bias (AIC\(_\text{c}\)) is defined as
\[
\text{AIC}_{\text{c}} = \text{AIC} + \frac{2k(k+1)}{T-k-1},
\]
and the Bayesian Information Criterion (BIC) is
\[
\text{BIC} = \text{AIC} + k[\log(T)-2].
\]

Three of the combinations of (Error, Trend, Seasonal) can lead to numerical difficulties. Specifically, the models that can cause such instabilities are ETS(A,N,M), ETS(A,A,M), and ETS(A,A\(_d\),M), due to division by values potentially close to zero in the state equations. We normally do not consider these particular combinations when selecting a model.

Models with multiplicative errors are useful when the data are strictly positive, but are not numerically stable when the data contain zeros or negative values. Therefore, multiplicative error models will not be considered if the time series is not strictly positive. In that case, only the six fully additive models will be applied.

### Example: Domestic holiday tourist visitor nights in Australia

We now employ the ETS statistical framework to forecast Australian holiday tourism over the period 2016–2019. We let the `ETS()` function select the model by minimising the AICc.

```
aus_holidays <- tourism |>
  filter(Purpose == "Holiday") |>
  summarise(Trips = sum(Trips)/1e3)
fit <- aus_holidays |>
  model(ETS(Trips))
report(fit)
#> Series: Trips
#> Model: ETS(M,N,A)
#>   Smoothing parameters:
#>     alpha = 0.3484
#>     gamma = 1e-04
#>
#>   Initial states:
#>   l[0]    s[0]   s[-1]   s[-2] s[-3]
#>  9.727 -0.5376 -0.6884 -0.2934 1.519
#>
#>   sigma^2:  0.0022
#>
#>   AIC  AICc   BIC
#> 226.2 227.8 242.9
```

The model selected is ETS(M,N,A)
\[\begin{align\*}
y_{t} &= (\ell_{t-1}+s_{t-m})(1 + \varepsilon_t)\\
\ell_t &= \ell_{t-1} + \alpha(\ell_{t-1}+s_{t-m})\varepsilon_t\\
s_t &= s_{t-m} + \gamma(\ell_{t-1}+s_{t-m}) \varepsilon_t.
\end{align\*}\]

The parameter estimates are \(\hat\alpha= 0.3484\), and \(\hat\gamma=0.0001\). The output also returns the estimates for the initial states \(\ell_0\), \(s_{0}\), \(s_{-1}\), \(s_{-2}\) and \(s_{-3}.\) Compare these with the values obtained for the Holt-Winters method with additive seasonality presented in Table [8.3](https://otexts.com/fpp3/holt-winters.html#tab:tab75).

Figure [8.10](https://otexts.com/fpp3/ets-estimation.html#fig:MNAstates) shows the states over time, while Figure [8.12](https://otexts.com/fpp3/ets-forecasting.html#fig:MNAforecasts) shows point forecasts and prediction intervals generated from the model. The small values of \(\gamma\) indicate that the seasonal states change very little over time.

```
components(fit) |>
  autoplot() +
  labs(title = "ETS(M,N,A) components")
```

![Graphical representation of the estimated states over time.](https://otexts.com/fpp3/fpp_files/figure-html/MNAstates-1.png)

Figure 8.10: Graphical representation of the estimated states over time.

Because this model has multiplicative errors, the innovation residuals are not equivalent to the regular residuals (i.e., the one-step training errors). The innovation residuals are given by \(\hat{\varepsilon}_t\), while the regular residuals are defined as \(y_t - \hat{y}_{t|t-1}\). We can obtain both using the `augment()` function. They are plotted in Figure [8.11](https://otexts.com/fpp3/ets-estimation.html#fig:MNAresiduals).

![Residuals and one-step forecast errors from the ETS(M,N,A) model.](https://otexts.com/fpp3/fpp_files/figure-html/MNAresiduals-1.png)

Figure 8.11: Residuals and one-step forecast errors from the ETS(M,N,A) model.

### Bibliography

Hyndman, R. J., Koehler, A. B., Ord, J. K., & Snyder, R. D. (2008). *Forecasting with exponential smoothing: The state space approach*. Springer-Verlag.

## 8.7 Forecasting with ETS models

Point forecasts can be obtained from the models by iterating the equations for \(t=T+1,\dots,T+h\) and setting all \(\varepsilon_t=0\) for \(t>T\).

For example, for model ETS(M,A,N), \(y_{T+1} = (\ell_T + b_T )(1+ \varepsilon_{T+1}).\) Therefore \(\hat{y}_{T+1|T}=\ell_{T}+b_{T}.\) Similarly,
\[\begin{align\*}
y_{T+2} &= (\ell_{T+1} + b_{T+1})(1 + \varepsilon_{T+2})\\
&= \left[
(\ell_T + b_T) (1+ \alpha\varepsilon_{T+1}) +
b_T + \beta (\ell_T + b_T)\varepsilon_{T+1}
\right]
(1 + \varepsilon_{T+2}).
\end{align\*}\]
Therefore, \(\hat{y}_{T+2|T}= \ell_{T}+2b_{T},\) and so on. These forecasts are identical to the forecasts from Holt’s linear method, and also to those from model ETS(A,A,N). Thus, the point forecasts obtained from the method and from the two models that underlie the method are identical (assuming that the same parameter values are used). ETS point forecasts constructed in this way are equal to the means of the forecast distributions, except for the models with multiplicative seasonality ([Hyndman et al., 2008](#ref-expsmooth08)).

To obtain forecasts from an ETS model, we use the `forecast()` function from the `fable` package. This function will always return the means of the forecast distribution, even when they differ from these traditional point forecasts.

```
fit |>
  forecast(h = 8) |>
  autoplot(aus_holidays)+
  labs(title="Australian domestic tourism",
       y="Overnight trips (millions)")
```

![Forecasting Australian domestic overnight trips using an ETS(M,N,A) model.](https://otexts.com/fpp3/fpp_files/figure-html/MNAforecasts-1.png)

Figure 8.12: Forecasting Australian domestic overnight trips using an ETS(M,N,A) model.

### Prediction intervals

A big advantage of the statistical models is that prediction intervals can also be generated — something that cannot be done using the point forecasting methods alone. The prediction intervals will differ between models with additive and multiplicative methods.

For most ETS models, a prediction interval can be written as
\[
\hat{y}_{T+h|T} \pm c \sigma_h
\]
where \(c\) depends on the coverage probability, and \(\sigma_h^2\) is the forecast variance. Values for \(c\) were given in Table [5.1](https://otexts.com/fpp3/prediction-intervals.html#tab:pcmultipliers). For ETS models, formulas for \(\sigma_h^2\) can be complicated; the details are given in Chapter 6 of Hyndman et al. ([2008](#ref-expsmooth08)). In Table [8.8](https://otexts.com/fpp3/ets-forecasting.html#tab:pitable) we give the formulas for the additive ETS models, which are the simplest.

Table 8.8: Forecast variance expressions for each additive state space model, where \(\sigma^2\) is the residual variance, \(m\) is the seasonal period, and \(k\) is the integer part of \((h-1) /m\) (i.e., the number of complete years in the forecast period prior to time \(T+h\)).

| Model | Forecast variance: \(\sigma_h^2\) |
| --- | --- |
| (A,N,N) | \(\sigma_h^2 = \sigma^2\big[1 + \alpha^2(h-1)\big]\) |
| (A,A,N) | \(\sigma_h^2 = \sigma^2\Big[1 + (h-1)\big\{\alpha^2 + \alpha\beta h + \frac16\beta^2h(2h-1)\big\}\Big]\) |
| (A,A\(_d\),N) | \(\sigma_h^2 = \sigma^2\biggl[1 + \alpha^2(h-1) + \frac{\beta\phi h}{(1-\phi)^2} \left\{2\alpha(1-\phi) +\beta\phi\right\}\) |
|  | \(\mbox{} - \frac{\beta\phi(1-\phi^h)}{(1-\phi)^2(1-\phi^2)} \left\{ 2\alpha(1-\phi^2)+ \beta\phi(1+2\phi-\phi^h)\right\}\biggr]\) |
| (A,N,A) | \(\sigma_h^2 = \sigma^2\Big[1 + \alpha^2(h-1) + \gamma k(2\alpha+\gamma)\Big]\) |
| (A,A,A) | \(\sigma_h^2 = \sigma^2\Big[1 + (h-1)\big\{\alpha^2 + \alpha\beta h + \frac16\beta^2h(2h-1)\big\}\) |
|  | \(\mbox{} + \gamma k \big\{2\alpha+ \gamma + \beta m (k+1)\big\} \Big]\) |
| (A,A\(_d\),A) | \(\sigma_h^2 = \sigma^2\biggl[1 + \alpha^2(h-1) + \gamma k(2\alpha+\gamma)\) |
|  | \(\mbox{} +\frac{\beta\phi h}{(1-\phi)^2} \left\{2\alpha(1-\phi) + \beta\phi \right\}\) |
|  | \(\mbox{} - \frac{\beta\phi(1-\phi^h)}{(1-\phi)^2(1-\phi^2)} \left\{ 2\alpha(1-\phi^2)+ \beta\phi(1+2\phi-\phi^h)\right\}\) |
|  | \(\mbox{} + \frac{2\beta\gamma\phi}{(1-\phi)(1-\phi^m)}\left\{k(1-\phi^m) - \phi^m(1-\phi^{mk})\right\}\biggr]\) |

For a few ETS models, there are no known formulas for prediction intervals. In these cases, the `forecast()` function uses simulated future sample paths and computes prediction intervals from the percentiles of these simulated future paths.

### Bibliography

Hyndman, R. J., Koehler, A. B., Ord, J. K., & Snyder, R. D. (2008). *Forecasting with exponential smoothing: The state space approach*. Springer-Verlag.

## 8.8 Exercises

1. Consider the number of pigs slaughtered in Victoria, available in the `aus_livestock` dataset.

   1. Use the `ETS()` function to estimate the equivalent model for simple exponential smoothing. Find the optimal values of \(\alpha\) and \(\ell_0\), and generate forecasts for the next four months.
   2. Compute a 95% prediction interval for the first forecast using \(\hat{y} \pm 1.96s\) where \(s\) is the standard deviation of the residuals. Compare your interval with the interval produced by R.
2. Write your own function to implement simple exponential smoothing. The function should take arguments `y` (the time series), `alpha` (the smoothing parameter \(\alpha\)) and `level` (the initial level \(\ell_0\)). It should return the forecast of the next observation in the series. Does it give the same forecast as `ETS()`?
3. Modify your function from the previous exercise to return the sum of squared errors rather than the forecast of the next observation. Then use the `optim()` function to find the optimal values of \(\alpha\) and \(\ell_0\). Do you get the same values as the `ETS()` function?
4. Combine your previous two functions to produce a function that both finds the optimal values of \(\alpha\) and \(\ell_0\), and produces a forecast of the next observation in the series.
5. Data set `global_economy` contains the annual Exports from many countries. Select one country to analyse.

   1. Plot the Exports series and discuss the main features of the data.
   2. Use an ETS(A,N,N) model to forecast the series, and plot the forecasts.
   3. Compute the RMSE values for the training data.
   4. Compare the results to those from an ETS(A,A,N) model. (Remember that the trended model is using one more parameter than the simpler model.) Discuss the merits of the two forecasting methods for this data set.
   5. Compare the forecasts from both methods. Which do you think is best?
   6. Calculate a 95% prediction interval for the first forecast for each model, using the RMSE values and assuming normal errors. Compare your intervals with those produced using R.
6. Forecast the Chinese GDP from the `global_economy` data set using an ETS model. Experiment with the various options in the `ETS()` function to see how much the forecasts change with damped trend, or with a Box-Cox transformation. Try to develop an intuition of what each is doing to the forecasts.

   [Hint: use a relatively large value of `h` when forecasting, so you can clearly see the differences between the various options when plotting the forecasts.]
7. Find an ETS model for the Gas data from `aus_production` and forecast the next few years. Why is multiplicative seasonality necessary here? Experiment with making the trend damped. Does it improve the forecasts?
8. Recall your retail time series data (from Exercise 7 in Section [2.10](https://otexts.com/fpp3/graphics-exercises.html#graphics-exercises)).

   1. Why is multiplicative seasonality necessary for this series?
   2. Apply Holt-Winters’ multiplicative method to the data. Experiment with making the trend damped.
   3. Compare the RMSE of the one-step forecasts from the two methods. Which do you prefer?
   4. Check that the residuals from the best method look like white noise.
   5. Now find the test set RMSE, while training the model to the end of 2010. Can you beat the seasonal naïve approach from Exercise 7 in Section [5.11](https://otexts.com/fpp3/toolbox-exercises.html#toolbox-exercises)?
9. For the same retail data, try an STL decomposition applied to the Box-Cox transformed series, followed by ETS on the seasonally adjusted data. How does that compare with your best previous forecasts on the test set?
10. Compute the total domestic overnight trips across Australia from the `tourism` dataset.

    1. Plot the data and describe the main features of the series.
    2. Decompose the series using STL and obtain the seasonally adjusted data.
    3. Forecast the next two years of the series using an additive damped trend method applied to the seasonally adjusted data. (This can be specified using `decomposition_model()`.)
    4. Forecast the next two years of the series using an appropriate model for Holt’s linear method applied to the seasonally adjusted data (as before but without damped trend).
    5. Now use `ETS()` to choose a seasonal model for the data.
    6. Compare the RMSE of the ETS model with the RMSE of the models you obtained using STL decompositions. Which gives the better in-sample fits?
    7. Compare the forecasts from the three approaches? Which seems most reasonable?
    8. Check the residuals of your preferred model.
11. For this exercise use the quarterly number of arrivals to Australia from New Zealand, 1981 Q1 – 2012 Q3, from data set `aus_arrivals`.

    1. Make a time plot of your data and describe the main features of the series.
    2. Create a training set that withholds the last two years of available data. Forecast the test set using an appropriate model for Holt-Winters’ multiplicative method.
    3. Why is multiplicative seasonality necessary here?
    4. Forecast the two-year test set using each of the following methods:
       * an ETS model;
       * an additive ETS model applied to a log transformed series;
       * a seasonal naïve method;
       * an STL decomposition applied to the log transformed data followed by an ETS model applied to the seasonally adjusted (transformed) data.
    5. Which method gives the best forecasts? Does it pass the residual tests?
    6. Compare the same four methods using time series cross-validation instead of using a training and test set. Do you come to the same conclusions?
12. 1. Apply cross-validation techniques to produce 1 year ahead ETS and seasonal naïve forecasts for Portland cement production (from `aus_production`). Use a stretching data window with initial size of 5 years, and increment the window by one observation.
    2. Compute the MSE of the resulting \(4\)-step-ahead errors. Comment on which forecasts are more accurate. Is this what you expected?
13. Compare `ETS()`, `SNAIVE()` and `decomposition_model(STL, ???)` on the following five time series. You might need to use a Box-Cox transformation for the STL decomposition forecasts. Use a test set of three years to decide what gives the best forecasts.

    * Beer and bricks production from `aus_production`.
    * Cost of drug subsidies for diabetes (`ATC2 == "A10"`) and corticosteroids (`ATC2 == "H02"`) from `PBS`.
    * Total food retailing turnover for Australia from `aus_retail`.
14. 1. Use `ETS()` to select an appropriate model for the following series: total number of trips across Australia using `tourism`, the closing prices for the four stocks in `gafa_stock`, and the lynx series in `pelt`. Does it always give good forecasts?
    2. Find an example where it does not work well. Can you figure out why?
15. Show that the point forecasts from an ETS(M,A,M) model are the same as those obtained using Holt-Winters’ multiplicative method.
16. Show that the forecast variance for an ETS(A,N,N) model is given by
    \[
    \sigma^2\left[1+\alpha^2(h-1)\right].
    \]
17. Write down 95% prediction intervals for an ETS(A,N,N) model as a function of \(\ell_T\), \(\alpha\), \(h\) and \(\sigma\), assuming normally distributed errors.

## 8.9 Further reading

* Two articles by Ev Gardner ([Gardner, 1985](#ref-Gar1985), [2006](#ref-Gar2006)) provide a great overview of the history of exponential smoothing, and its many variations.
* A full book treatment of the subject providing the mathematical details is given by Hyndman et al. ([2008](#ref-expsmooth08)).

### Bibliography

Gardner, E. S. (1985). Exponential smoothing: The state of the art. *Journal of Forecasting*, *4*(1), 1–28.

Gardner, E. S. (2006). Exponential smoothing: The state of the art — Part II. *International Journal of Forecasting*, *22*, 637–666.

Hyndman, R. J., Koehler, A. B., Ord, J. K., & Snyder, R. D. (2008). *Forecasting with exponential smoothing: The state space approach*. Springer-Verlag.
