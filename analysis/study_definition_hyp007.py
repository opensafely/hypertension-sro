from cohortextractor import (
    StudyDefinition,
    patients,
    Measure,
)
import json
import pandas as pd
from config import (
    start_date,
    end_date,
    demographic_breakdowns,
    hyp_exclusions,
    hyp_data_check,
)
from dict_demo_variables import demographic_variables
from dict_hyp_variables import (
    hyp_ind_variables,
    hyp_reg_variables,
    hyp007_business_rules_variables,
)

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
    # Include denominator rules variables for hyp007
    **hyp007_business_rules_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # DEFINE COMPOSITE DENOMINATOR
    # NOTE: The individual rules (suffix: _r*) are specified as described
    # in the rules and the action (reject / select) are defined in the
    # composite denominator below (hyp007_denominator).
    hyp007_denominator=patients.satisfying(
        """
        # Require valid blood pressure values
        valid_bp_sys_dia_values AND

        # Specify denominator select / reject logic

        # Actions in business rules: True: Select; False: Reject
        hyp007_denominator_r1 AND

        # Actions in business rules: True: Select; False: Next
        (hyp007_denominator_r2 OR

            (
                (
                    # Actions in business rules: True: Reject; False: Next
                    hyp007_denominator_r3 OR

                    # Actions in business rules: True: Reject; False: Next
                    hyp007_denominator_r4 OR

                    # Actions in business rules: True: Reject; False: Next
                    hyp007_denominator_r5 OR

                    # Actions in business rules: True: Reject; False: Next
                    hyp007_denominator_r6 OR

                    # Actions in business rules: True: Reject; False: Next
                    hyp007_denominator_r7 OR

                    # Actions in business rules: True: Reject; False: Next
                    hyp007_denominator_r8
                ) AND
            # Actions in business rules: True: Reject; False: Select
            hyp007_denominator_r9
            )
        )
        """,
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
        id="hyp007_incl_denominator_r2_population_rate",
        numerator="hyp007_denominator_r2",
        denominator="population",
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

# Create hypertension exclusion measures (3) for total population
for data_check in hyp_data_check:
    m = Measure(
        id=f"hyp007_check_{data_check}_population_rate",
        numerator=data_check,
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)
