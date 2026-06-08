# Check the comparability of variables across IHS rounds

Evaluates the completeness and comparability of variables across the
available IHS rounds (IHS2, IHS3, IHS4, IHS5) using the bundled
crosswalk.

## Usage

``` r
ihs_crosswalk_check(verbose = TRUE)
```

## Arguments

- verbose:

  Logical. If `TRUE` (default), prints a summary report to the console
  using `cli`.

## Value

A `tibble` containing the full crosswalk. If `verbose` is `TRUE`, also
prints a summary.

## Examples

``` r
if (FALSE) { # \dontrun{
  # Check the crosswalk and print a report
  cw <- ihs_crosswalk_check()
} # }
```
