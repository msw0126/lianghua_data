# -*- coding:utf-8 -*-
import os

#当前日期
import datetime

target_date = datetime.datetime.now()
now_date = target_date.strftime( "%Y-%m-%d" )

code_list = ['600519',
             '002372',
             '002032',
             '300401',
             '000333',
             '300700']

notice_file_dir = os.path.join("../data/", now_date, "notice")
news_file_dir = os.path.join("./data", now_date, "news")
research_report_file_dir = os.path.join("./data", now_date, "research_report")