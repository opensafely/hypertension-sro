# Define common variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

from cohortextractor import patients
from codelists import hyp_codes, hypres_codes

hyp_reg_variables = dict(

  # Hypertension register:
  # Patients with an unresolved diagnosis of hypertension
  hyp=patients.with_these_clinical_events(
    between=["first_day_of_month(index_date) - 5 years",
             "last_day_of_month(index_date)"],
    codelist=hyp_codes,
    returning="binary_flag",
    ),

  hyp_res=patients.with_these_clinical_events(
    between=["first_day_of_month(index_date) - 5 years",
             "last_day_of_month(index_date)"],
    codelist=hypres_codes,
    returning="binary_flag",
    ),

    )
