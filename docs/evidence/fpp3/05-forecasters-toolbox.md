Source: https://otexts.com/fpp3/toolbox.html (chapter toolbox, 13 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - 05-forecasters-toolbox
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Chapter 5 The forecaster’s toolbox

In this chapter, we discuss some general tools that are useful for many different forecasting situations. We will describe some benchmark forecasting methods, procedures for checking whether a forecasting method has adequately utilised the available information, techniques for computing prediction intervals, and methods for evaluating forecast accuracy.

Each of the tools discussed in this chapter will be used repeatedly in subsequent chapters as we develop and explore a range of forecasting methods.

## 5.1 A tidy forecasting workflow

The process of producing forecasts for time series data can be broken down into a few steps.

![](https://otexts.com/fpp3/fpp_files/figure-html/workflow-1.png)

To illustrate the process, we will fit linear trend models to national GDP data stored in `global_economy`.

### Data preparation (tidy)

The first step in forecasting is to prepare data in the correct format. This process may involve loading in data, identifying missing values, filtering the time series, and other pre-processing tasks. The functionality provided by `tsibble` and other packages in the `tidyverse` substantially simplifies this step.

Many models have different data requirements; some require the series to be in time order, others require no missing values. Checking your data is an essential step to understanding its features and should always be done before models are estimated.

We will model GDP per capita over time; so first, we must compute the relevant variable.

```
gdppc <- global_economy |>
  mutate(GDP_per_capita = GDP / Population)
```

### Plot the data (visualise)

As we have seen in Chapter [2](https://otexts.com/fpp3/graphics.html#graphics), visualisation is an essential step in understanding the data. Looking at your data allows you to identify common patterns, and subsequently specify an appropriate model.

The data for one country in our example are plotted in Figure [5.1](https://otexts.com/fpp3/a-tidy-forecasting-workflow.html#fig:swedengdp).

```
gdppc |>
  filter(Country == "Sweden") |>
  autoplot(GDP_per_capita) +
  labs(y = "$US", title = "GDP per capita for Sweden")
```

![GDP per capita data for Sweden from 1960 to 2017.](https://otexts.com/fpp3/fpp_files/figure-html/swedengdp-1.png)

Figure 5.1: GDP per capita data for Sweden from 1960 to 2017.

### Define a model (specify)

There are many different time series models that can be used for forecasting, and much of this book is dedicated to describing various models. Specifying an appropriate model for the data is essential for producing appropriate forecasts.

Models in `fable` are specified using model functions, which each use a formula (`y ~ x`) interface. The response variable(s) are specified on the left of the formula, and the structure of the model is written on the right.

For example, a linear trend model (to be discussed in Chapter [7](https://otexts.com/fpp3/regression.html#regression)) for GDP per capita can be specified with

```
TSLM(GDP_per_capita ~ trend()).
```

In this case the model function is `TSLM()` (time series linear model), the response variable is `GDP_per_capita` and it is being modelled using `trend()` (a “special” function specifying a linear trend when it is used within `TSLM()`). We will be taking a closer look at how each model can be specified in their respective sections.

The special functions used to define the model’s structure vary between models (as each model can support different structures). The “Specials” section of the documentation for each model function lists these special functions and how they can be used.

The left side of the formula also supports the transformations discussed in Section [3.1](https://otexts.com/fpp3/transformations.html#transformations), which can be useful in simplifying the time series patterns or constraining the forecasts to be between specific values (see Section [13.3](https://otexts.com/fpp3/limits.html#limits)).

### Train the model (estimate)

Once an appropriate model is specified, we next train the model on some data. One or more model specifications can be estimated using the `model()` function.

To estimate the model in our example, we use

```
fit <- gdppc |>
  model(trend_model = TSLM(GDP_per_capita ~ trend()))
```

This fits a linear trend model to the GDP per capita data for each combination of key variables in the tsibble. In this example, it will fit a model to each of the 263 countries in the dataset. The resulting object is a model table or a “mable”.

```
fit
#> # A mable: 263 x 2
#> # Key:     Country [263]
#>    Country             trend_model
#>    <fct>                   <model>
#>  1 Afghanistan              <TSLM>
#>  2 Albania                  <TSLM>
#>  3 Algeria                  <TSLM>
#>  4 American Samoa           <TSLM>
#>  5 Andorra                  <TSLM>
#>  6 Angola                   <TSLM>
#>  7 Antigua and Barbuda      <TSLM>
#>  8 Arab World               <TSLM>
#>  9 Argentina                <TSLM>
#> 10 Armenia                  <TSLM>
#> # ℹ 253 more rows
```

Each row corresponds to one combination of the key variables. The `trend_model` column contains information about the fitted model for each country. In later chapters we will learn how to see more information about each model.

### Check model performance (evaluate)

Once a model has been fitted, it is important to check how well it has performed on the data. There are several diagnostic tools available to check model behaviour, and also accuracy measures that allow one model to be compared against another. Sections [5.8](https://otexts.com/fpp3/accuracy.html#accuracy) and [5.9](https://otexts.com/fpp3/distaccuracy.html#distaccuracy) go into further details.

### Produce forecasts (forecast)

With an appropriate model specified, estimated and checked, it is time to produce the forecasts using `forecast()`. The easiest way to use this function is by specifying the number of future observations to forecast. For example, forecasts for the next 10 observations can be generated using `h = 10`. We can also use natural language; e.g., `h = "2 years"` can be used to predict two years into the future.

In other situations, it may be more convenient to provide a dataset of future time periods to forecast. This is commonly required when your model uses additional information from the data, such as exogenous regressors. Additional data required by the model can be included in the dataset of observations to forecast.

```
fit |> forecast(h = "3 years")
#> # A fable: 789 x 5 [1Y]
#> # Key:     Country, .model [263]
#>    Country        .model       Year
#>    <fct>          <chr>       <dbl>
#>  1 Afghanistan    trend_model  2018
#>  2 Afghanistan    trend_model  2019
#>  3 Afghanistan    trend_model  2020
#>  4 Albania        trend_model  2018
#>  5 Albania        trend_model  2019
#>  6 Albania        trend_model  2020
#>  7 Algeria        trend_model  2018
#>  8 Algeria        trend_model  2019
#>  9 Algeria        trend_model  2020
#> 10 American Samoa trend_model  2018
#> # ℹ 779 more rows
#> # ℹ 2 more variables: GDP_per_capita <dist>, .mean <dbl>
```

This is a forecast table, or “fable”. Each row corresponds to one forecast period for each country. The `GDP_per_capita` column contains the forecast distribution, while the `.mean` column contains the point forecast. The point forecast is the mean (or average) of the forecast distribution.

The forecasts can be plotted along with the historical data using `autoplot()` as follows.

```
fit |>
  forecast(h = "3 years") |>
  filter(Country == "Sweden") |>
  autoplot(gdppc) +
  labs(y = "$US", title = "GDP per capita for Sweden")
```

![Forecasts of GDP per capita for Sweden using a simple trend model.](https://otexts.com/fpp3/fpp_files/figure-html/gdpforecastplot-1.png)

Figure 5.2: Forecasts of GDP per capita for Sweden using a simple trend model.

## 5.2 Some simple forecasting methods

Some forecasting methods are extremely simple and surprisingly effective. We will use four simple forecasting methods as benchmarks throughout this book. To illustrate them, we will use quarterly Australian clay brick production between 1970 and 2004.

```
bricks <- aus_production |>
  filter_index("1970 Q1" ~ "2004 Q4") |>
  select(Bricks)
```

The `filter_index()` function is a convenient shorthand for extracting a section of a time series.

### Mean method

Here, the forecasts of all future values are equal to the average (or “mean”) of the historical data. If we let the historical data be denoted by \(y_{1},\dots,y_{T}\), then we can write the forecasts as
\[
\hat{y}_{T+h|T} = \bar{y} = (y_{1}+\dots+y_{T})/T.
\]
The notation \(\hat{y}_{T+h|T}\) is a short-hand for the estimate of \(y_{T+h}\) based on the data \(y_1,\dots,y_T\).

```
bricks |> model(MEAN(Bricks))
```

![Mean (or average) forecasts applied to clay brick production in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/mean-method-explained-1.png)

Figure 5.3: Mean (or average) forecasts applied to clay brick production in Australia.

### Naïve method

For naïve forecasts, we simply set all forecasts to be the value of the last observation. That is,
\[
\hat{y}_{T+h|T} = y_{T}.
\]
This method works remarkably well for many economic and financial time series.

```
bricks |> model(NAIVE(Bricks))
```

![Naïve forecasts applied to clay brick production in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/naive-method-explained-1.png)

Figure 5.4: Naïve forecasts applied to clay brick production in Australia.

Because a naïve forecast is optimal when data follow a random walk (see Section [9.1](https://otexts.com/fpp3/stationarity.html#stationarity)), these are also called **random walk forecasts** and the `RW()` function can be used instead of `NAIVE`.

### Seasonal naïve method

A similar method is useful for highly seasonal data. In this case, we set each forecast to be equal to the last observed value from the same season (e.g., the same month of the previous year). Formally, the forecast for time \(T+h\) is written as
\[
\hat{y}_{T+h|T} = y_{T+h-m(k+1)},
\]
where \(m=\) the seasonal period, and \(k\) is the integer part of \((h-1)/m\) (i.e., the number of complete years in the forecast period prior to time \(T+h\)). This looks more complicated than it really is. For example, with monthly data, the forecast for all future February values is equal to the last observed February value. With quarterly data, the forecast of all future Q2 values is equal to the last observed Q2 value (where Q2 means the second quarter). Similar rules apply for other months and quarters, and for other seasonal periods.

```
bricks |> model(SNAIVE(Bricks ~ lag("year")))
```

The `lag()` function is optional here as `bricks` is quarterly data and so a seasonal naïve method will need a one-year lag. However, for some time series there is more than one seasonal period, and then the required lag must be specified.

![Seasonal naïve forecasts applied to clay brick production in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/snaive-method-explained-1.png)

Figure 5.5: Seasonal naïve forecasts applied to clay brick production in Australia.

### Drift method

A variation on the naïve method is to allow the forecasts to increase or decrease over time, where the amount of change over time (called the **drift**) is set to be the average change seen in the historical data. Thus the forecast for time \(T+h\) is given by
\[
\hat{y}_{T+h|T} = y_{T} + \frac{h}{T-1}\sum_{t=2}^T (y_{t}-y_{t-1}) = y_{T} + h \left( \frac{y_{T} -y_{1}}{T-1}\right).
\]
This is equivalent to drawing a line between the first and last observations, and extrapolating it into the future.

```
bricks |> model(RW(Bricks ~ drift()))
```

![Drift forecasts applied to clay brick production in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/drift-method-explained-1.png)

Figure 5.6: Drift forecasts applied to clay brick production in Australia.

### Example: Australian quarterly beer production

Figure [5.7](https://otexts.com/fpp3/simple-methods.html#fig:beerf) shows the first three methods applied to Australian quarterly beer production from 1992 to 2006, with the forecasts compared against actual values in the next 3.5 years.

```
# Set training data from 1992 to 2006
train <- aus_production |>
  filter_index("1992 Q1" ~ "2006 Q4")
# Fit the models
beer_fit <- train |>
  model(
    Mean = MEAN(Beer),
    `Naïve` = NAIVE(Beer),
    `Seasonal naïve` = SNAIVE(Beer)
  )
# Generate forecasts for 14 quarters
beer_fc <- beer_fit |> forecast(h = 14)
# Plot forecasts against actual values
beer_fc |>
  autoplot(train, level = NULL) +
  autolayer(
    filter_index(aus_production, "2007 Q1" ~ .),
    colour = "black"
  ) +
  labs(
    y = "Megalitres",
    title = "Forecasts for quarterly beer production"
  ) +
  guides(colour = guide_legend(title = "Forecast"))
```

![Forecasts of Australian quarterly beer production.](https://otexts.com/fpp3/fpp_files/figure-html/beerf-1.png)

Figure 5.7: Forecasts of Australian quarterly beer production.

In this case, only the seasonal naïve forecasts are close to the observed values from 2007 onwards.

### Example: Google’s daily closing stock price

In Figure [5.8](https://otexts.com/fpp3/simple-methods.html#fig:google2015), the non-seasonal methods are applied to Google’s daily closing stock price in 2015, and used to forecast one month ahead. Because stock prices are not observed every day, we first set up a new time index based on the trading days rather than calendar days.

```
# Re-index based on trading days
google_stock <- gafa_stock |>
  filter(Symbol == "GOOG", year(Date) >= 2015) |>
  mutate(day = row_number()) |>
  update_tsibble(index = day, regular = TRUE)
# Filter the year of interest
google_2015 <- google_stock |> filter(year(Date) == 2015)
# Fit the models
google_fit <- google_2015 |>
  model(
    Mean = MEAN(Close),
    `Naïve` = NAIVE(Close),
    Drift = NAIVE(Close ~ drift())
  )
# Produce forecasts for the trading days in January 2016
google_jan_2016 <- google_stock |>
  filter(yearmonth(Date) == yearmonth("2016 Jan"))
google_fc <- google_fit |>
  forecast(new_data = google_jan_2016)
# Plot the forecasts
google_fc |>
  autoplot(google_2015, level = NULL) +
  autolayer(google_jan_2016, Close, colour = "black") +
  labs(y = "$US",
       title = "Google daily closing stock prices",
       subtitle = "(Jan 2015 - Jan 2016)") +
  guides(colour = guide_legend(title = "Forecast"))
```

![Forecasts based on Google's daily closing stock price in 2015.](https://otexts.com/fpp3/fpp_files/figure-html/google2015-1.png)

Figure 5.8: Forecasts based on Google’s daily closing stock price in 2015.

Sometimes one of these simple methods will be the best forecasting method available; but in many cases, these methods will serve as benchmarks rather than the method of choice. That is, any forecasting methods we develop will be compared to these simple methods to ensure that the new method is better than these simple alternatives. If not, the new method is not worth considering.

## 5.3 Fitted values and residuals

### Fitted values

Each observation in a time series can be forecast using all previous observations. We call these **fitted values** and they are denoted by \(\hat{y}_{t|t-1}\), meaning the forecast of \(y_t\) based on observations \(y_{1},\dots,y_{t-1}\) . We use these so often, we sometimes drop part of the subscript and just write \(\hat{y}_t\) instead of \(\hat{y}_{t|t-1}\). Fitted values almost always involve one-step forecasts (but see Section [13.8](https://otexts.com/fpp3/training-test.html#training-test)).

Actually, fitted values are often not true forecasts because any parameters involved in the forecasting method are estimated using all available observations in the time series, including future observations. For example, if we use the mean method, the fitted values are given by
\[
\hat{y}_t = \hat{c}
\]
where \(\hat{c}\) is the average computed over all available observations, including those at times *after* \(t\). Similarly, for the drift method, the drift parameter is estimated using all available observations. In this case, the fitted values are given by
\[
\hat{y}_t = y_{t-1} + \hat{c}
\]
where
\(\hat{c} = (y_T-y_1)/(T-1)\). In both cases, there is a parameter to be estimated from the data. The “hat” above the \(c\) reminds us that this is an estimate. When the estimate of \(c\) involves observations after time \(t\), the fitted values are not true forecasts. On the other hand, naïve or seasonal naïve forecasts do not involve any parameters, and so fitted values are true forecasts in such cases.

### Residuals

The “residuals” in a time series model are what is left over after fitting a model. The residuals are equal to the difference between the observations and the corresponding fitted values:
\[
e_{t} = y_{t}-\hat{y}_{t}.
\]

If a transformation has been used in the model, then it is often useful to look at residuals on the transformed scale. We call these “**innovation residuals**”. For example, suppose we modelled the logarithms of the data, \(w_t = \log(y_t)\). Then the innovation residuals are given by \(w_t - \hat{w}_t\) whereas the regular residuals are given by \(y_t - \hat{y}_t\). (See Section [5.6](https://otexts.com/fpp3/ftransformations.html#ftransformations) for how to use transformations when forecasting.) If no transformation has been used then the innovation residuals are identical to the regular residuals, and in such cases we will simply call them “residuals”.

The fitted values and residuals from a model can be obtained using the `augment()` function. In the beer production example in Section [5.2](https://otexts.com/fpp3/simple-methods.html#simple-methods), we saved the fitted models as `beer_fit`. So we can simply apply `augment()` to this object to compute the fitted values and residuals for all models.

```
augment(beer_fit)
#> # A tsibble: 180 x 6 [1Q]
#> # Key:       .model [3]
#>    .model Quarter  Beer .fitted .resid .innov
#>    <chr>    <qtr> <dbl>   <dbl>  <dbl>  <dbl>
#>  1 Mean   1992 Q1   443    436.   6.55   6.55
#>  2 Mean   1992 Q2   410    436. -26.4  -26.4
#>  3 Mean   1992 Q3   420    436. -16.4  -16.4
#>  4 Mean   1992 Q4   532    436.  95.6   95.6
#>  5 Mean   1993 Q1   433    436.  -3.45  -3.45
#>  6 Mean   1993 Q2   421    436. -15.4  -15.4
#>  7 Mean   1993 Q3   410    436. -26.4  -26.4
#>  8 Mean   1993 Q4   512    436.  75.6   75.6
#>  9 Mean   1994 Q1   449    436.  12.6   12.6
#> 10 Mean   1994 Q2   381    436. -55.4  -55.4
#> # ℹ 170 more rows
```

There are three new columns added to the original data:

* `.fitted` contains the fitted values;
* `.resid` contains the residuals;
* `.innov` contains the “innovation residuals” which, in this case, are identical to the regular residuals.

Residuals are useful in checking whether a model has adequately captured the information in the data. For this purpose, we use innovation residuals.

If patterns are observable in the innovation residuals, the model can probably be improved. We will look at some tools for exploring patterns in residuals in the next section.

## 5.4 Residual diagnostics

A good forecasting method will yield innovation residuals with the following properties:

1. The innovation residuals are uncorrelated. If there are correlations between innovation residuals, then there is information left in the residuals which should be used in computing forecasts.
2. The innovation residuals have zero mean. If they have a mean other than zero, then the forecasts are biased.

Any forecasting method that does not satisfy these properties can be improved. However, that does not mean that forecasting methods that satisfy these properties cannot be improved. It is possible to have several different forecasting methods for the same data set, all of which satisfy these properties. Checking these properties is important in order to see whether a method is using all of the available information, but it is not a good way to select a forecasting method.

If either of these properties is not satisfied, then the forecasting method can be modified to give better forecasts. Adjusting for bias is easy: if the residuals have mean \(m\), then simply add \(m\) to all forecasts and the bias problem is solved. Fixing the correlation problem is harder, and we will not address it until Chapter [10](https://otexts.com/fpp3/dynamic.html#dynamic).

In addition to these essential properties, it is useful (but not necessary) for the residuals to also have the following two properties.

3. The innovation residuals have constant variance. This is known as “homoscedasticity”.
4. The innovation residuals are normally distributed.

These two properties make the calculation of prediction intervals easier (see Section [5.5](https://otexts.com/fpp3/prediction-intervals.html#prediction-intervals) for an example). However, a forecasting method that does not satisfy these properties cannot necessarily be improved. Sometimes applying a Box-Cox transformation may assist with these properties, but otherwise there is usually little that you can do to ensure that your innovation residuals have constant variance and a normal distribution. Instead, an alternative approach to obtaining prediction intervals is necessary. We will show how to deal with non-normal innovation residuals in Section [5.5](https://otexts.com/fpp3/prediction-intervals.html#prediction-intervals).

### Example: Forecasting Google daily closing stock prices

We will continue with the Google daily closing stock price example from Section [5.2](https://otexts.com/fpp3/simple-methods.html#simple-methods). For stock market prices and indexes, the best forecasting method is often the naïve method. That is, each forecast is simply equal to the last observed value, or \(\hat{y}_{t} = y_{t-1}\). Hence, the residuals are simply equal to the difference between consecutive observations:
\[
e_{t} = y_{t} - \hat{y}_{t} = y_{t} - y_{t-1}.
\]

The following graph shows the Google daily closing stock price for trading days during 2015. The large jump corresponds to 17 July 2015 when the price jumped 16% due to unexpectedly strong second quarter results. (The `google_2015` object was created in Section [5.2](https://otexts.com/fpp3/simple-methods.html#simple-methods).)

```
autoplot(google_2015, Close) +
  labs(y = "$US",
       title = "Google daily closing stock prices in 2015")
```

![Daily Google stock prices in 2015.](https://otexts.com/fpp3/fpp_files/figure-html/GSPautoplot-1.png)

Figure 5.9: Daily Google stock prices in 2015.

The residuals obtained from forecasting this series using the naïve method are shown in Figure [5.10](https://otexts.com/fpp3/diagnostics.html#fig:GSPresid). The large positive residual is a result of the unexpected price jump in July.

```
aug <- google_2015 |>
  model(NAIVE(Close)) |>
  augment()
autoplot(aug, .innov) +
  labs(y = "$US",
       title = "Residuals from the naïve method")
```

![Residuals from forecasting the Google stock price using the naïve method.](https://otexts.com/fpp3/fpp_files/figure-html/GSPresid-1.png)

Figure 5.10: Residuals from forecasting the Google stock price using the naïve method.

```
aug |>
  ggplot(aes(x = .innov)) +
  geom_histogram() +
  labs(title = "Histogram of residuals")
```

![Histogram of the residuals from the naïve method applied to the Google stock price. The right tail seems a little too long for a normal distribution.](https://otexts.com/fpp3/fpp_files/figure-html/GSPhist-1.png)

Figure 5.11: Histogram of the residuals from the naïve method applied to the Google stock price. The right tail seems a little too long for a normal distribution.

```
aug |>
  ACF(.innov) |>
  autoplot() +
  labs(title = "Residuals from the naïve method")
```

![ACF of the residuals from the naïve method applied to the Google stock price. The lack of correlation suggesting the forecasts are good.](https://otexts.com/fpp3/fpp_files/figure-html/GSPacf-1.png)

Figure 5.12: ACF of the residuals from the naïve method applied to the Google stock price. The lack of correlation suggesting the forecasts are good.

These graphs show that the naïve method produces forecasts that appear to account for all available information. The mean of the residuals is close to zero and there is no significant correlation in the residuals series. The time plot of the residuals shows that the variation of the residuals stays much the same across the historical data, apart from the one outlier, and therefore the residual variance can be treated as constant. This can also be seen on the histogram of the residuals. The histogram suggests that the residuals may not be normal — the right tail seems a little too long, even when we ignore the outlier. Consequently, forecasts from this method will probably be quite good, but prediction intervals that are computed assuming a normal distribution may be inaccurate.

A convenient shortcut for producing these residual diagnostic graphs is the `gg_tsresiduals()` function, which will produce a time plot, ACF plot and histogram of the residuals.

```
google_2015 |>
  model(NAIVE(Close)) |>
  gg_tsresiduals()
```

![Residual diagnostic graphs for the naïve method applied to the Google stock price.](https://otexts.com/fpp3/fpp_files/figure-html/tsresiduals-1.png)

Figure 5.13: Residual diagnostic graphs for the naïve method applied to the Google stock price.

### Portmanteau tests for autocorrelation

In addition to looking at the ACF plot, we can also do a more formal test for autocorrelation by considering a whole set of \(r_k\) values as a group, rather than treating each one separately.

Recall that \(r_k\) is the autocorrelation for lag \(k\). When we look at the ACF plot to see whether each spike is within the required limits, we are implicitly carrying out multiple hypothesis tests, each one with a small probability of giving a false positive. When enough of these tests are done, it is likely that at least one will give a false positive, and so we may conclude that the residuals have some remaining autocorrelation, when in fact they do not.

In order to overcome this problem, we test whether the first \(\ell\) autocorrelations are significantly different from what would be expected from a white noise process. A test for a group of autocorrelations is called a **portmanteau test**, from a French word describing a suitcase or coat rack carrying several items of clothing.

One such test is the **Box-Pierce test**, based on the following statistic
\[
Q = T \sum_{k=1}^\ell r_k^2,
\]
where \(\ell\) is the maximum lag being considered and \(T\) is the number of observations. If each \(r_k\) is close to zero, then \(Q\) will be small. If some \(r_k\) values are large (positive or negative), then \(Q\) will be large. We suggest using \(\ell=10\) for non-seasonal data and \(\ell=2m\) for seasonal data, where \(m\) is the period of seasonality. However, the test is not good when \(\ell\) is large, so if these values are larger than \(T/5\), then use \(\ell=T/5\)

A related (and more accurate) test is the **Ljung-Box test**, based on
\[
Q^\* = T(T+2) \sum_{k=1}^\ell (T-k)^{-1}r_k^2.
\]

Again, large values of \(Q^\*\) suggest that the autocorrelations do not come from a white noise series.

How large is too large? If the autocorrelations did come from a white noise series, then both \(Q\) and \(Q^\*\) would have a \(\chi^2\) distribution with \(\ell\) degrees of freedom.[4](#fn4).

In the following code, `lag`\(=\ell\).

```
aug |> features(.innov, box_pierce, lag = 10)
#> # A tibble: 1 × 4
#>   Symbol .model       bp_stat bp_pvalue
#>   <chr>  <chr>          <dbl>     <dbl>
#> 1 GOOG   NAIVE(Close)    7.74     0.654

aug |> features(.innov, ljung_box, lag = 10)
#> # A tibble: 1 × 4
#>   Symbol .model       lb_stat lb_pvalue
#>   <chr>  <chr>          <dbl>     <dbl>
#> 1 GOOG   NAIVE(Close)    7.91     0.637
```

For both \(Q\) and \(Q^\*\), the results are not significant (i.e., the \(p\)-values are relatively large). Thus, we can conclude that the residuals are not distinguishable from a white noise series.

An alternative simple approach that may be appropriate for forecasting the Google daily closing stock price is the drift method. The `tidy()` function shows the one estimated parameter, the drift coefficient, measuring the average daily change observed in the historical data.

```
fit <- google_2015 |> model(RW(Close ~ drift()))
tidy(fit)
#> # A tibble: 1 × 7
#>   Symbol .model              term  estimate std.error statistic p.value
#>   <chr>  <chr>               <chr>    <dbl>     <dbl>     <dbl>   <dbl>
#> 1 GOOG   RW(Close ~ drift()) b        0.944     0.705      1.34   0.182
```

Applying the Ljung-Box test, we obtain the following result.

```
augment(fit) |> features(.innov, ljung_box, lag=10)
#> # A tibble: 1 × 4
#>   Symbol .model              lb_stat lb_pvalue
#>   <chr>  <chr>                 <dbl>     <dbl>
#> 1 GOOG   RW(Close ~ drift())    7.91     0.637
```

As with the naïve method, the residuals from the drift method are indistinguishable from a white noise series.

---

4. For the ARIMA models discussed in chapters [9](https://otexts.com/fpp3/arima.html#arima) and [10](https://otexts.com/fpp3/dynamic.html#dynamic), the degrees of freedom is adjusted to give better results.[↩︎](https://otexts.com/fpp3/diagnostics.html#fnref4)

## 5.5 Distributional forecasts and prediction intervals

### Forecast distributions

As discussed in Section [1.7](https://otexts.com/fpp3/perspective.html#perspective), we express the uncertainty in our forecasts using a probability distribution. It describes the probability of observing possible future values using the fitted model. The point forecast is the mean of this distribution. Most time series models produce normally distributed forecasts — that is, we assume that the distribution of possible future values follows a normal distribution. We will look at a couple of alternatives to normal distributions later in this section.

### Prediction intervals

A prediction interval gives an interval within which we expect \(y_{t}\) to lie with a specified probability. For example, assuming that distribution of future observations is normal, a 95% prediction interval for the \(h\)-step forecast is
\[
\hat{y}_{T+h|T} \pm 1.96 \hat\sigma_h,
\]
where \(\hat\sigma_h\) is an estimate of the standard deviation of the \(h\)-step forecast distribution.

More generally, a prediction interval can be written as
\[
\hat{y}_{T+h|T} \pm c \hat\sigma_h
\]
where the multiplier \(c\) depends on the coverage probability. In this book we usually calculate 80% intervals and 95% intervals, although any percentage may be used. Table [5.1](https://otexts.com/fpp3/prediction-intervals.html#tab:pcmultipliers) gives the value of \(c\) for a range of coverage probabilities assuming a normal forecast distribution.

Table 5.1: Multipliers to be used for prediction intervals.

| Percentage | Multiplier |
| --- | --- |
| 50 | 0.67 |
| 55 | 0.76 |
| 60 | 0.84 |
| 65 | 0.93 |
| 70 | 1.04 |
| 75 | 1.15 |
| 80 | 1.28 |
| 85 | 1.44 |
| 90 | 1.64 |
| 95 | 1.96 |
| 96 | 2.05 |
| 97 | 2.17 |
| 98 | 2.33 |
| 99 | 2.58 |

The value of prediction intervals is that they express the uncertainty in the forecasts. If we only produce point forecasts, there is no way of telling how accurate the forecasts are. However, if we also produce prediction intervals, then it is clear how much uncertainty is associated with each forecast. For this reason, point forecasts can be of almost no value without the accompanying prediction intervals.

### One-step prediction intervals

When forecasting one step ahead, the standard deviation of the forecast distribution can be estimated using the standard deviation of the residuals given by
\[\begin{equation}
\hat{\sigma} = \sqrt{\frac{1}{T-K-M}\sum_{t=1}^T e_t^2}, \tag{5.1}
\end{equation}\]
where \(K\) is the number of parameters estimated in the forecasting method, and \(M\) is the number of missing values in the residuals. (For example, \(M=1\) for a naive forecast, because we can’t forecast the first observation.)

For example, consider a naïve forecast for the Google stock price data `google_2015` (shown in Figure [5.8](https://otexts.com/fpp3/simple-methods.html#fig:google2015)). The last value of the observed series is 758.88, so the forecast of the next value of the price is 758.88. The standard deviation of the residuals from the naïve method, as given by Equation [(5.1)](https://otexts.com/fpp3/prediction-intervals.html#eq:sigma1), is 11.19. Hence, a 95% prediction interval for the next value of the GSP is
\[
758.88 \pm 1.96(11.19) = [736.9, 780.8].
\]
Similarly, an 80% prediction interval is given by
\[
758.88 \pm 1.28(11.19) = [744.5, 773.2].
\]

The value of the multiplier (1.96 or 1.28) is taken from Table [5.1](https://otexts.com/fpp3/prediction-intervals.html#tab:pcmultipliers).

### Multi-step prediction intervals

A common feature of prediction intervals is that they usually increase in length as the forecast horizon increases. The further ahead we forecast, the more uncertainty is associated with the forecast, and thus the wider the prediction intervals. That is, \(\sigma_h\) usually increases with \(h\) (although there are some non-linear forecasting methods which do not have this property).

To produce a prediction interval, it is necessary to have an estimate of \(\sigma_h\). As already noted, for one-step forecasts (\(h=1\)), Equation [(5.1)](https://otexts.com/fpp3/prediction-intervals.html#eq:sigma1) provides a good estimate of the forecast standard deviation \(\sigma_1\). For multi-step forecasts, a more complicated method of calculation is required. These calculations assume that the residuals are uncorrelated.

### Benchmark methods

For the four benchmark methods, it is possible to mathematically derive the forecast standard deviation under the assumption of uncorrelated residuals. If \(\hat{\sigma}_h\) denotes the standard deviation of the \(h\)-step forecast distribution, and \(\hat{\sigma}\) is the residual standard deviation given by [(5.1)](https://otexts.com/fpp3/prediction-intervals.html#eq:sigma1), then we can use the expressions shown in Table [5.2](https://otexts.com/fpp3/prediction-intervals.html#tab:sigmatable). Note that when \(h=1\) and \(T\) is large, these all give the same approximate value \(\hat\sigma\).

Table 5.2: Multi-step forecast standard deviation for the four benchmark methods, where \(\sigma\) is the residual standard deviation, \(m\) is the seasonal period, and \(k\) is the integer part of \((h-1) /m\) (i.e., the number of complete years in the forecast period prior to time \(T+h\)).

| Benchmark method | \(h\)-step forecast standard deviation |
| --- | --- |
| Mean | \(\hat\sigma_h = \hat\sigma\sqrt{1 + 1/T}\) |
| Naïve | \(\hat\sigma_h = \hat\sigma\sqrt{h}\) |
| Seasonal naïve | \(\hat\sigma_h = \hat\sigma\sqrt{k+1}\) |
| Drift | \(\hat\sigma_h = \hat\sigma\sqrt{h(1+h/(T-1))}\) |

Prediction intervals can easily be computed for you when using the `fable` package. For example, here is the output when using the naïve method for the Google stock price.

```
google_2015 |>
  model(NAIVE(Close)) |>
  forecast(h = 10) |>
  hilo()
#> # A tsibble: 10 x 7 [1]
#> # Key:       Symbol, .model [1]
#>    Symbol .model         day
#>    <chr>  <chr>        <dbl>
#>  1 GOOG   NAIVE(Close)   253
#>  2 GOOG   NAIVE(Close)   254
#>  3 GOOG   NAIVE(Close)   255
#>  4 GOOG   NAIVE(Close)   256
#>  5 GOOG   NAIVE(Close)   257
#>  6 GOOG   NAIVE(Close)   258
#>  7 GOOG   NAIVE(Close)   259
#>  8 GOOG   NAIVE(Close)   260
#>  9 GOOG   NAIVE(Close)   261
#> 10 GOOG   NAIVE(Close)   262
#> # ℹ 4 more variables: Close <dist>, .mean <dbl>, `80%` <hilo>, `95%` <hilo>
```

The `hilo()` function converts the forecast distributions into intervals. By default, 80% and 95% prediction intervals are returned, although other options are possible via the `level` argument.

When plotted, the prediction intervals are shown as shaded regions, with the strength of colour indicating the probability associated with the interval. Again, 80% and 95% intervals are shown by default, with other options available via the `level` argument.

```
google_2015 |>
  model(NAIVE(Close)) |>
  forecast(h = 10) |>
  autoplot(google_2015) +
  labs(title="Google daily closing stock price", y="$US" )
```

![80% and 95% prediction intervals for the Google closing stock price based on a naïve method.](https://otexts.com/fpp3/fpp_files/figure-html/googforecasts2-1.png)

Figure 5.14: 80% and 95% prediction intervals for the Google closing stock price based on a naïve method.

### Prediction intervals from bootstrapped residuals

When a normal distribution for the residuals is an unreasonable assumption, one alternative is to use bootstrapping, which only assumes that the residuals are uncorrelated with constant variance. We will illustrate the procedure using a naïve forecasting method.

A one-step forecast error is defined as \(e_t = y_t - \hat{y}_{t|t-1}\). For a naïve forecasting method, \(\hat{y}_{t|t-1} = y_{t-1}\), so we can rewrite this as
\[
y_t = y_{t-1} + e_t.
\]
Assuming future errors will be similar to past errors, when \(t>T\) we can replace \(e_{t}\) by sampling from the collection of errors we have seen in the past (i.e., the residuals). So we can simulate the next observation of a time series using
\[
y^\*_{T+1} = y_{T} + e^\*_{T+1}
\]
where \(e^\*_{T+1}\) is a randomly sampled error from the past, and \(y^\*_{T+1}\) is the possible future value that would arise if that particular error value occurred. We use a \* to indicate that this is not the observed \(y_{T+1}\) value, but one possible future that could occur. Adding the new simulated observation to our data set, we can repeat the process to obtain
\[
y^\*_{T+2} = y_{T+1}^\* + e^\*_{T+2},
\]
where \(e^\*_{T+2}\) is another draw from the collection of residuals. Continuing in this way, we can simulate an entire set of future values for our time series.

Doing this repeatedly, we obtain many possible futures. To see some of them, we can use the `generate()` function.

```
fit <- google_2015 |>
  model(NAIVE(Close))
sim <- fit |> generate(h = 30, times = 5, bootstrap = TRUE)
sim
#> # A tsibble: 150 x 5 [1]
#> # Key:       Symbol, .model, .rep [5]
#>    Symbol .model         day .rep   .sim
#>    <chr>  <chr>        <dbl> <chr> <dbl>
#>  1 GOOG   NAIVE(Close)   253 1      756.
#>  2 GOOG   NAIVE(Close)   254 1      749.
#>  3 GOOG   NAIVE(Close)   255 1      751.
#>  4 GOOG   NAIVE(Close)   256 1      750.
#>  5 GOOG   NAIVE(Close)   257 1      754.
#>  6 GOOG   NAIVE(Close)   258 1      754.
#>  7 GOOG   NAIVE(Close)   259 1      758.
#>  8 GOOG   NAIVE(Close)   260 1      763.
#>  9 GOOG   NAIVE(Close)   261 1      759.
#> 10 GOOG   NAIVE(Close)   262 1      748.
#> # ℹ 140 more rows
```

Here we have generated five possible sample paths for the next 30 trading days. The `.rep` variable provides a new key for the tsibble. The plot below shows the five sample paths along with the historical data.

```
google_2015 |>
  ggplot(aes(x = day)) +
  geom_line(aes(y = Close)) +
  geom_line(aes(y = .sim, colour = as.factor(.rep)),
    data = sim) +
  labs(title="Google daily closing stock price", y="$US" ) +
  guides(colour = "none")
```

![Five simulated future sample paths of the Google closing stock price based on a naïve method with bootstrapped residuals.](https://otexts.com/fpp3/fpp_files/figure-html/showsim-1.png)

Figure 5.15: Five simulated future sample paths of the Google closing stock price based on a naïve method with bootstrapped residuals.

Then we can compute prediction intervals by calculating percentiles of the future sample paths for each forecast horizon. The result is called a **bootstrapped** prediction interval. The name “bootstrap” is a reference to pulling ourselves up by our bootstraps, because the process allows us to measure future uncertainty by only using the historical data.

This is all built into the `forecast()` function so you do not need to call `generate()` directly.

```
fc <- fit |> forecast(h = 30, bootstrap = TRUE)
fc
#> # A fable: 30 x 5 [1]
#> # Key:     Symbol, .model [1]
#>    Symbol .model         day        Close .mean
#>    <chr>  <chr>        <dbl>       <dist> <dbl>
#>  1 GOOG   NAIVE(Close)   253 sample[5000]  759.
#>  2 GOOG   NAIVE(Close)   254 sample[5000]  759.
#>  3 GOOG   NAIVE(Close)   255 sample[5000]  758.
#>  4 GOOG   NAIVE(Close)   256 sample[5000]  759.
#>  5 GOOG   NAIVE(Close)   257 sample[5000]  759.
#>  6 GOOG   NAIVE(Close)   258 sample[5000]  759.
#>  7 GOOG   NAIVE(Close)   259 sample[5000]  759.
#>  8 GOOG   NAIVE(Close)   260 sample[5000]  759.
#>  9 GOOG   NAIVE(Close)   261 sample[5000]  759.
#> 10 GOOG   NAIVE(Close)   262 sample[5000]  759.
#> # ℹ 20 more rows
```

Notice that the forecast distribution is now represented as a simulation with 5000 sample paths. Because there is no normality assumption, the prediction intervals are not symmetric. The `.mean` column is the mean of the bootstrap samples, so it may be slightly different from the results obtained without a bootstrap.

```
autoplot(fc, google_2015) +
  labs(title="Google daily closing stock price", y="$US" )
```

![Forecasts of the Google closing stock price based on a naïve method with bootstrapped residuals.](https://otexts.com/fpp3/fpp_files/figure-html/fcbootstrapplot-1.png)

Figure 5.16: Forecasts of the Google closing stock price based on a naïve method with bootstrapped residuals.

The number of samples can be controlled using the `times` argument for `forecast()`.
For example, intervals based on 1000 bootstrap samples can be sampled with:

```
google_2015 |>
  model(NAIVE(Close)) |>
  forecast(h = 10, bootstrap = TRUE, times = 1000) |>
  hilo()
#> # A tsibble: 10 x 7 [1]
#> # Key:       Symbol, .model [1]
#>    Symbol .model      day        Close .mean            `80%`            `95%`
#>    <chr>  <chr>     <dbl>       <dist> <dbl>           <hilo>           <hilo>
#>  1 GOOG   NAIVE(Cl…   253 sample[1000]  760. [748.2, 770.8]80 [743.9, 777.6]95
#>  2 GOOG   NAIVE(Cl…   254 sample[1000]  760. [743.9, 776.1]80 [734.1, 801.6]95
#>  3 GOOG   NAIVE(Cl…   255 sample[1000]  760. [739.5, 781.7]80 [728.6, 809.0]95
#>  4 GOOG   NAIVE(Cl…   256 sample[1000]  760. [736.7, 784.7]80 [723.4, 813.1]95
#>  5 GOOG   NAIVE(Cl…   257 sample[1000]  760. [734.4, 787.2]80 [719.4, 819.7]95
#>  6 GOOG   NAIVE(Cl…   258 sample[1000]  760. [731.5, 790.2]80 [717.8, 820.3]95
#>  7 GOOG   NAIVE(Cl…   259 sample[1000]  761. [730.4, 793.0]80 [713.0, 826.3]95
#>  8 GOOG   NAIVE(Cl…   260 sample[1000]  761. [726.2, 796.2]80 [706.3, 830.7]95
#>  9 GOOG   NAIVE(Cl…   261 sample[1000]  761. [723.5, 800.2]80 [707.5, 841.0]95
#> 10 GOOG   NAIVE(Cl…   262 sample[1000]  760. [719.2, 801.8]80 [701.9, 841.4]95
```

In this case, they are similar (but not identical) to the prediction intervals based on the normal distribution.

Use the slider below to see the effect of varying the number of bootstrap samples (`times`) on the forecast distribution:

## 5.6 Forecasting using transformations

Some common transformations which can be used when modelling were discussed in Section [3.1](https://otexts.com/fpp3/transformations.html#transformations). When forecasting from a model with transformations, we first produce forecasts of the transformed data. Then, we need to reverse the transformation (or *back-transform*) to obtain forecasts on the original scale. For Box-Cox transformations given by [(3.1)](https://otexts.com/fpp3/transformations.html#eq:boxcox), the reverse transformation is given by
\[\begin{equation}
\tag{5.2}
y_{t} =
\begin{cases}
\exp(w_{t}) & \text{if $\lambda=0$};\\
\text{sign}(\lambda w_t+1)|\lambda w_t+1|^{1/\lambda} & \text{otherwise}.
\end{cases}
\end{equation}\]

The `fable` package will automatically back-transform the forecasts whenever a transformation has been used in the model definition. The back-transformed forecast distribution is then a “transformed Normal” distribution.

### Prediction intervals with transformations

If a transformation has been used, then the prediction interval is first computed on the transformed scale, and the end points are back-transformed to give a prediction interval on the original scale. This approach preserves the probability coverage of the prediction interval, although it will no longer be symmetric around the point forecast.

The back-transformation of prediction intervals is done automatically when using the `fable` package, provided you have used a transformation in the model formula.

Transformations sometimes make little difference to the point forecasts but have a large effect on prediction intervals.

### Bias adjustments

One issue with using mathematical transformations such as Box-Cox transformations is that the back-transformed point forecast will not be the mean of the forecast distribution. In fact, it will usually be the median of the forecast distribution (assuming that the distribution on the transformed space is symmetric). For many purposes, this is acceptable, although the mean is usually preferable. For example, you may wish to add up sales forecasts from various regions to form a forecast for the whole country. But medians do not add up, whereas means do.

For a Box-Cox transformation, the back-transformed mean is given (approximately) by
\[\begin{equation}
\tag{5.3}
\hat{y}_{T+h|T} =
\begin{cases}
\exp(\hat{w}_{T+h|T})\left[1 + \frac{\sigma_h^2}{2}\right] & \text{if $\lambda=0$;}\\
(\lambda \hat{w}_{T+h|T}+1)^{1/\lambda}\left[1 + \frac{\sigma_h^2(1-\lambda)}{2(\lambda \hat{w}_{T+h|T}+1)^{2}}\right] & \text{otherwise;}
\end{cases}
\end{equation}\]
where \(\hat{w}_{T+h|T}\) is the \(h\)-step forecast mean and \(\sigma_h^2\) is the \(h\)-step forecast variance on the transformed scale. The larger the forecast variance, the bigger the difference between the mean and the median.

The difference between the simple back-transformed forecast given by [(5.2)](https://otexts.com/fpp3/ftransformations.html#eq:backtransform) and the mean given by [(5.3)](https://otexts.com/fpp3/ftransformations.html#eq:backtransformmean) is called the **bias**. When we use the mean, rather than the median, we say the point forecasts have been **bias-adjusted**.

To see how much difference this bias-adjustment makes, consider the following example, where we forecast the average annual price of eggs using the drift method with a log transformation \((\lambda=0)\). The log transformation is useful in this case to ensure the forecasts and the prediction intervals stay positive.

```
fc <- prices |>
  filter(!is.na(eggs)) |>
  model(RW(log(eggs) ~ drift())) |>
  forecast(h = 50) |>
  mutate(.median = median(eggs))
fc |>
  autoplot(prices |> filter(!is.na(eggs)), level = 80) +
  geom_line(aes(y = .median), data = fc, linetype = 2, col = "blue") +
  labs(title = "Annual egg prices",
       y = "$US (in cents adjusted for inflation) ")
```

![Forecasts of egg prices using the drift method applied to the logged data. The bias-adjusted mean forecasts are shown with a solid line, while the median forecasts are dashed.](https://otexts.com/fpp3/fpp_files/figure-html/biasadjust-1.png)

Figure 5.17: Forecasts of egg prices using the drift method applied to the logged data. The bias-adjusted mean forecasts are shown with a solid line, while the median forecasts are dashed.

The dashed line in Figure [5.17](https://otexts.com/fpp3/ftransformations.html#fig:biasadjust) shows the forecast medians while the solid line shows the forecast means. Notice how the skewed forecast distribution pulls up the forecast distribution’s mean; this is a result of the added term from the bias adjustment.

Bias-adjusted forecast means are automatically computed in the `fable` package. The forecast median (the point forecast prior to bias adjustment) can be obtained using the `median()` function on the distribution column.

## 5.7 Forecasting with decomposition

Time series decomposition (discussed in Chapter [3](https://otexts.com/fpp3/decomposition.html#decomposition)) can be a useful step in producing forecasts.

Assuming an additive decomposition, the decomposed time series can be written as
\[
y_t = \hat{S}_t + \hat{A}_t,
\]
where \(\hat{A}_t = \hat{T}_t+\hat{R}_{t}\) is the seasonally adjusted component. Or, if a multiplicative decomposition has been used, we can write
\[
y_t = \hat{S}_t\hat{A}_t,
\]
where \(\hat{A}_t = \hat{T}_t\hat{R}_{t}\).

To forecast a decomposed time series, we forecast the seasonal component, \(\hat{S}_t\), and the seasonally adjusted component \(\hat{A}_t\), separately. It is usually assumed that the seasonal component is unchanging, or changing extremely slowly, so it is forecast by simply taking the last year of the estimated component. In other words, a seasonal naïve method is used for the seasonal component.

To forecast the seasonally adjusted component, any non-seasonal forecasting method may be used. For example, the drift method, or Holt’s method (discussed in Chapter [8](https://otexts.com/fpp3/expsmooth.html#expsmooth)), or a non-seasonal ARIMA model (discussed in Chapter [9](https://otexts.com/fpp3/arima.html#arima)), may be used.

### Example: Employment in the US retail sector

```
us_retail_employment <- us_employment |>
  filter(year(Month) >= 1990, Title == "Retail Trade")
dcmp <- us_retail_employment |>
  model(STL(Employed ~ trend(window = 7), robust = TRUE)) |>
  components() |>
  select(-.model)
dcmp |>
  model(NAIVE(season_adjust)) |>
  forecast() |>
  autoplot(dcmp) +
  labs(y = "Number of people",
       title = "US retail employment")
```

![Naïve forecasts of the seasonally adjusted data obtained from an STL decomposition of the total US retail employment.](https://otexts.com/fpp3/fpp_files/figure-html/print-media4-1.png)

Figure 5.18: Naïve forecasts of the seasonally adjusted data obtained from an STL decomposition of the total US retail employment.

Figure [5.18](https://otexts.com/fpp3/forecasting-decomposition.html#fig:print-media4) shows naïve forecasts of the seasonally adjusted US retail employment data. These are then “reseasonalised” by adding in the seasonal naïve forecasts of the seasonal component.

This is made easy with the `decomposition_model()` function, which allows you to compute forecasts via any additive decomposition, using other model functions to forecast each of the decomposition’s components. Seasonal components of the model will be forecast automatically using `SNAIVE()` if a different model isn’t specified. The function will also do the reseasonalising for you, ensuring that the resulting forecasts of the original data are obtained. These are shown in Figure [5.19](https://otexts.com/fpp3/forecasting-decomposition.html#fig:print-media5).

```
fit_dcmp <- us_retail_employment |>
  model(stlf = decomposition_model(
    STL(Employed ~ trend(window = 7), robust = TRUE),
    NAIVE(season_adjust)
  ))
fit_dcmp |>
  forecast() |>
  autoplot(us_retail_employment)+
  labs(y = "Number of people",
       title = "US retail employment")
```

![Forecasts of the total US retail employment data based on a naïve forecast of the seasonally adjusted data and a seasonal naïve forecast of the seasonal component, after an STL decomposition of the data.](https://otexts.com/fpp3/fpp_files/figure-html/print-media5-1.png)

Figure 5.19: Forecasts of the total US retail employment data based on a naïve forecast of the seasonally adjusted data and a seasonal naïve forecast of the seasonal component, after an STL decomposition of the data.

The prediction intervals shown in this graph are constructed in the same way as the point forecasts. That is, the upper and lower limits of the prediction intervals on the seasonally adjusted data are “reseasonalised” by adding in the forecasts of the seasonal component.

The ACF of the residuals, shown in Figure [5.20](https://otexts.com/fpp3/forecasting-decomposition.html#fig:print-media5-resids), displays significant autocorrelations. These are due to the naïve method not capturing the changing trend in the seasonally adjusted series.

```
fit_dcmp |> gg_tsresiduals()
```

![Checking the residuals.](https://otexts.com/fpp3/fpp_files/figure-html/print-media5-resids-1.png)

Figure 5.20: Checking the residuals.

In subsequent chapters we study more suitable methods that can be used to forecast the seasonally adjusted component instead of the naïve method.

## 5.8 Evaluating point forecast accuracy

### Training and test sets

It is important to evaluate forecast accuracy using genuine forecasts. Consequently, the size of the residuals is not a reliable indication of how large true forecast errors are likely to be. The accuracy of forecasts can only be determined by considering how well a model performs on new data that were not used when fitting the model.

When choosing models, it is common practice to separate the available data into two portions, **training** and **test** data, where the training data is used to estimate any parameters of a forecasting method and the test data is used to evaluate its accuracy. Because the test data is not used in determining the forecasts, it should provide a reliable indication of how well the model is likely to forecast on new data.

![](https://otexts.com/fpp3/fpp_files/figure-html/traintest-1.png)

The size of the test set is typically about 20% of the total sample, although this value depends on how long the sample is and how far ahead you want to forecast. The test set should ideally be at least as large as the maximum forecast horizon required. The following points should be noted.

* A model which fits the training data well will not necessarily forecast well.
* A perfect fit can always be obtained by using a model with enough parameters.
* Over-fitting a model to data is just as bad as failing to identify a systematic pattern in the data.

Some references describe the test set as the “hold-out set” because these data are “held out” of the data used for fitting. Other references call the training set the “in-sample data” and the test set the “out-of-sample data”. We prefer to use “training data” and “test data” in this book.

### Functions to subset a time series

The `filter()` function is useful when extracting a portion of a time series, such as we need when creating training and test sets. When splitting data into evaluation sets, filtering the index of the data is particularly useful. For example,

```
aus_production |> filter(year(Quarter) >= 1995)
```

extracts all data from 1995 onward. Equivalently,

```
aus_production |> filter_index("1995 Q1" ~ .)
```

can be used.

Another useful function is `slice()`, which allows the use of indices to choose a subset from each group. For example,

```
aus_production |>
  slice(n()-19:0)
```

extracts the last 20 observations (5 years).

Slice also works with groups, making it possible to subset observations from each key. For example,

```
aus_retail |>
  group_by(State, Industry) |>
  slice(1:12)
```

will subset the first year of data from each time series in the data.

### Forecast errors

A forecast “error” is the difference between an observed value and its forecast. Here “error” does not mean a mistake, it means the unpredictable part of an observation. It can be written as
\[
e_{T+h} = y_{T+h} - \hat{y}_{T+h|T},
\]
where the training data is given by \(\{y_1,\dots,y_T\}\) and the test data is given by \(\{y_{T+1},y_{T+2},\dots\}\).

Note that forecast errors are different from residuals in two ways. First, residuals are calculated on the *training* set while forecast errors are calculated on the *test* set. Second, residuals are based on *one-step* forecasts while forecast errors can involve *multi-step* forecasts.

We can measure forecast accuracy by summarising the forecast errors in different ways.

### Scale-dependent errors

The forecast errors are on the same scale as the data. Accuracy measures that are based only on \(e_{t}\) are therefore scale-dependent and cannot be used to make comparisons between series that involve different units.

The two most commonly used scale-dependent measures are based on the absolute errors or squared errors:
\[\begin{align\*}
\text{Mean absolute error: MAE} & = \text{mean}(|e_{t}|),\\
\text{Root mean squared error: RMSE} & = \sqrt{\text{mean}(e_{t}^2)}.
\end{align\*}\]
When comparing forecast methods applied to a single time series, or to several time series with the same units, the MAE is popular as it is easy to both understand and compute. A forecast method that minimises the MAE will lead to forecasts of the median, while minimising the RMSE will lead to forecasts of the mean. Consequently, the RMSE is also widely used, despite being more difficult to interpret.

### Percentage errors

The percentage error is given by \(p_{t} = 100 e_{t}/y_{t}\). Percentage errors have the advantage of being unit-free, and so are frequently used to compare forecast performances between data sets. The most commonly used measure is:
\[
\text{Mean absolute percentage error: MAPE} = \text{mean}(|p_{t}|).
\]
Measures based on percentage errors have the disadvantage of being infinite or undefined if \(y_{t}=0\) for any \(t\) in the period of interest, and having extreme values if any \(y_{t}\) is close to zero. Another problem with percentage errors that is often overlooked is that they assume the unit of measurement has a meaningful zero.[5](#fn5) For example, a percentage error makes no sense when measuring the accuracy of temperature forecasts on either the Fahrenheit or Celsius scales, because temperature has an arbitrary zero point.

They also have the disadvantage that they put a heavier penalty on negative errors than on positive errors. This observation led to the use of the so-called “symmetric” MAPE (sMAPE) proposed by Armstrong ([1978, p. 348](#ref-Armstrong85)), which was used in the M3 forecasting competition. It is defined by
\[
\text{sMAPE} = \text{mean}\left(200|y_{t} - \hat{y}_{t}|/(y_{t}+\hat{y}_{t})\right).
\]
However, if \(y_{t}\) is close to zero, \(\hat{y}_{t}\) is also likely to be close to zero. Thus, the measure still involves division by a number close to zero, making the calculation unstable. Also, the value of sMAPE can be negative, so it is not really a measure of “absolute percentage errors” at all.

Hyndman & Koehler ([2006](#ref-HK06)) recommend that the sMAPE not be used. It is included here only because it is widely used, although we will not use it in this book.

### Scaled errors

Scaled errors were proposed by Hyndman & Koehler ([2006](#ref-HK06)) as an alternative to using percentage errors when comparing forecast accuracy across series with different units. They proposed scaling the errors based on the *training* MAE from a simple forecast method.

For a non-seasonal time series, a useful way to define a scaled error uses naïve forecasts:
\[
q_{j} = \frac{\displaystyle e_{j}}
{\displaystyle\frac{1}{T-1}\sum_{t=2}^T |y_{t}-y_{t-1}|}.
\]
Because the numerator and denominator both involve values on the scale of the original data, \(q_{j}\) is independent of the scale of the data. A scaled error is less than one if it arises from a better forecast than the average one-step naïve forecast computed on the training data. Conversely, it is greater than one if the forecast is worse than the average one-step naïve forecast computed on the training data.

For seasonal time series, a scaled error can be defined using seasonal naïve forecasts:
\[
q_{j} = \frac{\displaystyle e_{j}}
{\displaystyle\frac{1}{T-m}\sum_{t=m+1}^T |y_{t}-y_{t-m}|}.
\]

The *mean absolute scaled error* is simply
\[
\text{MASE} = \text{mean}(|q_{j}|).
\]
Similarly, the *root mean squared scaled error* is given by
\[
\text{RMSSE} = \sqrt{\text{mean}(q_{j}^2)},
\]
where
\[
q^2_{j} = \frac{\displaystyle e^2_{j}}
{\displaystyle\frac{1}{T-m}\sum_{t=m+1}^T (y_{t}-y_{t-m})^2},
\]
and we set \(m=1\) for non-seasonal data.

### Examples

```
recent_production <- aus_production |>
  filter(year(Quarter) >= 1992)
beer_train <- recent_production |>
  filter(year(Quarter) <= 2007)

beer_fit <- beer_train |>
  model(
    Mean = MEAN(Beer),
    `Naïve` = NAIVE(Beer),
    `Seasonal naïve` = SNAIVE(Beer),
    Drift = RW(Beer ~ drift())
  )

beer_fc <- beer_fit |>
  forecast(h = 10)

beer_fc |>
  autoplot(
    aus_production |> filter(year(Quarter) >= 1992),
    level = NULL
  ) +
  labs(
    y = "Megalitres",
    title = "Forecasts for quarterly beer production"
  ) +
  guides(colour = guide_legend(title = "Forecast"))
```

![Forecasts of Australian quarterly beer production using data up to the end of 2007.](https://otexts.com/fpp3/fpp_files/figure-html/beeraccuracy-1.png)

Figure 5.21: Forecasts of Australian quarterly beer production using data up to the end of 2007.

Figure [5.21](https://otexts.com/fpp3/accuracy.html#fig:beeraccuracy) shows four forecast methods applied to the quarterly Australian beer production using data only to the end of 2007. The actual values for the period 2008–2010 are also shown. We compute the forecast accuracy measures for this period.

```
accuracy(beer_fc, recent_production)
```

| Method | RMSE | MAE | MAPE | MASE |
| --- | --- | --- | --- | --- |
| Drift method | 64.90 | 58.88 | 14.58 | 4.12 |
| Mean method | 38.45 | 34.83 | 8.28 | 2.44 |
| Naïve method | 62.69 | 57.40 | 14.18 | 4.01 |
| Seasonal naïve method | 14.31 | 13.40 | 3.17 | 0.94 |

The `accuracy()` function will automatically extract the relevant periods from the data (`recent_production` in this example) to match the forecasts when computing the various accuracy measures.

It is obvious from the graph that the seasonal naïve method is best for these data, although it can still be improved, as we will discover later. Sometimes, different accuracy measures will lead to different results as to which forecast method is best. However, in this case, all of the results point to the seasonal naïve method as the best of these four methods for this data set.

To take a non-seasonal example, consider the Google stock price. The following graph shows the closing stock prices from 2015, along with forecasts for January 2016 obtained from three different methods.

```
google_fit <- google_2015 |>
  model(
    Mean = MEAN(Close),
    `Naïve` = NAIVE(Close),
    Drift = RW(Close ~ drift())
  )

google_fc <- google_fit |>
  forecast(google_jan_2016)
```

```
google_fc |>
  autoplot(bind_rows(google_2015, google_jan_2016),
    level = NULL) +
  labs(y = "$US",
       title = "Google closing stock prices from Jan 2015") +
  guides(colour = guide_legend(title = "Forecast"))
```

![Forecasts of the Google stock price for Jan 2016.](https://otexts.com/fpp3/fpp_files/figure-html/GSPfc-1.png)

Figure 5.22: Forecasts of the Google stock price for Jan 2016.

```
accuracy(google_fc, google_stock)
```

| Method | RMSE | MAE | MAPE | MASE |
| --- | --- | --- | --- | --- |
| Drift method | 53.07 | 49.82 | 6.99 | 6.99 |
| Mean method | 118.03 | 116.95 | 16.24 | 16.41 |
| Naïve method | 43.43 | 40.38 | 5.67 | 5.67 |

Here, the best method is the naïve method (regardless of which accuracy measure is used).

### Bibliography

Armstrong, J. S. (1978). *Long-range forecasting: From crystal ball to computer*. John Wiley & Sons.

Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, *22*(4), 679–688.

---

5. That is, a percentage is valid on a ratio scale, but not on an interval scale. Only ratio scale variables have meaningful zeros.[↩︎](https://otexts.com/fpp3/accuracy.html#fnref5)

## 5.9 Evaluating distributional forecast accuracy

The preceding measures all measure point forecast accuracy. When evaluating distributional forecasts, we need to use some other measures.

### Quantile scores

Consider the Google stock price example from the previous section. Figure [5.23](https://otexts.com/fpp3/distaccuracy.html#fig:googlepi) shows an 80% prediction interval for the forecasts from the naïve method.

```
google_fc |>
  filter(.model == "Naïve") |>
  autoplot(bind_rows(google_2015, google_jan_2016), level=80)+
  labs(y = "$US",
       title = "Google closing stock prices")
```

![Naïve forecasts of the Google stock price for Jan 2016, along with 80% prediction intervals.](https://otexts.com/fpp3/fpp_files/figure-html/googlepi-1.png)

Figure 5.23: Naïve forecasts of the Google stock price for Jan 2016, along with 80% prediction intervals.

The lower limit of this prediction interval gives the 10th percentile (or 0.1 quantile) of the forecast distribution, so we would expect the actual value to lie below the lower limit about 10% of the time, and to lie above the lower limit about 90% of the time. When we compare the actual value to this percentile, we need to allow for the fact that it is more likely to be above than below.

More generally, suppose we are interested in the quantile forecast with probability \(p\) at future time \(t\), and let this be denoted by \(f_{p,t}\). That is, we expect the observation \(y_t\) to be less than \(f_{p,t}\) with probability \(p\). For example, the 10th percentile would be \(f_{0.10,t}\). If \(y_{t}\) denotes the observation at time \(t\), then the **Quantile Score** is
\[
Q_{p,t} = \begin{cases}
2(1 - p) \big(f_{p,t} - y_{t}\big), & \text{if $y_{t} < f_{p,t}$}\\
2p \big(y_{t} - f_{p,t}\big), & \text{if $y_{t} \ge f_{p,t}$} \end{cases}
\]
This is sometimes called the “pinball loss function” because a graph of it resembles the trajectory of a ball on a pinball table. The multiplier of 2 is often omitted, but including it makes the interpretation a little easier. A low value of \(Q_{p,t}\) indicates a better estimate of the quantile.

The quantile score can be interpreted like an absolute error. In fact, when \(p=0.5\), the quantile score \(Q_{0.5,t}\) is the same as the absolute error. For other values of \(p\), the “error” \((y_t - f_{p,t})\) is weighted to take account of how likely it is to be positive or negative. If \(p>0.5\), \(Q_{p,t}\) gives a heavier penalty when the observation is greater than the estimated quantile than when the observation is less than the estimated quantile. The reverse is true for \(p<0.5\).

In Figure [5.23](https://otexts.com/fpp3/distaccuracy.html#fig:googlepi), the one-step-ahead 10% quantile forecast (for 4 January 2016) is \(f_{0.1,t} = 744.54\) and the observed value is \(y_t = 741.84\). Then
\[
Q_{0.1,t} = 2(1-0.1) (744.54 - 741.84) = 4.86.
\]
This is easily computed using `accuracy()` with the `quantile_score()` function:

```
google_fc |>
  filter(.model == "Naïve", Date == "2016-01-04") |>
  accuracy(google_stock, list(qs=quantile_score), probs=0.10)
#> # A tibble: 1 × 4
#>   .model Symbol .type    qs
#>   <chr>  <chr>  <chr> <dbl>
#> 1 Naïve  GOOG   Test   4.86
```

### Winkler Score

It is often of interest to evaluate a prediction interval, rather than a few quantiles, and the Winkler score proposed by Winkler ([1972](#ref-Winkler1972)) is designed for this purpose. If the \(100(1-\alpha)\)% prediction interval at time \(t\) is given by \([\ell_{\alpha,t}, u_{\alpha,t}]\), then the Winkler score is defined as the length of the interval plus a penalty if the observation is outside the interval:
\[
W_{\alpha,t} = \begin{cases}
(u_{\alpha,t} - \ell_{\alpha,t}) + \frac{2}{\alpha} (\ell_{\alpha,t} - y_t) & \text{if } y_t < \ell_{\alpha,t} \\
(u_{\alpha,t} - \ell_{\alpha,t}) & \text{if } \ell_{\alpha,t} \le y_t \le u_{\alpha,t} \\
(u_{\alpha,t} - \ell_{\alpha,t}) + \frac{2}{\alpha} (y_t - u_{\alpha,t}) & \text{if } y_t > u_{\alpha,t}.
\end{cases}
\]
For observations that fall within the interval, the Winkler score is simply the length of the interval. Thus, low scores are associated with narrow intervals. However, if the observation falls outside the interval, the penalty applies, with the penalty proportional to how far the observation is outside the interval.

Prediction intervals are usually constructed from quantiles by setting \(\ell_{\alpha,t} = f_{\alpha/2,t}\) and \(u_{\alpha,t} = f_{1-\alpha/2,t}\). If we add the corresponding quantile scores and divide by \(\alpha\), we get the Winkler score:
\[
W_{\alpha,t} = (Q_{\alpha/2,t} + Q_{1-\alpha/2,t})/\alpha.
\]

The one-step-ahead 80% interval shown in Figure [5.23](https://otexts.com/fpp3/distaccuracy.html#fig:googlepi) for 4 January 2016 is [744.54, 773.22], and the actual value was 741.84, so the Winkler score is
\[
W_{\alpha,t} = (773.22 - 744.54) + \frac{2}{0.2} (744.54 - 741.84) =
55.68.
\]
This is easily computed using `accuracy()` with the `winkler_score()` function:

```
google_fc |>
  filter(.model == "Naïve", Date == "2016-01-04") |>
  accuracy(google_stock,
    list(winkler = winkler_score), level = 80)
#> # A tibble: 1 × 4
#>   .model Symbol .type winkler
#>   <chr>  <chr>  <chr>   <dbl>
#> 1 Naïve  GOOG   Test     55.7
```

### Continuous Ranked Probability Score

Often we are interested in the whole forecast distribution, rather than particular quantiles or prediction intervals. In that case, we can average the quantile scores over all values of \(p\) to obtain the **Continuous Ranked Probability Score** or CRPS ([Gneiting & Katzfuss, 2014](#ref-Gneiting2014)).

In the Google stock price example, we can compute the average CRPS value for all days in the test set. A CRPS value is a little like a weighted absolute error computed from the entire forecast distribution, where the weighting takes account of the probabilities.

```
google_fc |>
  accuracy(google_stock, list(crps = CRPS))
#> # A tibble: 3 × 4
#>   .model Symbol .type  crps
#>   <chr>  <chr>  <chr> <dbl>
#> 1 Drift  GOOG   Test   33.5
#> 2 Mean   GOOG   Test   76.7
#> 3 Naïve  GOOG   Test   26.5
```

Here, the naïve method is giving better distributional forecasts than the drift or mean methods.

### Scale-free comparisons using skill scores

As with point forecasts, it is useful to be able to compare the distributional forecast accuracy of several methods across series on different scales. For point forecasts, we used scaled errors for that purpose. Another approach is to use skill scores. These can be used for both point forecast accuracy and distributional forecast accuracy.

With skill scores, we compute a forecast accuracy measure relative to some benchmark method. For example, if we use the naïve method as a benchmark, and also compute forecasts using the drift method, we can compute the CRPS skill score of the drift method relative to the naïve method as
\[
\frac{\text{CRPS}_{\text{Naïve}} - \text{CRPS}_{\text{Drift}}}{\text{CRPS}_{\text{Naïve}}}.
\]
This gives the proportion that the drift method improves over the naïve method based on CRPS. It is easy to compute using the `accuracy()` function.

```
google_fc |>
  accuracy(google_stock, list(skill = skill_score(CRPS)))
#> # A tibble: 3 × 4
#>   .model Symbol .type  skill
#>   <chr>  <chr>  <chr>  <dbl>
#> 1 Drift  GOOG   Test  -0.266
#> 2 Mean   GOOG   Test  -1.90
#> 3 Naïve  GOOG   Test   0
```

Of course, the skill score for the naïve method is 0 because it can’t improve on itself. The other two methods have larger CRPS values than naïve, so the skills scores are negative; the drift method is 26.6% worse than the naïve method.

The `skill_score()` function will always compute the CRPS for the appropriate benchmark forecasts, even if these are not included in the `fable` object. When the data are seasonal, the benchmark used is the seasonal naïve method rather than the naïve method. To ensure that the same training data are used for the benchmark forecasts, it is important that the data provided to the `accuracy()` function starts at the same time as the training data.

The `skill_score()` function can be used with any accuracy measure. For example, `skill_score(MSE)` provides a way of comparing MSE values across diverse series. However, it is important that the test set is large enough to allow reliable calculation of the error measure, especially in the denominator. For that reason, MASE or RMSSE are often preferable scale-free measures for point forecast accuracy.

### Bibliography

Gneiting, T., & Katzfuss, N. (2014). Probabilistic forecasting. *Annual Review of Statistics and Its Application*, *1*(1), 125–151.

Winkler, R. L. (1972). A decision-theoretic approach to interval estimation. *Journal of the American Statistical Association*, *67*(337), 187–191.

## 5.10 Time series cross-validation

A more sophisticated version of training/test sets is time series cross-validation. In this procedure, there are a series of test sets, each consisting of a single observation. The corresponding training set consists only of observations that occurred *prior* to the observation that forms the test set. Thus, no future observations can be used in constructing the forecast. Since it is not possible to obtain a reliable forecast based on a small training set, the earliest observations are not considered as test sets.

The following diagram illustrates the series of training and test sets, where the blue observations form the training sets, and the orange observations form the test sets.

![](https://otexts.com/fpp3/fpp_files/figure-html/cv1-1.png)

The forecast accuracy is computed by averaging over the test sets. This procedure is sometimes known as “evaluation on a rolling forecasting origin” because the “origin” at which the forecast is based rolls forward in time.

With time series forecasting, one-step forecasts may not be as relevant as multi-step forecasts. In this case, the cross-validation procedure based on a rolling forecasting origin can be modified to allow multi-step errors to be used. Suppose that we are interested in models that produce good \(4\)-step-ahead forecasts. Then the corresponding diagram is shown below.

![](https://otexts.com/fpp3/fpp_files/figure-html/cv4-1.png)

In the following example, we compare the forecast accuracy obtained via time series cross-validation with the residual accuracy. The `stretch_tsibble()` function is used to create many training sets. In this example, we start with a training set of length `.init=3`, and increase the size of successive training sets by `.step=1`.

```
# Time series cross-validation accuracy
google_2015_tr <- google_2015 |>
  stretch_tsibble(.init = 3, .step = 1) |>
  relocate(Date, Symbol, .id)
google_2015_tr
#> # A tsibble: 31,875 x 10 [1]
#> # Key:       Symbol, .id [250]
#>    Date       Symbol   .id  Open  High   Low Close Adj_Close  Volume   day
#>    <date>     <chr>  <int> <dbl> <dbl> <dbl> <dbl>     <dbl>   <dbl> <int>
#>  1 2015-01-02 GOOG       1  526.  528.  521.  522.      522. 1447600     1
#>  2 2015-01-05 GOOG       1  520.  521.  510.  511.      511. 2059800     2
#>  3 2015-01-06 GOOG       1  512.  513.  498.  499.      499. 2899900     3
#>  4 2015-01-02 GOOG       2  526.  528.  521.  522.      522. 1447600     1
#>  5 2015-01-05 GOOG       2  520.  521.  510.  511.      511. 2059800     2
#>  6 2015-01-06 GOOG       2  512.  513.  498.  499.      499. 2899900     3
#>  7 2015-01-07 GOOG       2  504.  504.  497.  498.      498. 2065100     4
#>  8 2015-01-02 GOOG       3  526.  528.  521.  522.      522. 1447600     1
#>  9 2015-01-05 GOOG       3  520.  521.  510.  511.      511. 2059800     2
#> 10 2015-01-06 GOOG       3  512.  513.  498.  499.      499. 2899900     3
#> # ℹ 31,865 more rows
```

The `.id` column provides a new key indicating the various training sets. The `accuracy()` function can be used to evaluate the forecast accuracy across the training sets.

```
# TSCV accuracy
google_2015_tr |>
  model(RW(Close ~ drift())) |>
  forecast(h = 1) |>
  accuracy(google_2015)
# Training set accuracy
google_2015 |>
  model(RW(Close ~ drift())) |>
  accuracy()
```

| Evaluation method | RMSE | MAE | MAPE | MASE |
| --- | --- | --- | --- | --- |
| Cross-validation | 11.27 | 7.26 | 1.19 | 1.02 |
| Training | 11.15 | 7.16 | 1.18 | 1.00 |

As expected, the accuracy measures from the residuals are smaller, as the corresponding “forecasts” are based on a model fitted to the entire data set, rather than being true forecasts.

A good way to choose the best forecasting model is to find the model with the smallest RMSE computed using time series cross-validation.

### Example: Forecast horizon accuracy with cross-validation

The `google_2015` subset of the `gafa_stock` data, plotted in Figure [5.9](https://otexts.com/fpp3/diagnostics.html#fig:GSPautoplot), includes daily closing stock price of Google Inc from the NASDAQ exchange for all trading days in 2015.

The code below evaluates the forecasting performance of 1- to 8-step-ahead drift forecasts. The plot shows that the forecast error increases as the forecast horizon increases, as we would expect.

```
google_2015_tr <- google_2015 |>
  stretch_tsibble(.init = 3, .step = 1)
fc <- google_2015_tr |>
  model(RW(Close ~ drift())) |>
  forecast(h = 8) |>
  group_by(.id) |>
  mutate(h = row_number()) |>
  ungroup() |>
  as_fable(response = "Close", distribution = Close)
fc |>
  accuracy(google_2015, by = c("h", ".model")) |>
  ggplot(aes(x = h, y = RMSE)) +
  geom_point()
```

![RMSE as a function of forecast horizon for the drift method applied to Google closing stock prices.](https://otexts.com/fpp3/fpp_files/figure-html/CV-accuracy-plot-1.png)

Figure 5.24: RMSE as a function of forecast horizon for the drift method applied to Google closing stock prices.

## 5.11 Exercises

1. Produce forecasts for the following series using whichever of `NAIVE(y)`, `SNAIVE(y)` or `RW(y ~ drift())` is more appropriate in each case:

   * Australian Population (`global_economy`)
   * Bricks (`aus_production`)
   * NSW Lambs (`aus_livestock`)
   * Household wealth (`hh_budget`).
   * Australian takeaway food turnover (`aus_retail`).
2. Use the Facebook stock price (data set `gafa_stock`) to do the following:

   1. Produce a time plot of the series.
   2. Produce forecasts using the drift method and plot them.
   3. Show that the forecasts are identical to extending the line drawn between the first and last observations.
   4. Try using some of the other benchmark functions to forecast the same data set. Which do you think is best? Why?
3. Apply a seasonal naïve method to the quarterly Australian beer production data from 1992. Check if the residuals look like white noise, and plot the forecasts. The following code will help.

   ```
   # Extract data of interest
   recent_production <- aus_production |>
     filter(year(Quarter) >= 1992)
   # Define and estimate a model
   fit <- recent_production |> model(SNAIVE(Beer))
   # Look at the residuals
   fit |> gg_tsresiduals()
   # Look a some forecasts
   fit |> forecast() |> autoplot(recent_production)
   ```

   What do you conclude?
4. Repeat the previous exercise using the Australian Exports series from `global_economy` and the Bricks series from `aus_production`. Use whichever of `NAIVE()` or `SNAIVE()` is more appropriate in each case.
5. Produce forecasts for the 7 Victorian series in `aus_livestock` using `SNAIVE()`. Plot the resulting forecasts including the historical data. Is this a reasonable benchmark for these series?
6. Are the following statements true or false? Explain your answer.

   1. Good forecast methods should have normally distributed residuals.
   2. A model with small residuals will give good forecasts.
   3. The best measure of forecast accuracy is MAPE.
   4. If your model doesn’t forecast well, you should make it more complicated.
   5. Always choose the model with the best forecast accuracy as measured on the test set.
7. For your retail time series (from Exercise 7 in Section [2.10](https://otexts.com/fpp3/graphics-exercises.html#graphics-exercises)):

   1. Create a training dataset consisting of observations before 2011 using

      ```
      myseries_train <- myseries |>
        filter(year(Month) < 2011)
      ```
   2. Check that your data have been split appropriately by producing the following plot.

      ```
      autoplot(myseries, Turnover) +
        autolayer(myseries_train, Turnover, colour = "red")
      ```
   3. Fit a seasonal naïve model using `SNAIVE()` applied to your training data (`myseries_train`).

      ```
      fit <- myseries_train |>
        model(SNAIVE())
      ```
   4. Check the residuals.

      ```
      fit |> gg_tsresiduals()
      ```

      Do the residuals appear to be uncorrelated and normally distributed?
   5. Produce forecasts for the test data

      ```
      fc <- fit |>
        forecast(new_data = anti_join(myseries, myseries_train))
      fc |> autoplot(myseries)
      ```
   6. Compare the accuracy of your forecasts against the actual values.

      ```
      fit |> accuracy()
      fc |> accuracy(myseries)
      ```
   7. How sensitive are the accuracy measures to the amount of training data used?
8. Consider the number of pigs slaughtered in New South Wales (data set `aus_livestock`).

   1. Produce some plots of the data in order to become familiar with it.
   2. Create a training set of 486 observations, withholding a test set of 72 observations (6 years).
   3. Try using various benchmark methods to forecast the training set and compare the results on the test set. Which method did best?
   4. Check the residuals of your preferred method. Do they resemble white noise?
9. 1. Create a training set for household wealth (`hh_budget`) by withholding the last four years as a test set.
   2. Fit all the appropriate benchmark methods to the training set and forecast the periods covered by the test set.
   3. Compute the accuracy of your forecasts. Which method does best?
   4. Do the residuals from the best method resemble white noise?
10. 1. Create a training set for Australian takeaway food turnover (`aus_retail`) by withholding the last four years as a test set.
    2. Fit all the appropriate benchmark methods to the training set and forecast the periods covered by the test set.
    3. Compute the accuracy of your forecasts. Which method does best?
    4. Do the residuals from the best method resemble white noise?
11. We will use the Bricks data from `aus_production` (Australian quarterly clay brick production 1956–2005) for this exercise.

    1. Use an STL decomposition to calculate the trend-cycle and seasonal indices. (Experiment with having fixed or changing seasonality.)
    2. Compute and plot the seasonally adjusted data.
    3. Use a naïve method to produce forecasts of the seasonally adjusted data.
    4. Use `decomposition_model()` to reseasonalise the results, giving forecasts for the original data.
    5. Do the residuals look uncorrelated?
    6. Repeat with a robust STL decomposition. Does it make much difference?
    7. Compare forecasts from `decomposition_model()` with those from `SNAIVE()`, using a test set comprising the last 2 years of data. Which is better?
12. `tourism` contains quarterly visitor nights (in thousands) from 1998 to 2017 for 76 regions of Australia.

    1. Extract data from the Gold Coast region using `filter()` and aggregate total overnight trips (sum over `Purpose`) using `summarise()`. Call this new dataset `gc_tourism`.
    2. Using `slice()` or `filter()`, create three training sets for this data excluding the last 1, 2 and 3 years. For example, `gc_train_1 <- gc_tourism |> slice(1:(n()-4))`.
    3. Compute one year of forecasts for each training set using the seasonal naïve (`SNAIVE()`) method. Call these `gc_fc_1`, `gc_fc_2` and `gc_fc_3`, respectively.
    4. Use `accuracy()` to compare the test set forecast accuracy using MAPE. Comment on these.

## 5.12 Further reading

* Ord et al. ([2017](#ref-Ord2017)) provides further discussion of simple benchmark forecasting methods.
* A review of forecast evaluation methods is given in Hyndman & Koehler ([2006](#ref-HK06)), looking at the strengths and weaknesses of different approaches. This is the paper that introduced the MASE as a general-purpose forecast accuracy measure.
* For a discussion of forecasting using STL, see Theodosiou ([2011](#ref-Theodosiou2011)).
* An excellent discussion of evaluating distributional forecast accuracy is provided by Gneiting & Katzfuss ([2014](#ref-Gneiting2014)).

### Bibliography

Gneiting, T., & Katzfuss, N. (2014). Probabilistic forecasting. *Annual Review of Statistics and Its Application*, *1*(1), 125–151.

Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, *22*(4), 679–688.

Ord, J. K., Fildes, R., & Kourentzes, N. (2017). *Principles of business forecasting* (2nd ed.). Wessex Press Publishing Co.

Theodosiou, M. (2011). Forecasting monthly and quarterly time series using STL decomposition. *International Journal of Forecasting*, *27*(4), 1178–1195.
