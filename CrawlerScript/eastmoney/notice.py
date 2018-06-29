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


def save_report_text(notice_url, title, file_dir_path):
    notice_html = get_html( notice_url )
    c = ClassifyTableTxt()
    text = c.html_into_text( notice_html )
    head_n = 0
    for text_ in text.split( "\n" ):
        if title not in text_ and head_n == 0:
            continue
        # if "今日最新研究报告" in text_:
        #     break
        else:
            print( text_ )
            report_file_path = os.path.join( file_dir_path, title.strip().replace( "/", "_" ).replace("\"", "'") + ".txt" )
            # save_file( report_file_path, text_ + "\n" )
            head_n += 1


def save_file(file_path, content):
    """
    保存文件
    """
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content )


if __name__ == '__main__':
    code_list = crawler_config.title_date_code_list
    notice_list = []
    notice = []
    for code in code_list:
        file_dir_path = os.path.join( crawler_config.eastmoney_notice_dir, code )
        if not os.path.exists( file_dir_path ):
            os.makedirs( file_dir_path )
        url = "http://data.eastmoney.com/notices/stock/{}.html".format(code) #"300700"
        # url = "http://data.eastmoney.com/notices/stock/300700.html"
        html_data = get_html(url)
        res_tr = r'defjson:(.*?)charset: "gb2312"'
        data = re.findall( res_tr, html_data, re.S )
        # print(data[0].strip()[:-1])
        # if len( data[0] ) <= 1:
        #     continue
        data_dict = json.loads( data[0].strip()[:-1] )['data']
        # print(data_dict)
        for x in data_dict:
            print("------------------------------------------------")
            # print(x)
            time = x['NOTICEDATE']
            title = x['NOTICETITLE']
            INFOCODE = x['INFOCODE']
            notice_url = x['Url']
            date = time.split("T")[0]
            print(date)
            print(title)
            # print(code)
            # print(notice_url)
            # print(INFOCODE)
            #保存公告文本
            # todo 因为这里的所有公告是没有段落的，建议到网易财经拿
            # save_report_text(notice_url, title, file_dir_path)
            # 保存研报的标题、日期
            notice.append( code )
            notice.append( date )
            notice.append( title )
            notice.append("公司公告")
            notice_list.append( notice )
            notice = []
        print( notice_list )
        columns = ['code', 'date', 'title', 'type']
        df = pd.DataFrame( columns=columns, data=notice_list )
        df.to_csv( os.path.join( crawler_config.eastmoney_notice_dir, "title_date.csv" ),
                   index=False )