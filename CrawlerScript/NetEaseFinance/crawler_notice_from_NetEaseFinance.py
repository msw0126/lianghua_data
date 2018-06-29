# -*- coding:utf-8 -*-
import random
import urllib
import urllib.request as urllib2

import datetime
import html2text
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
        'User-Agent': random.choice( user_agent_list ),
    }
    request = urllib2.Request( url, headers=ua_headers )
    response = urllib2.urlopen( request )
    html = response.read().decode('utf-8')
    return html


def get_url_list(url):
    """
    得到相关股票的公告URL地址
    """
    notice_url_list = []
    notice_title_list = []
    html = get_html( url )
    soup = BeautifulSoup( html, "html.parser" )
    # 得到公告URL
    title = soup.findAll( 'td', {'class': 'td_text'} )
    soup = BeautifulSoup( str(title), "html.parser" )
    url_title = soup.find_all('a')
    for i in url_title:
        if len(notice_url_list) > 9:
            break
        notice_title = i.get('title')
        notice_url = i.get('href')
        notice_url_list.append(notice_url)
        notice_title_list.append(notice_title)
    return notice_title_list, notice_url_list


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


def save_notice_text():
    # 需要爬取得股票列表
    code_list = crawler_config.code_list
    for code in code_list:
        print( "-----------------------------------" )
        print("正在保存股票：{}，相关公告".format(code))
        # adj_code = processing_code(code)
        adj_code = code
        file_dir_path = os.path.join( crawler_config.notice_file_dir, adj_code )
        if not os.path.exists( file_dir_path ):
            os.makedirs( file_dir_path )
        stock_url = "http://quotes.money.163.com/f10/gsgg_{}.html#01e02".format(adj_code)
        notice_title_list, notice_url_list = get_url_list(stock_url)
        for notice_title, notice_url in zip(notice_title_list, notice_url_list):
            notice_url = "http://quotes.money.163.com" + notice_url
            # print(adj_code)
            # print(notice_title)
            # print(notice_url)
            notice_txt_path = os.path.join(file_dir_path, str(notice_title).strip().replace("/", "_") + ".txt")
            try:
                notice_html_data = get_html( notice_url )
                # print(notice_html_data)
                c = ClassifyTableTxt()
                notice_text = c.html_into_text( notice_html_data ).replace("关闭窗口", "")
                save_file(notice_txt_path, notice_text)
            except Exception as e:
                pass
            continue


if __name__ == '__main__':
    save_notice_text()