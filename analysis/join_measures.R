# This scrip loads all measures files and
# (1) joins them together (separate files for each indicator)
# (2) rounds counts to the nearest 10

# Note that the ungrouped measure (population) and grouped measures
# differ in the number of their variables

# Load packages ----
library(magrittr)
library(dplyr)
library(tidyr)
library(here)
library(readr)
library(fs)
library(purrr)
library(stringr)

# INDICATOR HYP_001 ---
# Get file names and path
dir_hyp_001_measures <- fs::dir_ls(path = "output/indicators/joined",
                                   glob = "*measure_hyp001_prevalence_*.csv$")

# Split dir paths because file structure differes
## Grouped measures (excluding practice)
dir_hyp_001_measures_groups <- dir_hyp_001_measures[!stringr::str_detect(dir_hyp_001_measures, "population")]
dir_hyp_001_measures_groups <- dir_hyp_001_measures_groups[!stringr::str_detect(dir_hyp_001_measures_groups, "practice")]

## Population measure
dir_hyp_001_measures_pop <- dir_hyp_001_measures[stringr::str_detect(dir_hyp_001_measures, "population")]

# Load files
## Load grouped measures
## Pivot longer so variable names are identical across measure files
df_hyp_001_measures_groups <- dir_hyp_001_measures_groups %>%
  purrr::map(readr::read_csv) %>%
  purrr::map_dfr(tidyr::pivot_longer,
                 cols = 1,
                 names_to = "group",
                 values_to = "category",
                 values_transform = list(category = as.character))

# Load population measure
# Add variables that are missing compared to grouped measures
df_hyp_001_measures_pop <- readr::read_csv(here::here(dir_hyp_001_measures_pop)) %>%
  dplyr::mutate(group = "population",
                category = "population")

# Join all measures into one object
df_hyp_001_measures <- df_hyp_001_measures_groups %>%
  dplyr::bind_rows(df_hyp_001_measures_pop)

# Write hyp001 csv file
## First create subdirectory (if it doesn't exist)
fs::dir_create(here::here("output", "indicators", "joined", "measures"))

# Round counts to the nearest 10 and recalculate value
df_hyp_001_measures <- df_hyp_001_measures %>%
   dplyr::mutate(dplyr::across(c("hyp_reg", "population"), round, -1)) %>%
   dplyr::mutate(value = hyp_reg / population)

## Next, write csv file
readr::write_csv(df_hyp_001_measures,
                 here::here("output", "indicators", "joined", "measures", "measures_hyp001.csv"))

# INDICATOR HYP_003 ---
# Get file names and path
dir_hyp_003_measures <- fs::dir_ls(path = "output/indicators/joined",
                                   glob = "*measure_hyp003_achievem_*.csv$")

# Split dir paths because file structure differes
## Grouped measures (excluding practice)
dir_hyp_003_measures_groups <- dir_hyp_003_measures[!stringr::str_detect(dir_hyp_003_measures, "population")]
dir_hyp_003_measures_groups <- dir_hyp_003_measures_groups[!stringr::str_detect(dir_hyp_003_measures_groups, "practice")]

## Population measure
dir_hyp_003_measures_pop <- dir_hyp_003_measures[stringr::str_detect(dir_hyp_003_measures, "population")]

# Load files
## Load grouped measures
## Pivot longer so variable names are identical across measure files
df_hyp_003_measures_groups <- dir_hyp_003_measures_groups %>%
  purrr::map(readr::read_csv) %>%
  purrr::map_dfr(tidyr::pivot_longer,
                 cols = 1,
                 names_to = "group",
                 values_to = "category",
                 values_transform = list(category = as.character))

# Load population measure
# Add variables that are missing compared to grouped measures
df_hyp_003_measures_pop <- readr::read_csv(here::here(dir_hyp_003_measures_pop)) %>%
  dplyr::mutate(group = "population",
                category = "population")

# Join all measures into one object
df_hyp_003_measures <- df_hyp_003_measures_groups %>%
  dplyr::bind_rows(df_hyp_003_measures_pop)

# Write hyp003 csv file
## First create subdirectory (if it doesn't exist)
fs::dir_create(here::here("output", "indicators", "joined", "measures"))

# Round counts to the nearest 10 and recalculate value
df_hyp_003_measures <- df_hyp_003_measures %>%
   dplyr::mutate(dplyr::across(c("hyp003_numerator", "hyp003_denominator", "population"), round, -1)) %>%
   dplyr::mutate(value = hyp003_numerator / hyp003_denominator)

## Next, write csv file
readr::write_csv(df_hyp_003_measures,
                 here::here("output", "indicators", "joined", "measures", "measures_hyp003.csv"))

