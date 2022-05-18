# Load pacakges
library(arrow)
library(here)
library(dplyr)
library(tidyr)
library(lubridate)
library(ggplot2)
library(magrittr)
library(readr)

# Import data 
## Indicator hyp003
## Date: 2019-01-01
df_hyp003_2019_01_01 <- read_feather(here("output/indicators/joined/input_hyp003_2019-01-01.feather"))

# Select variables
df_hyp003_2019_01_01 <- df_hyp003_2019_01_01 %>%
  select(patient_id,
         hyp003_numerator,
         bp_sys_val_12m_date_measured,
         bp_dia_val_12m_date_measured,
         bp_sys_val_12m,
         bp_dia_val_12m)

# Count available bp recordings for sys and dia readings in numerator
tab_hyp003_2019_01_01 <- df_hyp003_2019_01_01 %>%
  filter(hyp003_numerator == TRUE) %>%
  mutate(sys_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_recording = !is.na(bp_dia_val_12m_date_measured)) %>%
  select(sys_recording, dia_recording) %>%
  group_by(sys_recording, dia_recording) %>%
  count() %>%
  ungroup() %>%
  mutate(pct = n / sum(n))

# Create dir (if it doesnt exist)
fs::dir_create(here("output", "indicators", "joined", "data_check"))

# Write csv with counts
write_csv(tab_hyp003_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_2019_01_01.csv"))

# Calculate absolute diff (in days) between systolic and diastolic bp readings
df_bp_date_diff_2019_01_01 <- df_hyp003_2019_01_01 %>%
  mutate(bp_date_diff = abs(as.duration(bp_sys_val_12m_date_measured - bp_dia_val_12m_date_measured) / ddays()))

tab_bp_date_diff_2019_01_01 <- df_bp_date_diff_2019_01_01 %>%
  mutate(diff_weeks = case_when(bp_date_diff <= 7 ~ "1 week",
                                bp_date_diff <= 30 ~ "1 month",
                                bp_date_diff > 30 ~ "more than 1 month")) %>%
  count(diff_weeks) %>%
  mutate(pct = n / sum(n))

# Write csv with counts and pct
write_csv(tab_bp_date_diff_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_bp_date_diff_2019_01_01.csv"))


plot_bp_date_diff_2019_01_01 <- df_bp_date_diff_2019_01_01 %>%
  ggplot(aes(bp_date_diff)) +
  labs(x = "Absolute difference in days between systolic and diastolic blood pressure readings") +
  geom_histogram()

# Save plot
ggsave(here("output", "indicators", "joined", "data_check", "bp_date_diff_2019_01_01.png"),
       plot = plot_bp_date_diff_2019_01_01)
