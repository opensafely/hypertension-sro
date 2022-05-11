from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

from config import start_date, end_date, demographic_breakdowns
from codelists import hyp_codes, hyp_res_codes

from dict_hyp_variables import hyp_reg_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    # Include demographic variables
    **demographic_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    # Set start date
    index_date=start_date,
    # Set default expectations
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Define general study population
    # NOTE: For the HYP register this is the patient list size
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
)

# Create default measures
measures = [
    Measure(
        id="hyp001_prevalence_population_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="hyp001_prevalence_practice_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
]

# Create blood pressure exclusion measures (3) for total population
for breakdown in demographic_breakdowns:
    m = Measure(
        id=f"hyp001_prevalence_{breakdown}_breakdown_rate",
        numerator="hyp_reg",
        denominator="population",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)
