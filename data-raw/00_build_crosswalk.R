# data-raw/00_build_crosswalk.R

# This script fetches variable metadata for IHS rounds 2-5 from the World Bank API,
# standardises them, and builds a cross-round harmonisation crosswalk.

library(httr2)
library(dplyr)
library(purrr)
library(stringr)
library(tidyr)
library(stringdist)
library(readr)

# STEP 1 - FETCH VARIABLE METADATA
# ==============================================================================
idnos <- c(
  IHS2 = "MWI_2004_IHS-II_v01_M",
  IHS3 = "MWI_2010_IHS-III_v01_M",
  IHS4 = "MWI_2016_IHS-IV_v03_M",
  IHS5 = "MWI_2019_IHS-V_v06_M"
)

all_vars_list <- list()

for (rval in names(idnos)) {
  idno <- idnos[[rval]]
  url <- paste0("https://microdata.worldbank.org/index.php/api/catalog/", idno, "/variables")
  
  cat(sprintf("Fetching variables for %s (%s)...\n", rval, idno))
  
  req <- request(url)
  
  # Perform request gracefully
  resp <- tryCatch({
    req_perform(req)
  }, error = function(e) {
    warning("Failed to fetch ", rval, ": ", e$message)
    return(NULL)
  })
  
  if (!is.null(resp)) {
    resp_data <- resp_body_json(resp)
    
    vars <- if (!is.null(resp_data$variables$variable)) {
      resp_data$variables$variable
    } else {
      resp_data$variables
    }
    
    if (is.list(vars)) {
      this_round <- map_dfr(vars, function(v) {
        tibble(
          var_name = as.character(v$name %||% v$vid %||% NA),
          label = as.character(v$labl %||% NA),
          file_name = as.character(v$fid %||% v$file_id %||% NA),
          round = rval
        )
      })
      
      all_vars_list[[rval]] <- this_round
    } else {
      warning("No variables found or unexpected format for ", rval)
    }
  }
  
  Sys.sleep(1) # Be polite to the API
}

all_vars <- bind_rows(all_vars_list)

cat("\nVariables fetched per round:\n")
print(
  all_vars |> 
    count(round)
)

# STEP 2 - CLEAN AND STANDARDISE
# ==============================================================================
cat("\nCleaning and standardising...\n")

all_vars <- all_vars |>
  filter(!is.na(var_name), var_name != "") |>
  mutate(
    var_name = str_to_lower(var_name),
    file_name = str_to_lower(str_replace_all(file_name, "\\s+", "")),
    label = str_trim(label)
  )

# STEP 3 - IDENTIFY CROSS-ROUND VARIABLES
# ==============================================================================
cat("Identifying cross-round variables...\n")

# Group by var_name and identify exact matches
exact_matches <- all_vars |>
  group_by(var_name) |>
  summarise(
    rounds = list(round),
    n_rounds = n(),
    .groups = "drop"
  )

single_round_names <- exact_matches |> filter(n_rounds == 1) |> pull(var_name)

matches_df <- tibble(
  orig_name = exact_matches$var_name,
  harmonised_name = exact_matches$var_name,
  needs_review = FALSE
)

if (length(single_round_names) > 0) {
  cat("Performing fuzzy matching for variables unique to one round...\n")
  
  sim_matrix <- stringsimmatrix(single_round_names, exact_matches$var_name, method = "jw")
  threshold <- 0.92
  
  for (i in seq_along(single_round_names)) {
    this_name <- single_round_names[i]
    this_round <- all_vars$round[all_vars$var_name == this_name][1]
    
    sims <- sim_matrix[i, ]
    candidate_indices <- which(sims >= threshold)
    
    # Exclude itself
    candidate_indices <- candidate_indices[exact_matches$var_name[candidate_indices] != this_name]
    
    if (length(candidate_indices) > 0) {
      # Keep candidates from different rounds
      valid_candidates <- candidate_indices[vapply(candidate_indices, function(idx) {
        cand_rounds <- unlist(exact_matches$rounds[idx])
        !(this_round %in% cand_rounds)
      }, logical(1))]
      
      if (length(valid_candidates) > 0) {
        # Pick highest similarity match
        best_match_idx <- valid_candidates[which.max(sims[valid_candidates])]
        best_match_name <- exact_matches$var_name[best_match_idx]
        
        matches_df$harmonised_name[matches_df$orig_name == this_name] <- best_match_name
        matches_df$needs_review[matches_df$orig_name == this_name] <- TRUE
      }
    }
  }
}

