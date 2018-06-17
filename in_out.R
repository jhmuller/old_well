library(tidyr)
library(dplyr)
library(ggplot2)
library(readr)
library(lubridate)
library(magrittr)
library(dplyr)
library(stringr)

indir <- "data_derived"
prices <- readr::read_csv(file.path(indir, "prices.csv"))
prices[prices$gempermid == 8589996697,]

states <- readr::read_csv(file.path(indir, "states.csv"))
colnames(states)[1] = "gempermid"
colnames(states) <-  gsub(" ", "_", colnames(states))

returns_wide <- readr::read_csv(file.path(indir, "returns.csv"))

returns_long <- returns_wide %>%
  gather(key, return, -c(date, gempermid)) %>%
  separate(key, c("dir", "months"), "_")
returns_long$months <- as.factor(as.numeric(returns_long$months))

mngr_names <- colnames(select(states, -end_date, -gempermid))
glimpse(states)
i <- 5
mngr_name <- mngr_names[i]
state <- "up"
mngr = states[, c("gempermid", mngr_name, "end_date")]
temp <- filter(mngr, grepl(state, UQ(as.name(mngr_name))) )
nrow(temp)
temp
colnames(temp)[3] = "date"
combo <- merge(temp, returns_long, by.x=c("date", "gempermid"),
               by.y=c("date", "gempermid"))
nrow(combo)
ggplot(combo) + geom_boxplot(aes(x=dir, y=return )) + 
  facet_wrap(~months, labeller="label_both") + ggtitle(mngr_name, subtitle=state) +
  coord_cartesian(ylim = c(-.5, .5)) 


combo %>% group_by(months,dir) %>%
  summarise(mn=mean(return, na.rm=TRUE),
            p25=quantile(return, probs=0.25),   
            p45=quantile(return, probs=0.45),             
            md = median(return, na.rm=TRUE), 
            p55=quantile(return, probs=0.55),             
            p75=quantile(return, probs=0.75), 
            se=sd(return, na.rm=TRUE)/sqrt(n()),
            sd=sd(return, na.rm=TRUE),
            n=n()) %>%
  arrange(months, )


