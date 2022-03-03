from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

from config import start_date, end_date
from dict_hyp_variables import hyp_variables
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
        (sex = 'F' OR sex = 'M')

        """,
    ),

    # Include hypertension variables
    ** hyp_variables,

    # Include demographic variables
    ** demographic_variables

)
