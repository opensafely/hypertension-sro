from cohortextractor import StudyDefinition, patients, Measure

import json
import pandas as pd

# Import dates and codelists
from config import (
    start_date,
    end_date,
    demographic_breakdowns,
)

from codelists import bp_codes, bp_dec_codes

# Import shared variable dictionaries
from dict_bp_variables import bp002_variables_1y_lookback
from dict_demo_variables import demographic_variables
from dict_hyp_variables import hyp_reg_variables

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
        gms_reg_status AND
        (NOT died) AND
        (sex = 'F' OR sex = 'M') AND
        (age_band != 'missing') AND
        # Set population to be hypertension register
        hyp_reg
        """,
    ),
    # Include blood pressure and demographic variable dictionaries
    **demographic_variables,
    # Include hypertension variables for register
    **hyp_reg_variables,
    **bp002_variables_1y_lookback,
)

# Create blood pressure achievement measures
measures = [
    Measure(
        id="bp002_1y_achievem_hypreg_population_rate",
        numerator="bp002_numerator",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="bp002_1y_achievem_hypreg_practice_breakdown_rate",
        numerator="bp002_numerator",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),
]

# Create demographic breakdowns for blood pressure indicator BP002 measures
for breakdown in demographic_breakdowns:
    m = Measure(
        id=f"bp002_1y_achievem_hypreg_{breakdown}_breakdown_rate",
        numerator="bp002_numerator",
        denominator="population",
        group_by=[breakdown],
        small_number_suppression=True,
    )
    measures.append(m)
