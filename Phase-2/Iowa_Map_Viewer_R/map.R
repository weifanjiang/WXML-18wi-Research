# load libraries
library(ggplot2)
library(dplyr)
library(maps)
library(sp)
library(maptools)

index <- read.csv("Iowa-election-data.csv", stringsAsFactors = FALSE)
index$County.Name <- tolower(index$County.Name)
index <- index[3:19]
index[71, 15] <- "obrien"

for (i in 0:9) {

  m <- map_data("county", stringsAsFactors = FALSE) %>% filter(region == "iowa")

  colnames(index)[15] <- "subregion"
  m <- m %>% left_join(index, by = "subregion")

  result <- read.csv(paste0("output/output", i, ".csv"), stringsAsFactors = FALSE)
  colnames(result)[1] <- "Alex.number"
  m <- m %>% left_join(result, by = "Alex.number")
  
  p <- ggplot(data = m) +
    geom_polygon(mapping = aes(x = long, y = lat, group = group, fill = factor(district)), color = "white") +
    coord_quickmap() +
    scale_fill_brewer(palette = "Set1")+
    guides(fill = FALSE) +
    theme(panel.background = element_rect(fill = NA, colour = NA)) +
    theme(axis.title.x=element_blank(),
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank(),
          axis.title.y=element_blank(),
          axis.text.y=element_blank(),
          axis.ticks.y=element_blank())
  
  simulation <- m %>% group_by(district) %>% 
    summarise(district_gop_2016 = sum(gop_2016), 
              district_dem_2016 = sum(dem_2016), 
              district_total_2016 = sum(total_2016),
              district_gop_2012 = sum(gop_2012), 
              district_dem_2012 = sum(dem_2012), 
              district_total_2012 = sum(total_2012),
              district_gop_2008 = sum(gop_2008), 
              district_dem_2008 = sum(dem_2008), 
              district_total_2008 = sum(total_2008))
  simulation <- simulation %>% 
    mutate (average_gop = (district_gop_2016 + district_gop_2012 + district_gop_2008) / 3,
            average_dem = (district_dem_2016 + district_dem_2012 + district_dem_2008) / 3,
            average_total = (district_total_2016 + district_total_2012 + district_total_2008) / 3)
  simulation <- simulation %>% 
    mutate (winner_dem_2008 = (district_dem_2008 >= district_gop_2008),
            winner_dem_2012 = (district_dem_2012 >= district_gop_2012),
            winner_dem_2016 = (district_dem_2016 >= district_gop_2016),
            winner_dem_total = (average_dem >= average_gop))
  
  simul.data <- m %>% left_join(simulation, by = "district")
  
  s <- ggplot(data = simul.data) +
    geom_polygon(mapping = aes(x = long, y = lat, group = group, fill = factor(winner_dem_2016), color = "white")) +
    coord_quickmap() +
    scale_fill_manual(values = c("red", "blue")) +
    scale_color_manual(name = "district", values = c("yellow", "green", "magenta", "black")) +
    guides(fill = FALSE, color = FALSE) +
    theme(panel.background = element_rect(fill = NA)) +
    theme(axis.title.x=element_blank(),
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank(),
          axis.title.y=element_blank(),
          axis.text.y=element_blank(),
          axis.ticks.y=element_blank())
  
  
  
  png(filename=paste0("redistricting/redistricting", i ,".png"), width = 960, height = 720)
  plot(p)
  dev.off()
  
  png(filename=paste0("redistricting/simulation", i ,".png"), width = 960, height = 720)
  plot(s)
  dev.off()
}