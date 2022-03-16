from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

from config import start_date, end_date
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
        (sex = 'F' OR sex = 'M')

        (hyp = 1) AND
        (hyp_res = 0)
        """,
    ),

    registered=patients.registered_as_of(
        "index_date",
        return_expectations={"incidence": 0.9},
        ),

    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1}
        ),

    # Include hypertension variables
    ** hyp_reg_variables,

    # Include demographic variables
    ** demographic_variables,

)
