# test-survey.R
# Tests for IHS_survey() survey design object creation with mocked IHS().

# 20-row mock data with correct IHS5 weight/strata/cluster columns
mock_survey_df <- data.frame(
  case_id  = paste0("HH", 1:20),
  rexp_cat01 = runif(20, 10000, 500000),
  hhweight = runif(20, 0.5, 3.0),
  stratum  = rep(c("STR1", "STR2", "STR3", "STR4"), each = 5),
  ea_id    = paste0("EA", rep(1:10, each = 2)),
  ihs_round = rep("IHS5", 20),
  stringsAsFactors = FALSE
)

# Mock IHS that returns the survey dataframe
mock_IHS_for_survey <- function(indicator, round, extra = TRUE, return = "data.frame", ...) {
  mock_survey_df
}

test_that("IHS_survey returns a survey object for IHS5", {
  local_mocked_bindings(IHS = mock_IHS_for_survey)

  result <- suppressMessages(IHS_survey("rexp_cat01", round = "IHS5"))

  if (rlang::is_installed("srvyr")) {
    expect_s3_class(result, "tbl_svy")
  } else {
    expect_s3_class(result, "survey.design")
  }
})

test_that("IHS_survey returns list and warns when multiple rounds requested", {
  # Mock IHS to return round-appropriate weight column names
  mock_IHS_multiround <- function(indicator, round, extra = TRUE, return = "data.frame", ...) {
    wt_info <- .ihs_weight_vars[.ihs_weight_vars$round == round, ]
    df <- data.frame(
      case_id  = paste0("HH", 1:20),
      rexp_cat01 = runif(20, 10000, 500000),
      ihs_round = rep(round, 20),
      stringsAsFactors = FALSE
    )
    df[[wt_info$weight_var[1]]] <- runif(20, 0.5, 3.0)
    df[[wt_info$strata_var[1]]] <- rep(c("STR1", "STR2", "STR3", "STR4"), each = 5)
    df[[wt_info$cluster_var[1]]] <- paste0("EA", rep(1:10, each = 2))
    df
  }
  local_mocked_bindings(IHS = mock_IHS_multiround)

  expect_warning(
    result <- suppressMessages(IHS_survey("rexp_cat01", round = "all")),
    "cannot be pooled"
  )
  expect_type(result, "list")
  expect_true(length(result) >= 2)
})

test_that("IHS_survey aborts when weight columns are missing", {
  # Mock IHS returning df WITHOUT the hhweight column
  mock_missing_weights <- function(indicator, round, extra = TRUE, return = "data.frame", ...) {
    df <- mock_survey_df
    df$hhweight <- NULL
    df
  }
  local_mocked_bindings(IHS = mock_missing_weights)

  expect_error(
    suppressMessages(IHS_survey("rexp_cat01", round = "IHS5")),
    "Missing survey design variables"
  )
})

test_that("IHS_survey aborts when strata column is missing", {
  mock_missing_strata <- function(indicator, round, extra = TRUE, return = "data.frame", ...) {
    df <- mock_survey_df
    df$stratum <- NULL
    df
  }
  local_mocked_bindings(IHS = mock_missing_strata)

  expect_error(
    suppressMessages(IHS_survey("rexp_cat01", round = "IHS5")),
    "Missing survey design variables"
  )
})

test_that("IHS_survey has correct design variables set", {
  local_mocked_bindings(IHS = mock_IHS_for_survey)

  result <- suppressMessages(IHS_survey("rexp_cat01", round = "IHS5"))

  # Regardless of srvyr or base survey, check the call has the right variables
  if (rlang::is_installed("srvyr")) {
    # Extract underlying svydesign
    des <- result$variables
    expect_true("rexp_cat01" %in% names(des))
  } else {
    expect_true("rexp_cat01" %in% names(result$variables))
  }
})

test_that(".ihs_weight_vars has entries for all supported rounds", {
  for (r in c("IHS2", "IHS3", "IHS4", "IHS5")) {
    wt_row <- .ihs_weight_vars[.ihs_weight_vars$round == r, ]
    expect_equal(nrow(wt_row), 1, info = paste("Missing weight info for", r))
    expect_true(nzchar(wt_row$weight_var), info = paste("Empty weight_var for", r))
    expect_true(nzchar(wt_row$strata_var), info = paste("Empty strata_var for", r))
    expect_true(nzchar(wt_row$cluster_var), info = paste("Empty cluster_var for", r))
  }
})
