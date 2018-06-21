import os, sys
import pandas as pd
from jqdatasdk import *
from datetime import datetime, timedelta

#auth("15355402003", "111111")
auth('15558150270', '111111')
# target_date = "2018-05-30"
target_date = datetime.now()
target_date = target_date.strftime("%Y-%m-%d")
count = 1
for name in os.listdir("./data/hs300/"):
    csv_file_path = os.path.join("./data/hs300/", name)
    # print(csv_file_path)
    if (name.find(".csv") > -1 and name.find("parsed")==-1):
        # print(count, name)
        count += 1
        df = pd.read_csv(csv_file_path)
        df["code"] = df.apply(lambda row: str(row["code"]).zfill(6), axis=1)
        df = df.sort_values(by=["date"], ascending=[True])
        df.index = range(len(df))
        #df = df[~df.date.isin(["2018-05-28", "2018-05-29", "2018-05-30"])]
        last_date = df.at[len(df)-1, "date"]
        last_date = datetime.strptime(last_date, "%Y-%m-%d")
        start_date = last_date + timedelta(days=1)
        start_date = start_date.strftime("%Y-%m-%d")

        code = name.split(".")[0]
        if code.find("0")==0 or code.find("3")==0:
            code_adj = code + ".XSHE"
        elif code.find("6") == 0:
            code_adj = code + ".XSHG"
        else:
            print("name %s not find, exit." %(code))
            sys.exit(-1)
        df_tmp = get_price(code_adj, start_date=start_date, end_date=target_date, frequency="daily",
                       fields=["open", "high", "low", "close", "volume", "money", "factor"], skip_paused=True)
        print(code_adj, start_date, target_date)
        print("Add %d to origin df." %(len(df_tmp)))
        print(len(df_tmp))
        if len(df_tmp) < 1:
            continue
        else:
            print(df_tmp)
            df_tmp = df_tmp.rename(columns={"money": "amount"})
            df_tmp["date"] = df_tmp.index
            df_tmp["date"] = df_tmp.apply(lambda row: row["date"].strftime("%Y-%m-%d"), axis=1)
            df_tmp["code"] = [code] * len(df_tmp)
            df_tmp["vwap"] = df_tmp.apply(lambda row: (row["high"] + row["low"] + row["close"])/3, axis=1)
            df = pd.concat([df, df_tmp])
#             df.to_csv("./" + name, index=False)
# print("finish")