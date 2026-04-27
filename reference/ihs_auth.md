# Set up World Bank Microdata API Key

The World Bank Microdata Library uses API keys for authenticated
endpoints. The key is stored in the environment variable
`WORLDBANK_MICRODATA_KEY`.

If `key` is `NULL`, this function prints an interactive guide to
obtaining an API key. If a key is provided, the function validates it
against the NADA API, saves it to the session, and appends it to your
`~/.Renviron` file for future sessions.

## Usage

``` r
ihs_auth(key = NULL)
```

## Arguments

- key:

  A single string containing your World Bank Microdata API key. Defaults
  to `NULL`.

## Value

Invisibly returns the API key (if provided) or `NULL`.

## Examples

``` r
if (FALSE) { # \dontrun{
# Print interactive setup guide
ihs_auth()

# Set your API key
ihs_auth("paste_your_key_here")
} # }
```
