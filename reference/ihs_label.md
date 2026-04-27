# Fetch specific variable label locally or remotely

Quickly deciphers what an individual variable physically measures. Looks
through the offline dataset initially via harmonised mappings and
seamlessly falls through NADA otherwise.

## Usage

``` r
ihs_label(variable, round = "IHS5")
```

## Arguments

- variable:

  A single character variable map or harmonised standard to inspect
  precisely.

- round:

  The physical survey round to tie it structurally to if verifying
  non-harmonised entries. Default `"IHS5"`.

## Value

The extracted label mapping directly against what the variable
corresponds natively to.

## Examples

``` r
ihs_label("rexp_cat01")
#> [1] "Food/Bev, real(April 2019 price) annual consumption"
```
