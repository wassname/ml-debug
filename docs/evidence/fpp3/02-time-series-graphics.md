Source: https://otexts.com/fpp3/graphics.html (chapter graphics, 12 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - 02-time-series-graphics
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Chapter 2 Time series graphics

The first thing to do in any data analysis task is to plot the data. Graphs enable many features of the data to be visualised, including patterns, unusual observations, changes over time, and relationships between variables. The features that are seen in plots of the data must then be incorporated, as much as possible, into the forecasting methods to be used. Just as the type of data determines what forecasting method to use, it also determines what graphs are appropriate. But before we produce graphs, we need to set up our time series in R.

## 2.1 `tsibble` objects

A time series can be thought of as a list of numbers (the observations), along with some information about what times those numbers were recorded (the index). This information can be stored as a `tsibble` object in R.

### The index variable

Suppose you have annual observations for the last few years:

| Year | Observation |
| --- | --- |
| 2015 | 123 |
| 2016 | 39 |
| 2017 | 78 |
| 2018 | 52 |
| 2019 | 110 |

We turn this into a `tsibble` object using the `tsibble()` function:

```
y <- tsibble(
  Year = 2015:2019,
  Observation = c(123, 39, 78, 52, 110),
  index = Year
)
```

`tsibble` objects extend tidy data frames (`tibble` objects) by introducing temporal structure. We have set the time series `index` to be the `Year` column, which associates the measurements (`Observation`) with the time of recording (`Year`).

For observations that are more frequent than once per year, we need to use a time class function on the index. For example, suppose we have a monthly dataset `z`:

```
z
#> # A tibble: 5 × 2
#>   Month    Observation
#>   <chr>          <dbl>
#> 1 2019 Jan          50
#> 2 2019 Feb          23
#> 3 2019 Mar          34
#> 4 2019 Apr          30
#> 5 2019 May          25
```

This can be converted to a `tsibble` object using the following code:

```
z |>
  mutate(Month = yearmonth(Month)) |>
  as_tsibble(index = Month)
#> # A tsibble: 5 x 2 [1M]
#>      Month Observation
#>      <mth>       <dbl>
#> 1 2019 Jan          50
#> 2 2019 Feb          23
#> 3 2019 Mar          34
#> 4 2019 Apr          30
#> 5 2019 May          25
```

First, the `Month` column is being converted from text to a monthly time object with `yearmonth()`. We then convert the data frame to a `tsibble` by identifying the `index` variable using `as_tsibble()`. Note the addition of “[1M]” on the first line indicating this is monthly data.

Other time class functions can be used depending on the frequency of the observations.

| Frequency | Function |
| --- | --- |
| Annual | `start:end` |
| Quarterly | `yearquarter()` |
| Monthly | `yearmonth()` |
| Weekly | `yearweek()` |
| Daily | `as_date()`, `ymd()` |
| Sub-daily | `as_datetime()`, `ymd_hms()` |

### The key variables

A `tsibble` also allows multiple time series to be stored in a single object. Suppose you are interested in a dataset containing the fastest running times for women’s and men’s track races at the Olympics, from 100m to 10000m:

```
olympic_running
#> # A tsibble: 312 x 4 [4Y]
#> # Key:       Length, Sex [14]
#>     Year Length Sex    Time
#>    <int>  <int> <chr> <dbl>
#>  1  1896    100 men    12
#>  2  1900    100 men    11
#>  3  1904    100 men    11
#>  4  1908    100 men    10.8
#>  5  1912    100 men    10.8
#>  6  1916    100 men    NA
#>  7  1920    100 men    10.8
#>  8  1924    100 men    10.6
#>  9  1928    100 men    10.8
#> 10  1932    100 men    10.3
#> # ℹ 302 more rows
```

The summary above shows that this is a `tsibble` object, which contains 312 rows and 4 columns. Alongside this, “[4Y]” informs us that the interval of these observations is every four years. Below this is the key structure, which informs us that there are 14 separate time series in the `tsibble`. A preview of the first 10 observations is also shown, in which we can see a missing value occurs in 1916. This is because the Olympics were not held during World War I.

The 14 time series in this object are uniquely identified by the keys: the `Length` and `Sex` variables. The `distinct()` function can be used to show the categories of each variable or even combinations of variables:

```
olympic_running |> distinct(Sex)
#> # A tibble: 2 × 1
#>   Sex
#>   <chr>
#> 1 men
#> 2 women
```

### Working with `tsibble` objects

We can use `dplyr` functions such as `mutate()`, `filter()`, `select()` and `summarise()` to work with `tsibble` objects. To illustrate these, we will use the `PBS` tsibble containing sales data on pharmaceutical products in Australia.

```
PBS
#> # A tsibble: 67,596 x 9 [1M]
#> # Key:       Concession, Type, ATC1, ATC2 [336]
#>       Month Concession   Type    ATC1  ATC1_desc ATC2  ATC2_desc Scripts  Cost
#>       <mth> <chr>        <chr>   <chr> <chr>     <chr> <chr>       <dbl> <dbl>
#>  1 1991 Jul Concessional Co-pay… A     Alimenta… A01   STOMATOL…   18228 67877
#>  2 1991 Aug Concessional Co-pay… A     Alimenta… A01   STOMATOL…   15327 57011
#>  3 1991 Sep Concessional Co-pay… A     Alimenta… A01   STOMATOL…   14775 55020
#>  4 1991 Oct Concessional Co-pay… A     Alimenta… A01   STOMATOL…   15380 57222
#>  5 1991 Nov Concessional Co-pay… A     Alimenta… A01   STOMATOL…   14371 52120
#>  6 1991 Dec Concessional Co-pay… A     Alimenta… A01   STOMATOL…   15028 54299
#>  7 1992 Jan Concessional Co-pay… A     Alimenta… A01   STOMATOL…   11040 39753
#>  8 1992 Feb Concessional Co-pay… A     Alimenta… A01   STOMATOL…   15165 54405
#>  9 1992 Mar Concessional Co-pay… A     Alimenta… A01   STOMATOL…   16898 61108
#> 10 1992 Apr Concessional Co-pay… A     Alimenta… A01   STOMATOL…   18141 65356
#> # ℹ 67,586 more rows
```

