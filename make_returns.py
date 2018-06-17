import os
import datetime
import pandas as pd
import utils

def main():
    indir = "data_derived"
    prices = pd.DataFrame.from_csv(os.path.join(indir, "prices.csv"), index_col=False)

    tmp = pd.to_datetime(prices.marketdate)
    prices["date"] = [d.date() for d in tmp]

    min_date = datetime.date(2005, 1, 1)
    max_date = prices.date.max()
    start = min_date

    fulldf = pd.DataFrame()
    diter = utils.month_iterator(first=min_date, last=max_date)
    dflist = []
    for date in diter:
        print(date)
        datedf = pd.DataFrame()
        for nmonths in [1, 3, 6, 9, 12, 15]:
            fwd_month = utils.add_months(date, n=nmonths)
            next_ser = utils.gross_period_returns(df=prices,
                                                  id_col="gempermid",
                                                  date_col="date",
                                                  value_col="close_",
                                                  start=date,
                                                  end=fwd_month)
            back_month = utils.add_months(date, n=-nmonths)
            back_ser = utils.gross_period_returns(df=prices,
                                                  id_col="gempermid",
                                                  date_col="date",
                                                  value_col="close_",
                                                  start=back_month,
                                                  end=date)
            print("N= %d back= %s, Fwd= %s" % (nmonths, str(back_month), str(fwd_month)))
            df = pd.merge(back_ser.to_frame(), next_ser.to_frame(), left_index=True, right_index=True, how="outer")
            df.columns = ["back_%d" % (nmonths,), "fwd_%d" % (nmonths,)]
            df["backmo_%s" %(back_month,)] = back_month
            df["fwdmo_%s" % (fwd_month,)] = fwd_month
            datedf = (df if (datedf.shape[0] == 0)
                      else pd.merge(datedf, df, how="outer", left_index=True, right_index=True))
        datedf["date"] = date
        dflist.append(datedf)
        #print(datedf.tail())
    fulldf = pd.concat(dflist)
    odir = "data_derived"
    if (not os.path.isdir(odir)):
        os.makedirs(odir)
    fulldf.to_csv(os.path.join(odir, "returns.csv"))
    print("done")

if __name__ == "__main__":
    main()