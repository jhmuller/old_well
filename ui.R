#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(readr)
library(DT)
library(dplyr)



# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Impact of trades in Japan"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      uiOutput("managerSelector"),      
      selectInput("eventSelector", "Event",
                  choices=c("in_init", "up", "down", "out_init",
                            "in_init|up", "down|out_init"))
    #textInput("stateRegex", "State" , value = "in_init", )
    ),
    # Show a plot of the generated distribution
    mainPanel(
       plotOutput("distPlot"),
       DT::dataTableOutput("statsTable")       
    )
  )
))