This contains monthly data on Medicare Australia prescription data from July 1991 to June 2008. These are classified according to various concession types, and Anatomical Therapeutic Chemical (ATC) indexes. For this example, we are interested in the `Cost` time series (total cost of scripts in Australian dollars).

We can use the `filter()` function to extract the A10 scripts:

```
PBS |>
  filter(ATC2 == "A10")
#> # A tsibble: 816 x 9 [1M]
#> # Key:       Concession, Type, ATC1, ATC2 [4]
#>       Month Concession   Type   ATC1  ATC1_desc ATC2  ATC2_desc Scripts   Cost
#>       <mth> <chr>        <chr>  <chr> <chr>     <chr> <chr>       <dbl>  <dbl>
#>  1 1991 Jul Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   89733 2.09e6
#>  2 1991 Aug Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   77101 1.80e6
#>  3 1991 Sep Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   76255 1.78e6
#>  4 1991 Oct Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   78681 1.85e6
#>  5 1991 Nov Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   70554 1.69e6
#>  6 1991 Dec Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   75814 1.84e6
#>  7 1992 Jan Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   64186 1.56e6
#>  8 1992 Feb Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   75899 1.73e6
#>  9 1992 Mar Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   89445 2.05e6
#> 10 1992 Apr Concessional Co-pa… A     Alimenta… A10   ANTIDIAB…   97315 2.23e6
#> # ℹ 806 more rows
```

This allows rows of the tsibble to be selected. Next we can simplify the resulting object by selecting the columns we will need in subsequent analysis.

```
PBS |>
  filter(ATC2 == "A10") |>
  select(Month, Concession, Type, Cost)
#> # A tsibble: 816 x 4 [1M]
#> # Key:       Concession, Type [4]
#>       Month Concession   Type           Cost
#>       <mth> <chr>        <chr>         <dbl>
#>  1 1991 Jul Concessional Co-payments 2092878
#>  2 1991 Aug Concessional Co-payments 1795733
#>  3 1991 Sep Concessional Co-payments 1777231
#>  4 1991 Oct Concessional Co-payments 1848507
#>  5 1991 Nov Concessional Co-payments 1686458
#>  6 1991 Dec Concessional Co-payments 1843079
#>  7 1992 Jan Concessional Co-payments 1564702
#>  8 1992 Feb Concessional Co-payments 1732508
#>  9 1992 Mar Concessional Co-payments 2046102
#> 10 1992 Apr Concessional Co-payments 2225977
#> # ℹ 806 more rows
```

The `select()` function allows us to select particular columns, while `filter()` allows us to keep particular rows.

Note that the index variable `Month`, and the keys `Concession` and `Type`, would be returned even if they were not explicitly selected as they are required for a tsibble (to ensure each row contains a unique combination of keys and index).

Another useful function is `summarise()` which allows us to combine data across keys. For example, we may wish to compute total cost per month regardless of the `Concession` or `Type` keys.

```
PBS |>
  filter(ATC2 == "A10") |>
  select(Month, Concession, Type, Cost) |>
  summarise(TotalC = sum(Cost))
#> # A tsibble: 204 x 2 [1M]
#>       Month  TotalC
#>       <mth>   <dbl>
#>  1 1991 Jul 3526591
#>  2 1991 Aug 3180891
#>  3 1991 Sep 3252221
#>  4 1991 Oct 3611003
#>  5 1991 Nov 3565869
#>  6 1991 Dec 4306371
#>  7 1992 Jan 5088335
#>  8 1992 Feb 2814520
#>  9 1992 Mar 2985811
#> 10 1992 Apr 3204780
#> # ℹ 194 more rows
```

The new variable `TotalC` is the sum of all `Cost` values for each month.

We can create new variables using the `mutate()` function. Here we change the units from dollars to millions of dollars:

```
PBS |>
  filter(ATC2 == "A10") |>
  select(Month, Concession, Type, Cost) |>
  summarise(TotalC = sum(Cost)) |>
  mutate(Cost = TotalC/1e6)
#> # A tsibble: 204 x 3 [1M]
#>       Month  TotalC  Cost
#>       <mth>   <dbl> <dbl>
#>  1 1991 Jul 3526591  3.53
#>  2 1991 Aug 3180891  3.18
#>  3 1991 Sep 3252221  3.25
#>  4 1991 Oct 3611003  3.61
#>  5 1991 Nov 3565869  3.57
#>  6 1991 Dec 4306371  4.31
#>  7 1992 Jan 5088335  5.09
#>  8 1992 Feb 2814520  2.81
#>  9 1992 Mar 2985811  2.99
#> 10 1992 Apr 3204780  3.20
#> # ℹ 194 more rows
```

Finally, we will save the resulting tsibble for examples later in this chapter.

```
PBS |>
  filter(ATC2 == "A10") |>
  select(Month, Concession, Type, Cost) |>
  summarise(TotalC = sum(Cost)) |>
  mutate(Cost = TotalC / 1e6) -> a10
```

At the end of this series of piped functions, we have used a right assignment (`->`), which is not common in R code, but is convenient at the end of a long series of commands as it continues the flow of the code.

### Read a csv file and convert to a tsibble

Almost all of the data used in this book is already stored as `tsibble` objects. But most data lives in databases, MS-Excel files or csv files, before it is imported into R. So often the first step in creating a tsibble is to read in the data, and then identify the index and key variables.

