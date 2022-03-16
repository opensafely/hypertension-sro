from cohortextractor import codelist_from_csv

bp_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv",
    system="snomed",
    column="code",
    )

bpdec_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bpdec_cod.csv",
    system="snomed",
    column="code",
    )

htmax_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-htmax_cod.csv",
    system="snomed",
    column="code",
    )

hyp_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
    system="snomed",
    column="code",
    )

hypinvite_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hypinvite_cod.csv",
    system="snomed",
    column="code",
    )

hyppcadec_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyppcadec_cod.csv",
    system="snomed",
    column="code",
    )

hyppcapu_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyppcapu_cod.csv",
    system="snomed",
    column="code",
    )

hypres_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hypres_cod.csv",
    system="snomed",
    column="code",
    )

ethnicity6_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
    )

ld_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ld_cod.csv",
    system="snomed",
    column="code",
)
carehome_codes = codelist_from_csv(
    "codelists/opensafely-nhs-england-care-homes-residential-status.csv",
    system="snomed",
    column="code",
)
