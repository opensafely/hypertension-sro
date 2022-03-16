# Define common variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

from cohortextractor import patients

hyp_reg_variables = dict(

  # Rules for indicators HYP003 and HYP007
  # The only differences between the indicators are:
  # - Age (Denominator rule 1)
  #   - HYP003: >79
  #   - HYP007: <80
  # - Values of last blood pressure (Denominator rules 2, 7)
  #   - HYP003: SYS<= 140, DIA <= 90
  #   - HYP007: SYS <= 150, DIA <= 90

  # Denominator
  # Rule 1
  # TODO
  # Rule 2
  # TODO
  # Rule 3
  # TODO
  # Rule 4
  # TODO
  # Rule 5
  # TODO
  # Rule 6
  # TODO
  # Rule 7
  # TODO
  # Rule 8
  # TODO
  # Rule 9
  # TODO

  # Numerator
  # Rule 1
  # TODO
)
