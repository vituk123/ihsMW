# Contributing to ihsMW

Thank you for your interest in contributing to ihsMW! This document outlines how to report bugs, suggest improvements, and submit code.

## Reporting bugs

Please open an issue on [GitHub Issues](https://github.com/vituk123/ihsMW/issues) with:

1. A short, descriptive title.
2. The output of `sessionInfo()`.
3. A minimal reproducible example (reprex) demonstrating the problem.
4. The expected vs. actual behaviour.

## Suggesting crosswalk corrections

The harmonisation crosswalk lives at `inst/extdata/ihs_crosswalk.csv`. To correct a mapping or add a new variable:

1. Fork the repository and create a branch (e.g., `fix/rexp-cat01-mapping`).
2. Edit `inst/extdata/ihs_crosswalk.csv` directly.
3. If you are unsure about a mapping, set `needs_review = TRUE`.
4. Open a pull request describing which variable changed, in which round, and your source (e.g., the BID page number).

## Code style

- Follow the [tidyverse style guide](https://style.tidyverse.org/).
- Use `cli::cli_abort()`, `cli::cli_warn()`, and `cli::cli_inform()` for all user-facing messages. Never use `stop()`, `message()`, or `cat()`.
- Use `rlang::abort()` only if you need a low-level programmatic error.
- Use `httr2` for all HTTP calls, not `httr` or `curl`.

## Running tests locally

```r
devtools::test()
```

All tests use httptest2 mocks and run completely offline. No API key is required.

## Adding a new Malawi survey

To extend `ihsMW` with a new survey (e.g., IHPS or future IHS6):

1. Add the round key and IDNo to `.IHS_ROUNDS` and `.IHS_IDNOS` in `R/utils.R`.
2. Add weight/strata/cluster mappings to `.ihs_weight_vars` in `R/IHS_survey.R`.
3. Extend `inst/extdata/ihs_crosswalk.csv` with a new `ihs{N}_name` column.
4. Update `mwi_surveys()` in the relevant R file.
5. Add corresponding tests and update the vignettes.
