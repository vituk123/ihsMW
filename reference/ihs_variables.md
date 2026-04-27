# Inspect all variables for a study

Provides real-time variable availability inspection straight from the
NADA API.

## Usage

``` r
ihs_variables(round = "IHS5", module = NULL)
```

## Arguments

- round:

  A specific round to fetch variables for (e.g. `"IHS5"`).

- module:

  An optional module string to specifically look down variables isolated
  to that path natively (case-insensitive).

## Value

Invisibly returns a tibble profiling the variables dynamically mapped
alongside known names.

## Examples

``` r
if (FALSE) { # \dontrun{
ihs_variables(round = "IHS4")
ihs_variables(round = "IHS5", module = "hh_mod_g")
} # }
```
