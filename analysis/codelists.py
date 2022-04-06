from cohortextractor import codelist_from_csv

# Cluster name: BP_COD
# Description: Blood pressure (BP) recording codes
# SNOMED CT: ^999012731000230108
bp_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bp_cod.csv",
    system="snomed",
    column="code",
)

# Codes from BP_COD related systolic blood pressure readings
bp_sys_codes = codelist_from_csv(
    "codelists/opensafely-systolic-blood-pressure-qof.csv",
    system="snomed",
    column="code",
)

# Codes from BP_COD related diastolic blood pressure readings
bp_dia_codes = codelist_from_csv(
    "codelists/user-milanwiedemann-diastolic-blood-pressure-qof.csv",
    system="snomed",
    column="code",
)

# Cluster name: BPDEC_COD
# Description: Codes indicating the patient has chosen not to have blood
# pressure procedure
# SNOMED CT: ^999012611000230106
bp_dec_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-bpdec_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: HTMAX_COD
# Description: Codes for maximal blood pressure (BP) therapy
# SNOMED CT: ^999006651000230109
ht_max_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-htmax_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: HYP_COD
# Description: Hypertension diagnosis codes
# SNOMED CT: ^999006611000230105
hyp_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: HYPINVITE_COD
# Description: Invite for hypertension care review codes
# SNOMED CT: ^999012971000230108
hyp_invite_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hypinvite_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: HYPPCADEC_COD
# Description: Codes indicating the patient has chosen not to receive
# hypertension quality indicator care
# SNOMED CT: ^999013091000230102
hyp_pca_dec_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyppcadec_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: HYPPCAPU_COD
# Description: Codes for hypertension quality indicator care unsuitable for
# patient
# SNOMED CT: ^999013211000230104
hyp_pca_pu_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyppcapu_cod.csv",
    system="snomed",
    column="code",
)

# Cluster name: HYPRES_COD
# Description: Hypertension resolved codes
# SNOMED CT: ^999006531000230101
hyp_res_codes = codelist_from_csv(
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

learning_disability_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ld_cod.csv",
    system="snomed",
    column="code",
)

nhse_care_homes_codes = codelist_from_csv(
    "codelists/opensafely-nhs-england-care-homes-residential-status.csv",
    system="snomed",
    column="code",
)
