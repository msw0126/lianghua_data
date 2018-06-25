# -*- coding:utf-8 -*-
import random
import urllib.request as urllib2

import datetime
import html2text
import time
import os
from bs4 import BeautifulSoup
import tushare as ts

from CrawlerScript import crawler_config


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


def get_url_list(code):
    """
    得到相关股票的新闻URL地址
    """
    url_list = []
    title_list = []
    url = r"http://stockpage.10jqka.com.cn/ajax/code/{}/type/news/".format(code)
    html = get_html( url )
    soup = BeautifulSoup( html, "html.parser" )
    # 得到新闻URL
    title = soup.findAll( 'a', {'class': 'client'} )
    for t in title:
        url = t.get( 'href' )
        if url.endswith('shtml'):
            title_list.append(t.get('title'))
            url_list.append(url)
    return title_list, url_list


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


def save_file(file_path, content):
    """
    保存文件
    """
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content )


def save_news_text():
    # 股票代码列表
    code_list = crawler_config.code_list
    for code in code_list:
        n = 0
        print( "-----------------------------------" )
        # 保存文件路径
        print( "正在保存股票：{}，相关的新闻...".format( code ) )
        file_dir_path = os.path.join( crawler_config.news_file_dir, code )
        if not os.path.exists( file_dir_path ):
            os.makedirs( file_dir_path )
        news_title_list, news_url_list = get_url_list( code )
        for news_title, news_url in zip( news_title_list, news_url_list ):
            time.sleep( 3 )
            # print( "-------------------------------------------------------" )
            # print( news_title )
            # print( news_url )
            file_path = os.path.join( file_dir_path, code + "_" + str( n ) + ".txt" )
            html_data = get_html( news_url )
            c = ClassifyTableTxt()
            news_text = c.html_into_text( html_data )
            if len( news_text ) <= 1:
                continue
            new_text_list = news_text.split( "\n" )
            for text in new_text_list:
                if "###### 相关板块" in text:
                    break
                # print(text)
                save_file( file_path, text + "\n" )
            n += 1


if __name__ == '__main__':
    save_news_text()