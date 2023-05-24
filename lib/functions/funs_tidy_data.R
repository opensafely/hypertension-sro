#' Tidy categories in joint measures file
#'
#' @param df Dataframe in wich category names need to be cleaned
#' @param group String, specifying variable name of group variable
#' @param category String, specifying variable name of category (or subgroup) variable
#' @param care_home String, specifying the variable name with care home information  
#' @param learning_disability String, specifying the variable name with learning disability information
#' @param imd String, specifying the variable name with imd information
#' @param imd_explicit_na String, specifying the value to explicitly code missing imd values
#' @param sex String, specifying the variable name with sex information
#' @param population String, specifying the variable name with population information
#' @param long_labels Logical, specyfying whether to code 'long' names/labels
#'
#' @return Dataframe with consistent labels/names for groups/subgroups
tidy_category_names <- function(df,
                                group = NULL,
                                category = NULL,
                                care_home = NULL,
                                learning_disability = NULL,
                                imd = NULL,
                                imd_explicit_na = TRUE,
                                sex = NULL,
                                population = NULL,
                                long_labels = FALSE) {
  # Convert to string
  df <- df %>%
    mutate({{ category }} := as.character({{ category }}))

  if (!is.null(population)) {
    df <- df %>%
      mutate({{ category }} := case_when(
        {{ group }} == {{ population }} & indicator == "bp002" ~
          as.character("Total (Age >= 45)"),
        {{ group }} == {{ population }} & indicator == "hyp001" ~
          as.character("Total"),
        {{ group }} == {{ population }} & indicator == "hyp003" ~
          as.character("Total (Age <= 79)"),
        {{ group }} == {{ population }} & indicator == "hyp007" ~
          as.character("Total (Age >= 80)"),
        TRUE ~ {{ category }}
      ))
  }

  if (long_labels) {
    if (!is.null(care_home)) {
      df <- df %>%
        mutate({{ category }} := case_when(
          {{ group }} == {{ care_home }} ~
            as.character(factor({{ category }},
              levels = c(TRUE, FALSE),
              labels = c(
                "Record of care home status",
                "No record of care home status"
              )
            )),
          TRUE ~ {{ category }}
        ))
    }

    if (!is.null(learning_disability)) {
      df <- df %>%
        mutate({{ category }} := case_when(
          {{ group }} == {{ learning_disability }} ~
            as.character(factor({{ category }},
              levels = c(TRUE, FALSE),
              labels = c(
                "Record of learning disability",
                "No record of learning disability"
              )
            )),
          TRUE ~ {{ category }}
        ))
    }
  } else {
    if (!is.null(care_home)) {
      df <- df %>%
        mutate({{ category }} := case_when(
          {{ group }} == {{ care_home }} ~
            as.character(factor({{ category }},
              levels = c(TRUE, FALSE),
              labels = c(
                "Yes",
                "No"
              )
            )),
          TRUE ~ {{ category }}
        ))
    }

    if (!is.null(learning_disability)) {
      df <- df %>%
        mutate({{ category }} := case_when(
          {{ group }} == {{ learning_disability }} ~
            as.character(factor({{ category }},
              levels = c(TRUE, FALSE),
              labels = c(
                "Yes",
                "No"
              )
            )),
          TRUE ~ {{ category }}
        ))
    }
  }

  if (!is.null(imd)) {
    imd_levels <- c(1:5, "Unknown")
    imd_labels <- c(
      "1 - Most deprived",
      "2", "3", "4",
      "5 - Least deprived",
      "(Missing)"
    )

    df <- df %>%
      mutate({{ category }} := case_when(
        {{ group }} == {{ imd }} ~
          as.character(factor({{ category }},
            levels = imd_levels,
            labels = imd_labels
          )),
        TRUE ~ {{ category }}
      ))
  }

  if (!is.null(sex)) {
    df <- df %>%
      mutate({{ category }} := case_when(
        {{ group }} == {{ sex }} ~
          as.character(factor({{ category }},
            levels = c("F", "M"),
            labels = c("Female", "Male")
          )),
        TRUE ~ {{ category }}
      ))
  }

  return(df)
}
