Source: https://otexts.com/fpp3/dynamic.html (chapter dynamic, 9 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - 10-dynamic-regression
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Chapter 10 Dynamic regression models

The time series models in the previous two chapters allow for the inclusion of information from past observations of a series, but not for the inclusion of other information that may also be relevant. For example, the effects of holidays, competitor activity, changes in the law, the wider economy, or other external variables, may explain some of the historical variation and may lead to more accurate forecasts. On the other hand, the regression models in Chapter [7](https://otexts.com/fpp3/regression.html#regression) allow for the inclusion of a lot of relevant information from predictor variables, but do not allow for the subtle time series dynamics that can be handled with ARIMA models. In this chapter, we consider how to extend ARIMA models in order to allow other information to be included in the models.

In Chapter [7](https://otexts.com/fpp3/regression.html#regression) we considered regression models of the form
\[
y_t = \beta_0 + \beta_1 x_{1,t} + \dots + \beta_k x_{k,t} + \varepsilon_t,
\]
where \(y_t\) is a linear function of the \(k\) predictor variables (\(x_{1,t},\dots,x_{k,t}\)), and \(\varepsilon_t\) is usually assumed to be an uncorrelated error term (i.e., it is white noise). We considered tests such as the Ljung-Box test for assessing whether the resulting residuals were significantly correlated.

In this chapter, we will allow the errors from a regression to contain autocorrelation. To emphasise this change in perspective, we will replace \(\varepsilon_t\) with \(\eta_t\) in the equation. The error series \(\eta_t\) is assumed to follow an ARIMA model. For example, if \(\eta_t\) follows an ARIMA(1,1,1) model, we can write
\[\begin{align\*}
y_t &= \beta_0 + \beta_1 x_{1,t} + \dots + \beta_k x_{k,t} + \eta_t,\\
& (1-\phi_1B)(1-B)\eta_t = (1+\theta_1B)\varepsilon_t,
\end{align\*}\]
where \(\varepsilon_t\) is a white noise series.

Notice that the model has two error terms here — the error from the regression model, which we denote by \(\eta_t\), and the error from the ARIMA model, which we denote by \(\varepsilon_t\). Only the ARIMA model errors are assumed to be white noise.

## 10.1 Estimation

When we estimate the parameters from the model, we need to minimise the sum of squared \(\varepsilon_t\) values. If we minimise the sum of squared \(\eta_t\) values instead (which is what would happen if we estimated the regression model ignoring the autocorrelations in the errors), then several problems arise.

1. The estimated coefficients \(\hat{\beta}_0,\dots,\hat{\beta}_k\) are no longer the best estimates, as some information has been ignored in the calculation;
2. Any statistical tests associated with the model (e.g., t-tests on the coefficients) will be incorrect.
3. The AICc values of the fitted models are no longer a good guide as to which is the best model for forecasting.
4. In most cases, the \(p\)-values associated with the coefficients will be too small, and so some predictor variables will appear to be important when they are not. This is known as “spurious regression”.

Minimising the sum of squared \(\varepsilon_t\) values avoids these problems. Alternatively, maximum likelihood estimation can be used; this will give similar estimates of the coefficients.

An important consideration when estimating a regression with ARMA errors is that all of the variables in the model must first be stationary. Thus, we first have to check that \(y_t\) and all of the predictors \((x_{1,t},\dots,x_{k,t})\) appear to be stationary. If we estimate the model when any of these are non-stationary, the estimated coefficients will not be consistent estimates (and therefore may not be meaningful). One exception to this is the case where non-stationary variables are co-integrated. If there exists a linear combination of the non-stationary \(y_t\) and the predictors that is stationary, then the estimated coefficients will be consistent.[21](#fn21)

We therefore first difference the non-stationary variables in the model. It is often desirable to maintain the form of the relationship between \(y_t\) and the predictors, and consequently it is common to difference all of the variables if any of them need differencing. The resulting model is then called a “model in differences”, as distinct from a “model in levels”, which is what is obtained when the original data are used without differencing.

If all of the variables in the model are stationary, then we only need to consider an ARMA process for the errors. It is easy to see that a regression model with ARIMA errors is equivalent to a regression model in differences with ARMA errors. For example, if the above regression model with ARIMA(1,1,1) errors is differenced we obtain the model
\[\begin{align\*}
y'_t &= \beta_1 x'_{1,t} + \dots + \beta_k x'_{k,t} + \eta'_t,\\
& (1-\phi_1B)\eta'_t = (1+\theta_1B)\varepsilon_t,
\end{align\*}\]
where \(y'_t=y_t-y_{t-1}\), \(x'_{t,i}=x_{t,i}-x_{t-1,i}\) and \(\eta'_t=\eta_t-\eta_{t-1}\), which is a regression model in differences with ARMA errors.

### Bibliography

Harris, R., & Sollis, R. (2003). *Applied time series modelling and forecasting*. John Wiley & Sons.

---

21. Forecasting with cointegrated models is discussed by Harris & Sollis ([2003](#ref-Harris03)).[↩︎](https://otexts.com/fpp3/estimation.html#fnref21)

## 10.2 Regression with ARIMA errors using `fable`

The function `ARIMA()` will fit a regression model with ARIMA errors if exogenous regressors are included in the formula. As introduced in Section [9.5](https://otexts.com/fpp3/non-seasonal-arima.html#non-seasonal-arima), the `pdq()` special specifies the order of the ARIMA error model. If differencing is specified, then the differencing is applied to all variables in the regression model before the model is estimated. For example, the command

```
ARIMA(y ~ x + pdq(1,1,0))
```

will fit the model \(y_t' = \beta_1 x'_t + \eta'_t\), where \(\eta'_t = \phi_1 \eta'_{t-1} + \varepsilon_t\) is an AR(1) error. This is equivalent to the model
\[
y_t = \beta_0 + \beta_1 x_t + \eta_t,
\]
where \(\eta_t\) is an ARIMA(1,1,0) error. Notice that the constant term disappears due to the differencing. To include a constant in the differenced model, we would add `1` to the model formula.

The `ARIMA()` function can also be used to select the best ARIMA model for the errors. This is done by not specifying the `pdq()` special. Whether differencing is required is determined by applying a KPSS test to the residuals from the regression model estimated using ordinary least squares. If differencing is required, then all variables are differenced and the model re-estimated using maximum likelihood estimation. The final model will be expressed in terms of the original variables, even if it has been estimated using differenced variables.

The AICc is calculated for the final model, and this value can be used to determine the best predictors. That is, the procedure should be repeated for all subsets of predictors to be considered, and the model with the lowest AICc value selected.

### Example: US Personal Consumption and Income

Figure [10.1](https://otexts.com/fpp3/regarima.html#fig:usconsump) shows the quarterly changes in personal consumption expenditure and personal disposable income from 1970 to 2019 Q2. We would like to forecast changes in expenditure based on changes in income. A change in income does not necessarily translate to an instant change in consumption (e.g., after the loss of a job, it may take a few months for expenses to be reduced to allow for the new circumstances). However, we will ignore this complexity in this example and try to measure the instantaneous effect of the average change of income on the average change of consumption expenditure.

```
us_change |>
  pivot_longer(c(Consumption, Income),
               names_to = "var", values_to = "value") |>
  ggplot(aes(x = Quarter, y = value)) +
  geom_line() +
  facet_grid(vars(var), scales = "free_y") +
  labs(title = "US consumption and personal income",
       y = "Quarterly % change")
```

![Percentage changes in quarterly personal consumption expenditure and personal disposable income for the USA, 1970 Q1 to 2019 Q2.](https://otexts.com/fpp3/fpp_files/figure-html/usconsump-1.png)

Figure 10.1: Percentage changes in quarterly personal consumption expenditure and personal disposable income for the USA, 1970 Q1 to 2019 Q2.

```
fit <- us_change |>
  model(ARIMA(Consumption ~ Income))
report(fit)
#> Series: Consumption
#> Model: LM w/ ARIMA(1,0,2) errors
#>
#> Coefficients:
#>          ar1      ma1     ma2  Income  intercept
#>       0.7070  -0.6172  0.2066  0.1976     0.5949
#> s.e.  0.1068   0.1218  0.0741  0.0462     0.0850
#>
#> sigma^2 estimated as 0.3113:  log likelihood=-163
#> AIC=338.1   AICc=338.5   BIC=357.8
```

The data are clearly already stationary (as we are considering percentage changes rather than raw expenditure and income), so there is no need for any differencing. The fitted model is
\[\begin{align\*}
y_t &= 0.595 +
0.198 x_t + \eta_t, \\
\eta_t &= 0.707 \eta_{t-1} + \varepsilon_t
-0.617 \varepsilon_{t-1} +
0.207 \varepsilon_{t-2},\\
\varepsilon_t &\sim \text{NID}(0,0.311).
\end{align\*}\]

We can recover estimates of both the \(\eta_t\) and \(\varepsilon_t\) series using the `residuals()` function.

```
bind_rows(
    `Regression residuals` =
        as_tibble(residuals(fit, type = "regression")),
    `ARIMA residuals` =
        as_tibble(residuals(fit, type = "innovation")),
    .id = "type"
  ) |>
  mutate(
    type = factor(type, levels=c(
      "Regression residuals", "ARIMA residuals"))
  ) |>
  ggplot(aes(x = Quarter, y = .resid)) +
  geom_line() +
  facet_grid(vars(type))
```

![Regression residuals ($\eta_t$) and ARIMA residuals ($\varepsilon_t$) from the fitted model.](https://otexts.com/fpp3/fpp_files/figure-html/usconsumpres-1.png)

Figure 10.2: Regression residuals (\(\eta_t\)) and ARIMA residuals (\(\varepsilon_t\)) from the fitted model.

It is the ARIMA estimated errors (the innovation residuals) that should resemble a white noise series.

```
fit |> gg_tsresiduals()
```

![The innovation residuals (i.e., the estimated ARIMA errors) are not significantly different from white noise.](https://otexts.com/fpp3/fpp_files/figure-html/usconsumpres2-1.png)

Figure 10.3: The innovation residuals (i.e., the estimated ARIMA errors) are not significantly different from white noise.

```
augment(fit) |>
  features(.innov, ljung_box, dof = 3, lag = 8)
#> # A tibble: 1 × 3
#>   .model                      lb_stat lb_pvalue
#>   <chr>                         <dbl>     <dbl>
#> 1 ARIMA(Consumption ~ Income)    5.21     0.391
```

## 10.3 Forecasting

To forecast using a regression model with ARIMA errors, we need to forecast the regression part of the model and the ARIMA part of the model, and combine the results. As with ordinary regression models, in order to obtain forecasts we first need to forecast the predictors. When the predictors are known into the future (e.g., calendar-related variables such as time, day-of-week, etc.), this is straightforward. But when the predictors are themselves unknown, we must either model them separately, or use assumed future values for each predictor.

### Example: US Personal Consumption and Income

We will calculate forecasts for the next eight quarters assuming that the future percentage changes in personal disposable income will be equal to the mean percentage change from the last forty years.

```
us_change_future <- new_data(us_change, 8) |>
  mutate(Income = mean(us_change$Income))
forecast(fit, new_data = us_change_future) |>
  autoplot(us_change) +
  labs(y = "Percentage change")
```

![Forecasts obtained from regressing the percentage change in consumption expenditure on the percentage change in disposable income, with an ARIMA(1,0,2) error model.](https://otexts.com/fpp3/fpp_files/figure-html/usconsump3-1.png)

Figure 10.4: Forecasts obtained from regressing the percentage change in consumption expenditure on the percentage change in disposable income, with an ARIMA(1,0,2) error model.

The prediction intervals for this model are narrower than if we had fitted an ARIMA model without covariates, because we are now able to explain some of the variation in the data using the income predictor.

It is important to realise that the prediction intervals from regression models (with or without ARIMA errors) do not take into account the uncertainty in the forecasts of the predictors. So they should be interpreted as being conditional on the assumed (or estimated) future values of the predictor variables.

### Example: Forecasting electricity demand

Daily electricity demand can be modelled as a function of temperature. As can be observed on an electricity bill, more electricity is used on cold days due to heating and hot days due to air conditioning. The higher demand on cold and hot days is reflected in the U-shape of Figure [10.5](https://otexts.com/fpp3/forecasting.html#fig:elecscatter), where daily demand is plotted versus daily maximum temperature.

```
vic_elec_daily <- vic_elec |>
  filter(year(Time) == 2014) |>
  index_by(Date = date(Time)) |>
  summarise(
    Demand = sum(Demand) / 1e3,
    Temperature = max(Temperature),
    Holiday = any(Holiday)
  ) |>
  mutate(Day_Type = case_when(
    Holiday ~ "Holiday",
    wday(Date) %in% 2:6 ~ "Weekday",
    TRUE ~ "Weekend"
  ))

vic_elec_daily |>
  ggplot(aes(x = Temperature, y = Demand, colour = Day_Type)) +
  geom_point() +
  labs(y = "Electricity demand (GW)",
       x = "Maximum daily temperature")
```

![Daily electricity demand versus maximum daily temperature for the state of Victoria in Australia for 2014.](https://otexts.com/fpp3/fpp_files/figure-html/elecscatter-1.png)

Figure 10.5: Daily electricity demand versus maximum daily temperature for the state of Victoria in Australia for 2014.

The data stored as `vic_elec_daily` includes total daily demand, daily maximum temperatures, and an indicator variable for if that day is a public holiday. Figure [10.6](https://otexts.com/fpp3/forecasting.html#fig:electime) shows the time series of both daily demand and daily maximum temperatures. The plots highlight the need for both a non-linear and a dynamic model.

```
vic_elec_daily |>
  pivot_longer(c(Demand, Temperature)) |>
  ggplot(aes(x = Date, y = value)) +
  geom_line() +
  facet_grid(name ~ ., scales = "free_y") + ylab("")
```

![Daily electricity demand and maximum daily temperature for the state of Victoria in Australia for 2014.](https://otexts.com/fpp3/fpp_files/figure-html/electime-1.png)

Figure 10.6: Daily electricity demand and maximum daily temperature for the state of Victoria in Australia for 2014.

In this example, we fit a quadratic regression model with ARMA errors using the `ARIMA()` function. The model also includes an indicator variable for if the day was a working day or not.

```
fit <- vic_elec_daily |>
  model(ARIMA(Demand ~ Temperature + I(Temperature^2) +
                (Day_Type == "Weekday")))
fit |> gg_tsresiduals()
```

![Residuals diagnostics for a dynamic regression model for daily electricity demand with workday and quadratic temperature effects.](https://otexts.com/fpp3/fpp_files/figure-html/elecdailyfit-1.png)

Figure 10.7: Residuals diagnostics for a dynamic regression model for daily electricity demand with workday and quadratic temperature effects.

The fitted model has an ARIMA(2,1,2)(2,0,0)[7] error, so there are 6 AR and MA coefficients.

```
augment(fit) |>
  features(.innov, ljung_box, dof = 6, lag = 14)
#> # A tibble: 1 × 3
#>   .model                                                     lb_stat lb_pvalue
#>   <chr>                                                        <dbl>     <dbl>
#> 1 "ARIMA(Demand ~ Temperature + I(Temperature^2) + (Day_Typ…    28.4  0.000404
```

There is clear heteroscedasticity in the residuals, with higher variance in January and February, and lower variance in May. The model also has some significant autocorrelation in the residuals, and the histogram of the residuals shows long tails. All of these issues with the residuals may affect the coverage of the prediction intervals, but the point forecasts should still be ok.

Using the estimated model we forecast 14 days ahead starting from Thursday 1 January 2015 (a non-work-day being a public holiday for New Years Day). In this case, we could obtain weather forecasts from the weather bureau for the next 14 days. But for the sake of illustration, we will use scenario based forecasting (as introduced in Section [7.6](https://otexts.com/fpp3/forecasting-regression.html#forecasting-regression)) where we set the temperature for the next 14 days to a constant 26 degrees.

```
vic_elec_future <- new_data(vic_elec_daily, 14) |>
  mutate(
    Temperature = 26,
    Holiday = c(TRUE, rep(FALSE, 13)),
    Day_Type = case_when(
      Holiday ~ "Holiday",
      wday(Date) %in% 2:6 ~ "Weekday",
      TRUE ~ "Weekend"
    )
  )
forecast(fit, vic_elec_future) |>
  autoplot(vic_elec_daily) +
  labs(title="Daily electricity demand: Victoria",
       y="GW")
```

![Forecasts from the dynamic regression model for daily electricity demand. All future temperatures have been set to 26 degrees, and the working day dummy variable has been set to known future values.](https://otexts.com/fpp3/fpp_files/figure-html/elecdailyfc-1.png)

Figure 10.8: Forecasts from the dynamic regression model for daily electricity demand. All future temperatures have been set to 26 degrees, and the working day dummy variable has been set to known future values.

The point forecasts look reasonable for the first two weeks of 2015. The slow down in electricity demand at the end of 2014 (due to many people taking summer vacations) has caused the forecasts for the next two weeks to show similarly low demand values.

## 10.4 Stochastic and deterministic trends

There are two different ways of modelling a linear trend. A *deterministic trend* is obtained using the regression model
\[
y_t = \beta_0 + \beta_1 t + \eta_t,
\]
where \(\eta_t\) is an ARMA process. A *stochastic trend* is obtained using the model
\[
y_t = \beta_0 + \beta_1 t + \eta_t,
\]
where \(\eta_t\) is an ARIMA process with \(d=1\). In the latter case, we can difference both sides so that \(y_t' = \beta_1 + \eta_t'\), where \(\eta_t'\) is an ARMA process. In other words,
\[
y_t = y_{t-1} + \beta_1 + \eta_t'.
\]
This is similar to a random walk with drift (introduced in Section [9.1](https://otexts.com/fpp3/stationarity.html#stationarity)), but here the error term is an ARMA process rather than simply white noise.

Although these models appear quite similar (they only differ in the number of differences that need to be applied to \(\eta_t\)), their forecasting characteristics are quite different.

### Example: Air transport passengers Australia

```
aus_airpassengers |>
  autoplot(Passengers) +
  labs(y = "Passengers (millions)",
       title = "Total annual air passengers")
```

![Total annual passengers (in millions) for Australian air carriers, 1970--2016.](https://otexts.com/fpp3/fpp_files/figure-html/austa-1.png)

Figure 10.9: Total annual passengers (in millions) for Australian air carriers, 1970–2016.

Figure [10.9](https://otexts.com/fpp3/stochastic-and-deterministic-trends.html#fig:austa) shows the total number of passengers for Australian air carriers each year from 1970 to 2016. We will fit both a deterministic and a stochastic trend model to these data.

The deterministic trend model is obtained as follows:

```
fit_deterministic <- aus_airpassengers |>
  model(deterministic = ARIMA(Passengers ~ 1 + trend() +
                                pdq(d = 0)))
report(fit_deterministic)
#> Series: Passengers
#> Model: LM w/ ARIMA(1,0,0) errors
#>
#> Coefficients:
#>          ar1  trend()  intercept
#>       0.9564   1.4151     0.9014
#> s.e.  0.0362   0.1972     7.0751
#>
#> sigma^2 estimated as 4.343:  log likelihood=-100.88
#> AIC=209.77   AICc=210.72   BIC=217.17
```

This model can be written as
\[\begin{align\*}
y_t &= 0.901 + 1.415 t + \eta_t \\
\eta_t &= 0.956 \eta_{t-1} + \varepsilon_t\\
\varepsilon_t &\sim \text{NID}(0,4.343).
\end{align\*}\]

The estimated growth in visitor numbers is 1.42 million people per year.

Alternatively, the stochastic trend model can be estimated.

```
fit_stochastic <- aus_airpassengers |>
  model(stochastic = ARIMA(Passengers ~ pdq(d = 1)))
report(fit_stochastic)
#> Series: Passengers
#> Model: ARIMA(0,1,0) w/ drift
#>
#> Coefficients:
#>       constant
#>         1.4191
#> s.e.    0.3014
#>
#> sigma^2 estimated as 4.271:  log likelihood=-98.16
#> AIC=200.31   AICc=200.59   BIC=203.97
```

This model can be written as \(y_t-y_{t-1} = 1.419 + \varepsilon_t\), or equivalently
\[\begin{align\*}
y_t &= y_0 + 1.419 t + \eta_t \\
\eta_t &= \eta_{t-1} + \varepsilon_{t}\\
\varepsilon_t &\sim \text{NID}(0,4.271).
\end{align\*}\]

In this case, the estimated growth in visitor numbers is also 1.42 million people per year. Although the growth estimates are similar, the prediction intervals are not, as Figure [10.10](https://otexts.com/fpp3/stochastic-and-deterministic-trends.html#fig:austaf) shows. In particular, stochastic trends have much wider prediction intervals because the errors are non-stationary.

```
aus_airpassengers |>
  autoplot(Passengers) +
  autolayer(fit_stochastic |> forecast(h = 20),
    colour = "#0072B2", level = 95) +
  autolayer(fit_deterministic |> forecast(h = 20),
    colour = "#D55E00", alpha = 0.65, level = 95) +
  labs(y = "Air passengers (millions)",
       title = "Forecasts from trend models")
```

![Forecasts of annual passengers for Australian air carriers using a deterministic trend model (orange) and a stochastic trend model (blue).](https://otexts.com/fpp3/fpp_files/figure-html/austaf-1.png)

Figure 10.10: Forecasts of annual passengers for Australian air carriers using a deterministic trend model (orange) and a stochastic trend model (blue).

There is an implicit assumption with deterministic trends that the slope of the trend is not going to change over time. On the other hand, stochastic trends can change, and the estimated growth is only assumed to be the average growth over the historical period, not necessarily the rate of growth that will be observed into the future. Consequently, it is safer to forecast with stochastic trends, especially for longer forecast horizons, as the prediction intervals allow for greater uncertainty in future growth.

## 10.5 Dynamic harmonic regression

When there are long seasonal periods, a dynamic regression with Fourier terms is often better than other models we have considered in this book.[22](#fn22)

For example, daily data can have annual seasonality of length 365, weekly data has seasonal period of approximately 52, while half-hourly data can have several seasonal periods, the shortest of which is the daily pattern of period 48.

Seasonal versions of ARIMA and ETS models are designed for shorter periods such as 12 for monthly data or 4 for quarterly data. The `ETS()` model restricts seasonality to be a maximum period of 24 to allow hourly data but not data with a larger seasonal period. The problem is that there are \(m-1\) parameters to be estimated for the initial seasonal states where \(m\) is the seasonal period. So for large \(m\), the estimation becomes almost impossible.

The `ARIMA()` function will allow a seasonal period up to \(m=350\), but in practice will usually run out of memory whenever the seasonal period is more than about 200. In any case, seasonal differencing of high order does not make a lot of sense — for daily data it involves comparing what happened today with what happened exactly a year ago and there is no constraint that the seasonal pattern is smooth.

So for such time series, we prefer a harmonic regression approach where the seasonal pattern is modelled using Fourier terms with short-term time series dynamics handled by an ARMA error.

The advantages of this approach are:

* it allows any length seasonality;
* for data with more than one seasonal period, Fourier terms of different frequencies can be included;
* the smoothness of the seasonal pattern can be controlled by \(K\), the number of Fourier sin and cos pairs – the seasonal pattern is smoother for smaller values of \(K\);
* the short-term dynamics are easily handled with a simple ARMA error.

The only real disadvantage (compared to a seasonal ARIMA model) is that the seasonality is assumed to be fixed — the seasonal pattern is not allowed to change over time. But in practice, seasonality is usually remarkably constant so this is not a big disadvantage except for long time series.

### Example: Australian eating out expenditure

In this example we demonstrate combining Fourier terms for capturing seasonality with ARIMA errors capturing other dynamics in the data. For simplicity, we will use an example with monthly data. The same modelling approach using weekly data is discussed in Section [13.1](https://otexts.com/fpp3/weekly.html#weekly).

We use the total monthly expenditure on cafes, restaurants and takeaway food services in Australia ($billion) from 2004 up to 2018 and forecast 24 months ahead. We vary \(K\), the number of Fourier sin and cos pairs, from \(K=1\) to \(K=6\) (which is equivalent to including seasonal dummies). Figure [10.11](https://otexts.com/fpp3/dhr.html#fig:eatout) shows the seasonal pattern projected forward as \(K\) increases. Notice that as \(K\) increases the Fourier terms capture and project a more “wiggly” seasonal pattern and simpler ARIMA models are required to capture other dynamics. The AICc value is minimised for \(K=6\), with a significant jump going from \(K=4\) to \(K=5\), hence the forecasts generated from this model would be the ones used.

```
aus_cafe <- aus_retail |>
  filter(
    Industry == "Cafes, restaurants and takeaway food services",
    year(Month) %in% 2004:2018
  ) |>
  summarise(Turnover = sum(Turnover))

fit <- model(aus_cafe,
  `K = 1` = ARIMA(log(Turnover) ~ fourier(K=1) + PDQ(0,0,0)),
  `K = 2` = ARIMA(log(Turnover) ~ fourier(K=2) + PDQ(0,0,0)),
  `K = 3` = ARIMA(log(Turnover) ~ fourier(K=3) + PDQ(0,0,0)),
  `K = 4` = ARIMA(log(Turnover) ~ fourier(K=4) + PDQ(0,0,0)),
  `K = 5` = ARIMA(log(Turnover) ~ fourier(K=5) + PDQ(0,0,0)),
  `K = 6` = ARIMA(log(Turnover) ~ fourier(K=6) + PDQ(0,0,0))
)

fit |>
  forecast(h = "2 years") |>
  autoplot(aus_cafe, level = 95) +
  facet_wrap(vars(.model), ncol = 2) +
  guides(colour = "none", fill = "none", level = "none") +
  geom_label(
    aes(x = yearmonth("2007 Jan"), y = 4250,
        label = paste0("AICc = ", format(AICc))),
    data = glance(fit)
  ) +
  labs(title= "Total monthly eating-out expenditure",
       y="$ billions")
```

![Using Fourier terms and ARIMA errors for forecasting monthly expenditure on eating out in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/eatout-1.png)

Figure 10.11: Using Fourier terms and ARIMA errors for forecasting monthly expenditure on eating out in Australia.

### Bibliography

Young, P. C., Pedregal, D. J., & Tych, W. (1999). Dynamic harmonic regression. *Journal of Forecasting*, *18*, 369–394.

---

22. The term “dynamic harmonic regression” is also used for a harmonic regression with time-varying parameters ([Young et al., 1999](#ref-DHR99)).[↩︎](https://otexts.com/fpp3/dhr.html#fnref22)

## 10.6 Lagged predictors

Sometimes, the impact of a predictor that is included in a regression model will not be simple and immediate. For example, an advertising campaign may impact sales for some time beyond the end of the campaign, and sales in one month will depend on the advertising expenditure in each of the past few months. Similarly, a change in a company’s safety policy may reduce accidents immediately, but have a diminishing effect over time as employees take less care when they become familiar with the new working conditions.

In these situations, we need to allow for lagged effects of the predictor. Suppose that we have only one predictor in our model. Then a model which allows for lagged effects can be written as
\[
y_t = \beta_0 + \gamma_0x_t + \gamma_1 x_{t-1} + \dots + \gamma_k x_{t-k} + \eta_t,
\]
where \(\eta_t\) is an ARIMA process. The value of \(k\) can be selected using the AICc, along with the values of \(p\) and \(q\) for the ARIMA error.

### Example: TV advertising and insurance quotations

A US insurance company advertises on national television in an attempt to increase the number of insurance quotations provided (and consequently the number of new policies). Figure [10.12](https://otexts.com/fpp3/lagged-predictors.html#fig:tvadvert) shows the number of quotations and the expenditure on television advertising for the company each month from January 2002 to April 2005.

```
insurance |>
  pivot_longer(Quotes:TVadverts) |>
  ggplot(aes(x = Month, y = value)) +
  geom_line() +
  facet_grid(vars(name), scales = "free_y") +
  labs(y = "", title = "Insurance advertising and quotations")
```

![Numbers of insurance quotations provided per month and the expenditure on advertising per month.](https://otexts.com/fpp3/fpp_files/figure-html/tvadvert-1.png)

Figure 10.12: Numbers of insurance quotations provided per month and the expenditure on advertising per month.

We will consider including advertising expenditure for up to four months; that is, the model may include advertising expenditure in the current month, and the three months before that. When comparing models, it is important that they all use the same training set. In the following code, we exclude the first three months in order to make fair comparisons.

```
fit <- insurance |>
  # Restrict data so models use same fitting period
  mutate(Quotes = c(NA, NA, NA, Quotes[4:40])) |>
  # Estimate models
  model(
    lag0 = ARIMA(Quotes ~ pdq(d = 0) + TVadverts),
    lag1 = ARIMA(Quotes ~ pdq(d = 0) +
                 TVadverts + lag(TVadverts)),
    lag2 = ARIMA(Quotes ~ pdq(d = 0) +
                 TVadverts + lag(TVadverts) +
                 lag(TVadverts, 2)),
    lag3 = ARIMA(Quotes ~ pdq(d = 0) +
                 TVadverts + lag(TVadverts) +
                 lag(TVadverts, 2) + lag(TVadverts, 3))
  )
```

Next we choose the optimal lag length for advertising based on the AICc.

```
glance(fit)
#> # A tibble: 4 × 8
#>   .model sigma2 log_lik   AIC  AICc   BIC ar_roots  ma_roots
#>   <chr>   <dbl>   <dbl> <dbl> <dbl> <dbl> <list>    <list>
#> 1 lag0    0.265   -28.3  66.6  68.3  75.0 <cpl [2]> <cpl [0]>
#> 2 lag1    0.209   -24.0  58.1  59.9  66.5 <cpl [1]> <cpl [1]>
#> 3 lag2    0.215   -24.0  60.0  62.6  70.2 <cpl [1]> <cpl [1]>
#> 4 lag3    0.206   -22.2  60.3  65.0  73.8 <cpl [1]> <cpl [1]>
```

The best model (with the smallest AICc value) is `lag1` with two predictors; that is, it includes advertising only in the current month and the previous month. So we now re-estimate that model, but using all the available data.

```
fit_best <- insurance |>
  model(ARIMA(Quotes ~ pdq(d = 0) +
              TVadverts + lag(TVadverts)))
report(fit_best)
#> Series: Quotes
#> Model: LM w/ ARIMA(1,0,2) errors
#>
#> Coefficients:
#>          ar1     ma1     ma2  TVadverts  lag(TVadverts)  intercept
#>       0.5123  0.9169  0.4591     1.2527          0.1464     2.1554
#> s.e.  0.1849  0.2051  0.1895     0.0588          0.0531     0.8595
#>
#> sigma^2 estimated as 0.2166:  log likelihood=-23.94
#> AIC=61.88   AICc=65.38   BIC=73.7
```

The chosen model has ARIMA(1,0,2) errors. The model can be written as
\[
y_t = 2.155 +
1.253 x_t +
0.146 x_{t-1} + \eta_t,
\]
where \(y_t\) is the number of quotations provided in month \(t\), \(x_t\) is the advertising expenditure in month \(t\),
\[
\eta_t = 0.512 \eta_{t-1} +
\varepsilon_t +
0.917 \varepsilon_{t-1} +
0.459 \varepsilon_{t-2},
\]
and \(\varepsilon_t\) is white noise.

We can calculate forecasts using this model if we assume future values for the advertising variable. If we set the future monthly advertising to 8 units, we get the forecasts in Figure [10.13](https://otexts.com/fpp3/lagged-predictors.html#fig:tvadvertf8).

```
insurance_future <- new_data(insurance, 20) |>
  mutate(TVadverts = 8)
fit_best |>
  forecast(insurance_future) |>
  autoplot(insurance) +
  labs(
    y = "Quotes",
    title = "Forecast quotes with future advertising set to 8"
  )
```

![Forecasts of monthly insurance quotes, assuming that the future advertising expenditure is 8 units in each future month.](https://otexts.com/fpp3/fpp_files/figure-html/tvadvertf8-1.png)

Figure 10.13: Forecasts of monthly insurance quotes, assuming that the future advertising expenditure is 8 units in each future month.

## 10.7 Exercises

1. This exercise uses data set `LakeHuron` giving the level of Lake Huron from 1875–1972.

   1. Convert the data to a tsibble object using the `as_tsibble()` function.
   2. Fit a piecewise linear trend model to the Lake Huron data with a knot at 1920 and an ARMA error structure.
   3. Forecast the level for the next 30 years. Do you think the extrapolated linear trend is realistic?
2. Repeat Exercise 4 from Section [7.10](https://otexts.com/fpp3/regression-exercises.html#regression-exercises), but this time adding in ARIMA errors to address the autocorrelations in the residuals.

   1. How much difference does the ARIMA error process make to the regression coefficients?
   2. How much difference does the ARIMA error process make to the forecasts?
   3. Check the residuals of the fitted model to ensure the ARIMA process has adequately addressed the autocorrelations seen in the `TSLM` model.
3. Repeat the daily electricity example, but instead of using a quadratic function of temperature, use a piecewise linear function with the “knot” around 25 degrees Celsius (use predictors `Temperature` & `Temp2`). How can you optimise the choice of knot?

   The data can be created as follows.

   ```
   vic_elec_daily <- vic_elec |>
     filter(year(Time) == 2014) |>
     index_by(Date = date(Time)) |>
     summarise(
       Demand = sum(Demand)/1e3,
       Temperature = max(Temperature),
       Holiday = any(Holiday)) |>
     mutate(
       Temp2 = I(pmax(Temperature-25,0)),
       Day_Type = case_when(
         Holiday ~ "Holiday",
         wday(Date) %in% 2:6 ~ "Weekday",
         TRUE ~ "Weekend"))
   ```
4. This exercise concerns `aus_accommodation`: the total quarterly takings from accommodation and the room occupancy level for hotels, motels, and guest houses in Australia, between January 1998 and June 2016. Total quarterly takings are in millions of Australian dollars.

   1. Compute the CPI-adjusted takings and plot the result for each state
   2. For each state, fit a dynamic regression model of CPI-adjusted takings with seasonal dummy variables, a piecewise linear time trend with one knot at 2008 Q1, and ARIMA errors.
   3. Check that the residuals of the model look like white noise.
   4. Forecast the takings for each state to the end of 2017. (Hint: You will need to produce forecasts of the CPI first.)
   5. What sources of uncertainty have not been taken into account in the prediction intervals?
5. We fitted a harmonic regression model to part of the `us_gasoline` series in Exercise 5 in Section [7.10](https://otexts.com/fpp3/regression-exercises.html#regression-exercises). We will now revisit this model, and extend it to include more data and ARMA errors.

   1. Using `TSLM()`, fit a harmonic regression with a piecewise linear time trend to the full series. Select the position of the knots in the trend and the appropriate number of Fourier terms to include by minimising the AICc or CV value.
   2. Now refit the model using `ARIMA()` to allow for correlated errors, keeping the same predictor variables as you used with `TSLM()`.
   3. Check the residuals of the final model using the `gg_tsresiduals()` function and a Ljung-Box test. Do they look sufficiently like white noise to continue? If not, try modifying your model, or removing the first few years of data.
   4. Once you have a model with white noise residuals, produce forecasts for the next year.
6. Electricity consumption is often modelled as a function of temperature. Temperature is measured by daily heating degrees and cooling degrees. Heating degrees is \(18^\circ\)C minus the average daily temperature when the daily average is below \(18^\circ\)C; otherwise it is zero. This provides a measure of our need to heat ourselves as temperature falls. Cooling degrees measures our need to cool ourselves as the temperature rises. It is defined as the average daily temperature minus \(18^\circ\)C when the daily average is above \(18^\circ\)C; otherwise it is zero. Let \(y_t\) denote the monthly total of kilowatt-hours of electricity used, let \(x_{1,t}\) denote the monthly total of heating degrees, and let \(x_{2,t}\) denote the monthly total of cooling degrees.

   An analyst fits the following model to a set of such data:
   \[y^\*_t = \beta_1x^\*_{1,t} + \beta_2x^\*_{2,t} + \eta_t,\]
   where
   \[(1-\Phi_{1}B^{12} - \Phi_{2}B^{24})(1-B)(1-B^{12})\eta_t = (1+\theta_1 B)\varepsilon_t\]
   and \(y^\*_t = \log(y_t)\), \(x^\*_{1,t} = \sqrt{x_{1,t}}\) and \(x^\*_{2,t}=\sqrt{x_{2,t}}\).

   1. What sort of ARIMA model is identified for \(\eta_t\)?
   2. The estimated coefficients are

   | Parameter | Estimate | s.e. | \(Z\) | \(P\)-value |
   | --- | --- | --- | --- | --- |
   | \(\beta_1\) | 0.0077 | 0.0015 | 4.98 | 0.000 |
   | \(\beta_2\) | 0.0208 | 0.0023 | 9.23 | 0.000 |
   | \(\theta_1\) | -0.5830 | 0.0720 | 8.10 | 0.000 |
   | \(\Phi_{1}\) | -0.5373 | 0.0856 | -6.27 | 0.000 |
   | \(\Phi_{2}\) | -0.4667 | 0.0862 | -5.41 | 0.000 |

   Explain what the estimates of \(\beta_1\) and \(\beta_2\) tell us about electricity consumption.

   c. Write the equation in a form more suitable for forecasting.

   d. Describe how this model could be used to forecast electricity demand for the next 12 months.

   e. Explain why the \(\eta_t\) term should be modelled with an ARIMA model rather than modelling the data using a standard regression package. In your discussion, comment on the properties of the estimates, the validity of the standard regression results, and the importance of the \(\eta_t\) model in producing forecasts.
7. For the retail time series considered in earlier chapters:

   1. Develop an appropriate dynamic regression model with Fourier terms for the seasonality. Use the AICc to select the number of Fourier terms to include in the model. (You will probably need to use the same Box-Cox transformation you identified previously.)
   2. Check the residuals of the fitted model. Does the residual series look like white noise?
   3. Compare the forecasts with those you obtained earlier using alternative models.

## 10.8 Further reading

* A detailed discussion of dynamic regression models is provided in Pankratz ([1991](#ref-Pankratz91)).
* A generalisation of dynamic regression models, known as “transfer function models”, is discussed in Box et al. ([2015](#ref-BJRL15)).

### Bibliography

Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). *Time series analysis: Forecasting and control* (5th ed). John Wiley & Sons.

Pankratz, A. E. (1991). *Forecasting with dynamic regression models*. John Wiley & Sons.
