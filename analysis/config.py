# Study start date
# Note: This should match the start dates in project.yaml
# In QOF also: Payment Period Start Date (PPSD)
start_date = "2019-03-01"

# Study end date
# Note: This should match the end dates in project.yaml
# In QOF also: Payment Period End Date (PPED)
end_date = "2022-04-01"

# Demographic variables by which measures are broken down
demographic_breakdowns = [
    "age_band",
    "sex",
    "region",
    "care_home",
    "learning_disability",
    "imd_q5",
    "ethnicity",
]

# Define list of rules with exclusion (reject) criteria
hyp_exclusions = [
    "denominator_r1",
    "denominator_r3",
    "denominator_r4",
    "denominator_r5",
    "denominator_r6",
    "denominator_r7",
    "denominator_r8",
    "denominator_r9",
]

hyp_flowchart = [
    "denominator_r1_reject",
    "denominator_r2_select",
    "denominator_r3_reject",
    "denominator_r4_reject",
    "denominator_r5_reject",
    "denominator_r6_reject",
    "denominator_r7_reject",
    "denominator_r8_reject",
    "denominator_r9_reject",
]

# Define list of variables for checking data quality
hyp_data_check = [
    "bp_sys_dia_min_cutoff",
    "bp_sys_dia_max_cutoff",
    "bp_sys_dia_date_missing",
    "bp_sys_dia_date_available",
    "bp_sys_dia_date_equal",
]
