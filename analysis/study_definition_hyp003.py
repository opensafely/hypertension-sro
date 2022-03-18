from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date
from codelists import hyp_codes, hypres_codes

from dict_hyp_variables import hyp_ind_variables, hyp_reg_variables
from dict_hyp_variables import hyp_reg_variables

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

        hypertension AND
        (NOT hypertension_resolved)
        """,
    ),

    # Include hypertension variables
    ** hyp_ind_variables,
    ** hyp_reg_variables,

    # Include demographic variables
    ** demographic_variables

)

# Create default measures
measures = [

    Measure(
        id="hyp003_code_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["hypertension_code"],
        small_number_suppression=True
    ),

    Measure(
        id="hyp003_practice_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True
    ),

    Measure(
        id="hyp003_age_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["age_band"],
        small_number_suppression=True
    ),

    Measure(
        id="hyp003_sex_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["sex"],
        small_number_suppression=True
    ),

    Measure(
        id="hyp003_imd_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["imd"],
        small_number_suppression=True
    ),

    Measure(
        id="hyp003_region_rate",
        numerator="hypertension",
        denominator="population",
        group_by=["region"],
        small_number_suppression=True
    ),

]
