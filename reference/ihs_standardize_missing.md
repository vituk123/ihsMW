# Standardize Survey Missing Codes

Converts common negative missing codes (like -99 for "Refused" or -98
for "Don't Know") into standard R \`NA\` values to prevent them from
skewing numeric calculations.

## Usage

``` r
ihs_standardize_missing(data)
```

## Arguments

- data:

  A data.frame

## Value

A data.frame with missing values standardized
