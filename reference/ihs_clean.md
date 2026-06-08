# Clean and Harmonise IHS Data

This wrapper function applies standard cleaning procedures to Malawi IHS
data. It handles missing value conversions, winsorization of continuous
variables, and returns an audit log of all transformations applied.

## Usage

``` r
ihs_clean(
  data,
  winsorize_vars = NULL,
  winsorize_by = NULL,
  probs = c(0.01, 0.99)
)
```

## Arguments

- data:

  A data.frame (typically loaded from a \`.dta\` file)

- winsorize_vars:

  Character vector of continuous variables to winsorize (e.g.,
  consumption, harvest)

- winsorize_by:

  Optional character string of a grouping variable (e.g., region) for
  stratified winsorization

- probs:

  Numeric vector of length 2 specifying the lower and upper quantiles
  for winsorization. Default is \`c(0.01, 0.99)\`.

## Value

A data.frame with cleaning applied. The returned object has an
\`ihs_audit\` attribute containing a log of modifications.
