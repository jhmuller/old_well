#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(readr)
library(DT)
library(dplyr)
library(tidyr)
library(ggplot2)

indir <- file.path( "data_derived")
print(indir)
states <- readr::read_csv(file.path( indir, "states.csv"))
colnames(states)[1] = "gempermid"
colnames(states) <-  gsub(" ", "_", colnames(states))
colnames(states)[length(colnames(states))] = "date"

mngr_names <- colnames(select(states, -date, -gempermid))


returns_wide <- readr::read_csv(file.path(indir, "returns.csv"))

returns_long <- returns_wide %>%
  gather(key, return, -c(date, gempermid)) %>%
  separate(key, c("dir", "months"), "_")
returns_long$months <- as.factor(as.numeric(returns_long$months))




combo <- merge(states, returns_long, by.x=c("date", "gempermid"),
               by.y=c("date", "gempermid"))

glimpse(combo)

mngr_name <- mngr_names[1]


# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  
  output$managerSelector <- renderUI({
    selectInput("Manager", "Choose Manager:", as.list(mngr_names)) 
  })
  
  
  output$distPlot <- renderPlot({
    
    state = input$eventSelector
    mngr_name <- input$Manager
    if (FALSE){
      mngr = states[, c("gempermid", mngr_name, "end_date")]
      temp <- filter(mngr, grepl(state, UQ(as.name(mngr_name))) )

      colnames(temp)[3] = "date"
      combo <- merge(temp, returns_long, by.x=c("date", "gempermid"),
                   by.y=c("date", "gempermid"))
    }
    
    qmngr <- enquo(mngr_name)
    temp <- select(combo, date, !! qmngr, dir, months, return)
    temp2 <- filter(temp, grepl(state, UQ(as.name(mngr_name))) )
    
    ggplot(temp2) + geom_boxplot(aes(x=dir, y=return )) + 
      facet_wrap(~months, labeller="label_both") + 
      ggtitle(paste("Manager: ",mngr_name), 
              subtitle=paste("event: ",state)) +
      coord_cartesian(ylim = c(-.5, .5)) +  geom_hline(yintercept = 0, col="blue")
    
  })
  
  output$statsTable <- DT::renderDataTable({
    state = input$eventSelector
    mngr_name <- input$Manager
    
    if (FALSE){
      mngr = states[, c("gempermid", mngr_name, "end_date")]
      temp <- filter(mngr, grepl(state, UQ(as.name(mngr_name))) )
      colnames(temp)[3] = "date"
      combo <- merge(temp, returns_long, by.x=c("date", "gempermid"),
                   by.y=c("date", "gempermid"))
    }
    qmngr <- enquo(mngr_name)
    temp <- select(combo, date, !! qmngr, dir, months, return)
    temp2 <- filter(temp, grepl(state, UQ(as.name(mngr_name))) )
    
    sTable <- temp2 %>% group_by(months,dir) %>%
      summarise(Avg=mean(return, na.rm=TRUE),
                Median = median(return, na.rm=TRUE), 
                StdDev=sd(return, na.rm=TRUE),
                StdErr=sd(return, na.rm=TRUE) / sqrt(n()),                
                n=n()) %>%
      arrange(months)
    sTable$Avg <- round(x = sTable$Avg,digits = 3)
    sTable$StdDev <- round(x = sTable$StdDev,digits = 3)
    sTable$Median <- round(x = sTable$Median,digits = 3)
    sTable$StdErr <- round(x = sTable$StdErr,digits = 3)    
    sTable
  }, options = list(sDom  = '<"top">t<"bottom">'))
  
})
