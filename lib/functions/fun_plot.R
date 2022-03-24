#' Plotting function for measures
#'
#' @param df Dataframe from OpenSAFELY "Measures" framework.
#' Expects the following variables: 
#' value (percentage with leading 0, e.g., 0.50 indicates 50%) <dbl>; 
#' date (YYYY-MM-DD) <date>; 
#' group (e.g., age_group) <chr>; 
#' category (e.g., "65+) <chr>
#' @param title String, title of the plot
#' @param legend String, legend position, "none" to remove legend
#'
#' @return ggplot2 object
plot_qof_indicator <- function(df, title = NULL, legend_position = "top", set_y_scale_limits = FALSE, plotly = FALSE, show_label = FALSE) {
  
  # Create plot with legend
  plot <- df %>% 
    ggplot2::ggplot(ggplot2::aes(x = date,
                                 y = value,
                                 colour = category)) +
    ggplot2::geom_line(size = 1,
                       alpha = 0.3) +
    ggplot2::geom_point(size = 2) +
    ggplot2::scale_x_date(date_breaks = "4 month",
                          date_labels = "%b %y") +
    ggplot2::scale_y_continuous(labels = scales::percent) +
    ggplot2::labs(x = NULL,
                  y = "Prevalence",
                  colour = NULL,
                  title = title) +
    ggplot2::theme(text = ggplot2::element_text(size = 14)) +
    ggplot2::scale_color_viridis_d() +
    ggplot2::theme(legend.position = legend_position) 

  if  (set_y_scale_limits) {
    plot <-  plot + ggplot2::scale_y_continuous(labels = scales::percent,
                                                limits = c(0, 1))
  }

  if (show_label) {
    plot <- ggrepel::geom_label_repel(ggplot2::aes(label = ifelse(date == min(date), category, ""),
                            show.legend = FALSE,
                            segment.color = NA))
  }

  # if (plotly) {
  #   # Convert ggplot2 to plotly
  #   plot <- plotly::ggplotly(plot,
  #                            tooltip = "text") %>%
  #           plotly::config(displayModeBar = FALSE) %>% 
  # plotly::layout(legend = list(orientation = "h"))

  # }

  # Return plot
  return(plot)
}
