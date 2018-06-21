# -*- coding:utf-8 -*-
import urllib
import urllib.request as urllib2

import datetime
import html2text
import os
from bs4 import BeautifulSoup
import tushare as ts


def processing_code(code):
    """
    加工股票代码
    """
    if str(code).startswith("6"):
        return "sh" + str(code)
    elif str(code).startswith("0") or str(code).startswith("3"):
        return "sz" + str(code)


def get_html(url):
    """
    解析html网页，得到BeautifulSoup对象
    """
    ua_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    request = urllib2.Request( url, headers=ua_headers )
    response = urllib2.urlopen( request )
    html = response.read().decode('gbk')
    return html


def get_url_list(url):
    """
    得到相关股票的新闻URL地址
    """
    news_url_list = []
    news_title_list = []
    html = get_html( url )
    soup = BeautifulSoup( html, "html.parser" )
    # 得到新闻URL
    title = soup.findAll( 'div', {'class': 'nlist','id': 'cggy1'} )
    soup = BeautifulSoup( str(title[0]), "html.parser" )
    url_title = soup.find_all('a')
    for i in url_title:
        news_title = i.get('title')
        news_url = i.get('href')
        news_url_list.append(news_url)
        news_title_list.append(news_title)
    return news_title_list, news_url_list


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


def get_code_list():
    """
    得到所有股票列表
    """
    df = ts.get_stock_basics()
    df["code"] = df.index
    return df["code"].values.tolist()


if __name__ == '__main__':
    code_list = get_code_list()
    for code in code_list:
        print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" )
        adj_code = processing_code(code)
        stock_url = "http://quote.eastmoney.com/{}.html".format(adj_code)
        news_title_list, news_url_list = get_url_list(stock_url)
        for news_title, news_url in zip(news_title_list, news_url_list):
            print(adj_code)
            print(news_title)
            print(news_url)
            try:
                news_html_data = None
                for _ in range(3):
                    news_html_data = get_html( news_url )
                c = ClassifyTableTxt()
                print( c.html_into_text( news_html_data ) )
            except Exception as e:
                pass
            continue