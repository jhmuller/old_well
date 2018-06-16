library(tidyr)
library(dplyr)
library(ggplot2)
library(readr)
library(lubridate)


indir <- "data_derived"

states <- readr::read_csv(file.path(indir, "states.csv"))
returns <- readr::read_csv(file.path(indir, "returns.csv"))

states[states$state == "up" && states$pct < 5]

glimpse(returns)
glimpse(states)
combo <- merge(states, returns, by.x=c("date", "gempermid"),
               by.y=c("date", "gempermid"))

glimpse(combo)

goin <- combo %>%
  filter(state %in% c("in", "out"))

ggplot(goin, aes(x=pct, y=ret360, col=state)) + geom_point() + facet_wrap(~name) 



mngrs <- events %>% group_by(name) %>%
  summarise(cnt = n(),
            cnt_coms = n_distinct(comname),
            min_dt = min(holddate),
            max_dt = max(holddate),
            sum_sharesadj = sum(shareshldadj)) %>%
  arrange(cnt_coms)  



nrow(mngrs)
head(mngrs)
tail(mngrs)
nrow(coms)


mngr <- filter(events, grepl("Ichi",name))
glimpse(mngr)
ggplot(mngr, aes(x=holddate, y=pctshouthld, col=comname)) + geom_line() + geom_point()

bad <- filter(events, pctshouthld < 5)
bad
