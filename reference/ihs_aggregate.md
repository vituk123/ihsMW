# Smart Aggregation to Household Level

Automatically detects variable types and applies sensible aggregations
(e.g., \`sum\` for continuous quantities, \`max\` or logical OR for
dummies). Throws warnings for ambiguous columns rather than failing
silently.

## Usage

``` r
ihs_aggregate(data, group_col = "case_id")
```

## Arguments

- data:

  A data.frame at the individual or plot level

- group_col:

  The column name identifying the household (e.g., "case_id" or
  "y4_hhid")

## Value

A data.frame aggregated to the household level
