library(xml2)
library(ggplot2)
library(dplyr)

url <- "http://ergast.com/api/f1/2024/18/laps.xml"
lap_data <- read_xml(url)
