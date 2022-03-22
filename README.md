# Hypertension Service Restoration Observatory (SRO)

## Overview
 
General practice has been disrupted by the pandemic in many clinical areas (e.g., Curtis et al., [2021](https://bjgp.org/content/72/714/e63); Williams et al., [2020](https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(20)30201-2/fulltext)). 
This project aims to assess the impact of the pandemic on the routine management of hypertension. 
High blood pressure is one of the leading risk factors for several diseases (e.g., cardiovascular disease, stroke) worldwide. 
Research suggests that delays in the management of high blood pressure are associated with worse clinical outcomes, for example acute cardiovascular events, or death (Xu et al., [2015](https://www.bmj.com/content/350/bmj.h158)). 

[The Quality and Outcomes Framework (QOF)](https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/general-practice-data-hub/quality-outcomes-framework-qof) outlines several indicators that focus hypertension (HYP) targets. 
This project aim to use OpenSAFELY to quantify the extent to which any of the relevant Hypertension QOF indicators ([v46](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/quality-and-outcome-framework-qof-business-rules/qof-business-rules-v46.0-2021-2022-baseline-release)) were disrupted during the pandemic but wont link our results to clinical outcomes.

---

A short description of the QOF Hypertension ([v46](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/quality-and-outcome-framework-qof-business-rules/qof-business-rules-v46.0-2021-2022-baseline-release)) register and each indicator is shown below:

* **HYP_REG**: Hypertension register: Patients with an unresolved diagnosis of hypertension.
* **HYP001**: The contractor establishes and maintains a register of patients with established hypertension
* **HYP003**: The percentage of patients **aged 79 years or under**, with hypertension, in whom the last blood pressure reading (measured in the preceding 12 months) is **140/90 mmHg or less**.
* **HYP007**: The percentage of patients **aged 80 years or over**, with hypertension, in whom the last blood pressure reading (measured in the preceding 12 months) is **150/90 mmHg or less**.

## Repository structure

### Codelists

* All codelists used in this project are available in the [codelists](codelists) folder

### Variable dictionaries

* Variables that are shared across study definitions are specified in dictionaries:
  * **Demographic variables**: [analysis/dict_demo_variables.py](analysis/dict_demo_variables.py)
  * **Hypertension register and indicators**: [analysis/dict_hyp_variables.py](analysis/dict_hyp_variables.py)

### Study definitions

* The hypertension register (HYP_REG / HYP001) and each indicator (HYP003, HYP007) are specified in individual study definitions. 
  Each denominator and numerator rule is defined in its own `patients.satisfying()` function (e.g., `hyp003_denominator_r1`) and summarised in a composite variable (e.g., `hyp003_denominator`).
  * **HYP001**: [analysis/study_definition_hyp001.py](analysis/study_definition_hyp001.py)
  * **HYP003**: [analysis/study_definition_hyp003.py](analysis/study_definition_hyp003.py)
  * **HYP007**: [analysis/study_definition_hyp007.py](analysis/study_definition_hyp007.py) (Waiting for code review of HYP001 and HYP001 before finishing)
* Commonly used dates are defined in [analysis/config.py](analysis/config.py)

### Actions

All actions are defined in the [project.yaml](project.yaml).

* Each indicator has the following actions:
  * `generate_study_population_hyp***`: Extract study population
  * `generate_measures_hyp***`: Generate measures using the `Measure()` framework
* TODO ADD PLOTS
* TODO ADD TABLES
* TODO ADD REPORT

# About the OpenSAFELY framework

Developers and epidemiologists interested in the framework should review [the OpenSAFELY documentation](https://docs.opensafely.org)
The OpenSAFELY framework is a Trusted Research Environment (TRE) for electronic
health records research in the NHS, with a focus on public accountability and
research quality.
Read more at [OpenSAFELY.org](https://opensafely.org).

# Licences
As standard, research projects have a MIT license. 
