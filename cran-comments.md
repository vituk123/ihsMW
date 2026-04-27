## Resubmission (v0.1.2)

- This is a resubmission. Changes from v0.1.1:
  - Added `Depends: R (>= 4.1.0)` to declare the minimum R version
    required by the native pipe `|>` syntax used in the package.

## Test environments

- Ubuntu 24.04 (GitHub Actions), R release and R devel
- Windows Server 2022 (GitHub Actions), R release
- macOS 14 (GitHub Actions), R release

## R CMD check results

0 errors | 0 warnings | 1 note

- NOTE (new submission): The flagged words "IHS" and "Microdata" are
  not misspellings. IHS is the standard abbreviation for the
  Integrated Household Survey conducted by Malawi's National
  Statistical Office, and Microdata refers to the World Bank
  Microdata Library.

## Notes for CRAN reviewers

- This package downloads data at runtime from the World Bank Microdata Library.
  Users must register for a free account and obtain an API key via `ihs_auth()`.
  No data is bundled with the package.

- All tests mock HTTP calls using httptest2. Tests do not require an API key
  or internet connection.

- The package stores a user API key in `.Renviron` (with user consent via
  `ihs_auth()`). This is the same pattern used by the gh, googledrive, and
  rtweet packages.

- The only file written to disk by the package is the user's data cache, stored
  in `rappdirs::user_cache_dir("ihsMW")`. The cache can be cleared with
  `ihs_cache_clear()`.
