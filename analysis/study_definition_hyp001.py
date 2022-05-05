from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date
from codelists import hyp_codes, hyp_res_codes

from dict_hyp_variables import hyp_reg_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    # Set start date
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Define population
    population=patients.satisfying(
        """
        # Define general population parameters
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND
        (age_band != 'missing') AND

        # Define GMS registration status
        gms_reg_status 

        # Define list size type:
        # TOTAL for HYP so no further exclusions
        """,
    ),
    # Include demographic variables
    **demographic_variables,
    # Include hypertension variables
    **hyp_reg_variables,
)

# Create default measures
measures = [
    Measure(
        id="hyp001_population_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_practice_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_age_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["age_band"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_sex_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["sex"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_imd_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["imd"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_region_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["region"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_ethnicity_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["ethnicity"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_learning_disability_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["learning_disability"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_care_home_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["care_home"],
        small_number_suppression=True,
    ),
]
