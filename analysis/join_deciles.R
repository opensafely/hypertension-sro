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


df_hyp001_deciles <- read_csv("output/indicators/joined/deciles_table_hyp001_prevalence_practice_breakdown_rate.csv") %>%
  mutate(indicator = "hyp001")

df_hyp003_deciles <- read_csv("output/indicators/joined/deciles_table_hyp003_achievem_practice_breakdown_rate.csv") %>%
  mutate(indicator = "hyp007")

df_hyp007_deciles <- read_csv("output/indicators/joined/deciles_table_hyp007_achievem_practice_breakdown_rate.csv") %>%
  mutate(indicator = "hyp007")

df_hyp_deciles_practice <- bind_rows(df_hyp001_deciles, df_hyp003_deciles, df_hyp007_deciles) %>%
  relocate(indicator)

fs::dir_create(here::here("output", "indicators", "joined", "deciles"))

## Next, write csv file
readr::write_csv(df_hyp_deciles_practice,
                 here::here("output", "indicators", "joined", "deciles", "deciles_hyp_practice.csv"))
