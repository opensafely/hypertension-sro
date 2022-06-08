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
    # Date variable extracted: "bp_sys_val_12m_date_measured"
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
    # BPDIA_VAL: The diastolic blood pressure values associated
    # with each date in the BPSYS_DAT array.
    # Date variable extracted: "bp_dia_val_12m_date_measured"
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
    # HTMAX_DAT: Date of the most recent maximal blood pressure
    # therapy code recorded up to and including the achievement date.
    # Date variable extracted: "ht_max_12m_date"
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
    # Date variable extracted: "hyp_pca_pu_12m_date"
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
    # Date variable extracted: "bp_dec_12m_date"
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
    # Date variable extracted: "hyp_pca_dec_12m_date"
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
    # Date variable extracted: "hyp_invite_1_date"
    hyp_invite_1=patients.with_these_clinical_events(
        between=[
            "first_day_of_month(index_date) - 11 months",
            "last_day_of_month(index_date)",
        ],
        codelist=hyp_invite_codes,
        returning="binary_flag",
        find_first_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # HYPINVITE2_DAT: Date of the earliest invite for a hypertension care
    # review recorded at least 7 days after the first invitation and up to
    # and including the achievement date.
    # Date variable extracted: "hyp_invite_2_date"
    hyp_invite_2=patients.with_these_clinical_events(
        between=["hyp_invite_1_date + 7 days", "last_day_of_month(index_date)"],
        codelist=hyp_invite_codes,
        returning="binary_flag",
        find_first_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Reject patients passed to this rule whose earliest hypertension
    # diagnosis was in the 9 months leading up to and including the
    # paymentperiod end date. Pass all remaining patients to the next rule.
    hyp_9m=patients.satisfying(
        """
        (NOT hyp_before_9m) AND
        hyp_last_9m
        """,
        hyp_before_9m=patients.with_these_clinical_events(
            on_or_before="first_day_of_month(index_date) - 9 months",
            codelist=hyp_codes,
            returning="binary_flag",
            include_date_of_match=False,
        ),
        hyp_last_9m=patients.with_these_clinical_events(
            between=[
                "first_day_of_month(index_date) - 9 months",
                "last_day_of_month(index_date)",
            ],
            codelist=hyp_codes,
            returning="binary_flag",
            include_date_of_match=False,
        ),
    ),
    # Reject patients passed to this rule who were recently registered at the
    # practice (patient registered in the 9 month period leading up to and
    # including the payment period end date).
    # NOTE: This variable selects patients that were registered with one
    # practice in the last 9 months. Therefore, this variable (reg_9m)
    # specifies the patients that need to be selected for in the
    # denominator.
    reg_9m=patients.registered_with_one_practice_between(
        start_date="first_day_of_month(index_date) - 9 months",
        end_date="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.1},
    ),
    # Define variable to check for blood pressure values within a
    # prespecified range.
    # NOTE: This is not part of the QOF business rules but a first step at
    # tidying the underlying data.
    # TODO: This approach and the cutoff values both need to be reviewed.
    valid_or_missing_bp_sys_dia_values=patients.satisfying(
        """
        valid_bp_sys_dia_values
        # OR missing_bp_sys_dia_values
        """,
        valid_bp_sys_dia_values=patients.satisfying(
            """
            # Set min cutoff values
            (bp_sys_val_12m > 0) AND
            (bp_dia_val_12m > 0) AND
            # Set max cutoff values
            (bp_sys_val_12m < 500) AND
            (bp_dia_val_12m < 500)
            """
        ),
        # missing_bp_sys_dia_values=patients.satisfying(
        #     """
        #     # No bp measurement
        #     (NOT bp_sys_val_12m_date_measured) AND
        #     (NOT bp_dia_val_12m_date_measured)
        #     """
        # ),
    ),
)


# Rules for indicator HYP007
hyp007_denominator_rules_variables = dict(
    # Reject patients from the specified population who are aged less
    # than 80 years old.
    hyp007_denominator_r1=patients.satisfying(
        """
        age >= 80
        """
    ),
    # Select patients passed to this rule who meet all of the criteria
    # below:
    # - Systolic blood pressure value was 150 mmHg or less.
    # - Diastolic blood pressure value was 90 mmHg or less.
    # Most recent blood pressure recording was in the 12 months leading up
    # to and including the payment period end date.
    # NOTE: This implementation assumes that both values (sys, dia) were
    # measured on the same day.
    hyp007_denominator_r2=patients.satisfying(
        """
        bp_sys_val_12m <= 150 AND
        bp_dia_val_12m <= 90
        """
    ),
    # Reject patients passed to this rule who are receiving maximal blood
    # pressure therapy in the 12 months leading up to and including the
    # payment period end date.
    hyp007_denominator_r3=patients.satisfying(
        """
        NOT ht_max_12m
        """
    ),
    # Reject patients passed to this rule for whom hypertension quality
    # indicator care was unsuitable in the 12 months leading up to and
    # including the payment period end date.
    hyp007_denominator_r4=patients.satisfying(
        """
        NOT hyp_pca_pu_12m
        """
    ),
    # Reject patients passed to this rule who chose not to have their
    # blood pressure recorded in the 12 months leading up to and including
    # the payment period end date.
    hyp007_denominator_r5=patients.satisfying(
        """
        NOT bp_dec_12m
        """
    ),
    # Reject patients passed to this rule who chose not to receive
    # hypertension quality indicator care in the 12 months leading up to
    # and including the payment period end date.
    hyp007_denominator_r6=patients.satisfying(
        """
        NOT hyp_pca_dec_12m
        """
    ),
    # Reject patients passed to this rule who meet either of the criteria
    # below:
    # - Latest blood pressure reading in the 12 months leading up to
    # and including the payment period end date was above target levels
    # (systolic value of over 150 mmHg and/or a diastolic value of over 90
    # mmHg), and was followed by two invitations for hypertension
    # monitoring.
    # - Received two invitations for hypertension monitoring and
    # had no blood pressure recordings during the 12 months leading up to
    # and including the achievement date.
    # NOTE: This implementation assumes that both values (sys, dia) were
    # measured on the same day.
    hyp007_denominator_r7=patients.satisfying(
        """
        ((NOT hyp007_denominator_r7_crit1_1) AND
        hyp007_denominator_r7_crit1_2)
        OR
        ((NOT hyp007_denominator_r7_crit2_1) AND
        (NOT hyp007_denominator_r7_crit2_2))
        """,
        hyp007_denominator_r7_crit1_1=patients.satisfying(
            """
            # Criterion 1.1
            bp_sys_val_12m > 150 OR bp_dia_val_12m > 90
            """
        ),
        hyp007_denominator_r7_crit1_2=patients.satisfying(
            """
            # Criterion 1.2
            (hyp_invite_1 AND hyp_invite_2) AND
            (hyp_invite_1_date > bp_sys_val_12m_date_measured) AND
            (hyp_invite_1_date > bp_dia_val_12m_date_measured)
            """
        ),
        hyp007_denominator_r7_crit2_1=patients.satisfying(
            """
            # Criterion 2.1
            hyp_invite_1 AND hyp_invite_2
            """
        ),
        hyp007_denominator_r7_crit2_2=patients.satisfying(
            """
            # Criterion 2.2
            (NOT bp_sys_val_12m_date_measured) AND
            (NOT bp_dia_val_12m_date_measured)
            """
        ),
    ),
    # Reject patients passed to this rule whose earliest hypertension
    # diagnosis was in the 9 months leading up to and including the
    # payment period end date.
    hyp007_denominator_r8=patients.satisfying(
        """
        NOT hyp_9m
        """
    ),
    # Reject patients passed to this rule who were recently registered at
    # the practice (registered in the 9 month period leading up to
    # and including the payment period end date).
    # NOTE: This variable selects patients that were registered with one
    # practice in the last 9 months. Therefore, this variable (reg_9m)
    # specifies the patients that need to be selected for in the
    # denominator.
    hyp007_denominator_r9=patients.satisfying(
        """
        reg_9m
        """
    ),
)
