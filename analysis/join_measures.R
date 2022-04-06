# This scrip loads all measure files and joins them together
# Note that the ungrouped measure (population) and grouped measures
# differ in the number of their variables

# Load packages ----
library(ggplot2)
library(magrittr)
library(dplyr)
library(tidyr)
library(here)
library(readr)
library(fs)
library(purrr)
library(stringr)

# Get file names and path ----
dir_hyp_001_measures <- fs::dir_ls(path = "output/indicators/joined",
                                   glob = "*hyp001*.csv$")

# Split dir paths because file structure differes
## Grouped measures
dir_hyp_001_measures_groups <- dir_hyp_001_measures[!stringr::str_detect(dir_hyp_001_measures, "population")]
## Population measure
dir_hyp_001_measures_pop <- dir_hyp_001_measures[stringr::str_detect(dir_hyp_001_measures, "population")]

# Load files ----
## Load grouped measures
## Pivot longer so variable names are identical across measure files
df_hyp_001_measures_groups <- dir_hyp_001_measures_groups %>%
  purrr::map(readr::read_csv) %>%
  purrr::map_dfr(tidyr::pivot_longer,
                 cols = 1,
                 names_to = "group",
                 values_to = "category",
                 values_transform = list(category = as.character))

# Load population measure ---
# Add variables that are missing compared to grouped measures
df_hyp_001_measures_pop <- readr::read_csv(here::here(dir_hyp_001_measures_pop)) %>%
  dplyr::mutate(group = "population",
                category = "population")

# Join all measures into one object ---
df_hyp_001_measures <- df_hyp_001_measures_groups %>%
  dplyr::bind_rows(df_hyp_001_measures_pop)

# Write hyp001 csv file
## First create subdirectory (if it doesn't exist)
fs::dir_create(here::here("output", "measures"))

## Next, write csv file
readr::write_csv(df_hyp_001_measures,
                 here::here("output", "measures", "measures_hyp001.csv"))
