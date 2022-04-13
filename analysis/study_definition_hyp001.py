from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date
from codelists import hyp_codes, hyp_res_codes

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
        (age_band != 'missing') AND
        """,
    ),
    # Include hypertension variables
    **hyp_reg_variables,
    # Include demographic variables
    **demographic_variables,
)

# Create default measures
measures = [
    Measure(
        id="hyp001_population_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_practice_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_age_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["age_band"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_sex_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["sex"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_imd_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["imd"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_region_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["region"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_ethnicity_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["ethnicity"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_learning_disability_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["learning_disability"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_care_home_rate",
        numerator="hypertension_register",
        denominator="population",
        group_by=["care_home"],
        small_number_suppression=True,
    ),
]
