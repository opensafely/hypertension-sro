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
    hyp_flowchart,
    hyp_data_check,
)
from dict_demo_variables import demographic_variables
from dict_hyp_variables import (
    hyp_ind_variables,
    hyp_reg_variables,
    hyp007_business_rules_variables,
    bp_check_values_variables,
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
        # Set population to be hypertension register
        hyp_reg
        """,
    ),
    # Include demographic variables
    **demographic_variables,
    # Include hypertension variables for denominator and numerator rules
    **hyp_ind_variables,
    # Add variables to check blood pressure values
    **bp_check_values_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # Include denominator rules variables for hyp007
    **hyp007_business_rules_variables,
    # DEFINE COMPOSITE DENOMINATOR
    # NOTE: The individual rules (suffix: _r*) are specified in the
    # hypertensin variable dictionary
    hyp007_denominator=patients.satisfying(
        """
        # Specify denominator select / reject / next logic

        # R1: Actions in business rules: True: Reject; False: Next
        # NOTE: This rule is coded reversely. True: Select; False: Next
        hyp007_denominator_r1 AND

        # R2: Actions in business rules: True: Select; False: Next
        (hyp007_denominator_r2 OR

            (
               # R3: Actions in business rules: True: Reject; False: Next
               # NOTE: This rule is coded reversely. True: Select; False: Next
               hyp007_denominator_r3 AND

               # R4: Actions in business rules: True: Reject; False: Next
               # NOTE: This rule is coded reversely. True: Select; False: Next
               hyp007_denominator_r4 AND

               # R5: Actions in business rules: True: Reject; False: Next
               # NOTE: This rule is coded reversely. True: Select; False: Next
               hyp007_denominator_r5 AND

               # R6: Actions in business rules: True: Reject; False: Next
               # NOTE: This rule is coded reversely. True: Select; False: Next
               hyp007_denominator_r6 AND

               # R7: Actions in business rules: True: Reject; False: Next
               # NOTE: This rule is coded reversely. True: Select; False: Next
               (NOT hyp007_denominator_r7) AND

               # R8: Actions in business rules: True: Reject; False: Next
               # NOTE: This rule is coded reversely. True: Select; False: Next
               hyp007_denominator_r8 AND

               # R9: Actions in business rules: True: Reject; False: Select
               # NOTE: This rule is coded reversely. True: Select; False: Reject
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

# Create measures for total population and breakdown by practice
measures = [
    Measure(
        id="hyp007_achievem_population_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp007_achievem_practice_breakdown_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=["practice"],
        small_number_suppression=True,
    ),
]

# Create hypertension breakdown measures
for breakdown in demographic_breakdowns:
    m = Measure(
        id=f"hyp007_achievem_{breakdown}_breakdown_rate",
        numerator="hyp007_numerator",
        denominator="hyp007_denominator",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)

# Create hypertension exclusion count measures
for exclusion in hyp_exclusions:
    m = Measure(
        id=f"""hyp007_excl_{exclusion.lstrip("hyp007_")}_population_rate""",
        numerator=f"hyp007_{exclusion}_excl",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)

# Create hypertension flowchart count measures
for select_reject in hyp_flowchart:
    m = Measure(
        id=f"hyp007_flow_{select_reject}_population_rate",
        numerator=f"hyp007_{select_reject}",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)

# Create data check measures
for data_check in hyp_data_check:
    m = Measure(
        id=f"hyp007_check_{data_check}_population_rate",
        numerator=data_check,
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    )
    measures.append(m)