For example, suppose we have the following quarterly data stored in a csv file (only the first 10 rows are shown). This data set provides information on the size of the prison population in Australia, disaggregated by state, gender, legal status and indigenous status. (Here, ATSI stands for Aboriginal or Torres Strait Islander.)

| Date | State | Gender | Legal | Indigenous | Count |
| --- | --- | --- | --- | --- | --- |
| 2005-03-01 | ACT | Female | Remanded | ATSI | 0 |
| 2005-03-01 | ACT | Female | Remanded | Non-ATSI | 2 |
| 2005-03-01 | ACT | Female | Sentenced | ATSI | 0 |
| 2005-03-01 | ACT | Female | Sentenced | Non-ATSI | 5 |
| 2005-03-01 | ACT | Male | Remanded | ATSI | 7 |
| 2005-03-01 | ACT | Male | Remanded | Non-ATSI | 58 |
| 2005-03-01 | ACT | Male | Sentenced | ATSI | 5 |
| 2005-03-01 | ACT | Male | Sentenced | Non-ATSI | 101 |
| 2005-03-01 | NSW | Female | Remanded | ATSI | 51 |
| 2005-03-01 | NSW | Female | Remanded | Non-ATSI | 131 |

We can read it into R, and create a tsibble object, by simply identifying which column contains the time index, and which columns are keys. The remaining columns are values — there can be many value columns, although in this case there is only one (`Count`). The original csv file stored the dates as individual days, although the data is actually quarterly, so we need to convert the `Date` variable to quarters.

```
prison <- readr::read_csv("https://OTexts.com/fpp3/extrafiles/prison_population.csv")
```

```
prison <- prison |>
  mutate(Quarter = yearquarter(Date)) |>
  select(-Date) |>
  as_tsibble(key = c(State, Gender, Legal, Indigenous),
             index = Quarter)

prison
#> # A tsibble: 3,072 x 6 [1Q]
#> # Key:       State, Gender, Legal, Indigenous [64]
#>    State Gender Legal    Indigenous Count Quarter
#>    <chr> <chr>  <chr>    <chr>      <dbl>   <qtr>
#>  1 ACT   Female Remanded ATSI           0 2005 Q1
#>  2 ACT   Female Remanded ATSI           1 2005 Q2
#>  3 ACT   Female Remanded ATSI           0 2005 Q3
#>  4 ACT   Female Remanded ATSI           0 2005 Q4
#>  5 ACT   Female Remanded ATSI           1 2006 Q1
#>  6 ACT   Female Remanded ATSI           1 2006 Q2
#>  7 ACT   Female Remanded ATSI           1 2006 Q3
#>  8 ACT   Female Remanded ATSI           0 2006 Q4
#>  9 ACT   Female Remanded ATSI           0 2007 Q1
#> 10 ACT   Female Remanded ATSI           1 2007 Q2
#> # ℹ 3,062 more rows
```

This tsibble contains 64 separate time series corresponding to the combinations of the 8 states, 2 genders, 2 legal statuses and 2 indigenous statuses. Each of these series is 48 observations in length, from 2005 Q1 to 2016 Q4.

For a tsibble to be valid, it requires a unique index for each combination of keys. The `tsibble()` or `as_tsibble()` function will return an error if this is not true.

### The seasonal period

Some graphics and some models will use the seasonal period of the data. The seasonal period is the number of observations before the seasonal pattern repeats. In most cases, this will be automatically detected using the time index variable.

Some common periods for different time intervals are shown in the table below:

| Data | Minute | Hour | Day | Week | Year |
| --- | --- | --- | --- | --- | --- |
| Quarters |  |  |  |  | 4 |
| Months |  |  |  |  | 12 |
| Weeks |  |  |  |  | 52 |
| Days |  |  |  | 7 | 365.25 |
| Hours |  |  | 24 | 168 | 8766 |
| Minutes |  | 60 | 1440 | 10080 | 525960 |
| Seconds | 60 | 3600 | 86400 | 604800 | 31557600 |

For quarterly, monthly and weekly data, there is only one seasonal period — the number of observations within each year. Actually, there are not \(52\) weeks in a year, but \(365.25/7 = 52.18\) on average, allowing for a leap year every fourth year. Approximating seasonal periods to integers can be useful as many seasonal terms in models only support integer seasonal periods.

If the data is observed more than once per week, then there is often more than one seasonal pattern in the data. For example, data with daily observations might have weekly (period\(=7\)) or annual (period\(=365.25\)) seasonal patterns. Similarly, data that are observed every minute might have hourly (period\(=60\)), daily (period\(=24\times60=1440\)), weekly (period\(=24\times60\times7=10080\)) and annual seasonality (period\(=24\times60\times365.25=525960\)).

More complicated (and unusual) seasonal patterns can be specified using the `period()` function in the `lubridate` package.

## 2.2 Time plots

