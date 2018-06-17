import os
import datetime
import pandas as pd
import numpy as np
import utils

indir = "data_derived"
events = pd.DataFrame.from_csv(os.path.join(indir, "events.csv"), index_col=False)
events['date'] = utils.date_from_string(df=events, date_str="holddate")

names = events.name.unique()
gids = events.gempermid.unique()

start_date = datetime.date(2009, 1, 1)
end_date = datetime.date(2018, 1, 1)

incr_days = 30
diter = utils.date_iterator(first=start_date, last=end_date, incr_days=incr_days)

fulldf = pd.DataFrame()
prevfull = pd.DataFrame(columns = ['name', 'gempermid', 'pctchouthld', 'state', 'pct'])
prev_date = start_date - datetime.timedelta(incr_days)
evlist = []
for date in diter:
    print (date)
    datedf = pd.DataFrame()
    newev = dict()
    ev = utils.date_filter(df=events, date_col="date", start=prev_date,
                       end=date)
    if ev.shape[0] == 0:
        continue
    ev.sort_values(by="date", inplace=True)
    ev.drop_duplicates(subset=['name', 'gempermid'], inplace=True)
    for idx, ser in ev.iterrows():
        name = ser['name']
        cid = ser['gempermid']
        pct = ser['pctshouthld']
        key = (name, cid)
        newev = dict(name=name, gempermid=cid, pct=pct, date=date)
        try:
            temp = prevfull[np.logical_and(prevfull.name == name,
                                       prevfull.gempermid == cid)]
            lastev = (dict() if temp.shape[0] == 0
                        else temp.ix[temp.index[0]].to_dict())
        except Exception as exc:
            print (exc)
            lastev = dict()
        if pct < 5.0:
            newev["state"] = "out"
        elif lastev.get("state", "out") == "out":
            newev["state"] = "in_init"
        else:
            if pct >= 0:
                newev["state"] = "in_up"
            else:
                newev["state"] = "in_down"
        evlist.append(newev)
    #print (evlist)
    prevmon = pd.DataFrame(evlist)
    prevfull = (prevmon if prevfull.shape[0] == 0
                else pd.concat([prevfull, prevmon]))
    prevfull.sort_values(by=["date", "name", "gempermid"], ascending=False)
    #print (prevev)
    print ('')
evdf = pd.DataFrame(evlist)
evdf.to_csv(os.path.join("data_derived", "states.csv"))
print (evdf)


print ("done")