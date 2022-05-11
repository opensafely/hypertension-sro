from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date, demographic_breakdowns
from dict_hyp_variables import hyp_ind_variables, hyp_reg_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    # Include demographic variables
    **demographic_variables,
    # Include hypertension variables for denominator and numerator rules
    **hyp_ind_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # Set index date to start date
    index_date=start_date,
    # Set default expectations
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Define general study population
    # NOTE: For indicator HYP003 this is the HYP register
    population=patients.satisfying(
        """
        # Define general population parameters
        gms_reg_status AND
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND
        (age_band != 'missing') AND

        hyp_reg
        """,
    ),
    # Define composite denominator
    # NOTE: The individual rules (suffix: _r*) are specified as described
    # in the rules and the action (reject / select) is defined in the composite
    # denominator.
    hyp003_denominator=patients.satisfying(
        """
        (NOT hyp003_denominator_r1) AND

            (hyp003_denominator_r2 OR

            (
                (NOT hyp003_denominator_r3) AND
                (NOT hyp003_denominator_r4) AND
                (NOT hyp003_denominator_r5) AND
                (NOT hyp003_denominator_r6) AND
                (NOT hyp003_denominator_r7) AND
                (NOT hyp003_denominator_r8) AND
                (NOT hyp003_denominator_r9)
            )
        )
        """,
        # Reject patients from the specified population who are aged greater
        # than 79 years old.
        hyp003_denominator_r1=patients.satisfying(
            """
            age > 79
            """
        ),
        # Select patients passed to this rule who meet all of the criteria
        # below:
        # - Systolic blood pressure value was 140 mmHg or less.
        # - Diastolic blood pressure value was 90 mmHg or less.
        # Most recent blood pressure recording was in the 12 months leading up
        # to and including the payment period end date.
        # NOTE: This implementation assumes that both values (sys, dia) were
        # measured on the same day.
        hyp003_denominator_r2=patients.satisfying(
            """
            bp_sys_val_12m <= 140 AND
            bp_dia_val_12m <= 90
            """
        ),
        # Reject patients passed to this rule who are receiving maximal blood
        # pressure therapy in the 12 months leading up to and including the
        # payment period end date.
        hyp003_denominator_r3=patients.satisfying(
            """
            ht_max_12m
            """
        ),
        # Reject patients passed to this rule for whom hypertension quality
        # indicator care was unsuitable in the 12 months leading up to and
        # including the payment period end date.
        hyp003_denominator_r4=patients.satisfying(
            """
            hyp_pca_pu_12m
            """
        ),
        # Reject patients passed to this rule who chose not to have their
        # blood pressure recorded in the 12 months leading up to and including
        # the payment period end date.
        hyp003_denominator_r5=patients.satisfying(
            """
            bp_dec_12m
            """
        ),
        # Reject patients passed to this rule who chose not to receive
        # hypertension quality indicator care in the 12 months leading up to
        # and including the payment period end date.
        hyp003_denominator_r6=patients.satisfying(
            """
            hyp_pca_dec_12m
            """
        ),
        # Reject patients passed to this rule who meet either of the criteria
        # below:
        # - Latest blood pressure reading in the 12 months leading up to
        # and including the payment period end date was above target levels
        # (systolic value of over 140 mmHg and/or a diastolic value of over 90
        # mmHg), and was followed by two invitations for hypertension
        # monitoring.
        # - Received two invitations for hypertension monitoring and
        # had no blood pressure recordings during the 12 months leading up to
        # and including the achievement date.
        # NOTE: This implementation assumes that both values (sys, dia) were
        # measured on the same day.
        hyp003_denominator_r7=patients.satisfying(
            """
            ((bp_sys_val_12m > 140 OR bp_dia_val_12m > 90) AND
            (hyp_invite_1 AND
            hyp_invite_1_date > bp_sys_val_12m_date_measured AND
            hyp_invite_1_date > bp_dia_val_12m_date_measured) AND
            hyp_invite_2)

            OR

            (hyp_invite_2 AND
            (NOT bp_sys_val_12m_date_measured) AND
            (NOT bp_dia_val_12m_date_measured))
            """
        ),
        # Reject patients passed to this rule whose earliest hypertension
        # diagnosis was in the 9 months leading up to and including the
        # payment period end date.
        hyp003_denominator_r8=patients.satisfying(
            """
            hyp_9m
            """
        ),
        # Reject patients passed to this rule who were recently registered at
        # the practice (patient registered in the 9 month period leading up to
        # and including the payment period end date).
        hyp003_denominator_r9=patients.satisfying(
            """
            reg_9m
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
    hyp003_numerator=patients.satisfying(
        """
        hyp003_denominator AND
        hyp003_denominator_r2
        """,
    ),
)

# Create default measures
measures = [
    Measure(
        id="hyp003_achievem_population_rate",
        numerator="hyp003_numerator",
        denominator="hyp003_denominator",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp003_achievem_practice_rate",
        numerator="hyp003_numerator",
        denominator="hyp003_denominator",
        group_by=["practice"],
        small_number_suppression=True,
    ),
]

# Create blood pressure exclusion measures (3) for total population
for breakdown in demographic_breakdowns:
    m = Measure(
        id=f"hyp003_achievem_{breakdown}_breakdown_rate",
        numerator="hyp003_numerator",
        denominator="hyp003_denominator",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)
