# Define common variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

import pandas as pd
from config import start_date, end_date
from cohortextractor import patients
from codelists import (
    hyp_codes,
    hyp_res_codes,
    bp_sys_codes,
    bp_dia_codes,
    ht_max_codes,
    hyp_pca_pu_codes,
    hyp_pca_dec_codes,
    bp_dec_codes,
    hyp_invite_codes,
)

# Define unique list of hypertension codes to set expectations in dummy data
hyp_codes_path = "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv"
hyp_codes_df = pd.read_csv(hyp_codes_path)
hyp_codes_unique = hyp_codes_df["code"].unique()

# Define dictionary of variables needed for hypertension register:
# Patients with an unresolved diagnosis of hypertension
hyp_reg_variables = dict(
    registered=patients.registered_as_of(
        "index_date",
        return_expectations={"incidence": 0.9},
    ),
    # Define variables for hypertension (binary) and associated date
    # HYPLAT_DAT (hypertension_date): Date of the most recent hypertension
    # diagnosis up to and including the achievement date.
    # Note that this is the same variable description as:
    # HYP_DAT (hypertension_date): Date of the first hypertension
    # diagnosis up to and including the achievement date.
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
        codelist=hyp_res_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Define hypertension register
    # REG_DAT (hypertension_register_date): The most recent date that the
    # patient registered for GMS, where this registration occurred on or
    # before the achievement date
    hypertension_register=patients.satisfying(
        """
        # Select patients from the specified population who have a diagnosis
        # of hypertension which has not been subsequently resolved.
        (hypertension AND (NOT hypertension_resolved)) OR
        (hypertension_resolved_date <= hypertension_date)
        """
    ),
)
# Rules for indicators HYP003 and HYP007
hyp_ind_variables = dict(
    # PAT_AGE (age): The age of the patient in full years at the achievement
    # date. Note that this variable is defined in:
    # "analysis/dict_demo_variables.py".
    #
    # BPSYS_VAL: The systolic blood pressure values associated
    # with each date in the BPSYS_DAT array.
    bp_sys_val_12m=patients.mean_recorded_value(
        bp_sys_codes,
        on_most_recent_day_of_measurement=True,
        include_measurement_date=True,
        between=[
            "first_day_of_month(index_date) - 12 months",
            "last_day_of_month(index_date)",
        ],
        date_format="YYYY-MM-DD",
        return_expectations={
            "incidence": 0.8,
            "float": {"distribution": "normal", "mean": 110, "stddev": 20},
            "date": {"earliest": "index_date", "latest": "index_date + 1 year"},
            "rate": "uniform",
        },
    ),
    # BP_DAT: Date of the most recent blood
    # pressure reading with a systolic and diastolic value, up to and
    # including the achievement date.
    # Variable extracted above: bp_sys_val_12m_date_measured

    # BPDIA_VAL: The diastolic blood pressure values associated
    # with each date in the BPSYS_DAT array.
    bp_dia_val_12m=patients.mean_recorded_value(
        bp_dia_codes,
        on_most_recent_day_of_measurement=True,
        include_measurement_date=True,
        between=[
            "first_day_of_month(index_date) - 12 months",
            "last_day_of_month(index_date)",
        ],
        date_format="YYYY-MM-DD",
        return_expectations={
            "incidence": 0.8,
            "float": {"distribution": "normal", "mean": 70, "stddev": 20},
            "date": {"earliest": "index_date", "latest": "index_date + 1 year"},
            "rate": "uniform",
        },
    ),
    # BP_DAT: Date of the most recent blood
    # pressure reading with a systolic and diastolic value, up to and
    # including the achievement date.
    # Variable extracted above: bp_dia_val_12m_date_measured

    # PPED: Payment Period End Date. The last day of each period
    # for which payments are made for the Quality Service.
    # Note that this date gets defined in 'analysis/config.py'.
    #
    # HTMAX_DAT (ht_max_date): Date of the most recent maximal blood pressure
    # therapy code recorded up to and including the achievement date.
    ht_max_12m=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 12 months",
            "last_day_of_month(index_date)",
        ],
        codelist=ht_max_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # HYPPCAPU_DAT: Most recent date that hypertension
    # quality indicator care was deemed unsuitable for the patient up to and
    # including the achievement date.
    hyp_pca_pu_12m=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 12 months",
            "last_day_of_month(index_date)",
        ],
        codelist=hyp_pca_pu_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # BPDEC_DAT: Codes indicating the patient has chosen
    # not to have blood pressure procedure.
    bp_dec_12m=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 12 months",
            "last_day_of_month(index_date)",
        ],
        codelist=bp_dec_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # HYPPCADEC_DAT: Date the patient most recently chose
    # not receive hypertension quality indicator care up to and including
    # the achievement date.
    hyp_pca_dec_12m=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 12 months",
            "last_day_of_month(index_date)",
        ],
        codelist=hyp_pca_dec_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # HYPINVITE1_DAT: Date of the earliest invitation for a hypertension care
    # review on or after the quality service start date and up to and
    # including the achievement date.
    # Note that the hyp_invite_1_date variable gets defined here
    #
    # TODO: Note that the between argument should start with the 'start_date'
    # TODO: The current implementation looks back 12 months but we might need
    # TODO: to come up with a better approach
    hyp_invite_1=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 11 months",
            "last_day_of_month(index_date)"
            ],
        codelist=hyp_invite_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),

    # HYPINVITE2_DAT: Date of the earliest invite for a hypertension care
    # review recorded at least 7 days after the first invitation and up to
    # and including the achievement date.
    # TODO: Not sure if this is needed for us, need to check
    #
    # Variable for denominator rule 8
    hypertension_9m=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 9 months",
            "last_day_of_month(index_date)",
        ],
        codelist=hyp_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Reject patients passed to this rule who were recently registered at the
    # practice (patient registered in the 9 month period leading up to and
    # including the payment period end date).
    registered_9m=patients.registered_with_one_practice_between(
        start_date="first_day_of_month(index_date) - 9 months",
        end_date="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.1}
        )
    )
