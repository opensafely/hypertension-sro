# Hypertension Service Restoration Observatory (SRO)

## Overview
 
General practice has been disrupted by the pandemic in many clinical areas (e.g., Curtis et al., [2021](https://bjgp.org/content/72/714/e63); Williams et al., [2020](https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(20)30201-2/fulltext)). 
We aim to assess the impact of the pandemic on the routine management of blood pressure and hypertension. High blood pressure is one of the leading risk factors for several diseases (e.g., cardiovascular disease, stroke) worldwide. 
Research suggests that delays in the management of high blood pressure are associated with worse clinical outcomes, for example acute cardiovascular events, or death (Xu et al., [2015](https://www.bmj.com/content/350/bmj.h158)). 

[The Quality and Outcomes Framework (QOF)](https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/general-practice-data-hub/quality-outcomes-framework-qof) outlines several indicators that focus hypertension (HYP) targets. 
This project aim to use OpenSAFELY to quantify the extent to which any of the relevant Hypertension QOF indicators ([v46](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/quality-and-outcome-framework-qof-business-rules/qof-business-rules-v46.0-2021-2022-baseline-release)) were disrupted during the pandemic but wont link our results to clinical outcomes.

## Repository structure

* Variables that are shared across study definitions are specified in dictionaries:
  * **Demographic variables**: [analysis/dict_demo_variables.py](analysis/dict_demo_variables.py)
  * **Hypertension register and indicators**: [analysis/dict_hyp_variables.py](analysis/dict_hyp_variables.py)
* The hypertension register (HYP_001) and each indicator (HYP_003, HYP_007) are specified in individual study definitions. Each denominator and numerator rule is defined in its own `patients.satisfying()` function and summarised in a composite variable.
  * **HYP_001**: [analysis/study_definition_hyp001.py](analysis/study_definition_hyp001.py)
  * **HYP_003**: [analysis/study_definition_hyp003.py](analysis/study_definition_hyp003.py)
  * **HYP_007**: [analysis/study_definition_hyp007.py](analysis/study_definition_hyp007.py)
* Commonly used dates are defined in [analysis/config.py](analysis/config.py)

# About the OpenSAFELY framework

Developers and epidemiologists interested in the framework should review [the OpenSAFELY documentation](https://docs.opensafely.org)
The OpenSAFELY framework is a Trusted Research Environment (TRE) for electronic
health records research in the NHS, with a focus on public accountability and
research quality.

Read more at [OpenSAFELY.org](https://opensafely.org).

# Licences
As standard, research projects have a MIT license. 
