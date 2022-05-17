
library(arrow)
library(here)
library(dplyr)
library(tidyr)
library(lubridate)
library(ggplot2)
library(magrittr)
library(readr)

df_hyp003_2019_01_01 <- read_feather(here("output/indicators/input_hyp003_2019-01-01.feather"))
df_hyp007_2019_01_01 <- read_feather(here("output/indicators/input_hyp003_2019-01-01.feather"))

df_hyp003_2019_01_01 <- df_hyp003_2019_01_01 %>%
  select(patient_id, bp_sys_val_12m_date_measured,
         bp_dia_val_12m_date_measured,
         bp_sys_val_12m,
         bp_dia_val_12m)

tab_hyp003_2019_01_01 <- df_hyp003_2019_01_01 %>%
  mutate(sys_recording = !is.na(bp_sys_val_12m_date_measured),
         dia_recording = !is.na(bp_dia_val_12m_date_measured)) %>%
  select(patient_id, sys_recording, dia_recording) %>%
  pivot_longer(cols = c(sys_recording, dia_recording)) %>%
  group_by(name) |>
  count(available = value == TRUE)

fs::dir_create(here("output", "indicators", "joined", "data_check"))
write_csv(tab_hyp003_2019_01_01, here("output", "indicators", "joined", "data_check", "tab_hyp003_2019_01_01.csv"))

bp_date_diff_2019_01_01 <- df_hyp003_2019_01_01 %>%
  mutate(bp_date_diff = as.duration(bp_sys_val_12m_date_measured - bp_dia_val_12m_date_measured)) %>%
  ggplot(aes(bp_date_diff)) +
  geom_histogram() +
  scale_x_time()

ggsave(here("output", "indicators", "joined", "data_check", "bp_date_diff_2019_01_01.png"), plot = bp_date_diff_2019_01_01)
