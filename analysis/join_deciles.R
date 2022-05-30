# This scrip loads all deciles files and
# (1) joins them together (separate files for each indicator)

# Load packages ----
library(magrittr)
library(dplyr)
library(tidyr)
library(here)
library(readr)
library(fs)
library(purrr)
library(stringr)

# Get file names and path
dir_hyp_deciles_practice <- fs::dir_ls(path = "output/indicators/joined",
                                       glob = "*deciles_table_hyp*_*_practice_rate.csv$")


# Load files
## Load grouped measures
## Bind rows of all deciles files
## Extract indicator shortcut from file name
df_hyp_deciles_practice <- dir_hyp_deciles_practice %>%
  purrr::map(readr::read_csv, id = "id") %>%
  purrr::map_dfr(dplyr::bind_rows) %>%
  mutate(id = str_extract(id, "hyp\\d+"))

fs::dir_create(here::here("output", "indicators", "joined", "deciles"))

## Next, write csv file
readr::write_csv(df_hyp_deciles_practice,
                 here::here("output", "indicators", "joined", "deciles", "deciles_hyp_practice.csv"))
