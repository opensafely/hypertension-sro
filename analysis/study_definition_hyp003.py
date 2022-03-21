from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date
from codelists import hyp_codes, hyp_res_codes

from dict_hyp_variables import hyp_ind_variables, hyp_reg_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.satisfying(
        """
        # Define general population parameters
        registered AND
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND

        hypertension_register
        """,
    ),
    hyp003_denominator=patients.satisfying(
        """
        hyp003_denominator_r1
        """,
        hyp003_denominator_r1=patients.satisfying(
            """
            age > 79
            """
        ),
        # hyp003_denominator_r2=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r3=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r4=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r5=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r6=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r7=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r8=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
        # hyp003_denominator_r9=patients.satisfying(
        #     """
        #     # TODO
        #     """
        # ),
    ),
    hyp003_numerator=patients.satisfying(
        """
        hyp003_numerator_r1
        """,
        hyp003_numerator_r1=patients.satisfying(
            """
            bp_sys_val <= 140
            AND
            bp_dia_val <= 90
            # AND
            # BP_DAT > (PPED - 12 months)
            """
        ),

    ),
    # Include hypertension variables for denominator and numerator rules
    **hyp_ind_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # Include demographic variables
    **demographic_variables,
)

# Create default measures
measures = [
    Measure(
        id="hyp003_population_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp003_practice_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp003_age_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["age_band"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp003_sex_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["sex"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp003_imd_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["imd"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp003_region_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["region"],
        small_number_suppression=True,
    ),
]
