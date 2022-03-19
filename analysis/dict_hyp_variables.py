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
    # Define variables for hypertension (binary) and associated date
    # HYPLAT_DAT: Date of the most recent hypertension diagnosis up to and
    # including the achievement date.
    hypertension=patients.with_these_clinical_events(
        on_or_before="last_day_of_month(index_date)",
        codelist=hyp_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Define variables for resolved hypertension (binary) and associated date
    # HYPRES_DAT: Date of the most recent hypertension resolved code recorded
    # after the most recent hypertension diagnosis and up to and including
    # the achievement date.
    hypertension_resolved=patients.with_these_clinical_events(
        on_or_before="last_day_of_month(index_date)",
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

    # PAT_AGE: The age of the patient in full years at the achievement date.
    # TODO

    # BPSYS_VAL: The systolic blood pressure values associated with each
    # date in the BPSYS_DAT array.
    # TODO

    # BPDIA_VAL: The diastolic blood pressure values associated with each
    # date in the BPSYS_DAT array.
    # TODO

    # BP_DAT: Date of the most recent blood pressure reading with a systolic
    # and diastolic value, up to and including the achievement date.
    # TODO

    # PPED: Payment Period End Date. The last day of each period for which
    # payments are made for the Quality Service.
    # TODO

    # HTMAX_DAT: Date of the most recent maximal blood pressure therapy code
    # recorded up to and including the achievement date.
    # TODO

    # HYPPCAPU_DAT: Most recent date that hypertension quality indicator care
    # was deemed unsuitable for the patient up to and including the
    # achievement date.
    # TODO

    # BPDEC_DAT: Codes indicating the patient has chosen not to have blood
    # pressure procedure.
    # TODO

    # HYPPCADEC_DAT: Date the patient most recently chose not receive
    # hypertension quality indicator care up to and including the achievement
    # date.
    # TODO

    # HYPINVITE1_DAT: Date of the earliest invitation for a hypertension care
    # review on or after the quality service start date and up to and
    # including the achievement date.
    # TODO

    # HYPINVITE2_DAT: Date of the earliest invite for a hypertension care
    # review recorded at least 7 days after the first invitation and up to
    # and including the achievement date.
    # TODO

    # HYP_DAT: Date of the first hypertension diagnosis up to and including
    # the achievement date.
    # TODO

    # REG_DAT: The most recent date that the patient registered for GMS,
    # where this registration occurred on or before the achievement date
    # TODO

)