all_vars_mapped <- all_vars |>
  left_join(matches_df, by = c("var_name" = "orig_name"))

# STEP 4 - BUILD THE CROSSWALK TIBBLE
# ==============================================================================
cat("Building crosswalk tibble...\n")

wide_metadata <- all_vars_mapped |>
  group_by(harmonised_name, round) |>
  slice(1) |>
  ungroup()

names_wide <- wide_metadata |>
  select(harmonised_name, round, var_name) |>
  pivot_wider(
    names_from = round, 
    values_from = var_name,
    names_prefix = "ihs_name_"
  )

# Rename to ihs2_name, ihs3_name, ihs4_name, ihs5_name mapping
round_cols <- c("ihs_name_IHS2", "ihs_name_IHS3", "ihs_name_IHS4", "ihs_name_IHS5")
for (col in round_cols) {
  if (!col %in% names(names_wide)) {
    names_wide[[col]] <- NA_character_
  }
}

names_wide <- names_wide |>
  rename(
    ihs2_name = ihs_name_IHS2,
    ihs3_name = ihs_name_IHS3,
    ihs4_name = ihs_name_IHS4,
    ihs5_name = ihs_name_IHS5
  )

meta_recent <- wide_metadata |>
  arrange(harmonised_name, desc(round)) |>
  group_by(harmonised_name) |>
  summarise(
    label = first(na.omit(label)),
    module = first(na.omit(file_name)),
    needs_review = any(needs_review),
    n_rounds = n_distinct(round),
    .groups = "drop"
  )

ihs_crosswalk <- names_wide |>
  left_join(meta_recent, by = "harmonised_name") |>
  mutate(
    harmonised_name_new = coalesce(ihs5_name, ihs4_name, ihs3_name, ihs2_name)
  ) |>
  mutate(harmonised_name = harmonised_name_new) |>
  select(-harmonised_name_new) |>
  mutate(topic = NA_character_) |>
  select(
    harmonised_name,
    ihs2_name,
    ihs3_name,
    ihs4_name,
    ihs5_name,
    label,
    module,
    topic,
    needs_review,
    n_rounds
  ) |>
  arrange(desc(n_rounds), harmonised_name)

# STEP 5 - SAVE OUTPUTS
# ==============================================================================
cat("Saving outputs...\n")

dir.create("data-raw/processed", showWarnings = FALSE, recursive = TRUE)
dir.create("inst/extdata", showWarnings = FALSE, recursive = TRUE)

write_csv(ihs_crosswalk, "data-raw/processed/ihs_crosswalk_working.csv")
write_csv(ihs_crosswalk, "inst/extdata/ihs_crosswalk.csv")
saveRDS(all_vars, "data-raw/processed/all_vars_raw.rds")

# STEP 6 - PRINT SUMMARY REPORT
# ==============================================================================
cat("\n=== ihsMW crosswalk build summary ===\n")
cat(sprintf("Total unique harmonised variables : %d\n", nrow(ihs_crosswalk)))
cat(sprintf("Present in all 4 rounds           : %d\n", sum(ihs_crosswalk$n_rounds == 4)))
cat(sprintf("Present in 3 rounds               : %d\n", sum(ihs_crosswalk$n_rounds == 3)))
cat(sprintf("Present in 2 rounds               : %d\n", sum(ihs_crosswalk$n_rounds == 2)))
cat(sprintf("Present in 1 round only           : %d\n", sum(ihs_crosswalk$n_rounds == 1)))
cat(sprintf("Flagged for manual review         : %d\n\n", sum(ihs_crosswalk$needs_review)))

cat("Next step: open data-raw/processed/ihs_crosswalk_working.csv,\n")
cat("manually fill in the 'topic' column and resolve needs_review = TRUE rows,\n")
cat("then copy to inst/extdata/ihs_crosswalk.csv.\n")
