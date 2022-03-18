# Define common variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

import pandas as pd

from cohortextractor import patients
from codelists import hyp_codes, hypres_codes

hyp_codes_df = pd.read_csv("codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv")
hyp_codes_unique = hyp_codes_df["code"].unique()

# Hypertension register:
# Patients with an unresolved diagnosis of hypertension
hyp_reg_variables = dict(
    registered=patients.registered_as_of(
        "index_date",
        return_expectations={"incidence": 0.9},
    ),
    hypertension=patients.with_these_clinical_events(
        on_or_before="first_day_of_month(index_date)",
        codelist=hyp_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Hypertension resolved binary
    hypertension_resolved=patients.with_these_clinical_events(
        on_or_before="first_day_of_month(index_date)",
        codelist=hypres_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    hyp001_indicator=patients.satisfying(
        """
    hypertension AND
    (NOT hypertension_resolved)
    """
    ),
)

hyp_ind_variables = dict(
    # Rules for indicators HYP003 and HYP007
    # The only differences between the indicators are:
    # - Age (Denominator rule 1)
    #   - HYP003: >79
    #   - HYP007: <80
    # - Values of last blood pressure (Denominator rules 2, 7)
    #   - HYP003: SYS <= 140, DIA <= 90
    #   - HYP007: SYS <= 150, DIA <= 90
    # Denominator
    # Rule 1
    # Age is defined in demographic_variables
    # Rule 2
    # TODO
    # Rule 3
    # TODO
    # Rule 4
    # TODO
    # Rule 5
    # TODO
    # Rule 6
    # TODO
    # Rule 7
    # TODO
    # Rule 8
    # TODO
    # Rule 9
    # TODO
    # Numerator
    # Rule 1
    # TODO
)
