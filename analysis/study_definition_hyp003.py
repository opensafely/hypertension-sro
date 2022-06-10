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
    hyp003_business_rules_variables,
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
    # Include demographic variables
    **demographic_variables,
    # Include hypertension variables for denominator and numerator rules
    **hyp_ind_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # Include denominator rules variables for hyp007
    **hyp003_business_rules_variables,
    # Define composite denominator
    # NOTE: The individual rules (suffix: _r*) are specified as described
    # in the rules and the actions (reject / select) are defined in the
    # composite denominator below (hyp003_denominator).
    hyp003_denominator=patients.satisfying(
        """
        # Specify denominator select / reject logic:

        # Actions in business rules: True: Reject; False: Next
        # NOTE: This rule is coded reversely. True: Select; False: Next
        hyp003_denominator_r1 AND

        # Actions in business rules: True: Select; False: Next
        (hyp003_denominator_r2 OR

            (
                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Select; False: Next
                hyp003_denominator_r3 AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Select; False: Next
                hyp003_denominator_r4 AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Select; False: Next
                hyp003_denominator_r5 AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Select; False: Next
                hyp003_denominator_r6 AND

                # Actions in business rules: True: Reject; False: Next
                (NOT hyp003_denominator_r7) AND

                # Actions in business rules: True: Reject; False: Next
                # NOTE: This rule is coded reversely. True: Select; False: Next
                hyp003_denominator_r8 AND

                # Actions in business rules: True: Reject; False: Select
                # NOTE: This rule is coded reversely. True: Select; False: Reject
                hyp003_denominator_r9
            )
        )
        """,
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

# Create hypertension exclusion measures (3) for total population
for exclusion in hyp_exclusions:
    m = Measure(
        id=f"""hyp003_excl_{exclusion.lstrip("hyp003_")}_population_rate""",
        numerator=f"hyp003_{exclusion}_excl",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)

# Create hypertension exclusion measures (3) for total population
for data_check in hyp_data_check:
    m = Measure(
        id=f"hyp003_check_{data_check}_population_rate",
        numerator=data_check,
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)
