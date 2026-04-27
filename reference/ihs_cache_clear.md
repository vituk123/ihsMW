# Clear Cached IHS Data

Removes downloaded datasets from the internal package cache. This is
useful for freeing up disk space. You can clear the cache for specific
rounds or entirely.

## Usage

``` r
ihs_cache_clear(round = NULL)
```

## Arguments

- round:

  A specific round to clear (e.g. `"IHS5"`). If `NULL`, asks for
  confirmation to clear all IHS data depending on the interactivity of
  the session. Defaults to `NULL`.

## Value

Invisibly returns `NULL`.

## Examples

``` r
if (FALSE) { # \dontrun{
# Clear all
ihs_cache_clear()

# Clear only IHS3 data
ihs_cache_clear(round = "IHS3")
} # }
```
