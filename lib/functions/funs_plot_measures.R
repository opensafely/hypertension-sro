# TODO DOCUMENT THIS FUNCTION
plot_qof_values <- function(df,
                            point_size = .7,
                            line_size = .5,
                            line_alpha = 1,
                            date_breaks = NULL,
                            ylab = c("Prevalence", "% of patients receiving indicated care"),
                            legend_position = "top",
                            legend_top_nrow = 1,
                            legend_label = NULL,
                            text_size = 14,
                            facet_wrap = TRUE,
                            facet_wrap_var = indicator,
                            facet_wrap_ncol = 3,
                            axis_x_text_size = 10) {
  plot <- df |>
    ggplot(aes(
      x = date,
      y = value,
      colour = subgroup
    )) +
    geom_vline(
      xintercept = lubridate::as_date(c(
        "2019-03-01", "2020-03-01",
        "2021-03-01", "2022-03-01"
      )),
      linetype = "dotted",
      colour = "orange",
      size = .7
    ) +
    geom_point(size = point_size) +
    geom_line(
      size = line_size,
      alpha = line_alpha
    ) +
    scale_x_date(
      breaks = date_breaks,
      labels = scales::label_date_short()
    ) +
    scale_y_continuous(labels = scales::label_percent()) +
    scale_colour_viridis_d(direction = -1) +
    labs(x = NULL, y = ylab, colour = legend_label, title = legend_label) +
    theme(
      legend.position = legend_position,
      text = element_text(size = text_size),
      axis.text.x = element_text(size = axis_x_text_size)
    )

  if (legend_position == "top") {
    plot <- plot + guides(
      colour = guide_legend(nrow = legend_top_nrow),
      group = guide_legend(nrow = legend_top_nrow),
      size = guide_legend(nrow = legend_top_nrow),
      linetype = guide_legend(nrow = legend_top_nrow)
    )
  }


  if (facet_wrap) {
    plot + facet_wrap(vars({{ facet_wrap_var }}), ncol = facet_wrap_ncol)
  } else {
    plot
  }
}


plot_qof_deciles <- function(df,
                             date_breaks = NULL,
                             ylab = c("Prevalence", "% Achievement"),
                             ylimits = c(0, 1),
                             ybreaks = seq(0, 1, .25),
                             scale_size_manual = c(.4, .4, .5, .6, .8, .6, .5, .4, .4),
                             text_size = 14,
                             legend_label = NULL,
                             legend_position = "top",
                             legend_top_nrow = 1,
                             axis_x_text_size = 10,
                             facet_wrap = TRUE,
                             facet_wrap_var = indicator) {
  plot <- df |>
    ggplot(aes(
      x = date,
      y = value,
      colour = percentile,
      group = percentile,
      size = percentile
    )) +
    geom_vline(
      xintercept = lubridate::as_date(c(
        "2019-03-01", "2020-03-01",
        "2021-03-01", "2022-03-01"
      )),
      linetype = "dotted",
      colour = "orange",
      size = .7
    ) +
    geom_point(alpha = 1) +
    geom_line(alpha = 1) +
    scale_size_manual(values = scale_size_manual) +
    scale_y_continuous(
      labels = scales::label_percent(),
      limits = ylimits,
      breaks = ybreaks
    ) +
    scale_x_date(
      breaks = date_breaks,
      labels = scales::label_date_short()
    ) +
    labs(x = NULL, y = ylab,
      colour = legend_label,
      linetype = legend_label,
      size = legend_label) +
    theme(legend.position = legend_position) +
    scale_colour_manual(values = c(
      "#9ecae1", "#6baed6", "#4292c6", "#2171b5",
      "#084594",
      "#2171b5", "#4292c6", "#6baed6", "#9ecae1"
    )) +
    theme(text = element_text(size = text_size), axis.text.x = element_text(size = axis_x_text_size))

  if (legend_position == "top") {
    plot <- plot + guides(
      colour = guide_legend(nrow = legend_top_nrow),
      group = guide_legend(nrow = legend_top_nrow),
      size = guide_legend(nrow = legend_top_nrow),
      linetype = guide_legend(nrow = legend_top_nrow)
    )
  }

  if (facet_wrap) {
    plot + facet_wrap(vars({{ facet_wrap_var }}), ncol = 3)
  } else {
    plot
  }
}
