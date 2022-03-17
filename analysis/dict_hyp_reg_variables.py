# Define common variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

import pandas as pd

from cohortextractor import patients
from codelists import hyp_codes, hypres_codes

hyp_codes_df = pd.read_csv("codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv")
hyp_codes_unique = hyp_codes_df['code'].unique()

# Hypertension register:
# Patients with an unresolved diagnosis of hypertension

hyp_reg_variables = dict(

  registered=patients.registered_as_of(
     "index_date",
     return_expectations={"incidence": 0.9},
     ),

  hyp=patients.with_these_clinical_events(
    between=["first_day_of_month(index_date) - 110 years",
             "last_day_of_month(index_date)"],
    codelist=hyp_codes,
    returning="binary_flag",
    ),

  # Also return hyp codes
  hyp_code=patients.with_these_clinical_events(
    between=["first_day_of_month(index_date) - 110 years",
             "last_day_of_month(index_date)"],
    codelist=hyp_codes,
    returning="code",
    return_expectations={"category": {
      "ratios": {x: 1/len(hyp_codes_unique) for x in hyp_codes_unique}}, }
    ),

  # Hypertension resolved binary
  hyp_res=patients.with_these_clinical_events(
    between=["first_day_of_month(index_date) - 110 years",
             "last_day_of_month(index_date)"],
    codelist=hypres_codes,
    returning="binary_flag",
    ),

    )
