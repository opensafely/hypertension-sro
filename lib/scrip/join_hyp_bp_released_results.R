library(readr)
library(dplyr)
library(here)
library(tindicatoryr)
library(stringr)

# Deciles tables ----
## Read csv
df_defiles_hyp <- read_csv(here("released_outputs/deciles/deciles_hyp_practice.csv")) |>
  rename(indicator = id)

df_defiles_bp <- read_csv(here("released_outputs/deciles/deciles_table_bp002_achievem_practice_rate.csv")) |>
  mutate(indicator = "bp002") |>
  relocate(indicator)

# Join csv
df_defiles_bp_hyp <- df_defiles_hyp |>
  bind_rows(df_defiles_bp)

# Write csv
write_csv(df_defiles_bp_hyp, here("released_outputs/deciles/deciles_bp_hyp_practice.csv"))

# Measures files ----
## Read individual measures files
df_measures_bp002 <- read_csv(here("released_outputs/measures/measures_bp002_achievem.csv"))
df_measures_hyp001 <- read_csv(here("released_outputs/measures/measures_hyp001.csv"))
df_measures_hyp003 <- read_csv(here("released_outputs/measures/measures_hyp003.csv"))
df_measures_hyp007 <- read_csv(here("released_outputs/measures/measures_hyp007.csv"))

# Read all measures files and pivot into indicatorentical structure
df_measures_bp002_long <- df_measures_bp002 |>
  pivot_longer(cols = c(bp002_numerator, bp002_denominator, population),
               values_to = "count", names_to = "variable") |>
  mutate(indicator = "bp002",
         variable = str_remove(variable, "bp002_")) |>
  rename(pct = value) |>
  relocate(indicator, date, variable, group, category, count)

df_measures_hyp001_long <- df_measures_hyp001 |>
  pivot_longer(cols = c(hyp_reg, population),
               values_to = "count", names_to = "variable") |>
  mutate(indicator = "hyp001",
         variable = case_when(variable == "hyp_reg" ~ "register",
                              TRUE ~ variable)) |>
  rename(pct = value) |>
  relocate(indicator, date, variable, group, category, count)

df_measures_hyp003_long <- df_measures_hyp003 |>
  pivot_longer(cols = c(hyp003_numerator, hyp003_denominator, population),
               values_to = "count", names_to = "variable") |>
  mutate(indicator = "hyp003",
         variable = str_remove(variable, "hyp003_")) |>
  rename(pct = value) |>
  relocate(indicator, date, variable, group, category, count)

df_measures_hyp007_long <- df_measures_hyp007 |>
  pivot_longer(cols = c(hyp007_numerator, hyp007_denominator, population),
               values_to = "count", names_to = "variable") |>
  mutate(indicator = "hyp007",
         variable = str_remove(variable, "hyp007_")) |>
  rename(pct = value) |>
  relocate(indicator, date, variable, group, category, count)

# Join measures files
df_measures_bp_hyp <- df_measures_bp002_long |>
 bind_rows(df_measures_hyp001_long,
           df_measures_hyp003_long,
           df_measures_hyp007_long)

# Write measures files
write_csv(df_measures_bp_hyp, here("released_outputs/measures/df_measures_bp_hyp.csv"))
