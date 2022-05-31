# Study start date
# Note: This should match the start dates in project.yaml
# In QOF also: Payment Period Start Date (PPSD)
start_date = "2020-03-01"

# Study end date
# Note: This should match the end dates in project.yaml
# In QOF also: Payment Period End Date (PPED)
end_date = "2020-05-01"
 
# Demographic variables by which measures are broken down
demographic_breakdowns = [
    "age_band",
    "sex",
    "region",
    "care_home",
    "learning_disability",
    "imd",
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
