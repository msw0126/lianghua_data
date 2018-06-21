# -*- coding:utf-8 -*-

import json
import requests
import os, sys
import pandas as pd
from jqdatasdk import *
from datetime import datetime, timedelta
auth('15558150270', '111111')

code_adj = "601006.XSHG"
start_date = "2018-06-15"

df_tmp = get_price(code_adj, start_date=start_date, end_date=start_date, frequency="daily",
                       fields=["open", "high", "low", "close", "volume", "money", "factor"], skip_paused=True)

print(df_tmp)