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

lastdf = pd.DataFrame(columns= names + ["end_date"],
                      index = gids)
for name in names:
    for gid in gids:
        lastdf[name].ix[gid] = ("none_init", 0.0)

dflist = []
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
    for name in names:
        for gid in gids:
            prev_state, prev_pct = lastdf[name].ix[gid]
            new_state = prev_state.split("_")[0]
            new_state = new_state + "_unch"
            thisdf[name].ix[gid] = (new_state, prev_pct)

    for idx, ser in ev.iterrows():
        name = ser['name']
        gid = ser['gempermid']
        pct = ser['pctshouthld']
        prev_state, prev_pct = lastdf[name].ix[gid]
        if pct < 5.0:
            new_tpl = ("out_init", pct)
        elif re.search("none|out", prev_state):
            print("In %s, %s, %s" % (name, gid, pct))
            new_tpl = ("in_init", pct)
        else:
            if pct > prev_pct:
                print("up %s, %s, %s" % (name, gid, pct))
                new_tpl = ("in_up", pct)
            else:
                print("Down %s, %s, %s" % (name, gid, pct))
                new_tpl = ("in_down", pct)

        thisdf[name].ix[gid] = new_tpl
    dflist.append(thisdf)
    lastdf = thisdf

fulldf = pd.concat(dflist)
fulldf.to_csv(os.path.join("data_derived", "states.csv"))
print ("done")