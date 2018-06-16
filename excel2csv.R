library(readxl)
library(tibble)
library(tidyr)
library(dplyr)
library(readr)


fpath <- "data_orig/japan-data-2018-06-12.xlsx"


odir <- "data_derived"
dir.create(odir, showWarnings = TRUE)

for (si in 1:length(sheets)) {
  sheet <- sheets[si]
  print(paste(si, sheet))
  df <- read_xlsx(fpath, sheet=sheet)
  tbl <- tbl_df(df)
  newpath <- file.path(odir, paste0(sheet,".csv"))
  write_csv(tbl, newpath)
  assign(sheet, tbl)
}
