Source: https://otexts.com/fpp3/decomposition.html (chapter decomposition, 9 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - 03-time-series-decomposition
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Chapter 3 Time series decomposition

Time series data can exhibit a variety of patterns, and it is often helpful to split a time series into several components, each representing an underlying pattern category.

In Section [2.3](https://otexts.com/fpp3/tspatterns.html#tspatterns) we discussed three types of time series patterns: trend, seasonality and cycles. When we decompose a time series into components, we usually combine the trend and cycle into a single **trend-cycle** component (often just called the **trend** for simplicity). Thus we can think of a time series as comprising three components: a trend-cycle component, a seasonal component, and a remainder component (containing anything else in the time series). For some time series (e.g., those that are observed at least daily), there can be more than one seasonal component, corresponding to the different seasonal periods.

In this chapter, we consider the most common methods for extracting these components from a time series. Often this is done to help improve understanding of the time series, but it can also be used to improve forecast accuracy.

When decomposing a time series, it is sometimes helpful to first transform or adjust the series in order to make the decomposition (and later analysis) as simple as possible. So we will begin by discussing transformations and adjustments.

## 3.1 Transformations and adjustments

Adjusting the historical data can often lead to a simpler time series. Here, we deal with four kinds of adjustments: calendar adjustments, population adjustments, inflation adjustments and mathematical transformations. The purpose of these adjustments and transformations is to simplify the patterns in the historical data by removing known sources of variation, or by making the pattern more consistent across the whole data set. Simpler patterns are usually easier to model and lead to more accurate forecasts.

### Calendar adjustments

Some of the variation seen in seasonal data may be due to simple calendar effects. In such cases, it is usually much easier to remove the variation before doing any further analysis.

For example, if you are studying the total monthly sales in a retail store, there will be variation between the months simply because of the different numbers of trading days in each month, in addition to the seasonal variation across the year. It is easy to remove this variation by computing average sales per trading day in each month, rather than total sales in the month. Then we effectively remove the calendar variation.

### Population adjustments

Any data that are affected by population changes can be adjusted to give per-capita data. That is, consider the data per person (or per thousand people, or per million people) rather than the total. For example, if you are studying the number of hospital beds in a particular region over time, the results are much easier to interpret if you remove the effects of population changes by considering the number of beds per thousand people. Then you can see whether there have been real increases in the number of beds, or whether the increases are due entirely to population increases. It is possible for the total number of beds to increase, but the number of beds per thousand people to decrease. This occurs when the population is increasing faster than the number of hospital beds. For most data that are affected by population changes, it is best to use per-capita data rather than the totals.

This can be seen in the `global_economy` dataset, where a common transformation of GDP is GDP per-capita.

```
global_economy |>
  filter(Country == "Australia") |>
  autoplot(GDP/Population) +
  labs(title= "GDP per capita", y = "$US")
```

![Australian GDP per-capita.](https://otexts.com/fpp3/fpp_files/figure-html/gdp-per-capita-1.png)

Figure 3.1: Australian GDP per-capita.

### Inflation adjustments

Data which are affected by the value of money are best adjusted before modelling. For example, the average cost of a new house will have increased over the last few decades due to inflation. A $200,000 house this year is not the same as a $200,000 house twenty years ago. For this reason, financial time series are usually adjusted so that all values are stated in dollar values from a particular year. For example, the house price data may be stated in year 2000 dollars.

To make these adjustments, a price index is used. If \(z_{t}\) denotes the price index and \(y_{t}\) denotes the original house price in year \(t\), then \(x_{t} = y_{t}/z_{t} \* z_{2000}\) gives the adjusted house price at year 2000 dollar values. Price indexes are often constructed by government agencies. For consumer goods, a common price index is the Consumer Price Index (or CPI).

This allows us to compare the growth or decline of industries relative to a common price value. For example, looking at aggregate annual “newspaper and book” retail turnover from `aus_retail`, and adjusting the data for inflation using CPI from `global_economy` allows us to understand the changes over time.

```
print_retail <- aus_retail |>
  filter(Industry == "Newspaper and book retailing") |>
  group_by(Industry) |>
  index_by(Year = year(Month)) |>
  summarise(Turnover = sum(Turnover))
aus_economy <- global_economy |>
  filter(Code == "AUS")
```

```
print_retail |>
  left_join(aus_economy, by = "Year") |>
  mutate(Adjusted_turnover = Turnover / CPI * 100) |>
  pivot_longer(c(Turnover, Adjusted_turnover),
               values_to = "Turnover") |>
  mutate(name = factor(name,
         levels=c("Turnover","Adjusted_turnover"))) |>
  ggplot(aes(x = Year, y = Turnover)) +
  geom_line() +
  facet_grid(name ~ ., scales = "free_y") +
  labs(title = "Turnover: Australian print media industry",
       y = "$AU")
```

![Turnover for the Australian print media industry in Australian dollars. The 'Adjusted' turnover has been adjusted for inflation using the CPI.](https://otexts.com/fpp3/fpp_files/figure-html/printretail-1.png)

Figure 3.2: Turnover for the Australian print media industry in Australian dollars. The ‘Adjusted’ turnover has been adjusted for inflation using the CPI.

By adjusting for inflation using the CPI, we can see that Australia’s newspaper and book retailing industry has been in decline much longer than the original data suggests. The adjusted turnover is in 2010 Australian dollars, as CPI is 100 in 2010 in this data set.

### Mathematical transformations

If the data shows variation that increases or decreases with the level of the series, then a transformation can be useful. For example, a logarithmic transformation is often useful. If we denote the original observations as \(y_{1},\dots,y_{T}\) and the transformed observations as \(w_{1}, \dots, w_{T}\), then \(w_t = \log(y_t)\). Logarithms are useful because they are interpretable: changes in a log value are relative (or percentage) changes on the original scale. So if log base 10 is used, then an increase of 1 on the log scale corresponds to a multiplication of 10 on the original scale. If any value of the original series is zero or negative, then logarithms are not possible.

Sometimes other transformations are also used (although they are not so interpretable). For example, square roots and cube roots can be used. These are called **power transformations** because they can be written in the form \(w_{t} = y_{t}^p\).

A useful family of transformations, that includes both logarithms and power transformations, is the family of **Box-Cox transformations** ([Box & Cox, 1964](#ref-BC64)), which depend on the parameter \(\lambda\) and are defined as follows:
\[\begin{equation}
w_t =
\begin{cases}
\log(y_t) & \text{if $\lambda=0$}; \\
(\text{sign}(y_t)|y_t|^\lambda-1)/\lambda & \text{otherwise}.
\end{cases}
\tag{3.1}
\end{equation}\]
This is actually a modified Box-Cox transformation, discussed in Bickel & Doksum ([1981](#ref-Bickel1981)), which allows for negative values of \(y_t\) provided \(\lambda > 0\).

The logarithm in a Box-Cox transformation is always a natural logarithm (i.e., to base \(e\)). So if \(\lambda=0\), natural logarithms are used, but if \(\lambda\ne0\), a power transformation is used, followed by some simple scaling.

If \(\lambda=1\), then \(w_t = y_t-1\), so the transformed data is shifted downwards but there is no change in the shape of the time series. For all other values of \(\lambda\), the time series will change shape.

Use the slider below to see the effect of varying \(\lambda\) to transform Australian quarterly gas production:

Figure 3.3: Box-Cox transformations applied to Australian quarterly gas production.

A good value of \(\lambda\) is one which makes the size of the seasonal variation about the same across the whole series, as that makes the forecasting model simpler. In this case, \(\lambda=0.10\) works quite well, although any value of \(\lambda\) between 0.0 and 0.2 would give similar results.

The `guerrero` feature ([Guerrero, 1993](#ref-Guerrero93)) can be used to choose a value of lambda for you. In this case it chooses \(\lambda=0.11\). (See the next chapter for discussion of the `features()` function.)

```
lambda <- aus_production |>
  features(Gas, features = guerrero) |>
  pull(lambda_guerrero)
aus_production |>
  autoplot(box_cox(Gas, lambda)) +
  labs(y = "",
       title = latex2exp::TeX(paste0(
         "Transformed gas production with $\\lambda$ = ",
         round(lambda,2))))
```

![Transformed Australian quarterly gas production with the $\lambda$ parameter chosen using the Guerrero method.](https://otexts.com/fpp3/fpp_files/figure-html/BoxCoxlambda-1.png)

Figure 3.4: Transformed Australian quarterly gas production with the \(\lambda\) parameter chosen using the Guerrero method.

### Bibliography

Bickel, P. J., & Doksum, K. A. (1981). An analysis of transformations revisited. *Journal of the American Statistical Association*, *76*(374), 296–311.

Box, G. E. P., & Cox, D. R. (1964). An analysis of transformations. *Journal of the Royal Statistical Society. Series B, Statistical Methodology*, *26*(2), 211–252.

Guerrero, V. M. (1993). Time-series analysis supported by power transformations. *Journal of Forecasting*, *12*(1), 37–48.

## 3.2 Time series components

If we assume an additive decomposition, then we can write
\[
y_{t} = S_{t} + T_{t} + R_t,
\]
where \(y_{t}\) is the data, \(S_{t}\) is the seasonal component, \(T_{t}\) is the trend-cycle component, and \(R_t\) is the remainder component, all at period \(t\). Alternatively, a multiplicative decomposition would be written as
\[
y_{t} = S_{t} \times T_{t} \times R_t.
\]

The additive decomposition is the most appropriate if the magnitude of the seasonal fluctuations, or the variation around the trend-cycle, does not vary with the level of the time series. When the variation in the seasonal pattern, or the variation around the trend-cycle, appears to be proportional to the level of the time series, then a multiplicative decomposition is more appropriate. Multiplicative decompositions are common with economic time series.

An alternative to using a multiplicative decomposition is to first transform the data until the variation in the series appears to be stable over time, then use an additive decomposition. When a log transformation has been used, this is equivalent to using a multiplicative decomposition on the original data because
\[
y_{t} = S_{t} \times T_{t} \times R_t \quad\text{is equivalent to}\quad
\log y_{t} = \log S_{t} + \log T_{t} + \log R_t.
\]

### Example: Employment in the US retail sector

We will look at several methods for obtaining the components \(S_{t}\), \(T_{t}\) and \(R_{t}\) later in this chapter, but first it is helpful to see an example. We will decompose the number of persons employed in retail as shown in Figure [3.5](https://otexts.com/fpp3/components.html#fig:usretailemployment). The data shows the total monthly number of persons in thousands employed in the retail sector across the US since 1990.

```
us_retail_employment <- us_employment |>
  filter(year(Month) >= 1990, Title == "Retail Trade") |>
  select(-Series_ID)
autoplot(us_retail_employment, Employed) +
  labs(y = "Persons (thousands)",
       title = "Total employment in US retail")
```

![Total number of persons employed in US retail.](https://otexts.com/fpp3/fpp_files/figure-html/usretailemployment-1.png)

Figure 3.5: Total number of persons employed in US retail.

To illustrate the ideas, we will use the STL decomposition method, which is discussed in Section [3.6](https://otexts.com/fpp3/stl.html#stl).

```
dcmp <- us_retail_employment |>
  model(stl = STL(Employed))
components(dcmp)
#> # A dable: 357 x 7 [1M]
#> # Key:     .model [1]
#> # :        Employed = trend + season_year + remainder
#>    .model    Month Employed  trend season_year remainder season_adjust
#>    <chr>     <mth>    <dbl>  <dbl>       <dbl>     <dbl>         <dbl>
#>  1 stl    1990 Jan   13256. 13288.      -33.0      0.836        13289.
#>  2 stl    1990 Feb   12966. 13269.     -258.     -44.6          13224.
#>  3 stl    1990 Mar   12938. 13250.     -290.     -22.1          13228.
#>  4 stl    1990 Apr   13012. 13231.     -220.       1.05         13232.
#>  5 stl    1990 May   13108. 13211.     -114.      11.3          13223.
#>  6 stl    1990 Jun   13183. 13192.      -24.3     15.5          13207.
#>  7 stl    1990 Jul   13170. 13172.      -23.2     21.6          13193.
#>  8 stl    1990 Aug   13160. 13151.       -9.52    17.8          13169.
#>  9 stl    1990 Sep   13113. 13131.      -39.5     22.0          13153.
#> 10 stl    1990 Oct   13185. 13110.       61.6     13.2          13124.
#> # ℹ 347 more rows
```

The output above shows the components of an STL decomposition. The original data is shown (as `Employed`), followed by the estimated components. This output forms a “dable” or decomposition table. The header to the table shows that the `Employed` series has been decomposed additively.

The `trend` column (containing the trend-cycle \(T_t\)) follows the overall movement of the series, ignoring any seasonality and random fluctuations, as shown in Figure [3.6](https://otexts.com/fpp3/components.html#fig:empltrend).

```
components(dcmp) |>
  as_tsibble() |>
  autoplot(Employed, colour="gray") +
  geom_line(aes(y=trend), colour = "#D55E00") +
  labs(
    y = "Persons (thousands)",
    title = "Total employment in US retail"
  )
```

![Total number of persons employed in US retail: the trend-cycle component (orange) and the raw data (grey).](https://otexts.com/fpp3/fpp_files/figure-html/empltrend-1.png)

Figure 3.6: Total number of persons employed in US retail: the trend-cycle component (orange) and the raw data (grey).

We can plot all of the components in a single figure using `autoplot()`, as shown in Figure [3.7](https://otexts.com/fpp3/components.html#fig:emplstl).

```
components(dcmp) |> autoplot()
```

![The total number of persons employed in US retail (top) and its three additive components.](https://otexts.com/fpp3/fpp_files/figure-html/emplstl-1.png)

Figure 3.7: The total number of persons employed in US retail (top) and its three additive components.

The three components are shown separately in the bottom three panels. These components can be added together to reconstruct the data shown in the top panel. Notice that the seasonal component changes over time, so that any two consecutive years have similar patterns, but years far apart may have different seasonal patterns. The remainder component shown in the bottom panel is what is left over when the seasonal and trend-cycle components have been subtracted from the data.

The grey bars to the left of each panel show the relative scales of the components. Each grey bar represents the same length but because the plots are on different scales, the bars vary in size. The large grey bar in the bottom panel shows that the variation in the remainder component is smallest compared to the variation in the data. If we shrank the bottom three panels until their bars became the same size as that in the data panel, then all the panels would be on the same scale.

### Seasonally adjusted data

If the seasonal component is removed from the original data, the resulting values are the “seasonally adjusted” data. For an additive decomposition, the seasonally adjusted data are given by \(y_{t}-S_{t}\), and for multiplicative data, the seasonally adjusted values are obtained using \(y_{t}/S_{t}\).

Figure [3.8](https://otexts.com/fpp3/components.html#fig:empl-retail-sa) shows the seasonally adjusted number of persons employed.

```
components(dcmp) |>
  as_tsibble() |>
  autoplot(Employed, colour = "gray") +
  geom_line(aes(y=season_adjust), colour = "#0072B2") +
  labs(y = "Persons (thousands)",
       title = "Total employment in US retail")
```

![Seasonally adjusted retail employment data (blue) and the original data (grey).](https://otexts.com/fpp3/fpp_files/figure-html/empl-retail-sa-1.png)

Figure 3.8: Seasonally adjusted retail employment data (blue) and the original data (grey).

If the variation due to seasonality is not of primary interest, the seasonally adjusted series can be useful. For example, monthly unemployment data are usually seasonally adjusted in order to highlight variation due to the underlying state of the economy rather than the seasonal variation. An increase in unemployment due to school leavers seeking work is seasonal variation, while an increase in unemployment due to an economic recession is non-seasonal. Most economic analysts who study unemployment data are more interested in the non-seasonal variation. Consequently, employment data (and many other economic series) are usually seasonally adjusted.

Seasonally adjusted series contain the remainder component as well as the trend-cycle. Therefore, they are not “smooth”, and “downturns” or “upturns” can be misleading. If the purpose is to look for turning points in a series, and interpret any changes in direction, then it is better to use the trend-cycle component rather than the seasonally adjusted data.

## 3.3 Moving averages

The classical method of time series decomposition originated in the 1920s and was widely used until the 1950s. It still forms the basis of many time series decomposition methods, so it is important to understand how it works. The first step in a classical decomposition is to use a moving average method to estimate the trend-cycle, so we begin by discussing moving averages.

### Moving average smoothing

A moving average of order \(m\) can be written as
\[\begin{equation}
\hat{T}_{t} = \frac{1}{m} \sum_{j=-k}^k y_{t+j}, \tag{3.2}
\end{equation}\]
where \(m=2k+1\). That is, the estimate of the trend-cycle at time \(t\) is obtained by averaging values of the time series within \(k\) periods of \(t\). Observations that are nearby in time are also likely to be close in value. Therefore, the average eliminates some of the randomness in the data, leaving a smooth trend-cycle component. We call this an **\(m\)-MA**, meaning a moving average of order \(m\).

For example, consider Figure [3.9](https://otexts.com/fpp3/moving-averages.html#fig:aus-exports) which shows exports of goods and services for Australia as a percentage of GDP from 1960 to 2017. The data are also shown in Table [3.1](https://otexts.com/fpp3/moving-averages.html#tab:aus-exports-tbl).

```
global_economy |>
  filter(Country == "Australia") |>
  autoplot(Exports) +
  labs(y = "% of GDP", title = "Total Australian exports")
```

![Australian exports of goods and services: 1960--2017.](https://otexts.com/fpp3/fpp_files/figure-html/aus-exports-1.png)

Figure 3.9: Australian exports of goods and services: 1960–2017.

Table 3.1: Annual Australian exports of goods and services: 1960–2017.

| Year | Exports | 5-MA |
| --- | --- | --- |
| 1960 | 12.99 |  |
| 1961 | 12.40 |  |
| 1962 | 13.94 | 13.46 |
| 1963 | 13.01 | 13.50 |
| 1964 | 14.94 | 13.61 |
| 1965 | 13.22 | 13.40 |
| 1966 | 12.93 | 13.25 |
| 1967 | 12.88 | 12.66 |
| … | … | … |
| 2010 | 19.84 | 21.21 |
| 2011 | 21.47 | 21.17 |
| 2012 | 21.52 | 20.78 |
| 2013 | 19.99 | 20.81 |
| 2014 | 21.08 | 20.37 |
| 2015 | 20.01 | 20.32 |
| 2016 | 19.25 |  |
| 2017 | 21.27 |  |

In the last column of this table, a moving average of order 5 is shown, providing an estimate of the trend-cycle. The first value in this column is the average of the first five observations, 1960–1964; the second value in the 5-MA column is the average of the values for 1961–1965; and so on. Each value in the 5-MA column is the average of the observations in the five year window centred on the corresponding year. In the notation of Equation [(3.2)](https://otexts.com/fpp3/moving-averages.html#eq:ma), column 5-MA contains the values of \(\hat{T}_{t}\) with \(k=2\) and \(m=2k+1=5\). There are no values for either the first two years or the last two years, because we do not have two observations on either side. Later we will use more sophisticated methods of trend-cycle estimation which do allow estimates near the endpoints.

This is easily computed using `slide_dbl()` from the `slider` package which applies a function to “sliding” time windows. In this case, we use the `mean()` function with a window of size 5.

```
aus_exports <- global_economy |>
  filter(Country == "Australia") |>
  mutate(
    `5-MA` = slider::slide_dbl(Exports, mean,
                .before = 2, .after = 2, .complete = TRUE)
  )
```

To see what the trend-cycle estimate looks like, we plot it along with the original data in Figure [3.10](https://otexts.com/fpp3/moving-averages.html#fig:aus-exports-plot).

```
aus_exports |>
  autoplot(Exports) +
  geom_line(aes(y = `5-MA`), colour = "#D55E00") +
  labs(y = "% of GDP",
       title = "Total Australian exports")
```

![Australian exports (black) along with the 5-MA estimate of the trend-cycle (orange).](https://otexts.com/fpp3/fpp_files/figure-html/aus-exports-plot-1.png)

Figure 3.10: Australian exports (black) along with the 5-MA estimate of the trend-cycle (orange).

Notice that the trend-cycle (in orange) is smoother than the original data and captures the main movement of the time series without all of the minor fluctuations. The order of the moving average determines the smoothness of the trend-cycle estimate. In general, a larger order means a smoother curve. Figure [3.11](https://otexts.com/fpp3/moving-averages.html#fig:aus-exports-compare) shows the effect of changing the order of the moving average for the Australian exports data.

![Different moving averages applied to the Australian exports data.](https://otexts.com/fpp3/fpp_files/figure-html/aus-exports-compare-1.png)

Figure 3.11: Different moving averages applied to the Australian exports data.

Simple moving averages such as these are usually of an odd order (e.g., 3, 5, 7, etc.). This is so they are symmetric: in a moving average of order \(m=2k+1\), the middle observation, and \(k\) observations on either side, are averaged. But if \(m\) was even, it would no longer be symmetric.

### Moving averages of moving averages

It is possible to apply a moving average to a moving average. One reason for doing this is to make an even-order moving average symmetric.

For example, we might take a moving average of order 4, and then apply another moving average of order 2 to the results. In the following table, this has been done for the first few years of the Australian quarterly beer production data.

```
beer <- aus_production |>
  filter(year(Quarter) >= 1992) |>
  select(Quarter, Beer)
beer_ma <- beer |>
  mutate(
    `4-MA` = slider::slide_dbl(Beer, mean,
                .before = 1, .after = 2, .complete = TRUE),
    `2x4-MA` = slider::slide_dbl(`4-MA`, mean,
                .before = 1, .after = 0, .complete = TRUE)
  )
```

Table 3.2: A moving average of order 4 applied to the quarterly beer data, followed by a moving average of order 2.

| Quarter | Beer | 4-MA | 2x4-MA |
| --- | --- | --- | --- |
| 1992 Q1 | 443.00 |  |  |
| 1992 Q2 | 410.00 | 451.25 |  |
| 1992 Q3 | 420.00 | 448.75 | 450.00 |
| 1992 Q4 | 532.00 | 451.50 | 450.12 |
| 1993 Q1 | 433.00 | 449.00 | 450.25 |
| 1993 Q2 | 421.00 | 444.00 | 446.50 |
| … | … | … | … |
| 2009 Q1 | 415.00 | 430.00 | 428.88 |
| 2009 Q2 | 398.00 | 430.00 | 430.00 |
| 2009 Q3 | 419.00 | 429.75 | 429.88 |
| 2009 Q4 | 488.00 | 423.75 | 426.75 |
| 2010 Q1 | 414.00 |  |  |
| 2010 Q2 | 374.00 |  |  |

The notation “\(2\times4\)-MA” in the last column means a 4-MA followed by a 2-MA. The values in the last column are obtained by taking a moving average of order 2 of the values in the previous column. For example, the first two values in the 4-MA column are
451.25=(443+410+420+532)/4
and
448.75=(410+420+532+433)/4.
The first value in the 2x4-MA column is the average of these two:
450.00=(451.25+448.75)/2.

When a 2-MA follows a moving average of an even order (such as 4), it is called a “centred moving average of order 4”. This is because the results are now symmetric. To see that this is the case, we can write the \(2\times4\)-MA as follows:
\[\begin{align\*}
\hat{T}_{t} &= \frac{1}{2}\Big[
\frac{1}{4} (y_{t-2}+y_{t-1}+y_{t}+y_{t+1}) +
\frac{1}{4} (y_{t-1}+y_{t}+y_{t+1}+y_{t+2})\Big] \\
&= \frac{1}{8}y_{t-2}+\frac14y_{t-1} +
\frac14y_{t}+\frac14y_{t+1}+\frac18y_{t+2}.
\end{align\*}\]
It is now a weighted average of observations that is symmetric.

Other combinations of moving averages are also possible. For example, a \(3\times3\)-MA is often used, and consists of a moving average of order 3 followed by another moving average of order 3. In general, an even order MA should be followed by an even order MA to make it symmetric. Similarly, an odd order MA should be followed by an odd order MA.

### Estimating the trend-cycle with seasonal data

The most common use of centred moving averages is for estimating the trend-cycle from seasonal data. Consider the \(2\times4\)-MA:
\[
\hat{T}_{t} = \frac{1}{8}y_{t-2} + \frac14y_{t-1} +
\frac14y_{t} + \frac14y_{t+1} + \frac18y_{t+2}.
\]
When applied to quarterly data, each quarter of the year is given equal weight as the first and last terms apply to the same quarter in consecutive years. Consequently, the seasonal variation will be averaged out and the resulting values of \(\hat{T}_t\) will have little or no seasonal variation remaining. A similar effect would be obtained using a \(2\times 8\)-MA or a \(2\times 12\)-MA to quarterly data.

In general, a \(2\times m\)-MA is equivalent to a weighted moving average of order \(m+1\) where all observations take the weight \(1/m\), except for the first and last terms which take weights \(1/(2m)\). So, if the seasonal period is even and of order \(m\), we use a \(2\times m\)-MA to estimate the trend-cycle. If the seasonal period is odd and of order \(m\), we use a \(m\)-MA to estimate the trend-cycle. For example, a \(2\times 12\)-MA can be used to estimate the trend-cycle of monthly data with annual seasonality and a 7-MA can be used to estimate the trend-cycle of daily data with a weekly seasonality.

Other choices for the order of the MA will usually result in trend-cycle estimates being contaminated by the seasonality in the data.

### Example: Employment in the US retail sector

```
us_retail_employment_ma <- us_retail_employment |>
  mutate(
    `12-MA` = slider::slide_dbl(Employed, mean,
                .before = 5, .after = 6, .complete = TRUE),
    `2x12-MA` = slider::slide_dbl(`12-MA`, mean,
                .before = 1, .after = 0, .complete = TRUE)
  )
us_retail_employment_ma |>
  autoplot(Employed, colour = "gray") +
  geom_line(aes(y = `2x12-MA`), colour = "#D55E00") +
  labs(y = "Persons (thousands)",
       title = "Total employment in US retail")
```

![A 2x12-MA applied to the US retail employment series.](https://otexts.com/fpp3/fpp_files/figure-html/empl-MA-1.png)

Figure 3.12: A 2x12-MA applied to the US retail employment series.

Figure [3.12](https://otexts.com/fpp3/moving-averages.html#fig:empl-MA) shows a \(2\times12\)-MA applied to the total number of persons employed in the US retail sector. Notice that the smooth line shows no seasonality; it is almost the same as the trend-cycle shown in Figure [3.6](https://otexts.com/fpp3/components.html#fig:empltrend), which was estimated using a much more sophisticated method than a moving average. Any other choice for the order of the moving average (except for 24, 36, etc.) would have resulted in a smooth line that showed some seasonal fluctuations.

### Weighted moving averages

Combinations of moving averages result in weighted moving averages. For example, the \(2\times4\)-MA discussed above is equivalent to a weighted 5-MA with weights given by
\(\left[\frac{1}{8},\frac{1}{4},\frac{1}{4},\frac{1}{4},\frac{1}{8}\right]\). In general, a weighted \(m\)-MA can be written as
\[
\hat{T}_t = \sum_{j=-k}^k a_j y_{t+j},
\]
where \(k=(m-1)/2\), and the weights are given by \(\left[a_{-k},\dots,a_k\right]\). It is important that the weights all sum to one and that they are symmetric so that \(a_j = a_{-j}\). The simple \(m\)-MA is a special case where all of the weights are equal to \(1/m\).

A major advantage of weighted moving averages is that they yield a smoother estimate of the trend-cycle. Instead of observations entering and leaving the calculation at full weight, their weights slowly increase and then slowly decrease, resulting in a smoother curve.

## 3.4 Classical decomposition

The classical decomposition method originated in the 1920s. It is a relatively simple procedure, and forms the starting point for most other methods of time series decomposition. There are two forms of classical decomposition: an additive decomposition and a multiplicative decomposition. These are described below for a time series with seasonal period \(m\) (e.g., \(m=4\) for quarterly data, \(m=12\) for monthly data, \(m=7\) for daily data with a weekly pattern).

In classical decomposition, we assume that the seasonal component is constant from year to year. For multiplicative seasonality, the \(m\) values that form the seasonal component are sometimes called the “seasonal indices”.

### Additive decomposition

Step 1
:   If \(m\) is an even number, compute the trend-cycle component \(\hat{T}_t\) using a \(2\times m\)-MA. If \(m\) is an odd number, compute the trend-cycle component \(\hat{T}_t\) using an \(m\)-MA.

Step 2
:   Calculate the detrended series: \(y_t - \hat{T}_t\).

Step 3
:   To estimate the seasonal component for each season, simply average the detrended values for that season. For example, with monthly data, the seasonal component for March is the average of all the detrended March values in the data. These seasonal component values are then adjusted to ensure that they add to zero. The seasonal component is obtained by stringing together these monthly values, and then replicating the sequence for each year of data. This gives \(\hat{S}_t\).

Step 4
:   The remainder component is calculated by subtracting the estimated seasonal and trend-cycle components: \(\hat{R}_t = y_t - \hat{T}_t - \hat{S}_t\).

Figure [3.13](https://otexts.com/fpp3/classical-decomposition.html#fig:classical-empl) shows a classical decomposition of the total retail employment series across the US.

```
us_retail_employment |>
  model(
    classical_decomposition(Employed, type = "additive")
  ) |>
  components() |>
  autoplot() +
  labs(title = "Classical additive decomposition of total
                  US retail employment")
```

![A classical additive decomposition of US retail employment.](https://otexts.com/fpp3/fpp_files/figure-html/classical-empl-1.png)

Figure 3.13: A classical additive decomposition of US retail employment.

### Multiplicative decomposition

A classical multiplicative decomposition is similar, except that the subtractions are replaced by divisions.

Step 1
:   If \(m\) is an even number, compute the trend-cycle component \(\hat{T}_t\) using a \(2\times m\)-MA. If \(m\) is an odd number, compute the trend-cycle component \(\hat{T}_t\) using an \(m\)-MA.

Step 2
:   Calculate the detrended series: \(y_t/ \hat{T}_t\).

Step 3
:   To estimate the seasonal component for each season, simply average the detrended values for that season. For example, with monthly data, the seasonal index for March is the average of all the detrended March values in the data. These seasonal indexes are then adjusted to ensure that they add to \(m\). The seasonal component is obtained by stringing together these monthly indexes, and then replicating the sequence for each year of data. This gives \(\hat{S}_t\).

Step 4
:   The remainder component is calculated by dividing out the estimated seasonal and trend-cycle components: \(\hat{R}_{t} = y_t /( \hat{T}_t \hat{S}_t)\).

### Comments on classical decomposition

While classical decomposition is still widely used, it is not recommended, as there are now several much better methods. Some of the problems with classical decomposition are summarised below.

* The estimate of the trend-cycle is unavailable for the first few and last few observations. For example, if \(m=12\), there is no trend-cycle estimate for the first six or the last six observations. Consequently, there is also no estimate of the remainder component for the same time periods.
* The trend-cycle estimate tends to over-smooth rapid rises and falls in the data.
* Classical decomposition methods assume that the seasonal component repeats from year to year. For many series, this is a reasonable assumption, but for some longer series it is not. For example, electricity demand patterns have changed over time as air conditioning has become more widespread. In many locations, the seasonal usage pattern from several decades ago had its maximum demand in winter (due to heating), while the current seasonal pattern has its maximum demand in summer (due to air conditioning). Classical decomposition methods are unable to capture these seasonal changes over time.
* Occasionally, the values of the time series in a small number of periods may be particularly unusual. For example, the monthly air passenger traffic may be affected by an industrial dispute, making the traffic during the dispute different from usual. The classical method is not robust to these kinds of unusual values.

## 3.5 Methods used by official statistics agencies

Official statistics agencies (such as the US Census Bureau and the Australian Bureau of Statistics) are responsible for a large number of official economic and social time series. These agencies have developed their own decomposition procedures which are used for seasonal adjustment. Most of them use variants of the X-11 method, or the SEATS method, or a combination of the two. These methods are designed specifically to work with quarterly and monthly data, which are the most common series handled by official statistics agencies. They will not handle seasonality of other kinds, such as daily data, or hourly data, or weekly data. We will use the latest implementation of this group of methods known as “X-13ARIMA-SEATS”. For the methods discussed in this section, you will need to have installed the `seasonal` package in R.

### X-11 method

The X-11 method originated in the US Census Bureau and was further developed by Statistics Canada. It is based on classical decomposition, but includes many extra steps and features in order to overcome the drawbacks of classical decomposition that were discussed in the previous section. In particular, trend-cycle estimates are available for all observations including the end points, and the seasonal component is allowed to vary slowly over time. X-11 also handles trading day variation, holiday effects and the effects of known predictors. There are methods for both additive and multiplicative decomposition. The process is entirely automatic and tends to be highly robust to outliers and level shifts in the time series. The details of the X-11 method are described in Dagum & Bianconcini ([2016](#ref-Dagum2016)).

```
x11_dcmp <- us_retail_employment |>
  model(x11 = X_13ARIMA_SEATS(Employed ~ x11())) |>
  components()
autoplot(x11_dcmp) +
  labs(title =
    "Decomposition of total US retail employment using X-11.")
```

![A multiplicative decomposition of US retail employment using X-11.](https://otexts.com/fpp3/fpp_files/figure-html/x11-1.png)

Figure 3.14: A multiplicative decomposition of US retail employment using X-11.

Compare this decomposition with the STL decomposition shown in Figure [3.7](https://otexts.com/fpp3/components.html#fig:emplstl) and the classical decomposition shown in Figure [3.13](https://otexts.com/fpp3/classical-decomposition.html#fig:classical-empl). The default approach for `X_13ARIMA_SEATS` shown here is a multiplicative decomposition, whereas the STL and classical decompositions shown earlier were additive; but it doesn’t make much difference in this case. The X-11 trend-cycle has captured the sudden fall in the data due to the 2007–2008 global financial crisis better than either of the other two methods (where the effect of the crisis has leaked into the remainder component). Also, the unusual observation in 1996 is now more clearly seen in the X-11 remainder component.

Figure [3.15](https://otexts.com/fpp3/methods-used-by-official-statistics-agencies.html#fig:x11-seasadj) shows the trend-cycle component and the seasonally adjusted data, along with the original data. The seasonally adjusted data is very similar to the trend-cycle component in this example, so it is hard to distinguish them on the plot.

```
x11_dcmp |>
  ggplot(aes(x = Month)) +
  geom_line(aes(y = Employed, colour = "Data")) +
  geom_line(aes(y = season_adjust,
                colour = "Seasonally Adjusted")) +
  geom_line(aes(y = trend, colour = "Trend")) +
  labs(y = "Persons (thousands)",
       title = "Total employment in US retail") +
  scale_colour_manual(
    values = c("gray", "#0072B2", "#D55E00"),
    breaks = c("Data", "Seasonally Adjusted", "Trend")
  )
```

![US retail employment: the original data (grey), the trend-cycle component (orange) and the seasonally adjusted data (barely visible in blue).](https://otexts.com/fpp3/fpp_files/figure-html/x11-seasadj-1.png)

Figure 3.15: US retail employment: the original data (grey), the trend-cycle component (orange) and the seasonally adjusted data (barely visible in blue).

It can be useful to use seasonal plots and seasonal sub-series plots of the seasonal component, to help us visualise the variation in the seasonal component over time. Figure [3.16](https://otexts.com/fpp3/methods-used-by-official-statistics-agencies.html#fig:print-media3) shows a seasonal sub-series plot of the seasonal component from Figure [3.14](https://otexts.com/fpp3/methods-used-by-official-statistics-agencies.html#fig:x11). In this case, there are only small changes over time.

```
x11_dcmp |>
  gg_subseries(seasonal)
```

![Seasonal sub-series plot of the seasonal component from the X-11 method applied to total US retail employment.](https://otexts.com/fpp3/fpp_files/figure-html/print-media3-1.png)

Figure 3.16: Seasonal sub-series plot of the seasonal component from the X-11 method applied to total US retail employment.

### SEATS method

“SEATS” stands for “Seasonal Extraction in ARIMA Time Series” (ARIMA models are discussed in Chapter [9](https://otexts.com/fpp3/arima.html#arima)). This procedure was developed at the Bank of Spain, and is now widely used by government agencies around the world. The details are beyond the scope of this book. However, a complete discussion of the method is available in Dagum & Bianconcini ([2016](#ref-Dagum2016)).

```
seats_dcmp <- us_retail_employment |>
  model(seats = X_13ARIMA_SEATS(Employed ~ seats())) |>
  components()
autoplot(seats_dcmp) +
  labs(title =
    "Decomposition of total US retail employment using SEATS")
```

![A  decomposition of US retail employment obtained using SEATS.](https://otexts.com/fpp3/fpp_files/figure-html/seats-1.png)

Figure 3.17: A decomposition of US retail employment obtained using SEATS.

Figure [3.17](https://otexts.com/fpp3/methods-used-by-official-statistics-agencies.html#fig:seats) shows the SEATS method applied to the total retail employment series across the US. The result is quite similar to that obtained using the X-11 method shown in Figure [3.14](https://otexts.com/fpp3/methods-used-by-official-statistics-agencies.html#fig:x11).

The `X_13ARIMA_SEATS()` function calls the `seasonal` package which has many options for handling variations of X-11 and SEATS. See [the package website](https://bit.ly/seaspkg) for a detailed introduction to the options and features available.

### Bibliography

Dagum, E. B., & Bianconcini, S. (2016). *Seasonal adjustment methods and real time trend-cycle estimation*. Springer.

## 3.6 STL decomposition

STL is a versatile and robust method for decomposing time series. STL is an acronym for “Seasonal and Trend decomposition using Loess”, while loess is a method for estimating nonlinear relationships. The STL method was developed by R. B. Cleveland et al. ([1990](#ref-Cleveland1990)), and later extended to handle multiple seasonal patterns by Bandara et al. ([2025](#ref-mstl)).

STL has several advantages over classical decomposition, and the SEATS and X-11 methods:

* Unlike SEATS and X-11, STL will handle any type of seasonality, not only monthly and quarterly data.
* The seasonal component is allowed to change over time, and the rate of change can be controlled by the user.
* The smoothness of the trend-cycle can also be controlled by the user.
* It can be robust to outliers (i.e., the user can specify a robust decomposition), so that occasional unusual observations will not affect the estimates of the trend-cycle and seasonal components. They will, however, affect the remainder component.

On the other hand, STL has some disadvantages. In particular, it does not handle trading day or calendar variation automatically, and it only provides facilities for additive decompositions.

A multiplicative decomposition can be obtained by first taking logs of the data, then back-transforming the components. Decompositions that are between additive and multiplicative can be obtained using a Box-Cox transformation of the data with \(0<\lambda<1\). A value of \(\lambda=0\) gives a multiplicative decomposition while \(\lambda=1\) gives an additive decomposition.

The best way to begin learning how to use STL is to see some examples and experiment with the settings. Figure [3.7](https://otexts.com/fpp3/components.html#fig:emplstl) showed an example of an STL decomposition applied to the total US retail employment series. Figure [3.18](https://otexts.com/fpp3/stl.html#fig:empl-stl2) shows an alternative STL decomposition where the trend-cycle is more flexible, the seasonal pattern is fixed, and the robust option has been used.

```
us_retail_employment |>
  model(
    STL(Employed ~ trend(window = 7) +
                   season(window = "periodic"),
    robust = TRUE)) |>
  components() |>
  autoplot()
```

![Total US retail employment (top) and its three additive components obtained from a robust STL decomposition with flexible trend-cycle and fixed seasonality.](https://otexts.com/fpp3/fpp_files/figure-html/empl-stl2-1.png)

Figure 3.18: Total US retail employment (top) and its three additive components obtained from a robust STL decomposition with flexible trend-cycle and fixed seasonality.

The two main parameters to be chosen when using STL are the trend-cycle window `trend(window = ?)` and the seasonal window `season(window = ?)`. These control how rapidly the trend-cycle and seasonal components can change. Smaller values allow for more rapid changes. Both trend and seasonal windows should be odd numbers; trend window is the number of consecutive observations to be used when estimating the trend-cycle; season window is the number of consecutive years to be used in estimating each value in the seasonal component. Setting the seasonal window to be infinite is equivalent to forcing the seasonal component to be periodic `season(window='periodic')` (i.e., identical across years). This was the case in Figure [3.18](https://otexts.com/fpp3/stl.html#fig:empl-stl2).

By default, the `STL()` function provides a convenient automated STL decomposition using a seasonal window of `season(window=11)` when there is a single seasonal period, and the trend window chosen automatically from the seasonal period. The default setting for monthly data is `trend(window=21)`. For multiple seasonal periods, the default seasonal windows are 11, 15, 19, etc., with larger windows corresponding to larger seasonal periods. This usually gives a good balance between overfitting the seasonality and allowing it to slowly change over time. But, as with any automated procedure, the default settings will need adjusting for some time series. In the example shown in Figure [3.7](https://otexts.com/fpp3/components.html#fig:emplstl), the default trend window setting produces a trend-cycle component that is too rigid. As a result, signal from the 2008 global financial crisis has leaked into the remainder component, as can be seen in the bottom panel of Figure [3.7](https://otexts.com/fpp3/components.html#fig:emplstl). Selecting a shorter trend window as in Figure [3.18](https://otexts.com/fpp3/stl.html#fig:empl-stl2) improves this.

### Bibliography

Bandara, K., Hyndman, R. J., & Bergmeir, C. (2025). MSTL: A seasonal-trend decomposition algorithm for time series with multiple seasonal patterns. *International J Operational Research*, *52*(1).

Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. J. (1990). STL: A seasonal-trend decomposition procedure based on loess. *Journal of Official Statistics*, *6*(1), 3–33.

## 3.7 Exercises

1. Consider the GDP information in `global_economy`. Plot the GDP per capita for each country over time. Which country has the highest GDP per capita? How has this changed over time?
2. For each of the following series, make a graph of the data. If transforming seems appropriate, do so and describe the effect.

   * United States GDP from `global_economy`.
   * Slaughter of Victorian “Bulls, bullocks and steers” in `aus_livestock`.
   * Victorian Electricity Demand from `vic_elec`.
   * Gas production from `aus_production`.
3. Why is a Box-Cox transformation unhelpful for the `canadian_gas` data?
4. What Box-Cox transformation would you select for your retail data (from Exercise 7 in Section [2.10](https://otexts.com/fpp3/graphics-exercises.html#graphics-exercises))?
5. For the following series, find an appropriate Box-Cox transformation in order to stabilise the variance. Tobacco from `aus_production`, Economy class passengers between Melbourne and Sydney from `ansett`, and Pedestrian counts at Southern Cross Station from `pedestrian`.
6. Show that a \(3\times5\) MA is equivalent to a 7-term weighted moving average with weights of 0.067, 0.133, 0.200, 0.200, 0.200, 0.133, and 0.067.
7. Consider the last five years of the Gas data from `aus_production`.

   ```
   gas <- tail(aus_production, 5*4) |> select(Gas)
   ```

   1. Plot the time series. Can you identify seasonal fluctuations and/or a trend-cycle?
   2. Use `classical_decomposition` with `type=multiplicative` to calculate the trend-cycle and seasonal indices.
   3. Do the results support the graphical interpretation from part a?
   4. Compute and plot the seasonally adjusted data.
   5. Change one observation to be an outlier (e.g., add 300 to one observation), and recompute the seasonally adjusted data. What is the effect of the outlier?
   6. Does it make any difference if the outlier is near the end rather than in the middle of the time series?
8. Recall your retail time series data (from Exercise 7 in Section [2.10](https://otexts.com/fpp3/graphics-exercises.html#graphics-exercises)).
   Decompose the series using X-11. Does it reveal any outliers, or unusual features that you had not noticed previously?
9. Figures [3.19](https://otexts.com/fpp3/decomposition-exercises.html#fig:labour) and [3.20](https://otexts.com/fpp3/decomposition-exercises.html#fig:labour2) show the result of decomposing the number of persons in the civilian labour force in Australia each month from February 1978 to August 1995.

   ![Decomposition of the number of persons in the civilian labour force in Australia each month from February 1978 to August 1995.](https://otexts.com/fpp3/fpp_files/figure-html/labour-1.png)

   Figure 3.19: Decomposition of the number of persons in the civilian labour force in Australia each month from February 1978 to August 1995.

   ![Seasonal component from the decomposition shown in the previous figure.](https://otexts.com/fpp3/fpp_files/figure-html/labour2-1.png)

   Figure 3.20: Seasonal component from the decomposition shown in the previous figure.

   1. Write about 3–5 sentences describing the results of the decomposition. Pay particular attention to the scales of the graphs in making your interpretation.
   2. Is the recession of 1991/1992 visible in the estimated components?
10. This exercise uses the `canadian_gas` data (monthly Canadian gas production in billions of cubic metres, January 1960 – February 2005).

    1. Plot the data using `autoplot()`, `gg_subseries()` and `gg_season()` to look at the effect of the changing seasonality over time.[3](#fn3)
    2. Do an STL decomposition of the data. You will need to choose a seasonal window to allow for the changing shape of the seasonal component.
    3. How does the seasonal shape change over time? [Hint: Try plotting the seasonal component using `gg_season()`.]
    4. Can you produce a plausible seasonally adjusted series?
    5. Compare the results with those obtained using SEATS and X-11. How are they different?

---

3. The evolving seasonal pattern is possibly due to changes in the regulation of gas prices — thanks to Lewis Kirvan for pointing this out.[↩︎](https://otexts.com/fpp3/decomposition-exercises.html#fnref3)

## 3.8 Further reading

* A detailed modern discussion of the SEATS and X-11 methods is provided by Dagum & Bianconcini ([2016](#ref-Dagum2016)).
* R. B. Cleveland et al. ([1990](#ref-Cleveland1990)) introduced STL, and still provides the best description of the algorithm.

### Bibliography

Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. J. (1990). STL: A seasonal-trend decomposition procedure based on loess. *Journal of Official Statistics*, *6*(1), 3–33.

Dagum, E. B., & Bianconcini, S. (2016). *Seasonal adjustment methods and real time trend-cycle estimation*. Springer.
