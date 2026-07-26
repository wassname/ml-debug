Source: https://otexts.com/fpp3/hierarchical.html (chapter hierarchical, 9 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - 11-hierarchical-grouped
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Chapter 11 Forecasting hierarchical and grouped time series

Time series can often be naturally disaggregated by various attributes of interest. For example, the total number of bicycles sold by a cycling manufacturer can be disaggregated by product type such as road bikes, mountain bikes and hybrids. Each of these can be disaggregated into finer categories. For example hybrid bikes can be divided into city, commuting, comfort, and trekking bikes; and so on. These categories are nested within the larger group categories, and so the collection of time series follows a hierarchical aggregation structure. Therefore we refer to these as “hierarchical time series”.

Hierarchical time series often arise due to geographic divisions. For example, the total bicycle sales can be disaggregated by country, then within each country by state, within each state by region, and so on down to the outlet level.

Alternative aggregation structures arise when attributes of interest are crossed rather than nested. For example, the bicycle manufacturer may be interested in attributes such as frame size, gender, price range, etc. Such attributes do not naturally disaggregate in a unique hierarchical manner as the attributes are not nested. We refer to the resulting time series of crossed attributes as “grouped time series”.

More complex structures arise when attributes of interest are both nested and crossed. For example, it would be natural for the bicycle manufacturer to be interested in sales by product type and also by geographic division. Then both the product groupings and the geographic hierarchy are mixed together. We introduce alternative aggregation structures in Section [11.1](https://otexts.com/fpp3/hts.html#hts).

Forecasts are often required for all disaggregate and aggregate series, and it is natural to want the forecasts to add up in the same way as the data. For example, forecasts of regional sales should add up to forecasts of state sales, which should in turn add up to give a forecast for national sales.

In this chapter we discuss forecasting large collections of time series that aggregate in some way. The challenge is that we require forecasts that are **coherent** across the entire aggregation structure. That is, we require forecasts to add up in a manner that is consistent with the aggregation structure of the hierarchy or group that defines the collection of time series.

## 11.1 Hierarchical and grouped time series

### Hierarchical time series

Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree) shows a simple hierarchical structure. At the top of the hierarchy is the “Total”, the most aggregate level of the data. The \(t\)th observation of the Total series is denoted by \(y_t\) for \(t=1,\dots,T\). The Total is disaggregated into two series, which in turn are divided into three and two series respectively at the bottom level of the hierarchy. Below the top level, we use \(y_{j,t}\) to denote the \(t\)th observation of the series corresponding to node \(j\). For example, \(\y{A}{t}\) denotes the \(t\)th observation of the series corresponding to node A, \(\y{AB}{t}\) denotes the \(t\)th observation of the series corresponding to node AB, and so on.

