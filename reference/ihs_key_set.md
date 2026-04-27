# Set up World Bank Microdata API Key (Alias)

A wrapper for
[`ihs_auth()`](https://username.github.io/ihsMW/reference/ihs_auth.md)
meant for use in scripted or non-interactive environments.

## Usage

``` r
ihs_key_set(key)
```

## Arguments

- key:

  A single string containing your World Bank Microdata API key.

## Value

Invisibly returns the API key.

## Examples

``` r
if (FALSE) { # \dontrun{
ihs_key_set("paste_your_key_here")
} # }
```
