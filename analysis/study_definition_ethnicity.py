from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv,
    Measure,
)

from config import end_date
from codelists import ethnicity6_codes
from dict_demo_variables import demographic_variables

study = StudyDefinition(
    # Set default expectations
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
    },
    # Set index date to end_date specified in config.py
    index_date=end_date,
    # Define general study population
    population=patients.satisfying(
        """
        (NOT died)
        AND
        gms_reg_status
        """,
        # Include demographic variables
        **demographic_variables,
    ),
    ethnicity=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "White": "eth='1' OR (NOT eth AND ethnicity_sus='1')",
            "Mixed": "eth='2' OR (NOT eth AND ethnicity_sus='2')",
            "Asian": "eth='3' OR (NOT eth AND ethnicity_sus='3')",
            "Black": "eth='4' OR (NOT eth AND ethnicity_sus='4')",
            "Other": "eth='5' OR (NOT eth AND ethnicity_sus='5')",
        },
        eth=patients.with_these_clinical_events(
            ethnicity6_codes,
            returning="category",
            find_last_match_in_period=True,
            include_date_of_match=False,
            return_expectations={
                "category": {
                    "ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}
                },
                "incidence": 0.75,
            },
        ),
        # fill missing ethnicity from SUS
        ethnicity_sus=patients.with_ethnicity_from_sus(
            returning="group_6",
            use_most_frequent_code=True,
            return_expectations={
                "category": {
                    "ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}
                },
                "incidence": 0.4,
            },
        ),
        return_expectations={
            "category": {
                "ratios": {
                    "White": 0.2,
                    "Mixed": 0.2,
                    "Asian": 0.2,
                    "Black": 0.2,
                    "Other": 0.2,
                }
            },
            "incidence": 0.8,
        },
    ),
)
