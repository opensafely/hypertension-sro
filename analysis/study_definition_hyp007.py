from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date
from dict_hyp_variables import hyp_ind_variables, hyp_reg_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    # Include hypertension variables for denominator and numerator rules
    **hyp_ind_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # Include demographic variables
    **demographic_variables,
    # Set index date to start date
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Define general study population
    population=patients.satisfying(
        """
        # Define general population parameters
        registered AND
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND
        (age_band != 'missing') AND

        hypertension_register
        """,
    ),
    # Define composite denominator
    # Note that the individual rules (suffix: _r*) are specified as described
    # in the rules and the action (reject / select) is defined in the composite
    # denominator.
    hyp007_denominator=patients.satisfying(
        """
        (NOT hyp007_denominator_r1) AND

            (hyp007_denominator_r2 OR

            (
                (NOT hyp007_denominator_r3) AND
                (NOT hyp007_denominator_r4) AND
                (NOT hyp007_denominator_r5) AND
                (NOT hyp007_denominator_r6) AND
                (NOT hyp007_denominator_r7) AND
                (NOT hyp007_denominator_r8) AND
                (NOT hyp007_denominator_r9)
            )
        )
        """,
        # Reject patients from the specified population who are aged greater
        # than 79 years old.
        hyp007_denominator_r1=patients.satisfying(
            """
            age < 80
            """
        ),
        # Select patients passed to this rule who meet all of the criteria
        # below:
        # - Systolic blood pressure value was 150 mmHg or less.
        # - Diastolic blood pressure value was 90 mmHg or less.
        # Most recent blood pressure recording was in the 12 months leading up
        # to and including the payment period end date.
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
            ht_max_12m
            """
        ),
        # Reject patients passed to this rule for whom hypertension quality
        # indicator care was unsuitable in the 12 months leading up to and
        # including the payment period end date.
        hyp007_denominator_r4=patients.satisfying(
            """
            hyp_pca_pu_12m
            """
        ),
        # Reject patients passed to this rule who chose not to have their
        # blood pressure recorded in the 12 months leading up to and including
        # the payment period end date.
        hyp007_denominator_r5=patients.satisfying(
            """
            bp_dec_12m
            """
        ),
        # Reject patients passed to this rule who chose not to receive
        # hypertension quality indicator care in the 12 months leading up to
        # and including the payment period end date.
        hyp007_denominator_r6=patients.satisfying(
            """
            hyp_pca_dec_12m
            """
        ),
        # Reject patients passed to this rule who meet either of the criteria
        # below: Latest blood pressure reading in the 12 months leading up to
        # and including the payment period end date was above target levels
        # (systolic value of over 140 mmHg and/or a diastolic value of over 90
        # mmHg), and was followed by two invitations for hypertension
        # monitoring. Received two invitations for hypertension monitoring and
        # had no blood pressure recordings during the 12 months leading up to
        # and including the achievement date.
        hyp007_denominator_r7=patients.satisfying(
            """
            bp_sys_val_12m <= 150 AND
            bp_dia_val_12m <= 90 AND

            (hyp_invite_1_date > bp_sys_val_12m_date_measured OR
            hyp_invite_1_date > bp_dia_val_12m_date_measured)
            """
        ),
        # Reject patients passed to this rule whose earliest hypertension
        # diagnosis was in the 9 months leading up to and including the
        # payment period end date.
        hyp007_denominator_r8=patients.satisfying(
            """
            hypertension_9m
            """
        ),
        # Reject patients passed to this rule who were recently registered at
        # the practice (patient registered in the 9 month period leading up to
        # and including the payment period end date).
        hyp007_denominator_r9=patients.satisfying(
            """
            registered_9m
            """
        ),
    ),
    # Define composite numerator
    # Select patients from the denominator who meet all of the criteria below:
    # - Systolic blood pressure value was 140 mmHg or less.
    # - Diastolic blood pressure value was 90 mmHg or less.
    # Most recent blood pressure recording was in the 12 months up to and
    # including the payment period end date.
    # Reject the remaining patients.
    hyp007_numerator=patients.satisfying(
        """
        hyp007_denominator AND
        hyp007_denominator_r2
        """,
    ),
)

# Create default measures
measures = [
    Measure(
        id="hyp007_population_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_practice_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_age_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["age_band"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_sex_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["sex"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_imd_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["imd"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_region_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["region"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_ethnicity_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["ethnicity"],
        small_number_suppression=True,
    ),
]
