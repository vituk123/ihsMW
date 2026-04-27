# Download Malawi IHS microdata

The main interface to the ihsMW package. Downloads one or more IHS
variables across one or more survey rounds, applies cross-round
harmonisation, and returns the data in the requested format.

## Usage

``` r
IHS(
  indicator,
  round = "IHS5",
  module = NULL,
  return = c("data.frame", "list", "survey"),
  format = c("parquet", "rds", "csv"),
  cache = TRUE,
  extra = FALSE
)
```

## Arguments

- indicator:

  Character vector of harmonised variable names. Use
  [`ihs_search`](https://username.github.io/ihsMW/reference/ihs_search.md)
  to discover variable names.

- round:

  Character vector of IHS rounds to include. One or more of `"IHS2"`,
  `"IHS3"`, `"IHS4"`, `"IHS5"`, or `"all"`. Note: IHS1 is not currently
  available via the API. Default: `"IHS5"`.

- module:

  Optional character string to restrict to a specific module. If NULL
  (default), the correct module is determined automatically from the
  crosswalk.

- return:

  Output format: `"data.frame"` (default), `"list"`, or `"survey"`.

- format:

  File format for download and caching: `"parquet"` (default), `"rds"`,
  or `"csv"`.

- cache:

  Logical. If TRUE (default), use and populate the disk cache.

- extra:

  Logical. If FALSE (default), return only the requested indicator
  columns plus household ID columns. If TRUE, include all variables in
  the downloaded module (stratum, cluster, weights, etc.).

## Value

If `return = "data.frame"`: a single `data.frame` with an `ihs_round`
column.  
If `return = "list"`: a named list of `data.frame`s, one per round.  
If `return = "survey"`: a `tbl_svy` or `svydesign` object.

## See also

[`ihs_search`](https://username.github.io/ihsMW/reference/ihs_search.md)
to find variable names.  
`IHS_survey` for weighted survey analysis.  
`ihs_crosswalk_check` to assess cross-round comparability.

## Examples

``` r
if (FALSE) { # \dontrun{
  # One-time setup
  ihs_auth()

  # Download a single variable from the latest round
  df <- IHS("rexp_cat01", round = "IHS5")

  # Multiple variables, multiple rounds
  df <- IHS(c("rexp_cat01", "hh_a02"), round = c("IHS4", "IHS5"))

  # All supported rounds
  df <- IHS("rexp_cat01", round = "all")

  # Return as a named list of data.frames
  lst <- IHS("rexp_cat01", round = c("IHS3", "IHS4", "IHS5"), return = "list")

  # Include weights and design variables
  df <- IHS("rexp_cat01", round = "IHS5", extra = TRUE)

  # Use rds format instead of parquet
  df <- IHS("rexp_cat01", round = "IHS5", format = "rds")
} # }
```
