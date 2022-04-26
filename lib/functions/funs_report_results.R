
report_measures <- function(df, value, date, group, category, convert_percent = TRUE) {
  
  report_value <- df %>% 
    filter(date == {{ date }}) %>% 
    filter(group == {{ group }}) %>% 
    filter(category == {{ category }}) %>% 
    pull({{ value }})
  
  if (convert_percent) {
    
    if (report_value <= 1) {
      report_value <-  scales::percent(report_value, accuracy = 0.01)
    } else {
        warning(paste0("value is greater than 1 (", report_value, ") and not converted to %."), 
                call. = FALSE)
      }
    }
  
  return(report_value)
  
  }