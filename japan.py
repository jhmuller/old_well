import pandas as pd
import datetime
import numpy as np
import os

prices = pd.DataFrame.from_csv("data/prices.csv", index_col=False)

tmp = pd.to_datetime(prices.marketdate)
prices["date"] = [d.date() for d in tmp]

def date_filter(df, date_col, start, end):
    print(type(end))
    print(type(df[date_col][1]))
    res = df[np.logical_and(df[date_col] >= start,
                            df[date_col] < end)]
    return (res)


def sum_max(df, group_cols, value_col):
    grp = group_cols + [value_col]
    res = df[grp].groupby(group_cols).sum().max()
    return (res)


def qtile_mean(df, group_cols, value_col, qtile):
    grp = group_cols + [value_col]
    res = df[grp].groupby(group_cols).quantile(qtile).mean()
    return (res)


def gross_period_returns(df, date_col, value_col, id_col, start, end):
    cols = [date_col, value_col, id_col]

    tmp = df[cols][df[date_col] <= start]
    tmp.sort_values(by=date_col, inplace=True)
    tmp = tmp.drop_duplicates(subset=id_col, keep="last")
    tmp.set_index(id_col, inplace=True)
    start_vals = tmp[value_col]

    tmp = df[cols][df[date_col] >= end]
    tmp.sort_values(by=date_col, inplace=True)
    tmp = tmp.drop_duplicates(subset=id_col, keep="first")
    tmp.set_index(id_col, inplace=True)
    end_vals = tmp[value_col]

    res = (end_vals - start_vals) / start_vals
    return (res)

def gross_nday_returns(df, date_col, id_col, value_col, start, ndays=30):
    end = start + datetime.timedelta(days=ndays)
    res = gross_period_returns(df=df, date_col=date_col, value_col=value_col, id_col=id_col,
                               start=start, end=end)
    return (res)

def date_iterator(first, last, incr_days=20 ):
    res = first
    while res <= last:
        yield res
        res = res + datetime.timedelta(days=incr_days)

min_date = prices.date.min()
max_date = prices.date.max()
start = min_date

fulldf = pd.DataFrame()
diter = date_iterator(first=min_date, last=max_date, incr_days=30)
for date in diter:
    print (date)
    datedf = pd.DataFrame()
    for ndays in [30, 90, 180, 360]:
        ser = gross_nday_returns(df=prices,
                               id_col="gempermid",
                               date_col="date",
                               value_col="close_",
                               start=date,
                               ndays=ndays)
        df = pd.DataFrame(ser)
        df.columns = ["ret%d" % (ndays)]
        datedf = (df if (datedf.shape[0] == 0)
                else pd.merge(datedf, df, how="outer", left_index=True, right_index=True))
        print(datedf.shape)
    datedf["date"] = date
    fulldf = (datedf if fulldf.shape[0] == 0 else
               pd.concat([fulldf, datedf]))
    print (fulldf.tail())

    print('')
if (not os.path.isdir("output")):
    os.makedirs("output")
fulldf.to_csv("output/returns.csv")
print ("done")