
import pandas as pd
import os, sys
from jqdatasdk import *
from datetime import datetime, timedelta
auth('15558150270', '111111')


source_folder = "./data/hs300"
output_folder = "./data/output_folder"


def preprocess(df):
    df["code"] = df.apply(lambda row: str(int(row["code"])).zfill(6), axis=1)
    return df


def adj_code(code):
    if code.find("0")==0 or code.find("3")==0:
        code_adj = code + ".XSHE"
    elif code.find("6") == 0:
        code_adj = code + ".XSHG"
    else:
        print("name %s not find, exit." %(code))
        sys.exit(-1)
    return code_adj


for name in os.listdir(source_folder):
    print( "----------------" )
    code = name[:6]
    code_adj = adj_code(code)
    print(name, code_adj)
    if os.path.exists(os.path.join(output_folder, name)):
        print("skip.")
        continue
    df = pd.read_csv(os.path.join(source_folder, name))
    df = preprocess(df)
    del df["cap"]
    df_tojoin = pd.DataFrame()
    for index, date in enumerate(df.date.tolist()):
        if (index>=500 and index%500 == 0):
            print(index)
        df_new = get_fundamentals(query(valuation).filter(valuation.code == code_adj), date)
        df_tojoin = pd.concat([df_tojoin, df_new])
    del df_tojoin["id"]
    del df_tojoin["code"]
    df_tojoin = df_tojoin.rename(columns={"day": "date", "market_cap": "cap"})
    # # cap的单位是 亿元，把它乘以1e8, https://www.joinquant.com/data/dict/fundamentals
    df_tojoin["cap"] = df_tojoin.apply(lambda row: row["cap"] * 1e8, axis=1)

    #两个DataFrame横向合并，以date字段
    df = pd.merge(df, df_tojoin, on="date", how="left")
    df.to_csv(os.path.join(output_folder, name), index=False)