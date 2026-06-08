# Harmonise Raw IHS Data

Takes a raw data.frame loaded from a Malawi IHS survey round (e.g. from
a \`.dta\` file) and renames its columns to the standard harmonised
variable names defined in the crosswalk.

## Usage

``` r
ihs_harmonise(data, round = "IHS5", extra = FALSE)
```

## Arguments

- data:

  A data.frame, typically read from a \`.dta\` file using
  `haven::read_dta`.

- round:

  A character string specifying the IHS round (e.g., `"IHS5"`,
  `"IHS4"`).

- extra:

  Logical. If FALSE (default), drops columns that are not in the
  harmonisation crosswalk or standard ID columns. If TRUE, keeps all
  original columns.

## Value

A data.frame with columns renamed to standard \`harmonised_name\`s where
applicable.
