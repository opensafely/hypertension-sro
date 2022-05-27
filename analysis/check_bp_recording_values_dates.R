# Load pacakges
library(arrow)
library(here)
library(dplyr)
library(tidyr)
library(lubridate)
library(ggplot2)
library(magrittr)
library(readr)
library(skimr)

# Create dir (if it doesnt exist)
fs::dir_create(here("output", "indicators", "joined", "data_check"))

# Import data
## Indicator hyp003 and hyp007
## Date: 2021-03-01
df_hyp003_2021_03_01 <- read_feather(here("output/indicators/joined/input_hyp003_2021-03-01.feather"))
df_hyp007_2021_03_01 <- read_feather(here("output/indicators/joined/input_hyp007_2021-03-01.feather"))

# Select variables
df_hyp003_2021_03_01 <- df_hyp003_2021_03_01 %>%
  select(hyp003_numerator,
         hyp003_denominator,
         bp_sys_val_12m_date_measured,
         bp_dia_val_12m_date_measured,
         bp_sys_val_12m,
         bp_dia_val_12m,
         valid_bp_sys_dia_values)

capture.output(
  skimr::skim_without_charts(df_hyp003_2021_03_01 %>% filter(valid_bp_sys_dia_values)),
  file = here("output", "indicators", "joined", "data_check", "skim_df_hyp003_2021_03_01.txt"),
  split = FALSE)

df_hyp007_2021_03_01 <- df_hyp007_2021_03_01 %>%
  select(hyp007_numerator,
         hyp007_denominator,
         bp_sys_val_12m_date_measured,
         bp_dia_val_12m_date_measured,
         bp_sys_val_12m,
         bp_dia_val_12m,
         valid_bp_sys_dia_values)

capture.output(
  skimr::skim_without_charts(df_hyp003_2021_03_01 %>% filter(valid_bp_sys_dia_values)),
  file = here("output", "indicators", "joined", "data_check", "skim_df_hyp007_2021_03_01.txt"),
  split = FALSE)

# Count available bp recordings for sys and dia readings in numerator

# Numerator
tab_hyp003_num_2021_03_01 <- df_hyp003_2021_03_01 %>%
  filter(hyp003_numerator) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording,
         valid_bp_sys_dia_values) %>%
  group_by(sys_date_recording, dia_date_recording,
           sys_value_recording, dia_value_recording,
           valid_bp_sys_dia_values) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = round(n / sum(n), 4))

tab_hyp007_num_2021_03_01 <- df_hyp007_2021_03_01 %>%
  filter(hyp007_numerator) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording,
         valid_bp_sys_dia_values) %>%
  group_by(sys_date_recording, dia_date_recording,
           sys_value_recording, dia_value_recording,
           valid_bp_sys_dia_values) %>%

  count() %>%
  ungroup() %>%
  mutate(pct = round(n / sum(n), 4))

# Write csv with counts
write_csv(tab_hyp003_num_2021_03_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_num_2021_03_01.csv"))
write_csv(tab_hyp007_num_2021_03_01, here("output", "indicators", "joined", "data_check", "tab_hyp007_num_2021_03_01.csv"))

# Count available bp recordings for sys and dia readings in denominator
tab_hyp003_den_2021_03_01 <- df_hyp003_2021_03_01 %>%
  filter(hyp003_denominator) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording,
          valid_bp_sys_dia_values) %>%
  group_by(sys_date_recording, dia_date_recording,
           sys_value_recording, dia_value_recording,
           valid_bp_sys_dia_values) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = round(n / sum(n), 4))

tab_hyp007_den_2021_03_01 <- df_hyp007_2021_03_01 %>%
  filter(hyp007_denominator) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording,
         valid_bp_sys_dia_values) %>%
  group_by(sys_date_recording, dia_date_recording,
           sys_value_recording, dia_value_recording,
           valid_bp_sys_dia_values) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = round(n / sum(n), 4))

# Write csv with counts
write_csv(tab_hyp003_den_2021_03_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_den_2021_03_01.csv"))
write_csv(tab_hyp007_den_2021_03_01, here("output", "indicators", "joined", "data_check", "tab_hyp007_den_2021_03_01.csv"))

# Calculate absolute diff (in days) between systolic and diastolic bp readings
df_hyp003_num_bp_date_diff_2021_03_01 <- df_hyp003_2021_03_01 %>%
  filter(hyp003_numerator) %>%
  mutate(bp_date_diff = abs(as.duration(bp_sys_val_12m_date_measured - bp_dia_val_12m_date_measured) / ddays()))

tab_hyp003_num_bp_date_diff_2020_05_01 <- df_hyp003_num_bp_date_diff_2020_05_01 %>%
  mutate(diff_weeks = case_when(bp_date_diff == 0 ~ "same day",
                                bp_date_diff > 0 & bp_date_diff <= 7 ~ "within 2 to 7 days",
                                bp_date_diff > 7 ~ "more than 1 week")) %>%
  count(diff_weeks) %>%
  mutate(pct = round(n / sum(n), 4))

df_hyp007_num_bp_date_diff_2021_03_01 <- df_hyp007_2021_03_01 %>%
  filter(hyp007_numerator) %>%
  mutate(bp_date_diff = abs(as.duration(bp_sys_val_12m_date_measured - bp_dia_val_12m_date_measured) / ddays()))

tab_hyp007_num_bp_date_diff_2020_05_01 <- df_hyp007_num_bp_date_diff_2020_05_01 %>%
  mutate(diff_weeks = case_when(bp_date_diff == 0 ~ "same day",
                                bp_date_diff > 0 & bp_date_diff <= 7 ~ "within 2 to 7 days",
                                bp_date_diff > 7 ~ "more than 1 week")) %>%
  count(diff_weeks) %>%
  mutate(pct = round(n / sum(n), 4))

# Write csv with counts and pct
write_csv(tab_hyp003_num_bp_date_diff_2021_03_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_num_bp_date_diff_2021_03_01.csv"))
write_csv(tab_hyp007_num_bp_date_diff_2021_03_01, here("output", "indicators", "joined", "data_check", "tab_hyp007_num_bp_date_diff_2021_03_01.csv"))


plot_hyp003_num_bp_date_diff_2021_03_01 <- df_hyp003_num_bp_date_diff_2021_03_01 %>%
  ggplot(aes(bp_date_diff)) +
  labs(x = "Absolute difference in days between systolic and diastolic blood pressure readings",
       y = "Count of patients in HYP003 numerator") +
  geom_histogram() +
  ggplot2::scale_y_continuous(labels = scales::label_comma())

plot_hyp007_num_bp_date_diff_2021_03_01 <- df_hyp007_num_bp_date_diff_2021_03_01 %>%
  ggplot(aes(bp_date_diff)) +
  labs(x = "Absolute difference in days between systolic and diastolic blood pressure readings",
       y = "Count of patients in HYP003 numerator") +
  geom_histogram() +
  ggplot2::scale_y_continuous(labels = scales::label_comma())

# Save plot
ggsave(here("output", "indicators", "joined", "data_check", "plot_hyp003_num_bp_date_diff_2021_03_01.png"),
       plot = plot_hyp003_num_bp_date_diff_2021_03_01)

ggsave(here("output", "indicators", "joined", "data_check", "plot_hyp007_num_bp_date_diff_2021_03_01.png"),
       plot = plot_hyp007_num_bp_date_diff_2021_03_01)

