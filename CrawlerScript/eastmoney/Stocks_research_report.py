# -*- coding:utf-8 -*-
import random
import re
import urllib.request as urllib2

import datetime
import html2text
import os

import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import tushare as ts

from CrawlerScript import crawler_config


# def get_html(url):
#     r = requests.get(url)
#     return r.text


def get_html(url):
    """
    解析html网页，得到BeautifulSoup对象
    """
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    ua_headers = {
        'User-Agent': random.choice(user_agent_list),
    }
    request = urllib2.Request( url, headers=ua_headers )
    response = urllib2.urlopen( request )
    html = response.read().decode('gbk')
    return html


class ClassifyTableTxt(object):
    def __init__(self):
        self.md = html2text.HTML2Text()
        self.md.ignore_links = True
        self.md.ignore_images = True
        self.md.single_line_break = True
        self.md.wrap_links = False
        self.md.unicode_snob = True  # Prevents accents removing
        self.md.skip_internal_links = True
        self.md.ignore_anchors = True
        self.md.body_width = 0
        self.md.use_automatic_links = True

    def html_into_text(self, html_data):
        """
        HTML转txt
        """
        try:
            return self.md.handle( html_data )
        except:
            raise Exception


def save_report_text(url_date, infoCode, title, file_dir_path):
    research_report_url = "http://data.eastmoney.com/report/" + url_date + "/" + infoCode + ".html"
    print( research_report_url )
    research_report_html = get_html( research_report_url )
    c = ClassifyTableTxt()
    text = c.html_into_text( research_report_html )
    head_n = 0
    for text_ in text.split( "\n" ):
        if title not in text_ and head_n == 0:
            continue
        if "今日最新研究报告" in text_:
            break
        else:
            print( text_ )
            report_file_path = os.path.join( file_dir_path, title.strip().replace( "/", "_" ) + ".txt" )
            save_file( report_file_path, text_ + "\n" )
            head_n += 1


def save_file(file_path, content):
    """
    保存文件
    """
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content )


if __name__ == '__main__':
    code_list = crawler_config.title_date_code_list
    stocks_report_list = []
    stocks_report = []
    for code in code_list:
        file_dir_path = os.path.join( crawler_config.eastmoney_stocks_research_report_dir, code )
        if not os.path.exists( file_dir_path ):
            os.makedirs( file_dir_path )
        url = "http://data.eastmoney.com/report/{}_1.html".format(code)
        html_data = get_html(url)
        res_tr = r'firstInit\((.*?)\);'
        data = re.findall(res_tr, html_data)
        if len(data[0]) <= 1:
            continue
        data_dict = json.loads(data[0])['data']
        for x in data_dict:
            print("------------------------------------------------------------------------")
            time = x['datetime']
            infoCode = x['infoCode']
            insName = x['insName']
            rate = x['rate']
            if len(rate) == 0:
                rate = "Null"
            title = x['title']
            # print(infoCode)
            print(insName)
            print(rate)
            print(title)
            url_date = str(time).split("T")[0].replace("-", "")
            date = str(time).split("T")[0]
            print(date)
            #保存研报文本
            save_report_text(url_date, infoCode, title, file_dir_path)
            #保存研报的标题、日期
            stocks_report.append(code)
            stocks_report.append(insName)
            stocks_report.append(rate)
            stocks_report.append(date)
            stocks_report.append(title)
            stocks_report.append("个股研报")
            stocks_report_list.append(stocks_report)
            stocks_report = []
    print(stocks_report_list)
    columns = ['code', 'organization', 'grade', 'date', 'title', 'type']
    df = pd.DataFrame( columns=columns, data=stocks_report_list )
    df.to_csv(os.path.join(crawler_config.eastmoney_stocks_research_report_dir, "title_date.csv"), index=False)


