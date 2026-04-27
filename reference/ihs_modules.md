# Inspect available modules for a study

Profiles the file hierarchy explicitly for each data survey pulling
nested variables counts efficiently per dataset.

## Usage

``` r
ihs_modules(round = "IHS5")
```

## Arguments

- round:

  A specific round to fetch dataset structures safely scoped against.
  (e.g. `"IHS5"`).

## Value

Invisibly returns a tibble mapping underlying module variables mapping
locally.

## Examples

``` r
if (FALSE) { # \dontrun{
ihs_modules("IHS5")
} # }
```
