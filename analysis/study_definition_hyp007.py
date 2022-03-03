from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA
from dict_hyp_variables import hyp_variables
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),

    # Include hypertension variables
    ** hyp_variables

    # Include demographic variables
    ** demographic_variables
)
