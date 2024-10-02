# Load required libraries
library(XML)
library(xml2)
library(ggplot2)
library(dplyr)

# Laptimes of Norris
url <- "http://ergast.com/api/f1/2024/18/drivers/norris/laps.xml?limit=62"
lap_data <- read_xml(url)

# Extract namespaces (important for selecting nodes)
ns <- xml_ns(lap_data)

# Find all 'Timing' nodes using the correct namespace
lap_nodes <- xml_find_all(lap_data, "//d1:Timing", ns = ns)

# Extract data from the nodes and convert to dataframe
lap_list <- lapply(lap_nodes, function(Timing) {
  lap_number <- xml_attr(Timing, "lap")
  lap_time <- xml_attr(Timing, "time")
  lap_position <- xml_attr(Timing, "position")
  
  # Return a named list for each lap
  return(list(
    lap_number = as.integer(lap_number),
    lap_time = as.numeric(gsub("[:]", "", lap_time)), # Remove colon for time conversion
    lap_position = as.integer(lap_position)
  ))
})

# Convert the list to a dataframe
lap_df <- bind_rows(lap_list)

# Check the dataframe
print(lap_df)

# Convert lap_time to a numeric value (if necessary, ensure it's numeric)
lap_df <- lap_df %>%
  mutate(lap_time = as.numeric(lap_time))

# Create a ggplot of lap times vs. lap number
ggplot(lap_df, aes(x = lap_number, y = lap_time)) +
  geom_line(color = "blue") +
  geom_point(color = "red") +
  labs(title = "Lando Norris Lap Times - 2024 Race",
       x = "Lap Number",
       y = "Lap Time (in seconds)") +
  theme_minimal()
