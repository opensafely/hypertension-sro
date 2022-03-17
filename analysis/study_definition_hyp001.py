from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv, Measure  # NOQA

import json
import pandas as pd

from config import start_date, end_date
from codelists import hyp_codes, hypres_codes

from dict_hyp_reg_variables import hyp_reg_variables
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

        (hyp = 1) AND
        (hyp_res = 0)
        """,
    ),

    # Include hypertension variables
    ** hyp_reg_variables,

    # Include demographic variables
    ** demographic_variables,

)
