import datetime
import copy
import pandas as pd
import numpy as np


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
    datedf = df[cols][np.logical_and(df[date_col] >= start,
                                     df[date_col] <= end)]

    datedf.sort_values(by=date_col, inplace=True)
    datedf = datedf[ np.isfinite(datedf[value_col])]

    tmp = datedf.drop_duplicates(subset=id_col, keep="first")
    tmp.set_index(id_col, inplace=True)
    start_vals = tmp[value_col]

    tmp = datedf.drop_duplicates(subset=id_col, keep="last")
    tmp.set_index(id_col, inplace=True)
    end_vals = tmp[value_col]

    res = (end_vals - start_vals) / start_vals
    return (res)

def gross_nday_returns(df, date_col, id_col, value_col, start, ndays=30):
    end = start + datetime.timedelta(days=ndays)
    res = gross_period_returns(df=df, date_col=date_col, value_col=value_col, id_col=id_col,
                               start=start, end=end)
    return (res)

def prev_month(date):
    year = date.year
    month = date.month
    day = date.day
    if month == 1:
        year = year - 1
    else:
        month = month - 1
    res = datetime.date(year, month, day)
    return (res)

def next_month(date):
    year = date.year
    month = date.month
    day = date.day
    if month == 12:
        year = year + 1
    else:
        month = month + 1
    res = datetime.date(year, month, day)
    return (res)

def add_months(date, n):
    (yadd, month) = divmod(n + date.month, 12)
    year = date.year + yadd
    if month == 0:
        month = 12
        year = year - 1
    day = date.day
    res = datetime.date(year, month, day)
    return (res)

def gross_nmonth_returns(df, date_col, id_col, value_col, start, nmonths=1):
    end = add_months(start, nmonths)
    res = gross_period_returns(df=df, date_col=date_col, value_col=value_col, id_col=id_col,
                               start=start, end=end)
    return (res)

def month_iterator(first, last ):
    res = copy.copy(first)
    while res <= last:
        yield res
        year = res.year
        month = res.month
        day = res.day
        if month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1
        day = 1
        res = datetime.date(year, month, day)

def date_from_string(df, date_str):
    tmp = pd.to_datetime(df[date_str])
    res = [d.date() for d in tmp]
    return (res)

if __name__ == "__main__":
    date = datetime.date(2018, 1, 1)
    n = -2
    res = add_months(date, n)
    assert (res == datetime.date(2017, 11, 1)), "Error adding %d res=%s" % (n,str(res))

    date = datetime.date(2017, 11, 1)
    n = 12
    res = add_months(date, n)
    assert(res == datetime.date(2018, 11, 1)), "Error adding %d res=%s" % (n,str(res))

    date =  datetime.date(2018, 11, 1)
    n = -14
    res = add_months(date, n)
    assert (res == datetime.date(2017, 9, 1)), "Error adding %d res=%s" % (n,str(res))

    date = datetime.date(2016, 12, 1)
    n = -12
    res = add_months(date, n)
    assert(res == datetime.date(2015, 12, 1)), "Error adding %d res=%s" % (n,str(res))

    date = datetime.date(2016, 12, 1)
    n = 12
    res = add_months(date, n)
    assert(res == datetime.date(2017, 12, 1)), "Error adding %d res=%s" % (n,str(res))