![A two level hierarchical tree diagram.](https://otexts.com/fpp3/figs/hts.png)

Figure 11.1: A two level hierarchical tree diagram.

In this small example, the total number of series in the hierarchy is \(n=1+2+5=8\), while the number of series at the bottom level is \(m=5\). Note that \(n>m\) in all hierarchies.

For any time \(t\), the observations at the bottom level of the hierarchy will sum to the observations of the series above. For example,
\[\begin{equation}
y_{t}=\y{AA}{t}+\y{AB}{t}+\y{AC}{t}+\y{BA}{t}+\y{BB}{t},
\tag{11.1}
\end{equation}\]
\[\begin{equation}
\y{A}{t}=\y{AA}{t}+\y{AB}{t}+\y{AC}{t}\qquad \text{and} \qquad \y{B}{t}=\y{BA}{t}+\y{BB}{t}.
\tag{11.2}
\end{equation}\]
Substituting [(11.2)](https://otexts.com/fpp3/hts.html#eq:middlelevel) into [(11.1)](https://otexts.com/fpp3/hts.html#eq:toplevel), we also get \(y_{t}=\y{A}{t}+\y{B}{t}\).

### Example: Australian tourism hierarchy

Australia is divided into six states and two territories, with each one having its own government and some economic and administrative autonomy. For simplicity, we refer to both states and territories as “states”. Each of these states can be further subdivided into regions as shown in Figure [11.2](https://otexts.com/fpp3/hts.html#fig:ausmap) and Table [11.1](https://otexts.com/fpp3/hts.html#tab:aus-states-tab). In total there are 76 such regions. Business planners and tourism authorities are interested in forecasts for the whole of Australia, for each of the states and territories, and also for the regions.

![Australian states and tourism regions.](https://otexts.com/fpp3/fpp_files/figure-html/ausmap-1.png)

Figure 11.2: Australian states and tourism regions.

Table 11.1: Australian tourism regions.

| State | Region |
| --- | --- |
| Australian Capital Territory | Canberra |
| New South Wales | Blue Mountains, Capital Country, Central Coast, Central NSW, Hunter, New England North West, North Coast NSW, Outback NSW, Riverina, Snowy Mountains, South Coast, Sydney, The Murray. |
| Northern Territory | Alice Springs, Barkly, Darwin, Kakadu Arnhem, Katherine Daly, Lasseter, MacDonnell. |
| Queensland | Brisbane, Bundaberg, Central Queensland, Darling Downs, Fraser Coast, Gold Coast, Mackay, Northern Outback, Sunshine Coast, Tropical North Queensland, Whitsundays. |
| South Australia | Adelaide, Adelaide Hills, Barossa, Clare Valley, Eyre Peninsula, Fleurieu Peninsula, Flinders Ranges and Outback, Kangaroo Island, Limestone Coast, Murraylands, Riverland, Yorke Peninsula. |
| Tasmania | East Coast, Hobart and the South, Launceston Tamar and the North, North West, Wilderness West. |
| Victoria | Ballarat, Bendigo Loddon, Central Highlands, Central Murray, Geelong and the Bellarine, Gippsland, Goulburn, Great Ocean Road, High Country, Lakes, Macedon, Mallee, Melbourne, Melbourne East, Murray East, Peninsula, Phillip Island, Spa Country, Upper Yarra, Western Grampians, Wimmera. |
| Western Australia | Australia’s Coral Coast, Australia’s Golden Outback, Australia’s North West, Australia’s South West, Experience Perth. |

The `tourism` tsibble contains data on quarterly domestic tourism demand, measured as the number of overnight trips Australians spend away from home. The key variables `State` and `Region` denote the geographical areas, while a further key `Purpose` describes the purpose of travel. For now, we will ignore the purpose of travel and just consider the geographic hierarchy. To make the graphs and tables simpler, we will recode `State` to use abbreviations.

```
tourism <- tsibble::tourism |>
  mutate(State = recode(State,
    `New South Wales` = "NSW",
    `Northern Territory` = "NT",
    `Queensland` = "QLD",
    `South Australia` = "SA",
    `Tasmania` = "TAS",
    `Victoria` = "VIC",
    `Western Australia` = "WA"
  ))
```

Using the `aggregate_key()` function, we can create the hierarchical time series with overnight trips in regions at the bottom level of the hierarchy, aggregated to states, which are aggregated to the national total. A hierarchical time series corresponding to the nested structure is created using a `parent/child` specification.

```
tourism_hts <- tourism |>
  aggregate_key(State / Region, Trips = sum(Trips))
tourism_hts
#> # A tsibble: 6,800 x 4 [1Q]
#> # Key:       State, Region [85]
#>    Quarter State        Region        Trips
#>      <qtr> <chr*>       <chr*>        <dbl>
#>  1 1998 Q1 <aggregated> <aggregated> 23182.
#>  2 1998 Q2 <aggregated> <aggregated> 20323.
#>  3 1998 Q3 <aggregated> <aggregated> 19827.
#>  4 1998 Q4 <aggregated> <aggregated> 20830.
#>  5 1999 Q1 <aggregated> <aggregated> 22087.
#>  6 1999 Q2 <aggregated> <aggregated> 21458.
#>  7 1999 Q3 <aggregated> <aggregated> 19914.
#>  8 1999 Q4 <aggregated> <aggregated> 20028.
#>  9 2000 Q1 <aggregated> <aggregated> 22339.
#> 10 2000 Q2 <aggregated> <aggregated> 19941.
#> # ℹ 6,790 more rows
```

The new `tsibble` now has some additional rows corresponding to state and national aggregations for each quarter. Figure [11.3](https://otexts.com/fpp3/hts.html#fig:tourismStates) shows the aggregate total overnight trips for the whole of Australia as well as the states, revealing diverse and rich dynamics. For example, there is noticeable national growth since 2010 and for some states such as the ACT, New South Wales, Queensland, South Australia, and Victoria. There seems to be a significant jump for Western Australia in 2014.

```
tourism_hts |>
  filter(is_aggregated(Region)) |>
  autoplot(Trips) +
  labs(y = "Trips ('000)",
       title = "Australian tourism: national and states") +
  facet_wrap(vars(State), scales = "free_y", ncol = 3) +
  theme(legend.position = "none")
```

![Domestic overnight trips from 1998 Q1 to 2017 Q4 aggregated by state.](https://otexts.com/fpp3/fpp_files/figure-html/tourismStates-1.png)

Figure 11.3: Domestic overnight trips from 1998 Q1 to 2017 Q4 aggregated by state.

```
tourism_hts |>
  filter(State == "NT" | State == "QLD" |
         State == "TAS" | State == "VIC", is_aggregated(Region)) |>
  select(-Region) |>
  mutate(State = factor(State, levels=c("QLD","VIC","NT","TAS"))) |>
  gg_season(Trips) +
  facet_wrap(vars(State), nrow = 2, scales = "free_y")+
  labs(y = "Trips ('000)")
```

![Seasonal plots for overnight trips for Queensland and the Northern Territory, and Victoria and Tasmania highlighting the contrast in seasonal patterns between northern and southern states in Australia.](https://otexts.com/fpp3/fpp_files/figure-html/seasonStates-1.png)

Figure 11.4: Seasonal plots for overnight trips for Queensland and the Northern Territory, and Victoria and Tasmania highlighting the contrast in seasonal patterns between northern and southern states in Australia.

The seasonal pattern of the northern states, such as Queensland and the Northern Territory, leads to peak visits in winter (corresponding to Q3) due to the tropical climate and rainy summer months. In contrast, the southern states tend to peak in summer (corresponding to Q1). This is highlighted in the seasonal plots shown in Figure [11.4](https://otexts.com/fpp3/hts.html#fig:seasonStates) for Queensland and the Northern Territory (shown in the left column) versus the most southern states of Victoria and Tasmania (shown in the right column).

![Domestic overnight trips from 1998 Q1 to 2017 Q4 for some selected regions.](https://otexts.com/fpp3/fpp_files/figure-html/tourismRegions-1.png)

Figure 11.5: Domestic overnight trips from 1998 Q1 to 2017 Q4 for some selected regions.

The plots in Figure [11.5](https://otexts.com/fpp3/hts.html#fig:tourismRegions) shows data for some selected regions. These help us visualise the diverse regional dynamics within each state, with some series showing strong trends or seasonality, some showing contrasting seasonality, while some series appear to be just noise.

### Grouped time series

With grouped time series, the data structure does not naturally disaggregate in a unique hierarchical manner. Figure [11.6](https://otexts.com/fpp3/hts.html#fig:GroupTree) shows a simple grouped structure. At the top of the grouped structure is the Total, the most aggregate level of the data, again represented by \(y_t\). The Total can be disaggregated by attributes (A, B) forming series \(\y{A}{t}\) and \(\y{B}{t}\), or by attributes (X, Y) forming series \(\y{X}{t}\) and \(\y{Y}{t}\). At the bottom level, the data are disaggregated by both attributes.

![Alternative representations of a two level grouped structure.](https://otexts.com/fpp3/fpp_files/figure-html/GroupTree-1.png)

Figure 11.6: Alternative representations of a two level grouped structure.

This example shows that there are alternative aggregation paths for grouped structures. For any time \(t\), as with the hierarchical structure,
\[\begin{equation\*}
y_{t}=\y{AX}{t}+\y{AY}{t}+\y{BX}{t}+\y{BY}{t}.
\end{equation\*}\]
However, for the first level of the grouped structure,
\[\begin{equation} \y{A}{t}=\y{AX}{t}+\y{AY}{t}\quad \quad \y{B}{t}=\y{BX}{t}+\y{BY}{t}
\tag{11.3}
\end{equation}\] but also
\[\begin{equation} \y{X}{t}=\y{AX}{t}+\y{BX}{t}\quad \quad \y{Y}{t}=\y{AY}{t}+\y{BY}{t}
\tag{11.4}.
\end{equation}\]

Grouped time series can sometimes be thought of as hierarchical time series that do not impose a unique hierarchical structure, in the sense that the order by which the series can be grouped is not unique.

### Example: Australian prison population

In this example we consider the Australia prison population data introduced in Chapter [2](https://otexts.com/fpp3/graphics.html#graphics). The top panel in Figure [11.7](https://otexts.com/fpp3/hts.html#fig:prisongts) shows the total number of prisoners in Australia over the period 2005Q1–2016Q4. This represents the top-level series in the grouping structure. The panels below show the prison population disaggregated or grouped by (a) state (b) legal status (whether prisoners have already been sentenced or are in remand waiting for a sentence), and (c) gender. The three factors are crossed, but none are nested within the others.

![Total Australian quarterly adult prison population, disaggregated by state, by legal status, and by gender.](https://otexts.com/fpp3/fpp_files/figure-html/prisongts-1.png)

Figure 11.7: Total Australian quarterly adult prison population, disaggregated by state, by legal status, and by gender.

The following code, introduced in Section [2.1](https://otexts.com/fpp3/tsibbles.html#tsibbles), builds a `tsibble` object for the prison data.

```
prison <- readr::read_csv("https://OTexts.com/fpp3/extrafiles/prison_population.csv") |>
  mutate(Quarter = yearquarter(Date)) |>
  select(-Date)  |>
  as_tsibble(key = c(Gender, Legal, State, Indigenous),
             index = Quarter) |>
  relocate(Quarter)
```

We create a grouped time series using `aggregate_key()` with attributes or groupings of interest now being crossed using the syntax `attribute1*attribute2` (in contrast to the `parent/child` syntax used for hierarchical time series). The following code builds a grouped tsibble for the prison data with crossed attributes: gender, legal status and state.

```
prison_gts <- prison |>
  aggregate_key(Gender * Legal * State, Count = sum(Count)/1e3)
```

Using `is_aggregated()` within `filter()` is helpful for exploring or plotting the main groups shown in the bottom panels of Figure [11.7](https://otexts.com/fpp3/hts.html#fig:prisongts). For example, the following code plots the total numbers of female and male prisoners across Australia.

```
prison_gts |>
  filter(!is_aggregated(Gender), is_aggregated(Legal),
         is_aggregated(State)) |>
  autoplot(Count) +
  labs(y = "Number of prisoners ('000)")
```

Plots of other group combinations can be obtained in a similar way. Figure [11.8](https://otexts.com/fpp3/hts.html#fig:prison1) shows the Australian prison population grouped by all possible combinations of two attributes at a time: state and gender, state and legal status, and legal status and gender. The following code will reproduce the first plot in Figure [11.8](https://otexts.com/fpp3/hts.html#fig:prison1).

![Australian adult prison population disaggregated by pairs of attributes.](https://otexts.com/fpp3/fpp_files/figure-html/prison1-1.png)

Figure 11.8: Australian adult prison population disaggregated by pairs of attributes.

```
prison_gts |>
  filter(!is_aggregated(Gender), !is_aggregated(Legal),
         !is_aggregated(State)) |>
  mutate(Gender = as.character(Gender)) |>
  ggplot(aes(x = Quarter, y = Count,
             group = Gender, colour=Gender)) +
  stat_summary(fun = sum, geom = "line") +
  labs(title = "Prison population by state and gender",
       y = "Number of prisoners ('000)") +
  facet_wrap(~ as.character(State),
             nrow = 1, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

Figure [11.9](https://otexts.com/fpp3/hts.html#fig:prisonBTS) shows the Australian adult prison population disaggregated by all three attributes: state, legal status and gender. These form the bottom-level series of the grouped structure.

![Bottom-level time series for the Australian adult prison population, grouped by state, legal status and gender.](https://otexts.com/fpp3/fpp_files/figure-html/prisonBTS-1.png)

Figure 11.9: Bottom-level time series for the Australian adult prison population, grouped by state, legal status and gender.

### Mixed hierarchical and grouped structure

Often disaggregating factors are both nested and crossed. For example, the Australian tourism data can also be disaggregated by the four purposes of travel: holiday, business, visiting friends and relatives, and other. This grouping variable does not nest within any of the geographical variables. In fact, we could consider overnight trips split by purpose of travel for the whole of Australia, and for each state, and for each region. We describe such a structure as a “nested” geographic hierarchy “crossed” with the purpose of travel. Using `aggregate_key()` this can be specified by simply combining the factors.

```
tourism_full <- tourism |>
  aggregate_key((State/Region) * Purpose, Trips = sum(Trips))
```

The `tourism_full` tsibble contains 425 series, including the 85 series from the hierarchical structure, as well as another 340 series obtained when each series of the hierarchical structure is crossed with the purpose of travel.

![Australian domestic overnight trips from 1998 Q1 to 2017 Q4 disaggregated by purpose of travel.](https://otexts.com/fpp3/fpp_files/figure-html/mixed-purpose-1.png)

Figure 11.10: Australian domestic overnight trips from 1998 Q1 to 2017 Q4 disaggregated by purpose of travel.

![Australian domestic overnight trips over the period 1998 Q1 to 2017 Q4 disaggregated by purpose of travel and by state.](https://otexts.com/fpp3/fpp_files/figure-html/mixed-state-purpose-1.png)

Figure 11.11: Australian domestic overnight trips over the period 1998 Q1 to 2017 Q4 disaggregated by purpose of travel and by state.

Figures [11.10](https://otexts.com/fpp3/hts.html#fig:mixed-purpose) and [11.11](https://otexts.com/fpp3/hts.html#fig:mixed-state-purpose) show the aggregate series grouped by purpose of travel, and the series grouped by purpose of travel and state, revealing further rich and diverse dynamics across these series.

## 11.2 Single level approaches

Traditionally, forecasts of hierarchical or grouped time series involved selecting one level of aggregation and generating forecasts for that level. These are then either aggregated for higher levels, or disaggregated for lower levels, to obtain a set of coherent forecasts for the rest of the structure.

### The bottom-up approach

A simple method for generating coherent forecasts is the “bottom-up” approach. This approach involves first generating forecasts for each series at the bottom level, and then summing these to produce forecasts for all the series in the structure.

For example, for the hierarchy of Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree), we first generate \(h\)-step-ahead forecasts for each of the bottom-level series:
\[
\yhat{AA}{h},~~\yhat{AB}{h},~~\yhat{AC}{h},~~ \yhat{BA}{h}~~\text{and}~~\yhat{BB}{h}.
\]
(We have simplified the previously used notation of \(\hat{y}_{T+h|T}\) for brevity.)

Summing these, we get \(h\)-step-ahead coherent forecasts for the rest of the series:
\[\begin{align\*}
\tilde{y}_{h} & =\yhat{AA}{h}+\yhat{AB}{h}+\yhat{AC}{h}+\yhat{BA}{h}+\yhat{BB}{h}, \\
\ytilde{A}{h} & = \yhat{AA}{h}+\yhat{AB}{h}+\yhat{AC}{h}, \\
\text{and}\quad
\ytilde{B}{h} &= \yhat{BA}{h}+\yhat{BB}{h}.
\end{align\*}\]
(In this chapter, we will use the “tilde” notation to indicate coherent forecasts.)

An advantage of this approach is that we are forecasting at the bottom level of a structure, and therefore no information is lost due to aggregation. On the other hand, bottom-level data can be quite noisy and more challenging to model and forecast.

#### Example: Generating bottom-up forecasts

Suppose we want national and state forecasts for the Australian tourism data, but we aren’t interested in disaggregations using regions or the purpose of travel. So we first create a simple `tsibble` object containing only state and national trip totals for each quarter.

```
tourism_states <- tourism |>
  aggregate_key(State, Trips = sum(Trips))
```

We could generate the bottom-level state forecasts first, and then sum them to obtain the national forecasts.

```
fcasts_state <- tourism_states |>
  filter(!is_aggregated(State)) |>
  model(ets = ETS(Trips)) |>
  forecast()

# Sum bottom-level forecasts to get top-level forecasts
fcasts_national <- fcasts_state |>
  summarise(value = sum(Trips), .mean = mean(value))
```

However, we want a more general approach that will work with all the forecasting methods discussed in this chapter. So we will use the `reconcile()` function to specify how we want to compute coherent forecasts.

```
tourism_states |>
  model(ets = ETS(Trips)) |>
  reconcile(bu = bottom_up(ets)) |>
  forecast()
#> # A fable: 144 x 5 [1Q]
#> # Key:     State, .model [18]
#>    State  .model Quarter
#>    <chr*> <chr>    <qtr>
#>  1 ACT    ets    2018 Q1
#>  2 ACT    ets    2018 Q2
#>  3 ACT    ets    2018 Q3
#>  4 ACT    ets    2018 Q4
#>  5 ACT    ets    2019 Q1
#>  6 ACT    ets    2019 Q2
#>  7 ACT    ets    2019 Q3
#>  8 ACT    ets    2019 Q4
#>  9 ACT    bu     2018 Q1
#> 10 ACT    bu     2018 Q2
#> # ℹ 134 more rows
#> # ℹ 2 more variables: Trips <dist>, .mean <dbl>
```

The `reconcile()` step has created a new “model” to produce bottom-up forecasts. The `fable` object contains the `ets` forecasts as well as the coherent `bu` forecasts, for the 8 states and the national aggregate. At the state level, these forecasts are identical, but the national `ets` forecasts will be different from the national `bu` forecasts.

For bottom-up forecasting, this is rather inefficient as we are not interested in the ETS model for the national total, and the resulting `fable` contains a lot of duplicates. But later we will introduce more advanced methods where we will need models for all levels of aggregation, and where the coherent forecasts are different from any of the original forecasts.

#### Workflow for forecasting aggregation structures

The above code illustrates the general workflow for hierarchical and grouped forecasts. We use the following pipeline of functions.

```
data |> aggregate_key() |> model() |>
  reconcile() |> forecast()
```

1. Begin with a `tsibble` object (here labelled `data`) containing the individual bottom-level series.
2. Define in `aggregate_key()` the aggregation structure and build a `tsibble` object that also contains the aggregate series.
3. Identify a `model()` for each series, at all levels of aggregation.
4. Specify in `reconcile()` how the coherent forecasts are to be generated from the selected models.
5. Use the `forecast()` function to generate forecasts for the whole aggregation structure.

### Top-down approaches

Top-down approaches involve first generating forecasts for the Total series \(y_t\), and then disaggregating these down the hierarchy.

Let \(p_1,\dots,p_{m}\) denote a set of disaggregation proportions which determine how the forecasts of the Total series are to be distributed to obtain forecasts for each series at the bottom level of the structure. For example, for the hierarchy of Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree), using proportions \(p_1,\dots,p_{5}\) we get
\[
\ytilde{AA}{t}=p_1\hat{y}_t,~~~\ytilde{AB}{t}=p_2\hat{y}_t,~~~\ytilde{AC}{t}=p_3\hat{y}_t,~~~\ytilde{BA}{t}=p_4\hat{y}_t~~~\text{and}~~~~~~\ytilde{BB}{t}=p_5\hat{y}_t.
\]
Once the bottom-level \(h\)-step-ahead forecasts have been generated, these are aggregated to generate coherent forecasts for the rest of the series.

Top-down forecasts can be generated using `top_down()` within the `reconcile()` function.

There are several possible top-down methods that can be specified. The two most common top-down approaches specify disaggregation proportions based on the historical proportions of the data. These performed well in the study of Gross & Sohl ([1990](#ref-GroSoh1990)).

#### Average historical proportions

\[
p_j=\frac{1}{T}\sum_{t=1}^{T}\frac{y_{j,t}}{{y_t}}
\]
for \(j=1,\dots,m\). Each proportion \(p_j\) reflects the average of the historical proportions of the bottom-level series \(y_{j,t}\) over the period \(t=1,\dots,T\) relative to the total aggregate \(y_t\).

This approach is implemented in the `top_down()` function by setting `method = "average_proportions"`.

#### Proportions of the historical averages

\[
p_j={\sum_{t=1}^{T}\frac{y_{j,t}}{T}}\Big/{\sum_{t=1}^{T}\frac{y_t}{T}}
\]
for \(j=1,\dots,m\). Each proportion \(p_j\) captures the average historical value of the bottom-level series \(y_{j,t}\) relative to the average value of the total aggregate \(y_t\).

This approach is implemented in the `top_down()` function by setting `method = "proportion_averages"`.

A convenient attribute of such top-down approaches is their simplicity. One only needs to model and generate forecasts for the most aggregated top-level series. In general, these approaches seem to produce quite reliable forecasts for the aggregate levels and they are useful with low count data. On the other hand, one disadvantage is the loss of information due to aggregation. Using such top-down approaches, we are unable to capture and take advantage of individual series characteristics such as time dynamics, special events, different seasonal patterns, etc.

#### Forecast proportions

Because historical proportions used for disaggregation do not take account of how those proportions may change over time, top-down approaches based on historical proportions tend to produce less accurate forecasts at lower levels of the hierarchy than bottom-up approaches. To address this issue, proportions based on forecasts rather than historical data can be used ([Athanasopoulos et al., 2009](#ref-AthEtAl2009)).

Consider a one level hierarchy. We first generate \(h\)-step-ahead forecasts for all of the series. We don’t use these forecasts directly, and they are not coherent (they don’t add up correctly). Let’s call these “initial” forecasts. We calculate the proportion of each \(h\)-step-ahead initial forecast at the bottom level, to the aggregate of all the \(h\)-step-ahead initial forecasts at this level. We refer to these as the forecast proportions, and we use them to disaggregate the top-level \(h\)-step-ahead initial forecast in order to generate coherent forecasts for the whole of the hierarchy.

For a \(K\)-level hierarchy, this process is repeated for each node, going from the top to the bottom level. Applying this process leads to the following general rule for obtaining the forecast proportions:
\[
p_j=\prod^{K-1}_{\ell=0}\frac{\hat{y}_{j,h}^{(\ell)}}{\hat{S}_{j,h}^{(\ell+1)}}
\]
where \(j=1,2,\dots,m\), \(\hat{y}_{j,h}^{(\ell)}\) is the \(h\)-step-ahead initial forecast of the series that corresponds to the node which is \(\ell\) levels above \(j\), and \(\hat{S}_{j,h}^{(\ell)}\) is the sum of the \(h\)-step-ahead initial forecasts below the node that is \(\ell\) levels above node \(j\) and are directly connected to that node. These forecast proportions disaggregate the \(h\)-step-ahead initial forecast of the Total series to get \(h\)-step-ahead coherent forecasts of the bottom-level series.

We will use the hierarchy of Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree) to explain this notation and to demonstrate how this general rule is reached. Assume we have generated initial forecasts for each series in the hierarchy. Recall that for the top-level “Total” series, \(\tilde{y}_{h}=\hat{y}_{h}\), for any top-down approach. Here are some examples using the above notation:

* \(\hat{y}_{\text{A},h}^{(1)}=\hat{y}_{\text{B},h}^{(1)}=\hat{y}_{h}= \tilde{y}_{h}\);
* \(\hat{y}_{\text{AA},h}^{(1)}=\hat{y}_{\text{AB},h}^{(1)}=\hat{y}_{\text{AC},h}^{(1)}= \hat{y}_{\text{A},h}\);
* \(\hat{y}_{\text{AA},h}^{(2)}=\hat{y}_{\text{AB},h}^{(2)}= \hat{y}_{\text{AC},h}^{(2)}=\hat{y}_{\text{BA},h}^{(2)}= \hat{y}_{\text{BB},h}^{(2)}=\hat{y}_{h}= \tilde{y}_{h}\);
* \(\Shat{AA}{h}{1} = \Shat{AB}{h}{1}= \Shat{AC}{h}{1}= \yhat{AA}{h}+\yhat{AB}{h}+\yhat{AC}{h}\);
* \(\Shat{AA}{h}{2} = \Shat{AB}{h}{2}= \Shat{AC}{h}{2}= \Shat{A}{h}{1} = \Shat{B}{h}{1}= \hat{S}_{h}= \yhat{A}{h}+\yhat{B}{h}\).

Moving down the farthest left branch of the hierarchy, coherent forecasts are given by
\[
\ytilde{A}{h} = \Bigg(\frac{\yhat{A}{h}}{\Shat{A}{h}{1}}\Bigg) \tilde{y}_{h} =
\Bigg(\frac{\yhat{AA}{h}^{(1)}}{\Shat{AA}{h}{2}}\Bigg) \tilde{y}_{h}
\]
and
\[
\ytilde{AA}{h} = \Bigg(\frac{\yhat{AA}{h}}{\Shat{AA}{h}{1}}\Bigg) \ytilde{A}{h}
=\Bigg(\frac{\yhat{AA}{h}}{\Shat{AA}{h}{1}}\Bigg) \Bigg(\frac{\yhat{AA}{h}^{(1)}}{\Shat{AA}{h}{2}}\Bigg)\tilde{y}_{h}.
\]
Consequently,
\[
p_1=\Bigg(\frac{\yhat{AA}{h}}{\Shat{AA}{h}{1}}\Bigg) \Bigg(\frac{\yhat{AA}{h}^{(1)}}{\Shat{AA}{h}{2}}\Bigg).
\]
The other proportions can be obtained similarly.

This approach is implemented in the `top_down()` function by setting `method = "forecast_proportions"`. Because this approach tends to work better than other top-down methods, it is the default choice in the `top_down()` function when no `method` argument is specified.

One disadvantage of all top-down approaches, is that they do not produce unbiased coherent forecasts ([Hyndman et al., 2011](#ref-HynEtAl2011)) even if the base forecasts are unbiased.

### Middle-out approach

The middle-out approach combines bottom-up and top-down approaches. Again, it can only be used for strictly hierarchical aggregation structures.

First, a “middle” level is chosen and forecasts are generated for all the series at this level. For the series above the middle level, coherent forecasts are generated using the bottom-up approach by aggregating the “middle-level” forecasts upwards. For the series below the “middle level”, coherent forecasts are generated using a top-down approach by disaggregating the “middle level” forecasts downwards.

This approach is implemented in the `middle_out()` function by specifying the appropriate middle level via the `level` argument and selecting the top-down approach with the `method` argument.

### Bibliography

Athanasopoulos, G., Ahmed, R. A., & Hyndman, R. J. (2009). Hierarchical forecasts for Australian domestic tourism. *International Journal of Forecasting*, *25*, 146–166.

Gross, C. W., & Sohl, J. E. (1990). Disaggregation methods to expedite product line forecasting. *Journal of Forecasting*, *9*, 233–254.

Hyndman, R. J., Ahmed, R. A., Athanasopoulos, G., & Shang, H. L. (2011). Optimal combination forecasts for hierarchical time series. *Computational Statistics and Data Analysis*, *55*(9), 2579–2589.

## 11.3 Forecast reconciliation

*Warning: the rest of this chapter is more advanced and assumes a knowledge of some basic matrix algebra.*

### Matrix notation

Recall that Equations [(11.1)](https://otexts.com/fpp3/hts.html#eq:toplevel) and [(11.2)](https://otexts.com/fpp3/hts.html#eq:middlelevel) represent how data, that adhere to the hierarchical structure of Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree), aggregate. Similarly [(11.3)](https://otexts.com/fpp3/hts.html#eq:middlelevelAB) and [(11.4)](https://otexts.com/fpp3/hts.html#eq:middlelevelXY) represent how data, that adhere to the grouped structure of Figure [11.6](https://otexts.com/fpp3/hts.html#fig:GroupTree), aggregate. These equations can be thought of as aggregation constraints or summing equalities, and can be more efficiently represented using matrix notation.

For any aggregation structure we construct an \(n\times m\) matrix \(\bm{S}\) (referred to as the “summing matrix”) which dictates the way in which the bottom-level series aggregate.

For the hierarchical structure in Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree), we can write
\[
\begin{bmatrix}
y_{t} \\
\y{A}{t} \\
\y{B}{t} \\
\y{AA}{t} \\
\y{AB}{t} \\
\y{AC}{t} \\
\y{BA}{t} \\
\y{BB}{t}
\end{bmatrix}
=
\begin{bmatrix}
1 & 1 & 1 & 1 & 1 \\
1 & 1 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 1 \\
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
\y{AA}{t} \\
\y{AB}{t} \\
\y{AC}{t} \\
\y{BA}{t} \\
\y{BB}{t}
\end{bmatrix}
\]
or in more compact notation
\[\begin{equation}
\bm{y}_t=\bm{S}\bm{b}_{t},
\tag{11.5}
\end{equation}\]
where \(\bm{y}_t\) is an \(n\)-dimensional vector of all the observations in the hierarchy at time \(t\), \(\bm{S}\) is the summing matrix, and \(\bm{b}_{t}\) is an \(m\)-dimensional vector of all the observations in the bottom level of the hierarchy at time \(t\). Note that the first row in the summing matrix \(\bm{S}\) represents Equation [(11.1)](https://otexts.com/fpp3/hts.html#eq:toplevel), the second and third rows represent [(11.2)](https://otexts.com/fpp3/hts.html#eq:middlelevel). The rows below these comprise an \(m\)-dimensional identity matrix \(\bm{I}_m\) so that each bottom-level observation on the right hand side of the equation is equal to itself on the left hand side.

Similarly for the grouped structure of Figure [11.6](https://otexts.com/fpp3/hts.html#fig:GroupTree) we write
\[
\begin{bmatrix}
y_{t} \\
\y{A}{t} \\
\y{B}{t} \\
\y{X}{t} \\
\y{Y}{t} \\
\y{AX}{t} \\
\y{AY}{t} \\
\y{BX}{t} \\
\y{BY}{t}
\end{bmatrix}
=
\begin{bmatrix}
1 & 1 & 1 & 1 \\
1 & 1 & 0 & 0 \\
0 & 0 & 1 & 1 \\
1 & 0 & 1 & 0 \\
0 & 1 & 0 & 1 \\
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
\y{AX}{t} \\
\y{AY}{t} \\
\y{BX}{t} \\
\y{BY}{t}
\end{bmatrix},
\]
or
\[\begin{equation}
\bm{y}_t=\bm{S}\bm{b}_{t},
\tag{11.6}
\end{equation}\]
where the second and third rows of \(\bm{S}\) represent Equation [(11.3)](https://otexts.com/fpp3/hts.html#eq:middlelevelAB) and the fourth and fifth rows represent [(11.4)](https://otexts.com/fpp3/hts.html#eq:middlelevelXY).

### Mapping matrices

This matrix notation allows us to represent all forecasting methods for hierarchical or grouped time series using a common notation.

Suppose we forecast all series ignoring any aggregation constraints. We call these the **base forecasts** and denote them by \(\hat{\bm{y}}_h\) where \(h\) is the forecast horizon. They are stacked in the same order as the data \(\bm{y}_t\).

Then all coherent forecasting approaches for either hierarchical or grouped structures can be represented as[23](#fn23)
\[\begin{equation}
\tilde{\bm{y}}_h=\bm{S}\bm{G}\hat{\bm{y}}_h,
\tag{11.7}
\end{equation}\]
where \(\bm{G}\) is a matrix that maps the base forecasts into the bottom level, and the summing matrix \(\bm{S}\) sums these up using the aggregation structure to produce a set of **coherent forecasts** \(\tilde{\bm{y}}_h\).

The \(\bm{G}\) matrix is defined according to the approach implemented. For example if the bottom-up approach is used to forecast the hierarchy of Figure [11.1](https://otexts.com/fpp3/hts.html#fig:HierTree), then
\[\bm{G}=
\begin{bmatrix}
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\\
\end{bmatrix}.
\]
Notice that \(\bm{G}\) contains two partitions. The first three columns zero out the base forecasts of the series above the bottom level, while the \(m\)-dimensional identity matrix picks only the base forecasts of the bottom level. These are then summed by the \(\bm{S}\) matrix.

If any of the top-down approaches were used then
\[
\bm{G}=
\begin{bmatrix}
p_1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
p_2 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
p_3 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
p_4 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
p_5 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
\end{bmatrix}.
\]
The first column includes the set of proportions that distribute the base forecasts of the top level to the bottom level. These are then summed up by the \(\bm{S}\) matrix. The rest of the columns zero out the base forecasts below the highest level of aggregation.

For a middle out approach, the \(\bm{G}\) matrix will be a combination of the above two. Using a set of proportions, the base forecasts of some pre-chosen level will be disaggregated to the bottom level, all other base forecasts will be zeroed out, and the bottom-level forecasts will then be summed up the hierarchy via the summing matrix.

### Forecast reconciliation

Equation [(11.7)](https://otexts.com/fpp3/reconciliation.html#eq:SG) shows that pre-multiplying any set of base forecasts with \(\bm{S}\bm{G}\) will return a set of coherent forecasts.

The traditional methods considered so far are limited in that they only use base forecasts from a single level of aggregation which have either been aggregated or disaggregated to obtain forecasts at all other levels. Hence, they use limited information. However, in general, we could use other \(\bm{G}\) matrices, and then \(\bm{S}\bm{G}\) combines and reconciles all the base forecasts in order to produce coherent forecasts.

In fact, we can find the optimal \(\bm{G}\) matrix to give the most accurate reconciled forecasts.

### The MinT optimal reconciliation approach

Wickramasuriya et al. ([2019](#ref-Mint)) found a \(\bm{G}\) matrix that minimises the total forecast variance of the set of coherent forecasts, leading to the MinT (Minimum Trace) optimal reconciliation approach.

Suppose we generate coherent forecasts using Equation [(11.7)](https://otexts.com/fpp3/reconciliation.html#eq:SG). First we want to make sure we have unbiased forecasts. If the base forecasts \(\hat{\bm{y}}_h\) are unbiased, then the coherent forecasts \(\tilde{\bm{y}}_h\) will be unbiased provided[24](#fn24) \(\bm{S}\bm{G}\bm{S}=\bm{S}\). This provides a constraint on the matrix \(\bm{G}\). Interestingly, no top-down method satisfies this constraint, so all top-down approaches result in biased coherent forecasts.

Next we need to find the errors in our forecasts. Wickramasuriya et al. ([2019](#ref-Mint)) show that the variance-covariance matrix of the \(h\)-step-ahead coherent forecast errors is given by
\[\begin{equation\*}
\bm{V}_h = \text{Var}[\bm{y}_{T+h}-\tilde{\bm{y}}_h]=\bm{S}\bm{G}\bm{W}_h\bm{G}'\bm{S}'
\end{equation\*}\]
where \(\bm{W}_h=\text{Var}[(\bm{y}_{T+h}-\hat{\bm{y}}_h)]\) is the variance-covariance matrix of the corresponding base forecast errors.

The objective is to find a matrix \(\bm{G}\) that minimises the error variances of the coherent forecasts. These error variances are on the diagonal of the matrix \(\bm{V}_h\), and so the sum of all the error variances is given by the trace of the matrix \(\bm{V}_h\). Wickramasuriya et al. ([2019](#ref-Mint)) show that the matrix \(\bm{G}\) which minimises the trace of \(\bm{V}_h\) such that \(\bm{S}\bm{G}\bm{S}=\bm{S}\), is given by
\[
\bm{G}=(\bm{S}'\bm{W}_h^{-1}\bm{S})^{-1}\bm{S}'\bm{W}_h^{-1}.
\]
Therefore, the optimally reconciled forecasts are given by
\[\begin{equation}
\tag{11.8}
\tilde{\bm{y}}_h=\bm{S}(\bm{S}'\bm{W}_h^{-1}\bm{S})^{-1}\bm{S}'\bm{W}_h^{-1}\hat{\bm{y}}_h.
\end{equation}\]

We refer to this as the MinT (or Minimum Trace) optimal reconciliation approach. MinT is implemented by `min_trace()` within the `reconcile()` function.

To use this in practice, we need to estimate \(\bm{W}_h\), the forecast error variance of the \(h\)-step-ahead base forecasts. This can be difficult, and so we provide four simplifying approximations that have been shown to work well in both simulations and in practice.

1. Set \(\bm{W}_h=k_h\bm{I}\) for all \(h\), where \(k_{h} > 0\).[25](#fn25) This is the most simplifying assumption to make, and means that \(\bm{G}\) is independent of the data, providing substantial computational savings. The disadvantage, however, is that this specification does not account for the differences in scale between the levels of the structure, or for relationships between series.

   Setting \(\bm{W}_h=k_h\bm{I}\) in [(11.8)](https://otexts.com/fpp3/reconciliation.html#eq:MinT) gives the ordinary least squares (OLS) estimator we introduced in Section [7.9](https://otexts.com/fpp3/regression-matrices.html#regression-matrices) with \(\bm{X}=\bm{S}\) and \(\bm{y}=\hat{\bm{y}}\). Hence this approach is usually referred to as OLS reconciliation. It is implemented in `min_trace()` by setting `method = "ols"`.
2. Set \(\bm{W}_{h} = k_{h}\text{diag}(\hat{\bm{W}}_{1})\) for all \(h\), where \(k_{h} > 0\),
   \[
   \hat{\bm{W}}_{1} = \frac{1}{T}\sum_{t=1}^{T}\bm{e}_{t}\bm{e}_{t}',
   \]
   and \(\bm{e}_{t}\) is an \(n\)-dimensional vector of residuals of the models that generated the base forecasts stacked in the same order as the data.

   This specification scales the base forecasts using the variance of the residuals and it is therefore referred to as the WLS (weighted least squares) estimator using *variance scaling*. The approach is implemented in `min_trace()` by setting `method = "wls_var"`.
3. Set \(\bm{W}_{h}=k_{h}\bm{\Lambda}\) for all \(h\), where \(k_{h} > 0\), \(\bm{\Lambda}=\text{diag}(\bm{S}\bm{1})\), and \(\bm{1}\) is a unit vector of dimension \(m\) (the number of bottom-level series). This specification assumes that the bottom-level base forecast errors each have variance \(k_{h}\) and are uncorrelated between nodes. Hence each element of the diagonal \(\bm{\Lambda}\) matrix contains the number of forecast error variances contributing to each node. This estimator only depends on the structure of the aggregations, and not on the actual data. It is therefore referred to as *structural scaling*. Applying the structural scaling specification is particularly useful in cases where residuals are not available, and so variance scaling cannot be applied; for example, in cases where the base forecasts are generated by judgmental forecasting (Chapter [6](https://otexts.com/fpp3/judgmental.html#judgmental)). The approach is implemented in `min_trace()` by setting `method = "wls_struct"`.
4. Set \(\bm{W}_h = k_h \hat{\bm{W}}_1\) for all \(h\), where \(k_h>0\). Here we only assume that the error covariance matrices are proportional to each other, and we directly estimate the full one-step covariance matrix \(\bm{W}_1\). The most obvious and simple way would be to use the sample covariance. This is implemented in `min_trace()` by setting `method = "mint_cov"`.

   However, for cases where the number of bottom-level series \(m\) is large compared to the length of the series \(T\), this is not a good estimator. Instead we use a shrinkage estimator which shrinks the sample covariance to a diagonal matrix. This is implemented in `min_trace()` by setting `method = "mint_shrink"`.

In summary, unlike any other existing approach, the optimal reconciliation forecasts are generated using all the information available within a hierarchical or a grouped structure. This is important, as particular aggregation levels or groupings may reveal features of the data that are of interest to the user and are important to be modelled. These features may be completely hidden or not easily identifiable at other levels.

For example, consider the Australian tourism data introduced in Section [11.1](https://otexts.com/fpp3/hts.html#hts), where the hierarchical structure followed the geographic division of a country into states and regions. Some areas will be largely summer destinations, while others may be winter destinations. We saw in Figure [11.4](https://otexts.com/fpp3/hts.html#fig:seasonStates) the contrasting seasonal patterns between the northern and the southern states. These differences will be smoothed at the country level due to aggregation.

### Bibliography

Hyndman, R. J., Ahmed, R. A., Athanasopoulos, G., & Shang, H. L. (2011). Optimal combination forecasts for hierarchical time series. *Computational Statistics and Data Analysis*, *55*(9), 2579–2589.

Panagiotelis, A., Athanasopoulos, G., Gamakumara, P., & Hyndman, R. J. (2021). Forecast reconciliation: A geometric view with new insights on bias correction. *International Journal of Forecasting*, *37*(1), 343–359.

Wickramasuriya, S. L., Athanasopoulos, G., & Hyndman, R. J. (2019). Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization. *Journal of the American Statistical Association*, *114*(526), 804–819.

---

23. Actually, some recent nonlinear reconciliation methods require a slightly more complicated equation. This equation is for general linear reconciliation methods.[↩︎](https://otexts.com/fpp3/reconciliation.html#fnref23)
24. This “unbiasedness preserving” constraint was first introduced in Hyndman et al. ([2011](#ref-HynEtAl2011)). Panagiotelis et al. ([2021](#ref-PanEtAl2020_Geometry)) show that this is equivalent to \(\bm{S}\bm{G}\) being a projection matrix onto the \(m\)-dimensional coherent subspace for which the aggregation constraints hold.[↩︎](https://otexts.com/fpp3/reconciliation.html#fnref24)
25. Note that \(k_{h}\) is a proportionality constant. It does not need to be estimated or specified here as it gets cancelled out in [(11.8)](https://otexts.com/fpp3/reconciliation.html#eq:MinT).[↩︎](https://otexts.com/fpp3/reconciliation.html#fnref25)

## 11.4 Forecasting Australian domestic tourism

We will compute forecasts for the Australian tourism data that was described in Section [11.1](https://otexts.com/fpp3/hts.html#hts). We use the data up to the end of 2015 as a training set, withholding the final two years (eight quarters, 2016Q1–2017Q4) as a test set for evaluation. The code below demonstrates the full workflow for generating coherent forecasts using the bottom-up, OLS and MinT methods.

```
tourism_full <- tourism |>
  aggregate_key((State/Region) * Purpose, Trips = sum(Trips))

fit <- tourism_full |>
  filter(year(Quarter) <= 2015) |>
  model(base = ETS(Trips)) |>
  reconcile(
    bu = bottom_up(base),
    ols = min_trace(base, method = "ols"),
    mint = min_trace(base, method = "mint_shrink")
  )
```

Here, `fit` contains the `base` ETS model (discussed in Chapter [8](https://otexts.com/fpp3/expsmooth.html#expsmooth)) for each series in `tourism_full`, along with the three methods for producing coherent forecasts as specified in the `reconcile()` function.

```
fc <- fit |> forecast(h = "2 years")
```

Passing `fit` into `forecast()` generates base and coherent forecasts across all the series in the aggregation structure. Figures [11.12](https://otexts.com/fpp3/tourism.html#fig:tourism-states) and [11.13](https://otexts.com/fpp3/tourism.html#fig:tourism-purpose) plot the four point forecasts for the overnight trips for the Australian total, the states, and the purposes of travel, along with the actual observations of the test set.

```
fc |>
  filter(is_aggregated(Region), is_aggregated(Purpose)) |>
  autoplot(
    tourism_full |> filter(year(Quarter) >= 2011),
    level = NULL
  ) +
  labs(y = "Trips ('000)") +
  facet_wrap(vars(State), scales = "free_y")
```

![Forecasts of overnight trips for Australia and its states over the test period 2016Q1--2017Q4.](https://otexts.com/fpp3/fpp_files/figure-html/tourism-states-1.png)

Figure 11.12: Forecasts of overnight trips for Australia and its states over the test period 2016Q1–2017Q4.

```
fc |>
  filter(is_aggregated(State), !is_aggregated(Purpose)) |>
  autoplot(
    tourism_full |> filter(year(Quarter) >= 2011),
    level = NULL
  ) +
  labs(y = "Trips ('000)") +
  facet_wrap(vars(Purpose), scales = "free_y")
```

![Forecasts of overnight trips by purpose of travel over the test period 2016Q1--2017Q4.](https://otexts.com/fpp3/fpp_files/figure-html/tourism-purpose-1.png)

Figure 11.13: Forecasts of overnight trips by purpose of travel over the test period 2016Q1–2017Q4.

To make it easier to see the differences, we have included only the last five years of the training data, and have omitted the prediction intervals. In most panels, the increase in overnight trips, especially in the second half of the test set, is higher than what is predicted by the point forecasts. This is particularly noticeable for the mainland eastern states of ACT, New South Wales, Queensland and Victoria, and across all purposes of travel.

The accuracy of the forecasts over the test set can be evaluated using the `accuracy()` function. We summarise some results in Table [11.2](https://otexts.com/fpp3/tourism.html#tab:tourism-evaluation) using RMSE and MASE.

Table 11.2: Accuracy of forecasts for Australian overnight trips over the test set 2016Q1–2017Q4.

|  | RMSE | | | | MASE | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Base | Bottom-up | MinT | OLS | Base | Bottom-up | MinT | OLS |
| Total | 1720.72 | 3071.11 | 2157.55 | 1803.51 | 1.53 | 3.17 | 2.09 | 1.63 |
| Purpose | 533.02 | 802.68 | 586.45 | 513.18 | 1.33 | 2.32 | 1.51 | 1.25 |
| State | 306.85 | 417.21 | 329.74 | 294.66 | 1.40 | 1.88 | 1.45 | 1.27 |
| Regions | 52.64 | 55.13 | 47.40 | 46.95 | 1.13 | 1.18 | 1.02 | 1.00 |
| Bottom | 19.38 | 19.38 | 17.97 | 18.32 | 0.98 | 0.98 | 0.94 | 1.02 |
| All series | 45.96 | 55.28 | 45.61 | 43.19 | 1.04 | 1.08 | 0.98 | 1.03 |

The scales of the series at different levels of aggregation are quite different, due to aggregation. Hence, we need to be cautious when comparing or calculating scale dependent error measures, such as the RMSE, across levels as the aggregate series will dominate. Therefore, we compare error measures across each level of aggregation, before providing the error measures across all the series in the bottom-row. Notice, that the RMSE increases as we go from the bottom level to the aggregate levels above.

The following code generates the accuracy measures for the aggregate series shown in the first row of the table. Similar code is used to evaluate forecasts for other levels.

```
fc |>
  filter(is_aggregated(State), is_aggregated(Purpose)) |>
  accuracy(
    data = tourism_full,
    measures = list(rmse = RMSE, mase = MASE)
  ) |>
  group_by(.model) |>
  summarise(rmse = mean(rmse), mase = mean(mase))
#> # A tibble: 4 × 3
#>   .model  rmse  mase
#>   <chr>  <dbl> <dbl>
#> 1 base   1721.  1.53
#> 2 bu     3071.  3.17
#> 3 mint   2158.  2.09
#> 4 ols    1804.  1.63
```

Reconciling the base forecasts using OLS and MinT results in more accurate forecasts compared to the bottom-up approach. This result is commonly observed in applications as reconciliation approaches use information from all levels of the structure, resulting in more accurate coherent forecasts compared to the older traditional methods which use limited information. Furthermore, reconciliation usually improves the incoherent base forecasts for almost all levels.

## 11.5 Reconciled distributional forecasts

So far we have only discussed the reconciliation of point forecasts. However, we are usually also interested in the forecast distributions so that we can compute prediction intervals.

Panagiotelis et al. ([2023](#ref-PanEtAl2020_Probabilistic)) present several important results for generating reconciled probabilistic forecasts. We focus here on two fundamental results that are implemented in the `reconcile()` function.

1. If the base forecasts are normally distributed, i.e.,
   \[
   \hat{\bm{y}}_h\sim N(\hat{\bm\mu}_h,\hat{\bm\Sigma}_h),
   \]
   then the reconciled forecasts are also normally distributed,
   \[
   \tilde{\bm{y}}_h \sim N(\bm{S}\bm{G}\hat{\bm{\mu}}_h,\bm{S}\bm{G}\hat{\bm{\Sigma}}_{h}\bm{G}'\bm{S}').
   \]
2. If it is unreasonable to assume normality for the base forecasts, we can use bootstrapping. Bootstrapped prediction intervals were introduced in Section [5.5](https://otexts.com/fpp3/prediction-intervals.html#prediction-intervals). The same idea can be used here. We can simulate future sample paths from the model(s) that produce the base forecasts, and then reconcile these sample paths. Coherent prediction intervals can be computed from the reconciled sample paths.

   Suppose that \((\hat{\bm{y}}_h^{[1]},\dots,\hat{\bm{y}}_h^{[B]})\) are a set of \(B\) simulated sample paths, generated independently from the models used to produce the base forecasts. Then \((\bm{S}\bm{G}\hat{\bm{y}}_h^{[1]},\dots,\bm{S}\bm{G}\hat{\bm{y}}_h^{[B]})\) provides a set of reconciled sample paths, from which percentiles can be calculated in order to construct coherent prediction intervals.

   To generate bootstrapped prediction intervals in this way, we simply set `bootstrap = TRUE` in the `forecast()` function.

### Bibliography

Panagiotelis, A., Gamakumara, P., Athanasopoulos, G., & Hyndman, R. J. (2023). Probabilistic forecast reconciliation: Properties, evaluation and score optimisation. *European J Operational Research*, *306*(2), 693–706.

## 11.6 Forecasting Australian prison population

Returning to the Australian prison population data (Section [11.1](https://otexts.com/fpp3/hts.html#hts)), we will compare the forecasts from bottom-up and MinT methods applied to base ETS models, using a test set comprising the final two years or eight quarters 2015Q1–2016Q4 of the available data.

```
fit <- prison_gts |>
  filter(year(Quarter) <= 2014) |>
  model(base = ETS(Count)) |>
  reconcile(
    bottom_up = bottom_up(base),
    MinT = min_trace(base, method = "mint_shrink")
  )
fc <- fit |> forecast(h = 8)
```

```
fc |>
  filter(is_aggregated(State), is_aggregated(Gender),
         is_aggregated(Legal)) |>
  autoplot(prison_gts, alpha = 0.7, level = 90) +
  labs(y = "Number of prisoners ('000)",
       title = "Australian prison population (total)")
```

![Forecasts for the total Australian quarterly adult prison population for the period 2015Q1--2016Q4.](https://otexts.com/fpp3/fpp_files/figure-html/prisonforecasts-aggregate-1.png)

Figure 11.14: Forecasts for the total Australian quarterly adult prison population for the period 2015Q1–2016Q4.

Figure [11.14](https://otexts.com/fpp3/prison.html#fig:prisonforecasts-aggregate) shows the three sets of forecasts for the aggregate Australian prison population. The base and bottom-up forecasts from the ETS models seem to underestimate the trend over the test period. The MinT approach combines information from all the base forecasts in the aggregation structure; in this case, the base forecasts at the top level are adjusted upwards.

The MinT reconciled prediction intervals are much tighter than the base forecasts, due to MinT being based on an estimator that minimizes variances. The base forecast distributions are also incoherent, and therefore carry with them the extra uncertainty of the incoherency error.

We exclude the bottom-up forecasts from the remaining plots in order to simplify the visual exploration. However, we do revisit their accuracy in the evaluation results presented later.

Figures [11.15](https://otexts.com/fpp3/prison.html#fig:prisonforecasts-State)–[11.17](https://otexts.com/fpp3/prison.html#fig:prisonforecasts-bottom) show the MinT and base forecasts at various levels of aggregation. To make it easier to see the effect, we only show the last five years of training data. In general, MinT adjusts the base forecasts in the direction of the test set, hence improving the forecast accuracy. There is no guarantee that MinT reconciled forecasts will be more accurate than the base forecasts for every series, but they will be more accurate on average (see [Panagiotelis et al., 2021](#ref-PanEtAl2020_Geometry)).

```
fc |>
  filter(
    .model %in% c("base", "MinT"),
    !is_aggregated(State), is_aggregated(Legal),
    is_aggregated(Gender)
  ) |>
  autoplot(
    prison_gts |> filter(year(Quarter) >= 2010),
    alpha = 0.7, level = 90
  ) +
  labs(title = "Prison population (by state)",
       y = "Number of prisoners ('000)") +
  facet_wrap(vars(State), scales = "free_y", ncol = 4) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

![Forecasts for the Australian quarterly adult prison population, disaggregated by state.](https://otexts.com/fpp3/fpp_files/figure-html/prisonforecasts-State-1.png)

Figure 11.15: Forecasts for the Australian quarterly adult prison population, disaggregated by state.

Figure [11.15](https://otexts.com/fpp3/prison.html#fig:prisonforecasts-State) shows forecasts for each of the eight states. There is a general upward trend during the test set period across all the states. However, there appears to be a relatively large and sudden surge in New South Wales and Tasmania, which means the test set observations are well outside the upper bound of the forecast intervals for both these states. Because New South Wales is the state with the largest prison population, this surge will have a substantial impact on the total. In contrast, Victoria shows a substantial dip in 2015Q2–2015Q3, before returning to an upward trend. This dip is not captured in any of the Victorian forecasts.

![Forecasts for the Australian quarterly adult prison population, disaggregated by legal status and by gender.](https://otexts.com/fpp3/fpp_files/figure-html/prisonforecasts-LegalGender-1.png)

Figure 11.16: Forecasts for the Australian quarterly adult prison population, disaggregated by legal status and by gender.

![Forecasts for bottom-level series the Australian quarterly adult prison population, disaggregated by state, by legal status and by gender.](https://otexts.com/fpp3/fpp_files/figure-html/prisonforecasts-bottom-1.png)

Figure 11.17: Forecasts for bottom-level series the Australian quarterly adult prison population, disaggregated by state, by legal status and by gender.

Figure [11.17](https://otexts.com/fpp3/prison.html#fig:prisonforecasts-bottom) shows the forecasts for some selected bottom-level series of the Australian prison population. The four largest states are represented across the columns, with legal status and gender down the rows. These allow for some interesting analysis and observations that have policy implications. The large increase observed across the states during the 2015Q1–2016Q4 test period appears to be driven by large increases in the remand prison population. These increases seem to be generally missed by both forecasts. In contrast to the other states, for New South Wales there is also a substantial increase in the sentenced prison population. In particular, the increase in numbers of sentenced males in NSW contributes substantially to the rise in state and national prison numbers.

Using the `accuracy()` function, we evaluate the forecast accuracy across the grouped structure. The code below evaluates the forecast accuracy for only the top-level national aggregate of the Australian prison population time series. Similar code is used for the rest of the results shown in Table [11.3](https://otexts.com/fpp3/prison.html#tab:tab-crime-evaluation).

```
fc |>
  filter(is_aggregated(State), is_aggregated(Gender),
         is_aggregated(Legal)) |>
  accuracy(data = prison_gts,
           measures = list(mase = MASE,
                           ss = skill_score(CRPS)
                           )
           ) |>
  group_by(.model) |>
  summarise(mase = mean(mase), sspc = mean(ss) * 100)
#> # A tibble: 3 × 3
#>   .model     mase  sspc
#>   <chr>     <dbl> <dbl>
#> 1 MinT      0.895  76.8
#> 2 base      1.72   55.9
#> 3 bottom_up 1.84   33.5
```

Table [11.3](https://otexts.com/fpp3/prison.html#tab:tab-crime-evaluation) summarises the accuracy of the base, bottom-up and the MinT reconciled forecasts over the 2015Q1–2016Q4 test period across each of the levels of the grouped aggregation structure as well as all the levels.

Table 11.3: Accuracy of Australian prison population forecasts for different groups of series.

|  | MASE | | | Skill Score (CRPS) | | |
| --- | --- | --- | --- | --- | --- | --- |
|  | Base | Bottom-up | MinT | Base | Bottom-up | MinT |
| Total | 1.72 | 1.84 | 0.90 | 55.91 | 33.46 | 76.80 |
| State | 2.12 | 1.88 | 1.78 | 6.40 | 24.10 | 22.46 |
| Legal status | 2.89 | 2.68 | 2.32 | 22.22 | 50.27 | 45.23 |
| Gender | 0.89 | 1.76 | 0.91 | 68.98 | 27.49 | 71.06 |
| Bottom | 2.23 | 2.23 | 2.06 | 0.93 | 0.93 | -3.23 |
| All series | 2.19 | 2.16 | 1.96 | 6.70 | 11.29 | 8.69 |

We use scaled measures because the numbers of prisoners vary substantially across the groups. The MASE gives a scaled measure of point-forecast accuracy (see Section [5.8](https://otexts.com/fpp3/accuracy.html#accuracy)), while the CRPS skill score gives a scaled measure of distributional forecast accuracy (see Section [5.9](https://otexts.com/fpp3/distaccuracy.html#distaccuracy)). A low value of MASE indicates a good forecast, while a high value of the skill score indicates a good forecast.

The results show that the MinT reconciled forecasts improve on the accuracy of the base forecasts and are also more accurate than the bottom-up forecasts. As the MinT optimal reconciliation approach uses information from all levels in the structure, it generates more accurate forecasts than the traditional approaches (such as bottom-up) which use limited information.

### Bibliography

Panagiotelis, A., Athanasopoulos, G., Gamakumara, P., & Hyndman, R. J. (2021). Forecast reconciliation: A geometric view with new insights on bias correction. *International Journal of Forecasting*, *37*(1), 343–359.

## 11.7 Exercises

1. Consider the `PBS` data which has aggregation structure `ATC1/ATC2 * Concession * Type`.

   1. Produce plots of the aggregated Scripts data by `Concession`, `Type` and `ATC1`.
   2. Forecast the PBS Scripts data using ETS, ARIMA and SNAIVE models, applied to all but the last three years of data.
   3. Reconcile each of the forecasts using MinT.
   4. Which type of model works best on the test set?
   5. Does the reconciliation improve the forecast accuracy?
   6. Why doesn’t the reconciliation make any difference to the SNAIVE forecasts?
2. Repeat the `tourism` example from Section [11.4](https://otexts.com/fpp3/tourism.html#tourism), but also evaluate the forecast distribution accuracy using CRPS skill scores. Which method does best on this measure?
3. Repeat the `prison` example from Section [11.6](https://otexts.com/fpp3/prison.html#prison), but using a bootstrap to generate the forecast distributions rather than assuming normality. Does it make much difference to the CRPS skill scores?

## 11.8 Further reading

There are no other textbooks which cover hierarchical forecasting in any depth, so interested readers will need to tackle the original research papers for further information.

* Gross & Sohl ([1990](#ref-GroSoh1990)) provide a good introduction to the top-down approaches.
* A recent survey of forecast reconciliation is provided by Athanasopoulos et al. ([2020](#ref-macrohts)).
* The reconciliation methods were developed in a series of papers. The later papers summarise previous results and present the most general theory: Wickramasuriya et al. ([2019](#ref-Mint)), Panagiotelis et al. ([2021](#ref-PanEtAl2020_Geometry)), Panagiotelis et al. ([2023](#ref-PanEtAl2020_Probabilistic)).
* Athanasopoulos et al. ([2017](#ref-AthEtAl2017)) extends the reconciliation approach to deal with temporal hierarchies.
* The tourism example is discussed in more detail in Athanasopoulos et al. ([2009](#ref-AthEtAl2009)), Wickramasuriya et al. ([2019](#ref-Mint)), and Kourentzes & Athanasopoulos ([2019](#ref-KouAth2019)).

### Bibliography

Athanasopoulos, G., Ahmed, R. A., & Hyndman, R. J. (2009). Hierarchical forecasts for Australian domestic tourism. *International Journal of Forecasting*, *25*, 146–166.

Athanasopoulos, G., Gamakumara, P., Panagiotelis, A., Hyndman, R. J., & Affan, M. (2020). Hierarchical forecasting. In P. Fuleky (Ed.), *Macroeconomic forecasting in the era of big data* (pp. 689–719). Springer.

Athanasopoulos, G., Hyndman, R. J., Kourentzes, N., & Petropoulos, F. (2017). Forecasting with temporal hierarchies. *European Journal of Operational Research*, *262*(1), 60–74.

Gross, C. W., & Sohl, J. E. (1990). Disaggregation methods to expedite product line forecasting. *Journal of Forecasting*, *9*, 233–254.

Kourentzes, N., & Athanasopoulos, G. (2019). Cross-temporal coherent forecasts for Australian tourism. *Annals of Tourism Research*, *75*, 393–409.

Panagiotelis, A., Athanasopoulos, G., Gamakumara, P., & Hyndman, R. J. (2021). Forecast reconciliation: A geometric view with new insights on bias correction. *International Journal of Forecasting*, *37*(1), 343–359.

Panagiotelis, A., Gamakumara, P., Athanasopoulos, G., & Hyndman, R. J. (2023). Probabilistic forecast reconciliation: Properties, evaluation and score optimisation. *European J Operational Research*, *306*(2), 693–706.

Wickramasuriya, S. L., Athanasopoulos, G., & Hyndman, R. J. (2019). Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization. *Journal of the American Statistical Association*, *114*(526), 804–819.
