# -*- coding:utf-8 -*-

import pandas as pd

df = pd.read_csv("./data/300638.csv")
price_list = df['price'].values
for inx, price in enumerate(price_list):
    try:
        float(price)
    except Exception as e:
        print("第{}行，不能转为浮点数".format(inx))
