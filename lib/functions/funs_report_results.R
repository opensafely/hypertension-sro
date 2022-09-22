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

compare_groups <- function(df,
                           variable = c("pct", "numerator", "denominator"),
                           group_var_name, category_var_name,
                           group_a, category_a,
                           group_b, category_b,
                           add_national_median = TRUE) {

                           filter_variable <- match.arg(variable)

                           # Check variables exist in data
                           if (group_var_name %in% names(df) == FALSE | category_var_name %in% names(df) == FALSE) {
                             stop("Variables specified in 'group_var_name' or 'category_var_name' must exist in 'df'")
                           }

                           if (group_var_name == category_var_name) {
                             stop("Two different variables need to be specified for 'group_var_name' and 'category_var_name'.")
                           }

                           # Check categories and groups exist
                           unique_groups <- unique(pull(df, group_var_name))
                           unique_categories <- unique(pull(df, category_var_name))

                           if ((group_a %in% unique_groups & group_b %in% unique_groups) == FALSE) {
                            stop(paste0("'group_a' and 'group_b must exist in 'unique_groups'. Options are: ", paste0(unique_groups, collapse = ", "), "."))
                           }

                           if ((category_a %in% unique_categories & category_b %in% unique_categories) == FALSE) {
                            stop(paste0("'category_a' and 'category_b' must exist in 'category_var_name'. Options are: ", paste0(unique_categories, collapse = ", "), "."))
                           }

                           if (category_a == category_b) {
                             stop("Two different categories need to be specified in 'category_a' and 'category_b'.")
                           }

                           str_var_name_a <- janitor::make_clean_names(paste(group_a, category_a, sep = "_"))
                           str_var_name_b <- janitor::make_clean_names(paste(group_b, category_b, sep = "_"))

                           group_01 <- df |>
                             filter(variable == filter_variable) |>
                             filter(group == group_a) |>
                             filter(category == category_a) |>
                             select(indicator, date, !!str_var_name_a := value)

                           group_02 <- df |>
                             filter(variable == filter_variable) |>
                             filter(group == group_b) |>
                             filter(category == category_b) |>
                             select(indicator, date, !!str_var_name_b := value)
                           
                           group_comparisons <- left_join(group_01, group_02) |>
                             mutate(diff_groups := !!rlang::sym(str_var_name_a) - !!rlang::sym(str_var_name_b))

                           if (variable == "pct" & add_national_median == TRUE) {

                           national_median <- df_measures_bp_hyp |>
                             filter(variable == "decile") |>
                             filter(category == "50") |>
                             select(indicator, date, national_median = value)

                           group_comparisons <- group_comparisons |>
                             left_join(national_median) |>
                             mutate("diff_median_{str_var_name_a}" := national_median - !!rlang::sym(str_var_name_a),
                                    "diff_median_{str_var_name_b}" := national_median - !!rlang::sym(str_var_name_b)) |>
                             relocate(indicator, date, national_median)
                           }

                           return(group_comparisons)

                           }
