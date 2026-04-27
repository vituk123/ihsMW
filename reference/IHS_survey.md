# Create a survey design object for Malawi IHS data

Creates a complex survey design object using the `survey` and `srvyr`
packages. Automatically incorporates the appropriate sampling weights,
strata, and clusters for the requested round to enable statistically
sound national estimations natively.

## Usage

``` r
IHS_survey(indicator, round = "IHS5", ...)
```

## Arguments

- indicator:

  Character vector of harmonised variable names.

- round:

  A single round string (e.g. `"IHS5"`) or `"all"`.

- ...:

  Additional arguments passed to
  [`IHS`](https://username.github.io/ihsMW/reference/IHS.md), such as
  `module` or `format`.

## Value

A `tbl_svy` object if the `srvyr` package is installed, otherwise a
`svydesign` object from the `survey` package. If multiple rounds are
requested, returns a named list of survey objects.

## Note

Survey weights differ across IHS rounds and reflect the complex sample
design of each survey. Estimates produced using this function are
representative at the national, urban/rural, regional, and district
level for each round independently. Do not pool weights across rounds
without consulting the relevant Basic Information Document for each
round. Cite the sampling methodology: NSO Malawi (year), IHS\[N\] Basic
Information Document. National Statistical Office, Zomba, Malawi.

## Examples

``` r
if (FALSE) { # \dontrun{
  svy <- IHS_survey("rexp_cat01", round = "IHS5")
  survey::svymean(~rexp_cat01, design = svy)
  svy |> srvyr::summarise(mean_cons = srvyr::survey_mean(rexp_cat01))
} # }
```
