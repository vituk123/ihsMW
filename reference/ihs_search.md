# Search across all IHS rounds for variables manually mapped

Searches the manual harmonisation crosswalk bundled within `ihsMW` for
specific variables.

## Usage

``` r
ihs_search(keyword, round = NULL, fields = c("name", "label", "module"))
```

## Arguments

- keyword:

  A single search string to find (case-insensitive).

- round:

  Limits search to a specific round. Valid inputs are `"IHS2"`,
  `"IHS3"`, `"IHS4"`, `"IHS5"`. Defaults to `NULL` (all rounds).

- fields:

  A character vector of fields to include in the search. Valid fields
  are `"name"`, `"label"`, and `"module"`.

## Value

A tibble with cross-round harmonised search results.

## Examples

``` r
ihs_search("consumption")
#> Found 106 variables matching "consumption".
#> # A tibble: 106 × 10
#>    harmonised_name label    module topic ihs2_name ihs3_name ihs4_name ihs5_name
#>    <chr>           <chr>    <chr>  <chr> <chr>     <chr>     <chr>     <chr>    
#>  1 aa01            Descrip… f2     demo… aa01      NA        NA        NA       
#>  2 epoor           =1 if 2… f84    fish… NA        epoor     NA        NA       
#>  3 exp_cat01       Food/Be… f85    cons… NA        exp_cat01 NA        NA       
#>  4 exp_cat011      Food, n… f85    cons… exp_cat0… exp_cat0… NA        NA       
#>  5 exp_cat012      Beverag… f85    cons… exp_cat0… exp_cat0… NA        NA       
#>  6 exp_cat02       Alc/Tob… f85    cons… NA        exp_cat02 NA        NA       
#>  7 exp_cat021      Alcohol… f85    cons… exp_cat0… exp_cat0… NA        NA       
#>  8 exp_cat022      Tobacco… f85    cons… exp_cat0… exp_cat0… NA        NA       
#>  9 exp_cat031      Clothin… f85    cons… exp_cat0… exp_cat0… NA        NA       
#> 10 exp_cat032      Footwea… f85    cons… exp_cat0… exp_cat0… NA        NA       
#> # ℹ 96 more rows
#> # ℹ 2 more variables: n_rounds <dbl>, needs_review <lgl>
ihs_search("expenditure", round = "IHS5")
#> Found 1 variable matching "expenditure".
#> # A tibble: 1 × 10
#>   harmonised_name label     module topic ihs2_name ihs3_name ihs4_name ihs5_name
#>   <chr>           <chr>     <chr>  <chr> <chr>     <chr>     <chr>     <chr>    
#> 1 hh_c22b         Expendit… f4     educ… NA        hh_c22b   hh_c22b   hh_c22b  
#> # ℹ 2 more variables: n_rounds <dbl>, needs_review <lgl>
ihs_search("age", fields = c("name", "label"))
#> Found 272 variables matching "age".
#> # A tibble: 272 × 10
#>    harmonised_name label    module topic ihs2_name ihs3_name ihs4_name ihs5_name
#>    <chr>           <chr>    <chr>  <chr> <chr>     <chr>     <chr>     <chr>    
#>  1 ac06a           Age at … f4     educ… ac06a     NA        NA        NA       
#>  2 ac06b           Age at … f4     educ… ac06b     NA        NA        NA       
#>  3 ac08            Did [na… f4     educ… ac08      NA        NA        NA       
#>  4 ac08oth         A08 - O… f4     educ… ac08oth   NA        NA        NA       
#>  5 adult           HH: Ind… f40    agri… adult     NA        NA        NA       
#>  6 ag_b18          Do you … f31    agri… NA        ag_b18    NA        NA       
#>  7 ag_b19          What is… f31    agri… NA        ag_b19    NA        NA       
#>  8 ag_b19_os       What is… f31    agri… NA        ag_b19_os NA        NA       
#>  9 ag_b214         During … f35    agri… NA        NA        ag_b214   ag_b214  
#> 10 ag_d14          Garden … f37    agri… NA        ag_d14    ag_d14    ag_d14   
#> # ℹ 262 more rows
#> # ℹ 2 more variables: n_rounds <dbl>, needs_review <lgl>
```
