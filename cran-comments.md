## Resubmission (v0.2.1)

This is a resubmission of the offline-first pivot.
Compared to the previous submission (v0.2.0), this version:
- Added `^scratch$` to `.Rbuildignore` to prevent the non-standard `scratch` directory from being included in the source archive.
- Added `winsorization` (and variations) to `inst/WORDLIST` to resolve the spelling check NOTE.

Key changes from the original CRAN release:
- Removed all external API orchestration, World Bank NADA dependencies, and authentication.
- Removed imports of `httr2`, `httptest2`, `rappdirs`, and `stringdist` to simplify the dependency tree.
- Built a bundled, comprehensive database of 1,608 region-crop-unit-condition conversion factors in the package.
- Added a robust offline unit-conversion engine (`ihs_convert_units()`) utilizing these official NSO conversion factors.
- All testing and execution are now completely local and offline-first.

## Test environments

- local Apple Silicon Mac, macOS Sequoia 15.1, R version 4.4.2
- Ubuntu 24.04 (GitHub Actions), R release and R devel
- Windows Server 2022 (GitHub Actions), R release
- macOS 14 (GitHub Actions), R release

## R CMD check results

0 errors | 0 warnings | 1 note

- The only note is: "checking for future file timestamps ... NOTE: unable to verify current time". This is environment-specific during standard checking under certain network/time-server restrictions.

## Notes for CRAN reviewers

- This package contains no network operations or external API connections.
- It ships with reference CSV metadata: `ihs_crosswalk.csv` (harmonisation crosswalk) and `crop_conversion_factors.csv` (NSO agricultural crop unit-to-kg factors).
- No directories or files are written to disk during ordinary execution.
