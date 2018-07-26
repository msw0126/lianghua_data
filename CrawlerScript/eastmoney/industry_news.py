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


def pro_code(code):
    # code = "300"
    if code.startswith("0") or code.startswith("3"):
        return "sz" + code
    elif code.startswith("6"):
        return "sh" + code


def get_html(url, charset='gbk'):
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
    html = response.read().decode(charset)
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


def save_report_text(news_url, title, file_dir_path, news_date):
    news_html = get_html( news_url, charset="utf-8" )
    c = ClassifyTableTxt()
    text = c.html_into_text( news_html )
    head_n = 0
    for text_ in text.split( "\n" ):
        if text_.strip() != "小" and head_n == 0:
            continue
        # if title in text_.strip() and head_n == 0:
        #     continue
        if "责任编辑" in text_:
            break
        else:
            if len(text_.strip()) == 1 and "小" in text_.strip():
                text_ = text_.strip().replace("小", "")
            #     # continue
            if head_n == 0:
                # print(title)
                # print("新闻日期：", news_date)
                text_ = title + "\n" + "新闻日期：" + news_date + "\n" + text_
            print( text_ )
            news_file_path = os.path.join( file_dir_path, title.strip().replace( "/", "_" ) + ".txt" )
            save_file( news_file_path, text_ + "\n" )
            head_n += 1


def save_file(file_path, content):
    """
    保存文件
    """
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content )


if __name__ == '__main__':
    code_list = crawler_config.title_date_code_list
    new_list = []
    new = []
    for code in code_list:
        file_dir_path = os.path.join( crawler_config.eastmoney_industry_news_dir, code )
        if not os.path.exists( file_dir_path ):
            os.makedirs( file_dir_path )
        # print("----------------------------------------")
        url = "http://quote.eastmoney.com/{}.html".format( pro_code( code ) )
    #     url = "http://quote.eastmoney.com/sz300700.html"
        html_data = get_html(url)
        industry_soup = BeautifulSoup(html_data, "html.parser")
        industry_html = industry_soup.findAll('li', {'class': 'w79', 'value': '2'})
        industry_url_soup = BeautifulSoup( str(industry_html), "html.parser" )
        s_tag_html = industry_url_soup.find_all('a')
        industry_url_soup = BeautifulSoup( str( s_tag_html[0] ), "html.parser" )
        industry_url = None
        for x in industry_url_soup:
            industry_url = x.get('href')
        industry_url_html = get_html(industry_url, charset="utf-8")
        industry_html_soup = BeautifulSoup( industry_url_html, "html.parser" )
        news_html = industry_html_soup.findAll('div', {'class': 'common_list'})
        a_tag_html = BeautifulSoup( str(news_html[0]), "html.parser" )
        a_tag = a_tag_html.find_all('a')
        for a in a_tag:
            industry_news_url = a.get('href')
            industry_news_title = a.get('title')
            print("--------------------------------------------------------------------------")
            # print(industry_news_url)
            # print(industry_news_title)
            industry_news_html = get_html(industry_news_url, charset="utf-8")
            industry_news_soup = BeautifulSoup(industry_news_html, "html.parser")
            industry_news_time = industry_news_soup.findAll('div', {'class': 'time'})
            industry_news_date = industry_news_time[0].get_text()
            # 保存文本
            save_report_text( industry_news_url, industry_news_title, file_dir_path, industry_news_date)
            new.append(code)
            new.append(industry_news_date)
            new.append( industry_news_title )
            new.append("行业新闻")
            new_list.append(new)
            new = []
    print( new_list )
    columns = ['code', 'date', 'title', 'type']
    df = pd.DataFrame( columns=columns, data=new_list )
    df.to_csv( os.path.join( crawler_config.eastmoney_industry_news_dir, "title_date.csv" ),
               index=False )