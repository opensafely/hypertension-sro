# Get file names and path ----
dir_hyp_003_measures <- fs::dir_ls(path = "output/",
                                   glob = "*hyp003*.csv$")
                                   
# Load files ----
df_hyp_003_measures <- dir_hyp_003_measures %>%
  map(read_csv) %>%
  map_dfr(pivot_longer,
          cols = 1,
          names_to = "group",
          values_to = "category",
          values_transform = list(category = as.character))

# Get file names and path ----
dir_hyp_007_measures <- fs::dir_ls(path = "output/",
                                   glob = "*hyp007*.csv$")

# Load files ----
df_hyp_007_measures <- dir_hyp_007_measures %>%
  map(read_csv) %>%
  map_dfr(pivot_longer,
          cols = 1,
          names_to = "group",
          values_to = "category",
          values_transform = list(category = as.character))