# INDICATOR HYP_007 ---
# Get file names and path
dir_hyp_007_measures <- fs::dir_ls(path = "output/indicators/joined",
                                   glob = "*measure_hyp007_achievem_*.csv$")

# Split dir paths because file structure differes
## Grouped measures (excluding practice)
dir_hyp_007_measures_groups <- dir_hyp_007_measures[!stringr::str_detect(dir_hyp_007_measures, "population")]
dir_hyp_007_measures_groups <- dir_hyp_007_measures_groups[!stringr::str_detect(dir_hyp_007_measures_groups, "practice")]

## Population measure
dir_hyp_007_measures_pop <- dir_hyp_007_measures[stringr::str_detect(dir_hyp_007_measures, "population")]

# Load files
## Load grouped measures
## Pivot longer so variable names are identical across measure files
df_hyp_007_measures_groups <- dir_hyp_007_measures_groups %>%
  purrr::map(readr::read_csv) %>%
  purrr::map_dfr(tidyr::pivot_longer,
                 cols = 1,
                 names_to = "group",
                 values_to = "category",
                 values_transform = list(category = as.character))

# Load population measure
# Add variables that are missing compared to grouped measures
df_hyp_007_measures_pop <- readr::read_csv(here::here(dir_hyp_007_measures_pop)) %>%
  dplyr::mutate(group = "population",
                category = "population")

# Join all measures into one object
df_hyp_007_measures <- df_hyp_007_measures_groups %>%
  dplyr::bind_rows(df_hyp_007_measures_pop)

# Write hyp007 csv file
## First create subdirectory (if it doesn't exist)
fs::dir_create(here::here("output", "indicators", "joined", "measures"))

# Round counts to the nearest 10 and recalculate value
df_hyp_007_measures <- df_hyp_007_measures %>%
   dplyr::mutate(dplyr::across(c("hyp007_numerator", "hyp007_denominator", "population"), round, -1)) %>%
   dplyr::mutate(value = hyp007_numerator / hyp007_denominator)

## Next, write csv file
readr::write_csv(df_hyp_007_measures,
                 here::here("output", "indicators", "joined", "measures", "measures_hyp007.csv"))

# INDICATOR BP002 with 1y lookback period applied to HYP001 population ---
# Get file names and path
dir_bp_002_hypreg_measures <- fs::dir_ls(path = "output/indicators/joined",
                                   glob = "*measure_bp002_1y_achievem_*.csv$")

# Split dir paths because file structure differes
## Grouped measures (excluding practice)
dir_bp_002_hypreg_measures_groups <- dir_bp_002_hypreg_measures[!stringr::str_detect(dir_bp_002_hypreg_measures, "population")]
dir_bp_002_hypreg_measures_groups <- dir_bp_002_hypreg_measures_groups[!stringr::str_detect(dir_bp_002_hypreg_measures_groups, "practice")]

## Population measure
dir_bp_002_hypreg_measures_pop <- dir_bp_002_hypreg_measures[stringr::str_detect(dir_bp_002_hypreg_measures, "population")]

# Load files
## Load grouped measures
## Pivot longer so variable names are identical across measure files
df_bp_002_hypreg_measures_groups <- dir_bp_002_hypreg_measures_groups %>%
  purrr::map(readr::read_csv) %>%
  purrr::map_dfr(tidyr::pivot_longer,
                 cols = 1,
                 names_to = "group",
                 values_to = "category",
                 values_transform = list(category = as.character))

# Load population measure
# Add variables that are missing compared to grouped measures
df_bp_002_hypreg_measures_pop <- readr::read_csv(here::here(dir_bp_002_hypreg_measures_pop)) %>%
  dplyr::mutate(group = "population",
                category = "population")

# Join all measures into one object
df_bp_002_hypreg_measures <- df_bp_002_hypreg_measures_groups %>%
  dplyr::bind_rows(df_bp_002_hypreg_measures_pop)

# Write hyp007 csv file
## First create subdirectory (if it doesn't exist)
fs::dir_create(here::here("output", "indicators", "joined", "measures"))

# Round counts to the nearest 10 and recalculate value
df_bp_002_hypreg_measures <- df_bp_002_hypreg_measures %>%
   dplyr::mutate(dplyr::across(c("bp002_numerator", "population"), round, -1)) %>%
   dplyr::mutate(value = bp002_numerator / population)

## Next, write csv file
readr::write_csv(df_bp_002_hypreg_measures,
                 here::here("output", "indicators", "joined", "measures", "measures_bp002_1y_hypreg.csv"))
