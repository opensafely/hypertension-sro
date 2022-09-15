#' Report count and percentage of measures
#'
#' @param df Data frame. Requires the variables named "date", "group", "category" used for filtering
#' @param var_value Name of variable with count or percent values
#' @param date String, specifying value for filtering date
#' @param group String, specifying value for filtering date
#' @param category String, specifying value for filtering date
#' @param convert_percent Logical, whether to convert percent (0.1) to 10.00%
#'
#' @return
#' @export
#'
#' @examples
report_measures <- function(df,
                            var_value,
                            filter_date, filter_group, filter_category,
                            convert_percent = TRUE) {
  report_value <- df %>%
    filter(date == filter_date) %>%
    filter(group == filter_group) %>%
    filter(category == filter_category) %>%
    pull({{ var_value }})

  if (convert_percent) {
    if (report_value <= 1) {
      report_value <- scales::percent(report_value, accuracy = 0.01)
    } else {
      warning(paste0("value is greater than 1 (", report_value, ") and not converted to %."),
        call. = FALSE
      )
    }
  }

  return(report_value)
}

summary_report_min_max <- function(df, filter_group, filter_variable = c("pct", "numerator", "denominator", "population", "decile")) {
  df_min <- df |>
    filter(group == {{ filter_group }}) |>
    filter(variable == {{ filter_variable }}) |>
    group_by(indicator, variable) |>
    slice_min(value, n = 1)

  df_max <- df |>
    filter(group == {{ filter_group }}) |>
    filter(variable == {{ filter_variable }}) |>
    group_by(indicator, variable) |>
    slice_max(value, n = 1)

  df_diff <- bind_rows(df_min, df_max) |>
    arrange(indicator, date, variable) |>
    group_by(indicator, variable) |>
    mutate(diff = value - lag(value))

  df_diff
}


report_national_median <- function(df, filter_date = NULL) {
  df <- df |>
    filter(variable == "decile") |>
    filter(category == "50") |>
    pivot_wider(names_from = indicator, values_from = value)

  if (is.null(filter_date)) {
    df
  } else {
    df |>
      filter(date == filter_date)
  }
}

report_group_pct <- function(df, filter_group, filter_category = NULL, filter_date = NULL) {
  df <- df |>
    filter(variable == "pct") |>
    filter(group == filter_group) |>
    pivot_wider(names_from = indicator, values_from = value)


  if (!is.null(filter_category)) {
    df <- df |>
      filter(category == filter_category)
  }

  if (is.null(filter_date)) {
    df
  } else {
    df |>
      filter(date == filter_date)
  }
}
