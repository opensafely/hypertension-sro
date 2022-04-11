#' Plotting function for measures
#'
#' @param df Dataframe from OpenSAFELY "Measures" framework.
#' Expects the following variables:
#' value (percentage with leading 0, e.g., 0.50 indicates 50%) <dbl>;
#' date (YYYY-MM-DD) <date>;
#' group (e.g., age_group) <chr>;
#' category (e.g., "65+) <chr>
#' @param df Dataframe
#' @param value variable name
#' @param y_scale String, specifying wheather variable `value` is
#' (i) in percent (where 0.5 indicates 50%) or
#' (ii) a count
#' @param title String, specifying title of plot
#' @param legend_position String, legend position, "none" to remove legend
#' @param x_label String, specifying x label
#' @param y_label String, specifying y label
#' @param set_y_scale_limits Logical, when  y_scale argument = "percent"
#' specifying whether to set y scale limits
#' @param vline_nhs_fy Logical, specifying whether to show NHS financial year
#' @param show_label Logical, specifying whether to show label

#'
#' @return ggplot2 object
plot_qof_indicator <- function(df,
                               value,
                               y_scale = c("percent", "count"),
                               title = NULL,
                               legend_position = "top",
                               x_scale_date_breaks = "4 months",
                               x_label = NULL,
                               y_label = NULL,
                               set_y_scale_limits = FALSE,
                               vline_nhs_fy = TRUE,
                               vline_1st_national_lockdown = FALSE,
                               show_label = FALSE) {
  y_scale <- match.arg(y_scale)

  # Create plot with legend
  plot <- df %>%
    ggplot2::ggplot(ggplot2::aes(
      x = date,
      y = {{ value }},
      colour = category
    )) +
    ggplot2::geom_line(
      size = 1,
      alpha = 0.3
    ) +
    ggplot2::geom_point(size = 2) +
    ggplot2::scale_x_date(
      date_breaks = x_scale_date_breaks,
      date_labels = "%b %y"
    ) +
    ggplot2::labs(
      x = x_label,
      y = y_label,
      colour = NULL,
      title = title
    ) +
    ggplot2::scale_color_viridis_d(na.value = "grey50") +
    ggplot2::theme_classic() +
    ggplot2::theme(legend.position = legend_position) +
    ggplot2::theme(text = ggplot2::element_text(size = 14))


  if (y_scale == "percent") {
    plot <- plot +
      ggplot2::scale_y_continuous(labels = scales::percent)

    if (set_y_scale_limits) {
      plot <- plot +
        ggplot2::scale_y_continuous(
          labels = scales::percent,
          limits = c(0, 1)
        )
    }
  } else if (y_scale == "count") {
    plot <- plot +
      ggplot2::scale_y_continuous(labels = scales::comma) +
      ggplot2::expand_limits(y = 0)
  }

  if (show_label) {
    plot <- plot +
      ggrepel::geom_label_repel(ggplot2::aes(label = ifelse(date == min(date), category, "")),
        show.legend = FALSE,
        segment.color = NA
      )
  }

  if (vline_nhs_fy) {
    # Extract all Aprils
    list_nhs_financial_years <- unique(df$date[lubridate::month(df$date) == 4])

    plot <- plot +
      ggplot2::geom_vline(
        xintercept = lubridate::as_date(list_nhs_financial_years),
        linetype = "dotted",
        colour = "orange",
        size = 1
      )
  }

  if (vline_1st_national_lockdown) {
    plot <- plot +
      ggplot2::geom_vline(
        xintercept = lubridate::as_date("2020-03-01"),
        linetype = "dotted",
        colour = "#00ffa2",
        size = 1
      )
  }

  # Return plot
  return(plot)
}