For time series data, the obvious graph to start with is a time plot. That is, the observations are plotted against the time of observation, with consecutive observations joined by straight lines. Figure [2.1](https://otexts.com/fpp3/time-plots.html#fig:ansett) shows the weekly economy passenger load on Ansett airlines between Australia’s two largest cities.

```
melsyd_economy <- ansett |>
  filter(Airports == "MEL-SYD", Class == "Economy") |>
  mutate(Passengers = Passengers/1000)
autoplot(melsyd_economy, Passengers) +
  labs(title = "Ansett airlines economy class",
       subtitle = "Melbourne-Sydney",
       y = "Passengers ('000)")
```

![Weekly economy passenger load on Ansett Airlines.](https://otexts.com/fpp3/fpp_files/figure-html/ansett-1.png)

Figure 2.1: Weekly economy passenger load on Ansett Airlines.

We will use the `autoplot()` command frequently. It automatically produces an appropriate plot of whatever you pass to it in the first argument. In this case, it recognises `melsyd_economy` as a time series and produces a time plot.

The time plot immediately reveals some interesting features.

* There was a period in 1989 when no passengers were carried — this was due to an industrial dispute.
* There was a period of reduced load in 1992. This was due to a trial in which some economy class seats were replaced by business class seats.
* A large increase in passenger load occurred in the second half of 1991.
* There are some large dips in load around the start of each year. These are due to holiday effects.
* There is a long-term fluctuation in the level of the series which increases during 1987, decreases in 1989, and increases again through 1990 and 1991.

Any model will need to take all these features into account in order to effectively forecast the passenger load into the future.

A simpler time series is shown in Figure [2.2](https://otexts.com/fpp3/time-plots.html#fig:a10plot), using the `a10` data saved earlier.

```
autoplot(a10, Cost) +
  labs(y = "$ (millions)",
       title = "Australian antidiabetic drug sales")
```

![Monthly sales of antidiabetic drugs in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/a10plot-1.png)

Figure 2.2: Monthly sales of antidiabetic drugs in Australia.

Here, there is a clear and increasing trend. There is also a strong seasonal pattern that increases in size as the level of the series increases. The sudden drop at the start of each year is caused by a government subsidisation scheme that makes it cost-effective for patients to stockpile drugs at the end of the calendar year. Any forecasts of this series would need to capture the seasonal pattern, and the fact that the trend is changing slowly.

## 2.3 Time series patterns

In describing these time series, we have used words such as “trend” and “seasonal” which need to be defined more carefully.

Trend
:   A *trend* exists when there is a long-term increase or decrease in the data. It does not have to be linear. Sometimes we will refer to a trend as “changing direction”, when it might go from an increasing trend to a decreasing trend. There is a trend in the antidiabetic drug sales data shown in Figure [2.2](https://otexts.com/fpp3/time-plots.html#fig:a10plot).

Seasonal
:   A *seasonal* pattern occurs when a time series is affected by seasonal factors such as the time of the year or the day of the week. Seasonality is always of a fixed and known period. The monthly sales of antidiabetic drugs (Figure [2.2](https://otexts.com/fpp3/time-plots.html#fig:a10plot)) shows seasonality which is induced partly by the change in the cost of the drugs at the end of the calendar year. (Note that one series can have more than one seasonal pattern.)

Cyclic
:   A *cycle* occurs when the data exhibit rises and falls that are not of a fixed frequency. These fluctuations are usually due to economic conditions, and are often related to the “business cycle”. The duration of these fluctuations is usually at least 2 years.

Many people confuse cyclic behaviour with seasonal behaviour, but they are really quite different. If the fluctuations are not of a fixed frequency then they are cyclic; if the frequency is unchanging and associated with some aspect of the calendar, then the pattern is seasonal. In general, the average length of cycles is longer than the length of a seasonal pattern, and the magnitudes of cycles tend to be more variable than the magnitudes of seasonal patterns.

Many time series include trend, cycles and seasonality. When choosing a forecasting method, we will first need to identify the time series patterns in the data, and then choose a method that is able to capture the patterns properly.

The examples in Figure [2.3](https://otexts.com/fpp3/tspatterns.html#fig:fourexamples) show different combinations of these components.

![Four examples of time series showing different patterns.](https://otexts.com/fpp3/fpp_files/figure-html/fourexamples-1.png)

Figure 2.3: Four examples of time series showing different patterns.

1. The monthly housing sales (top left) show strong seasonality within each year, as well as some strong cyclic behaviour with a period of about 6–10 years. There is no apparent trend in the data over this period.
2. The US treasury bill contracts (top right) show results from the Chicago market for 100 consecutive trading days in 1981. Here there is no seasonality, but an obvious downward trend. Possibly, if we had a much longer series, we would see that this downward trend is actually part of a long cycle, but when viewed over only 100 days it appears to be a trend.
3. The Australian quarterly electricity production (bottom left) shows a strong increasing trend, with strong seasonality. There is no evidence of any cyclic behaviour here.
4. The daily change in the Google closing stock price (bottom right) has no trend, seasonality or cyclic behaviour. There are random fluctuations which do not appear to be very predictable, and no strong patterns that would help with developing a forecasting model.

## 2.4 Seasonal plots

A seasonal plot is similar to a time plot except that the data are plotted against the individual “seasons” in which the data were observed. An example is given in Figure [2.4](https://otexts.com/fpp3/seasonal-plots.html#fig:seasonplot1) showing the antidiabetic drug sales.

```
a10 |>
  gg_season(Cost, labels = "both") +
  labs(y = "$ (millions)",
       title = "Seasonal plot: Antidiabetic drug sales")
```

![Seasonal plot of monthly antidiabetic drug sales in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/seasonplot1-1.png)

Figure 2.4: Seasonal plot of monthly antidiabetic drug sales in Australia.

This is the same data as was shown earlier, but now the data from each year overlap. A seasonal plot allows the underlying seasonal pattern to be seen more clearly, and is especially useful in identifying years in which the pattern changes.

There is a large jump in sales in January each year. These are probably sales in late December as customers stockpile before the end of the calendar year, but the sales are not registered with the government until a week or two later. The graph also shows that there was an unusually small number of sales in March 2008 (most other years show an increase between February and March). The small number of sales in June 2008 is probably due to incomplete counting of sales at the time the data were collected.

### Multiple seasonal periods

Where the data has more than one seasonal pattern, the `period` argument can be used to select which seasonal plot is required. The `vic_elec` data contains half-hourly electricity demand for the state of Victoria, Australia. We can plot the daily pattern, weekly pattern or yearly pattern by specifying the `period` argument as shown in Figures [2.5](https://otexts.com/fpp3/seasonal-plots.html#fig:multipleseasonplots1)–[2.7](https://otexts.com/fpp3/seasonal-plots.html#fig:multipleseasonplots3).

In the first plot, the three days with 25 hours are when daylight saving ended in each year and so these days contained an extra hour. There were also three days with only 23 hours each (when daylight saving started) but these are hidden beneath all the other lines on the plot.

```
vic_elec |> gg_season(Demand, period = "day") +
  theme(legend.position = "none") +
  labs(y="MWh", title="Electricity demand: Victoria")
```

![Seasonal plot showing daily seasonal patterns for Victorian electricity demand.](https://otexts.com/fpp3/fpp_files/figure-html/multipleseasonplots1-1.png)

Figure 2.5: Seasonal plot showing daily seasonal patterns for Victorian electricity demand.

```
vic_elec |> gg_season(Demand, period = "week") +
  theme(legend.position = "none") +
  labs(y="MWh", title="Electricity demand: Victoria")
```

![Seasonal plot showing weekly seasonal patterns for Victorian electricity demand.](https://otexts.com/fpp3/fpp_files/figure-html/multipleseasonplots2-1.png)

Figure 2.6: Seasonal plot showing weekly seasonal patterns for Victorian electricity demand.

```
vic_elec |> gg_season(Demand, period = "year") +
  labs(y="MWh", title="Electricity demand: Victoria")
```

![Seasonal plot showing yearly seasonal patterns for Victorian electricity demand.](https://otexts.com/fpp3/fpp_files/figure-html/multipleseasonplots3-1.png)

Figure 2.7: Seasonal plot showing yearly seasonal patterns for Victorian electricity demand.

## 2.5 Seasonal subseries plots

An alternative plot that emphasises the seasonal patterns is where the data for each season are collected together in separate mini time plots.

```
a10 |>
  gg_subseries(Cost) +
  labs(
    y = "$ (millions)",
    title = "Australian antidiabetic drug sales"
  )
```

![Seasonal subseries plot of monthly antidiabetic drug sales in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/subseriesplot-1.png)

Figure 2.8: Seasonal subseries plot of monthly antidiabetic drug sales in Australia.

The blue horizontal lines indicate the means for each month. This form of plot enables the underlying seasonal pattern to be seen clearly, and also shows the changes in seasonality over time. It is especially useful in identifying changes within particular seasons. In this example, the plot is not particularly revealing; but in some cases, this is the most useful way of viewing seasonal changes over time.

### Example: Australian holiday tourism

Australian quarterly vacation data provides an interesting example of how these plots can reveal information. First we need to extract the relevant data from the `tourism` tsibble. All the usual `tidyverse` wrangling verbs apply. To get the total visitor nights spent on Holiday by State for each quarter (i.e., ignoring Regions) we can use the following code. Note that we do not have to explicitly group by the time index as this is required in a `tsibble`.

```
holidays <- tourism |>
  filter(Purpose == "Holiday") |>
  group_by(State) |>
  summarise(Trips = sum(Trips))
```

```
holidays
#> # A tsibble: 640 x 3 [1Q]
#> # Key:       State [8]
#>    State Quarter Trips
#>    <chr>   <qtr> <dbl>
#>  1 ACT   1998 Q1  196.
#>  2 ACT   1998 Q2  127.
#>  3 ACT   1998 Q3  111.
#>  4 ACT   1998 Q4  170.
#>  5 ACT   1999 Q1  108.
#>  6 ACT   1999 Q2  125.
#>  7 ACT   1999 Q3  178.
#>  8 ACT   1999 Q4  218.
#>  9 ACT   2000 Q1  158.
#> 10 ACT   2000 Q2  155.
#> # ℹ 630 more rows
```

Time plots of each series show that there is strong seasonality for most states, but that the seasonal peaks do not coincide.

```
autoplot(holidays, Trips) +
  labs(y = "Overnight trips ('000)",
       title = "Australian domestic holidays")
```

![Time plots of Australian domestic holidays by state.](https://otexts.com/fpp3/fpp_files/figure-html/holidays-plot-1.png)

Figure 2.9: Time plots of Australian domestic holidays by state.

To see the timing of the seasonal peaks in each state, we can use a season plot. Figure [2.10](https://otexts.com/fpp3/subseries.html#fig:holidaysseason) makes it clear that the southern states of Australia (Tasmania, Victoria and South Australia) have strongest tourism in Q1 (their summer), while the northern states (Queensland and the Northern Territory) have the strongest tourism in Q3 (their dry season).

```
gg_season(holidays, Trips) +
  labs(y = "Overnight trips ('000)",
       title = "Australian domestic holidays")
```

![Season plots of Australian domestic holidays by state.](https://otexts.com/fpp3/fpp_files/figure-html/holidaysseason-1.png)

Figure 2.10: Season plots of Australian domestic holidays by state.

The corresponding subseries plots are shown in Figure [2.11](https://otexts.com/fpp3/subseries.html#fig:holidayssubseries).

```
holidays |>
  gg_subseries(Trips) +
  labs(y = "Overnight trips ('000)",
       title = "Australian domestic holidays")
```

![Subseries plots of Australian domestic holidays by state.](https://otexts.com/fpp3/fpp_files/figure-html/holidayssubseries-1.png)

Figure 2.11: Subseries plots of Australian domestic holidays by state.

This figure makes it evident that Western Australian tourism has jumped markedly in recent years, while Victorian tourism has increased in Q1 and Q4 but not in the middle of the year.

## 2.6 Scatterplots

The graphs discussed so far are useful for visualising individual time series. It is also useful to explore relationships *between* time series.

Figures [2.12](https://otexts.com/fpp3/scatterplots.html#fig:edemand) and [2.13](https://otexts.com/fpp3/scatterplots.html#fig:victemp) show two time series: half-hourly electricity demand (in Gigawatts) and temperature (in degrees Celsius), for 2014 in Victoria, Australia. The temperatures are for Melbourne, the largest city in Victoria, while the demand values are for the entire state.

```
vic_elec |>
  filter(year(Time) == 2014) |>
  autoplot(Demand) +
  labs(y = "GW",
       title = "Half-hourly electricity demand: Victoria")
```

![Half hourly electricity demand in Victoria, Australia, for 2014.](https://otexts.com/fpp3/fpp_files/figure-html/edemand-1.png)

Figure 2.12: Half hourly electricity demand in Victoria, Australia, for 2014.

```
vic_elec |>
  filter(year(Time) == 2014) |>
  autoplot(Temperature) +
  labs(
    y = "Degrees Celsius",
    title = "Half-hourly temperatures: Melbourne, Australia"
  )
```

![Half hourly temperature in Melbourne, Australia, for 2014.](https://otexts.com/fpp3/fpp_files/figure-html/victemp-1.png)

Figure 2.13: Half hourly temperature in Melbourne, Australia, for 2014.

We can study the relationship between demand and temperature by plotting one series against the other.

```
vic_elec |>
  filter(year(Time) == 2014) |>
  ggplot(aes(x = Temperature, y = Demand)) +
  geom_point() +
  labs(title="Electricity demand versus Temperature",
       x = "Temperature (degrees Celsius)",
       y = "Electricity demand (GW)")
```

![Half-hourly electricity demand plotted against temperature for 2014 in Victoria, Australia.](https://otexts.com/fpp3/fpp_files/figure-html/edemand2-1.png)

Figure 2.14: Half-hourly electricity demand plotted against temperature for 2014 in Victoria, Australia.

This scatterplot helps us to visualise the relationship between the variables. It is clear that high demand occurs when temperatures are high due to the effect of air-conditioning. But there is also a heating effect, where demand increases for very low temperatures.

### Correlation

It is common to compute *correlation coefficients* to measure the strength of the linear relationship between two variables. The correlation between variables \(x\) and \(y\) is given by
\[
r = \frac{\sum (x_{t} - \bar{x})(y_{t}-\bar{y})}{\sqrt{\sum(x_{t}-\bar{x})^2}\sqrt{\sum(y_{t}-\bar{y})^2}}.
\]
The value of \(r\) always lies between \(-1\) and \(1\) with negative values indicating a negative relationship and positive values indicating a positive relationship. The graphs in Figure [2.15](https://otexts.com/fpp3/scatterplots.html#fig:corr) show examples of data sets with varying levels of correlation.

![Examples of data sets with different levels of correlation.](https://otexts.com/fpp3/fpp_files/figure-html/corr-1.png)

Figure 2.15: Examples of data sets with different levels of correlation.

The correlation coefficient only measures the strength of the *linear* relationship between two variables, and can sometimes be misleading. For example, the correlation for the electricity demand and temperature data shown in Figure [2.14](https://otexts.com/fpp3/scatterplots.html#fig:edemand2) is 0.28, but the *non-linear* relationship is stronger than that.

![Each of these plots has a correlation coefficient of 0.82. Data from Anscombe (1973).](https://otexts.com/fpp3/fpp_files/figure-html/anscombe-1.png)

Figure 2.16: Each of these plots has a correlation coefficient of 0.82. Data from Anscombe ([1973](#ref-Anscombe1973graphs)).

The plots in Figure [2.16](https://otexts.com/fpp3/scatterplots.html#fig:anscombe) all have correlation coefficients of 0.82, but they have very different relationships. This shows how important it is to look at the plots of the data and not simply rely on correlation values.

### Scatterplot matrices

When there are several potential predictor variables, it is useful to plot each variable against each other variable. Consider the eight time series shown in Figure [2.17](https://otexts.com/fpp3/scatterplots.html#fig:vntimeplots), showing quarterly visitor numbers across states and territories of Australia.

```
visitors <- tourism |>
  group_by(State) |>
  summarise(Trips = sum(Trips))
visitors |>
  ggplot(aes(x = Quarter, y = Trips)) +
  geom_line() +
  facet_grid(vars(State), scales = "free_y") +
  labs(title = "Australian domestic tourism",
       y= "Overnight trips ('000)")
```

![Quarterly visitor nights for the states and territories of Australia.](https://otexts.com/fpp3/fpp_files/figure-html/vntimeplots-1.png)

Figure 2.17: Quarterly visitor nights for the states and territories of Australia.

To see the relationships between these eight time series, we can plot each time series against the others. These plots can be arranged in a scatterplot matrix, as shown in Figure [2.18](https://otexts.com/fpp3/scatterplots.html#fig:ScatterMatrixch2). (This plot requires the `GGally` package to be installed.)

```
visitors |>
  pivot_wider(values_from=Trips, names_from=State) |>
  GGally::ggpairs(columns = 2:9)
```

![A scatterplot matrix of the quarterly visitor nights in the states and territories of Australia.](https://otexts.com/fpp3/fpp_files/figure-html/ScatterMatrixch2-1.png)

Figure 2.18: A scatterplot matrix of the quarterly visitor nights in the states and territories of Australia.

For each panel, the variable on the vertical axis is given by the variable name in that row, and the variable on the horizontal axis is given by the variable name in that column. There are many options available to produce different plots within each panel. In the default version, the correlations are shown in the upper right half of the plot, while the scatterplots are shown in the lower half. On the diagonal are shown density plots.

The value of the scatterplot matrix is that it enables a quick view of the relationships between all pairs of variables. In this example, mostly positive relationships are revealed, with the strongest relationships being between the neighbouring states located in the south and south east coast of Australia, namely, New South Wales, Victoria and South Australia. Some negative relationships are also revealed between the Northern Territory and other regions. The Northern Territory is located in the north of Australia famous for its outback desert landscapes visited mostly in winter. Hence, the peak visitation in the Northern Territory is in the July (winter) quarter in contrast to January (summer) quarter for the rest of the regions.

### Bibliography

Anscombe, F. J. (1973). Graphs in statistical analysis. *The American Statistician*, *27*(1), 17–21.

## 2.7 Lag plots

Figure [2.19](https://otexts.com/fpp3/lag-plots.html#fig:beerlagplot) displays scatterplots of quarterly Australian beer production (introduced in Figure [1.1](https://otexts.com/fpp3/data-methods.html#fig:beer)), where the horizontal axis shows lagged values of the time series. Each graph shows \(y_{t}\) plotted against \(y_{t-k}\) for different values of \(k\).

```
recent_production <- aus_production |>
  filter(year(Quarter) >= 2000)
recent_production |>
  gg_lag(Beer, geom = "point") +
  labs(x = "lag(Beer, k)")
```

![Lagged scatterplots for quarterly beer production.](https://otexts.com/fpp3/fpp_files/figure-html/beerlagplot-1.png)

Figure 2.19: Lagged scatterplots for quarterly beer production.

Here the colours indicate the quarter of the variable on the vertical axis. The relationship is strongly positive at lags 4 and 8, reflecting the strong seasonality in the data. The negative relationship seen for lags 2 and 6 occurs because peaks (in Q4) are plotted against troughs (in Q2)

## 2.8 Autocorrelation

Just as correlation measures the extent of a linear relationship between two variables, autocorrelation measures the linear relationship between *lagged values* of a time series.

There are several autocorrelation coefficients, corresponding to each panel in the lag plot. For example, \(r_{1}\) measures the relationship between \(y_{t}\) and \(y_{t-1}\), \(r_{2}\) measures the relationship between \(y_{t}\) and \(y_{t-2}\), and so on.

The value of \(r_{k}\) can be written as
\[
r_{k} = \frac{\sum\limits_{t=k+1}^T (y_{t}-\bar{y})(y_{t-k}-\bar{y})}
{\sum\limits_{t=1}^T (y_{t}-\bar{y})^2},
\]
where \(T\) is the length of the time series. The autocorrelation coefficients make up the *autocorrelation function* or ACF.

The autocorrelation coefficients for the beer production data can be computed using the `ACF()` function.

```
recent_production |> ACF(Beer, lag_max = 9)
#> # A tsibble: 9 x 2 [1Q]
#>        lag      acf
#>   <cf_lag>    <dbl>
#> 1       1Q -0.0530
#> 2       2Q -0.758
#> 3       3Q -0.0262
#> 4       4Q  0.802
#> 5       5Q -0.0775
#> 6       6Q -0.657
#> 7       7Q  0.00119
#> 8       8Q  0.707
#> 9       9Q -0.0888
```

The values in the `acf` column are \(r_1,\dots,r_9\), corresponding to the nine scatterplots in Figure [2.19](https://otexts.com/fpp3/lag-plots.html#fig:beerlagplot). We usually plot the ACF to see how the correlations change with the lag \(k\). The plot is sometimes known as a *correlogram*.

```
recent_production |>
  ACF(Beer) |>
  autoplot() + labs(title="Australian beer production")
```

![Autocorrelation function of quarterly beer production.](https://otexts.com/fpp3/fpp_files/figure-html/beeracf-1.png)

Figure 2.20: Autocorrelation function of quarterly beer production.

In this graph:

* \(r_{4}\) is higher than for the other lags. This is due to the seasonal pattern in the data: the peaks tend to be four quarters apart and the troughs tend to be four quarters apart.
* \(r_{2}\) is more negative than for the other lags because troughs tend to be two quarters behind peaks.
* The dashed blue lines indicate whether the correlations are significantly different from zero (as explained in Section [2.9](https://otexts.com/fpp3/wn.html#wn)).

### Trend and seasonality in ACF plots

When data have a trend, the autocorrelations for small lags tend to be large and positive because observations nearby in time are also nearby in value. So the ACF of a trended time series tends to have positive values that slowly decrease as the lags increase.

When data are seasonal, the autocorrelations will be larger for the seasonal lags (at multiples of the seasonal period) than for other lags.

When data are both trended and seasonal, you see a combination of these effects. The `a10` data plotted in Figure [2.2](https://otexts.com/fpp3/time-plots.html#fig:a10plot) shows both trend and seasonality. Its ACF is shown in Figure [2.21](https://otexts.com/fpp3/acf.html#fig:acfa10). The slow decrease in the ACF as the lags increase is due to the trend, while the “scalloped” shape is due to the seasonality.

```
a10 |>
  ACF(Cost, lag_max = 48) |>
  autoplot() +
  labs(title="Australian antidiabetic drug sales")
```

![ACF of monthly Australian antidiabetic drug sales.](https://otexts.com/fpp3/fpp_files/figure-html/acfa10-1.png)

Figure 2.21: ACF of monthly Australian antidiabetic drug sales.

## 2.9 White noise

Time series that show no autocorrelation are called **white noise**. Figure [2.22](https://otexts.com/fpp3/wn.html#fig:wnoise) gives an example of a white noise series.

```
set.seed(30)
y <- tsibble(sample = 1:50, wn = rnorm(50), index = sample)
y |> autoplot(wn) + labs(title = "White noise", y = "")
```

![A white noise time series.](https://otexts.com/fpp3/fpp_files/figure-html/wnoise-1.png)

Figure 2.22: A white noise time series.

```
y |>
  ACF(wn) |>
  autoplot() + labs(title = "White noise")
```

![Autocorrelation function for the white noise series.](https://otexts.com/fpp3/fpp_files/figure-html/wnoiseacf-1.png)

Figure 2.23: Autocorrelation function for the white noise series.

For white noise series, we expect each autocorrelation to be close to zero. Of course, they will not be exactly equal to zero as there is some random variation. For a white noise series, we expect 95% of the spikes in the ACF to lie within \(\pm 1.96/\sqrt{T}\) where \(T\) is the length of the time series. It is common to plot these bounds on a graph of the ACF (the blue dashed lines above). If one or more large spikes are outside these bounds, or if substantially more than 5% of spikes are outside these bounds, then the series is probably not white noise.

In this example, \(T=50\) and so the bounds are at \(\pm 1.96/\sqrt{50} = \pm 0.28\). All of the autocorrelation coefficients lie within these limits, confirming that the data are white noise.

## 2.10 Exercises

1. Explore the following four time series: `Bricks` from `aus_production`, `Lynx` from `pelt`, `Close` from `gafa_stock`, `Demand` from `vic_elec`.

   * Use `?` (or `help()`) to find out about the data in each series.
   * What is the time interval of each series?
   * Use `autoplot()` to produce a time plot of each series.
   * For the last plot, modify the axis labels and title.
2. Use `filter()` to find what days corresponded to the peak closing price for each of the four stocks in `gafa_stock`.
3. Download the file `tute1.csv` from [the book website](https://bit.ly/fpptute1), open it in Excel (or some other spreadsheet application), and review its contents. You should find four columns of information. Columns B through D each contain a quarterly series, labelled Sales, AdBudget and GDP. Sales contains the quarterly sales for a small company over the period 1981-2005. AdBudget is the advertising budget and GDP is the gross domestic product. All series have been adjusted for inflation.

   1. You can read the data into R with the following script:

      ```
      tute1 <- readr::read_csv("tute1.csv")
      View(tute1)
      ```
   2. Convert the data to time series

      ```
      mytimeseries <- tute1 |>
        mutate(Quarter = yearquarter(Quarter)) |>
        as_tsibble(index = Quarter)
      ```
   3. Construct time series plots of each of the three series

      ```
      mytimeseries |>
        pivot_longer(-Quarter) |>
        ggplot(aes(x = Quarter, y = value, colour = name)) +
        geom_line() +
        facet_grid(name ~ ., scales = "free_y")
      ```

      Check what happens when you don’t include `facet_grid()`.
4. The `USgas` package contains data on the demand for natural gas in the US.

   1. Install the `USgas` package.
   2. Create a tsibble from `us_total` with year as the index and state as the key.
   3. Plot the annual natural gas consumption by state for the New England area (comprising the states of Maine, Vermont, New Hampshire, Massachusetts, Connecticut and Rhode Island).
5. 1. Download `tourism.xlsx` from [the book website](https://bit.ly/fpptourism) and read it into R using `readxl::read_excel()`.
   2. Create a tsibble which is identical to the `tourism` tsibble from the `tsibble` package.
   3. Find what combination of `Region` and `Purpose` had the maximum number of overnight trips on average.
   4. Create a new tsibble which combines the Purposes and Regions, and just has total trips by State.
6. The `aus_arrivals` data set comprises quarterly international arrivals to Australia from Japan, New Zealand, UK and the US.

   * Use `autoplot()`, `gg_season()` and `gg_subseries()` to compare the differences between the arrivals from these four countries.
   * Can you identify any unusual observations?
7. Monthly Australian retail data is provided in `aus_retail`. Select one of the time series as follows (but choose your own seed value):

   ```
   set.seed(12345678)
   myseries <- aus_retail |>
     filter(`Series ID` == sample(aus_retail$`Series ID`,1))
   ```

   Explore your chosen retail time series using the following functions:

   `autoplot()`, `gg_season()`, `gg_subseries()`, `gg_lag()`,

   `ACF() |> autoplot()`

   Can you spot any seasonality, cyclicity and trend? What do you learn about the series?

8. Use the following graphics functions: `autoplot()`, `gg_season()`, `gg_subseries()`, `gg_lag()`, `ACF()` and explore features from the following time series: “Total Private” `Employed` from `us_employment`, `Bricks` from `aus_production`, `Hare` from `pelt`, “H02” `Cost` from `PBS`, and `Barrels` from `us_gasoline`.

   * Can you spot any seasonality, cyclicity and trend?
   * What do you learn about the series?
   * What can you say about the seasonal patterns?
   * Can you identify any unusual years?
9. The following time plots and ACF plots correspond to four different time series. Your task is to match each time plot in the first row with one of the ACF plots in the second row.

   ![](https://otexts.com/fpp3/fpp_files/figure-html/acfguess-1.png)
10. The `aus_livestock` data contains the monthly total number of pigs slaughtered in Victoria, Australia, from Jul 1972 to Dec 2018. Use `filter()` to extract pig slaughters in Victoria between 1990 and 1995. Use `autoplot()` and `ACF()` for this data. How do they differ from white noise? If a longer period of data is used, what difference does it make to the ACF?
11. 1. Use the following code to compute the daily changes in Google closing stock prices.

       ```
       dgoog <- gafa_stock |>
         filter(Symbol == "GOOG", year(Date) >= 2018) |>
         mutate(trading_day = row_number()) |>
         update_tsibble(index = trading_day, regular = TRUE) |>
         mutate(diff = difference(Close))
       ```
    2. Why was it necessary to re-index the tsibble?
    3. Plot these differences and their ACF.
    4. Do the changes in the stock prices look like white noise?

## 2.11 Further reading

* W. S. Cleveland ([1993](#ref-Cleveland1993)) is a classic book on the principles of visualisation for data analysis. While it is more than 20 years old, the ideas are timeless.
* Unwin ([2015](#ref-Unwin2015)) is a modern introduction to graphical data analysis using R. It does not have much information on time series graphics, but plenty of excellent general advice on using graphics for data analysis.

### Bibliography

Cleveland, W. S. (1993). *Visualizing data*. Hobart Press.

Unwin, A. (2015). *Graphical data analysis with R*. Chapman; Hall/CRC.
