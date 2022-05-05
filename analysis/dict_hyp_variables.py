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
    # HYPLAT_DAT (hyp_lat_date): Date of the most recent hypertension
    # diagnosis up to and including the achievement date.
    hyp_lat=patients.with_these_clinical_events(
        on_or_before="last_day_of_month(index_date)",
        codelist=hyp_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # HYP_DAT: Date of the first hypertension
    # diagnosis up to and including the achievement date.
    hyp=patients.with_these_clinical_events(
        on_or_before="last_day_of_month(index_date)",
        codelist=hyp_codes,
        returning="binary_flag",
        find_first_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # HYPRES_DAT: Date of the most recent hypertension resolved code recorded
    # after the most recent hypertension diagnosis and up to and including
    # the achievement date.
    hyp_res=patients.with_these_clinical_events(
        on_or_before="last_day_of_month(index_date)",
        codelist=hyp_res_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Define hypertension register
    hyp_reg=patients.satisfying(
        """
        # Select patients from the specified population who have a diagnosis
        # of hypertension which has not been subsequently resolved.
        (hyp AND (NOT hyp_res)) OR
        (
            (hyp AND hyp_res) AND
            (hyp_res_date <= hyp_lat_date)
        )
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
            "first_day_of_month(index_date) - 11 months",
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
            "first_day_of_month(index_date) - 11 months",
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
            "first_day_of_month(index_date) - 11 months",
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
            "first_day_of_month(index_date) - 11 months",
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
            "first_day_of_month(index_date) - 11 months",
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
            "first_day_of_month(index_date) - 11 months",
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
    # NOTE: that the hyp_invite_1_date variable gets defined here
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
    hyp_invite_2=patients.with_these_clinical_events(
        between=[
            "hyp_invite_1_date + 7 days",
            "last_day_of_month(index_date)"
            ],
        codelist=hyp_invite_codes,
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Reject patients passed to this rule whose earliest hypertension
    # diagnosis was in the 9 months leading up to and including the 
    # paymentperiod end date. Pass all remaining patients to the next rule.
    hyp_9m=patients.with_these_clinical_events(
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
    # Reject patients passed to this rule who were recently gms_reg_status at the
    # practice (patient gms_reg_status in the 9 month period leading up to and
    # including the payment period end date).
    registered_9m=patients.registered_with_one_practice_between(
        start_date="first_day_of_month(index_date) - 9 months",
        end_date="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.1}
        )
    )
