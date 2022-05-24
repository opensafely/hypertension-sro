# Load pacakges
library(arrow)
library(here)
library(dplyr)
library(tidyr)
library(lubridate)
library(ggplot2)
library(magrittr)
library(readr)

# Create dir (if it doesnt exist)
fs::dir_create(here("output", "indicators", "joined", "data_check"))

# Import data
## Indicator hyp003 and hyp007
## Date: 2019-01-01
df_hyp003_2019_01_01 <- read_feather(here("output/indicators/joined/input_hyp003_2019-01-01.feather"))
df_hyp007_2019_01_01 <- read_feather(here("output/indicators/joined/input_hyp007_2019-01-01.feather"))

# Select variables
df_hyp003_2019_01_01 <- df_hyp003_2019_01_01 %>%
  select(patient_id,
         hyp003_numerator,
         hyp003_denominator,
         bp_sys_val_12m_date_measured,
         bp_dia_val_12m_date_measured,
         bp_sys_val_12m,
         bp_dia_val_12m)

df_hyp007_2019_01_01 <- df_hyp007_2019_01_01 %>%
  select(patient_id,
         hyp007_numerator,
         hyp007_denominator,
         bp_sys_val_12m_date_measured,
         bp_dia_val_12m_date_measured,
         bp_sys_val_12m,
         bp_dia_val_12m)

# Count available bp recordings for sys and dia readings in numerator

# Numerator
tab_hyp003_num_2019_01_01 <- df_hyp003_2019_01_01 %>%
  filter(hyp003_numerator == TRUE) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording) %>%
  group_by(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = n / sum(n))

tab_hyp007_num_2019_01_01 <- df_hyp007_2019_01_01 %>%
  filter(hyp007_numerator == TRUE) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording) %>%
  group_by(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = n / sum(n))

# Write csv with counts
write_csv(tab_hyp003_num_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_num_2019_01_01.csv"))
write_csv(tab_hyp007_num_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp007_num_2019_01_01.csv"))

# Count available bp recordings for sys and dia readings in denominator
tab_hyp003_den_2019_01_01 <- df_hyp003_2019_01_01 %>%
  filter(hyp003_denominator == TRUE) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording) %>%
  group_by(sys_date_recording, dia_date_recording,
           sys_value_recording, dia_value_recording) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = n / sum(n))

tab_hyp007_den_2019_01_01 <- df_hyp007_2019_01_01 %>%
  filter(hyp007_denominator == TRUE) %>%
  mutate(sys_date_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_date_recording = !is.na(bp_dia_val_12m_date_measured),
         sys_value_recording = !is.na(bp_sys_val_12m),
         dia_value_recording = !is.na(bp_dia_val_12m)) %>%
  select(sys_date_recording, dia_date_recording,
         sys_value_recording, dia_value_recording) %>%
  group_by(sys_date_recording, dia_date_recording,
           sys_value_recording, dia_value_recording) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = n / sum(n))

# Write csv with counts
write_csv(tab_hyp003_den_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_den_2019_01_01.csv"))
write_csv(tab_hyp007_den_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp007_den_2019_01_01.csv"))


# Calculate absolute diff (in days) between systolic and diastolic bp readings
df_hyp003_num_bp_date_diff_2019_01_01 <- df_hyp003_2019_01_01 %>%
  filter(hyp003_numerator == TRUE) %>%
  mutate(bp_date_diff = abs(as.duration(bp_sys_val_12m_date_measured - bp_dia_val_12m_date_measured) / ddays()))

tab_hyp003_num_bp_date_diff_2019_01_01 <- df_hyp003_num_bp_date_diff_2019_01_01 %>%
  mutate(diff_weeks = case_when(bp_date_diff <= 7 ~ "1 week",
                                bp_date_diff <= 30 ~ "1 month",
                                bp_date_diff > 30 ~ "more than 1 month")) %>%
  count(diff_weeks) %>%
  mutate(pct = n / sum(n))

df_hyp007_num_bp_date_diff_2019_01_01 <- df_hyp007_2019_01_01 %>%
  filter(hyp007_numerator == TRUE) %>%
  mutate(bp_date_diff = abs(as.duration(bp_sys_val_12m_date_measured - bp_dia_val_12m_date_measured) / ddays()))

tab_hyp007_num_bp_date_diff_2019_01_01 <- df_hyp007_num_bp_date_diff_2019_01_01 %>%
  mutate(diff_weeks = case_when(bp_date_diff <= 7 ~ "1 week",
                                bp_date_diff <= 30 ~ "1 month",
                                bp_date_diff > 30 ~ "more than 1 month")) %>%
  count(diff_weeks) %>%
  mutate(pct = n / sum(n))

# Write csv with counts and pct
write_csv(tab_hyp003_num_bp_date_diff_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_num_bp_date_diff_2019_01_01.csv"))
write_csv(tab_hyp007_num_bp_date_diff_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp007_num_bp_date_diff_2019_01_01.csv"))


plot_hyp003_num_bp_date_diff_2019_01_01 <- df_hyp003_num_bp_date_diff_2019_01_01 %>%
  ggplot(aes(bp_date_diff)) +
  labs(x = "Absolute difference in days between systolic and diastolic blood pressure readings",
       y = "Count of patients in HYP003 numerator") +
  geom_histogram() +
  ggplot2::scale_y_continuous(labels = scales::label_comma())

plot_hyp007_num_bp_date_diff_2019_01_01 <- df_hyp007_num_bp_date_diff_2019_01_01 %>%
  ggplot(aes(bp_date_diff)) +
  labs(x = "Absolute difference in days between systolic and diastolic blood pressure readings",
       y = "Count of patients in HYP003 numerator") +
  geom_histogram() +
  ggplot2::scale_y_continuous(labels = scales::label_comma())

# Save plot
ggsave(here("output", "indicators", "joined", "data_check", "plot_hyp003_num_bp_date_diff_2019_01_01.png"),
       plot = plot_hyp003_num_bp_date_diff_2019_01_01)

ggsave(here("output", "indicators", "joined", "data_check", "plot_hyp007_num_bp_date_diff_2019_01_01.png"),
       plot = plot_hyp007_num_bp_date_diff_2019_01_01)

