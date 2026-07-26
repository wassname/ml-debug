Source: https://otexts.com/fpp3/appendix-using-r.html (chapter appendix-using-r, 1 section pages merged)
Title: Forecasting: Principles and Practice 3rd ed - app-using-r
Fetched-via: urllib + markitdown (content div.page-inner section.normal), 2026-07-26
Fetch-status: full content; images/links point to absolute otexts.com URLs

# Appendix: Using R

This book uses R and is designed to be used with R. R is free, available on almost every operating system, and there are thousands of add-on packages to do almost anything you could ever want to do. We recommend you use R with RStudio.

### Installing R and RStudio

1. [Download and install R.](https://cran.r-project.org/)
2. [Download and install RStudio.](https://bit.ly/rstudiodownload)
3. Run RStudio. On the “Packages” tab, click on “Install” and install the package `fpp3` (make sure “install dependencies” is checked).

That’s it! You should now be ready to go.

### R examples in this book

We provide R code for most examples in shaded boxes like this:

```
# Load required packages
library(fpp3)

# Plot one time series
aus_retail |>
  filter(`Series ID`=="A3349640L") |>
  autoplot(Turnover)

# Produce some forecasts
aus_retail |>
  filter(`Series ID`=="A3349640L") |>
  model(ETS(Turnover)) |>
  forecast(h = "2 years")
```

These examples assume that you have the `fpp3` package loaded as shown above. This needs to be done at the start of every R session, but it won’t be included in our examples.

Sometimes we assume that the R code that appears earlier in the same chapter of the book has also been run; so it is best to work through the R code in the order provided within each chapter.

### Getting started with R

If you have never previously used R, please work through the first section (chapters 1-8) of [“R for Data Science”](https://r4ds.hadley.nz) by Garrett Grolemund and Hadley Wickham. While this does not cover time series or forecasting, it will get you used to the basics of the R language, and the `tidyverse` packages. The [Coursera R Programming](https://www.coursera.org/learn/r-programming) course is also highly recommended.

You will learn how to use R for forecasting using the exercises in this book.
