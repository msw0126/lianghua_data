# -*- coding:utf-8 -*-

import os, sys
import pandas as pd
from jqdatasdk import *

auth('15558150270', '111111')

security = "600519.XSHG"
start_dt = "2018-06-15"
end_dt = "2018-06-15"
count = 10

d = get_ticks(security, end_dt, start_dt, count)
print(d)