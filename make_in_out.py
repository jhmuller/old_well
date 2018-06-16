import os
import datetime
import pandas as pd
import re
import numpy as np
import utils

indir = "data_derived"
events = pd.DataFrame.from_csv(os.path.join(indir, "events.csv"), index_col=False)
events['date'] = utils.date_from_string(df=events, date_str="holddate")

names = list(events.name.unique())
#names = [re.sub(" ","_", name) for name in names]
gids = events.gempermid.unique()

start_date =  datetime.date(2005, 1, 1)
end_date = datetime.date(2018, 1, 1)

incr_days = 30
diter = utils.month_iterator(first=start_date, last=end_date)

fulldf = pd.DataFrame(columns= names + ["end_date"])
for start_date in diter:
    print (start_date)
    end_date = utils.add_months(start_date, n=1)
    ev = utils.date_filter(df=events, date_col="date", start=start_date,
                       end=end_date)
    if ev.shape[0] == 0:
        continue
    ev.sort_values(by="date", inplace=True)
    ev.drop_duplicates(subset=['name', 'gempermid'], inplace=True)

    thisdf = pd.DataFrame(columns=names + ["end_date"],
                          index=gids)

    thisdf["end_date"] = end_date

    lastdf = fulldf[fulldf.end_date == start_date]

    for name in names:
        for gid in gids:
            if lastdf.shape[0] > 0:
                laststate = lastdf[name].ix[gid]
            else:
                laststate = ("none", 0.0)

            if laststate[0] == "none":
                state = ("none", 0.0)
            else:
                state = ("unch", laststate[1])
            thisdf[name].ix[gid] = state

    for idx, ser in ev.iterrows():
        name = ser['name']
        gid = ser['gempermid']
        pct = ser['pctshouthld']
        try:
            if lastdf.shape[0] == 0:
                last_state = ("out", 0.0)
            else:
                last_state = lastdf[name].ix[gid]
        except Exception as exc:
            print (exc)
            lastev = dict()
        if pct < 5.0:
            state = ("out", pct)
        elif last_state[0] in ("none", "out"):
            print("In %s, %s, %s" % (name, gid, pct))
            state = ("in", pct)
        else:
            if pct > last_state[1]:
                print("up %s, %s, %s" % (name, gid, pct))
                state = ("up", pct)
            else:
                print("Down %s, %s, %s" % (name, gid, pct))
                state = ("down", pct)

        thisdf[name].ix[gid] = state
    #print (evlist)
    fulldf = (thisdf if fulldf.shape[0] == 0
              else pd.concat([fulldf, thisdf]))
    #print (prevev)
    print ('')

fulldf.to_csv(os.path.join("data_derived", "states.csv"))
print ("done")