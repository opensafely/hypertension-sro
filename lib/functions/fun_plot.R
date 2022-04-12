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
                               scale_colour = c("viridis", "brewer_dark2", "brewer_set1"),
                               title = NULL,
                               legend_position = "top",
                               x_scale_date_breaks = "4 months",
                               x_label = NULL,
                               y_label = NULL,
                               set_y_scale_limits = FALSE,
                               vline_nhs_fy = TRUE,
                               vline_1st_national_lockdown = FALSE,
                               plotly = FALSE,
                               show_label = FALSE) {
  # Check arguments                               
  y_scale <- match.arg(y_scale)
  scale_colour <- match.arg(scale_colour)

  # Create initial plot
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
    ggplot2::theme_classic() +
    ggplot2::theme(legend.position = legend_position) +
    ggplot2::theme(text = ggplot2::element_text(size = 14))

  # Add labels for y axis (pct or counts)
  if (y_scale == "percent") {
    plot <- plot +
        ggplot2::geom_point(ggplot2::aes(text = paste0("<b>Date:</b> ", 
                           lubridate::month(date, label = TRUE), " ",
                           lubridate::year(date), "<br>",
                           "<b>Percent:</b> ", scales::percent({{value}}, accuracy = 0.01))),
                        size = 1.5) +
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
      ggplot2::geom_point(ggplot2::aes(text = paste0("<b>Date:</b> ", 
                           lubridate::month(date, label = TRUE), " ",
                           lubridate::year(date), "<br>",
                           "<b>Count:</b> ", scales::comma({{value}}))),
                        size = 1.5) +
      ggplot2::scale_y_continuous(labels = scales::comma) +
      ggplot2::expand_limits(y = 0)
  }

  # Add label
  if (show_label) {
    plot <- plot +
      ggrepel::geom_label_repel(ggplot2::aes(label = ifelse(date == min(date), category, "")),
        show.legend = FALSE,
        segment.color = NA
      )
  }

  # Add vertical lines for nhs financial year
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

  # Add vertical line for first national lockdown
  if (vline_1st_national_lockdown) {
    plot <- plot +
      ggplot2::geom_vline(
        xintercept = lubridate::as_date("2020-03-01"),
        linetype = "dotted",
        colour = "#00ffa2",
        size = 1
      )
  }

  # Add colour palette
  if (scale_colour == "viridis") {
      plot <- plot +
        ggplot2::scale_color_viridis_d(na.value = "grey50")
  } else if (scale_colour == "brewer_dark2") {
      plot <- plot +
        ggplot2::scale_colour_brewer(palette = "Dark2")
  } else if (scale_colour == "brewer_set1") {
      plot <- plot +
        ggplot2::scale_colour_brewer(palette = "Set1")
  }

  # Convert to plotly
  if (plotly) {
  plot <- plotly::ggplotly(plot,
                             tooltip = "text") %>%
            plotly::config(displayModeBar = FALSE) %>% 
  plotly::layout(legend = list(orientation = "h"))
  }

  # Return plot
  return(plot)
}
