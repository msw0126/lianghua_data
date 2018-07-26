# -*- coding:utf-8 -*-
import datetime
import time
import os
# from selenium import webdriver
#
# google_driver = "D:/web/chromedriver.exe"
# browser = webdriver.Chrome(google_driver)
# browser.get( 'https://www.bloomberg.com/news/articles/2018-07-11/senate-sends-trump-message-to-slow-down-on-tariff-escalation' )
# print(browser.page_source)
# # browser.quit()
# browser.close()
import re


def trun_date(s):
    if len(s) == 1:
        return "0" + s
    return s
zero_date = str(datetime.datetime.now().strftime( "%Y%m%d" )) + "0000"

# json_date = "2018年 7月 13日 00:04 BJT"
# news_date = "2018年 7月 12日 05:18 BJT"
# json_date = news_date.replace("月", "").replace("日", "").replace("BJT", "").replace("年", "").replace(":", "")
# new_json_date = ""
# for x in json_date.split(" "):
#     new_json_date += str(trun_date(x))
# print(new_json_date)
# zero_time = time.mktime(time.strptime( str(datetime.datetime.now().strftime( "%Y%m%d" )) + "0000", '%Y%m%d%H%M%S' ))
# news_time = time.mktime(time.strptime( new_json_date, '%Y%m%d%H%M%S' ))
# print(news_time - zero_time)


def get_timestamp(news_date):
    def trun_date(s):
        if len( s ) == 1:
            return "0" + s
        return s
    json_date = news_date.\
        replace( "月", "" ).\
        replace( "日", "" ).\
        replace( "BJT", "" ).\
        replace( "年", "" ).\
        replace( ":", "" )
    new_json_date = ""
    for x in json_date.split( " " ):
        new_json_date += str( trun_date( x ) )
    return time.mktime( time.strptime( new_json_date, '%Y%m%d%H%M%S' ) )

# print(get_timestamp("2018年 7月 13日 05:18 BJT"))

# m = "world\"s"
# print(re.sub("[A-Z|a-z]\"[A-Z|a-z]", '', m))

usa_date = "JULY 12, 2018 11:38PM EDT"