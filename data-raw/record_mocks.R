library(ihsMW)
library(httptest2)

# Ensure the package is loaded directly from source to mirror functions dynamically
devtools::load_all()

# We record real HTTP dependencies natively matching accurate JSON fixtures 
# These will be written directly into tests/testthat/fixtures iteratively.
httptest2::with_mock_dir("tests/testthat/fixtures", {
  
  # Record the search catalog endpoints returning N-dimensions
  message("Recording .nada_search...")
  ihsMW:::.nada_search("consumption")
  
  # Record variable subsets for explicit IHS instances dynamically
  message("Recording .nada_variables...")
  ihsMW:::.nada_variables("MWI_2019_IHS-V_v06_M")
  
  # Record specific file structure queries accurately mapping format trees
  message("Recording .nada_data_files...")
  ihsMW:::.nada_data_files("MWI_2019_IHS-V_v06_M")
  
})

message("Mocks successfully recorded!")
