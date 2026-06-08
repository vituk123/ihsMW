# Winsorize Continuous Variables

Caps extreme outliers at specified percentiles. Crucially, this function
allows for stratified winsorization (e.g., by region) to avoid
over-trimming poor/rich areas, and it creates new \`\_w\` suffixed
columns to preserve raw data provenance.

## Usage

``` r
ihs_winsorize(data, vars, by = NULL, probs = c(0.01, 0.99))
```

## Arguments

- data:

  A data.frame

- vars:

  Character vector of column names to winsorize

- by:

  Optional grouping variable name (e.g., "region") for stratified
  thresholds

- probs:

  Numeric vector of lower and upper quantiles. Default \`c(0.01, 0.99)\`

## Value

A data.frame with new \`\*\_w\` columns added.
