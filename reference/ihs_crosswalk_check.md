# Check Crosswalk Health

Evaluates the ihsMW crosswalk variable map. Prints a formatted report
indicating how many variables are present across rounds, and flags any
variables needing manual review.

## Usage

``` r
ihs_crosswalk_check()
```

## Value

A `tibble` containing the master crosswalk, returned invisibly.

## Examples

``` r
if (FALSE) { # \dontrun{
cw <- ihs_crosswalk_check()
} # }
```
