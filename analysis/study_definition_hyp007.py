from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date, demographic_breakdowns, hyp_exclusions
from dict_hyp_variables import hyp_ind_variables, hyp_reg_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    # Set index date to start date
    index_date=start_date,
    # Set default expectations
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Define general study population
    # NOTE: For indicator HYP007 this is the HYP register
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
    # Include demographic variables
    **demographic_variables,
    # Include hypertension variables for denominator and numerator rules
    **hyp_ind_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # DEFINE COMPOSITE DENOMINATOR
    # NOTE: The individual rules (suffix: _r*) are specified as described
    # in the rules and the action (reject / select) are defined in the
    # composite denominator below (hyp007_denominator).
    hyp007_denominator=patients.satisfying(
        """
        # Require valid blood pressure values
        valid_or_missing_bp_sys_dia_values AND

        # Specify denominator select / reject logic

        # Actions in business rules: True: Select; False: Reject
        hyp007_denominator_r1 AND

        # Actions in business rules: True: Select; False: Next
        (hyp007_denominator_r2 OR

            (
                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Next; False: Reject
                hyp007_denominator_r3 AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Next; False: Reject
                hyp007_denominator_r4 AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Next; False: Reject
                hyp007_denominator_r5 AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Next; False: Reject
                hyp007_denominator_r6 AND

                # Actions in business rules: True: Reject; False: Next
                (NOT hyp007_denominator_r7) AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Next; False: Reject
                hyp007_denominator_r8 AND

                # Actions in business rules: True: Reject; False: Select
                # NOTE: This rule is coded reversely. True: Select; False: Reject
                hyp007_denominator_r9
            )
        )
        """,
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
            (hyp007_denominator_r7_crit1_1 AND
            hyp007_denominator_r7_crit1_2)

            OR

            (hyp007_denominator_r7_crit2_1 AND
            hyp007_denominator_r7_crit2_2)
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
    ),
    # Add exclusion variables
    hyp007_denominator_r1_excl=patients.satisfying(
        """
        NOT hyp007_denominator_r1
        """
    ),
    hyp007_denominator_r3_excl=patients.satisfying(
        """
        ht_max_12m
        """
    ),
    hyp007_denominator_r4_excl=patients.satisfying(
        """
        hyp_pca_pu_12m
        """
    ),
    hyp007_denominator_r5_excl=patients.satisfying(
        """
        bp_dec_12m
        """
    ),
    hyp007_denominator_r6_excl=patients.satisfying(
        """
        hyp_pca_dec_12m
        """
    ),
    hyp007_denominator_r7_excl=patients.satisfying(
        """
        hyp007_denominator_r7
        """
    ),
    hyp007_denominator_r8_excl=patients.satisfying(
        """
        hyp_9m
        """
    ),
    hyp007_denominator_r9_excl=patients.satisfying(
        """
        NOT reg_9m
        """
    ),
    # Define composite numerator
    # Select patients from the denominator who meet all of the criteria below:
    # - Systolic blood pressure value was 150 mmHg or less.
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
        id="hyp007_achievem_population_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_achievem_practice_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["practice"],
        small_number_suppression=True,
    ),
]

# Create blood pressure exclusion measures (3) for total population
for breakdown in demographic_breakdowns:
    m = Measure(
        id=f"hyp007_achievem_{breakdown}_breakdown_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)

# Create hypertension exclusion measures (3) for total population
for exclusion in hyp_exclusions:
    m = Measure(
        id=f"""hyp007_excl_{exclusion.lstrip("hyp007_")}_population_rate""",
        numerator=f"hyp007_{exclusion}_excl",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)
