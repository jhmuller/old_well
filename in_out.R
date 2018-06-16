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



mngr_names <- colnames(select(states, -end_date, -gempermid))
glimpse(states)
i <- 1
mngr_name <- mngr_names[i]
state <- "in"
mngr = states[, c("gempermid", mngr_name, "end_date")]
temp <- filter(mngr, grepl(state, UQ(as.name(mngr_name))) )
nrow(temp)
temp
colnames(temp)[3] = "date"
combo <- merge(temp, returns_long, by.x=c("date", "gempermid"),
               by.y=c("date", "gempermid"))
nrow(combo)
ggplot(combo) + geom_boxplot(aes(x=dir, y=return )) + 
  facet_wrap(~months) + ggtitle(name, subtitle=state) +
 ylim(c(-1, 1)) 

combo[combo$months == "12mo",]



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
