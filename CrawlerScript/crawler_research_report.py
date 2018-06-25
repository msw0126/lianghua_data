# -*- coding:utf-8 -*-
import random
import urllib.request as urllib2

import datetime
import html2text
import os
from bs4 import BeautifulSoup
import tushare as ts

from CrawlerScript import crawler_config


def save_file(file_path, content):
    """
    保存文件
    """
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content )


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
    html = response.read()#.decode( 'gb2312' )
    soup = BeautifulSoup( html, "html.parser" )
    return soup


def get_url_list(code):
    """
    得到相关股票的研报URL地址
    """
    url_list = []
    url = r"http://stockpage.10jqka.com.cn/ajax/code/{}/type/news/".format(code)
    soup = get_html( url )
    # 得到研报URL
    title = soup.findAll( 'a', {'class': 'client'} )
    for t in title:
        url = t.get( 'href' )
        if "news.10jqka.com.cn/field/sr" in url:
            # print( url )
            url_list.append(url)
    return url_list


def save_html_txt(code_list, file_path):
    """
    保存html解析出的txt文本
    """
    for code in code_list:
        try:
            print( "-------------------------------------------------------------------------------" )
            print( "正在保存股票：{}，相关的研报...".format( code ) )
            url_list = get_url_list( code.strip() )
            save_report_txt(url_list, file_path,code.strip())
        except Exception as e:
            raise e


def save_report_txt(url_list, file_path, code):
    """
    保存研报的txt文本
    """
    file_path = os.path.join(file_path, code)
    for url in url_list:
        # print( "*********************************" )
        # print(url)
        soup = get_html(url)
        title = soup.findAll('div', {'class': 'YBhead'})
        txt_title = ""
        #保存研报的标题
        for t in title:
            text_title = t.text.strip().replace("\n\n", " ")
            txt_title = t.text.strip().replace("\n\n", " ").split("\n")[0].strip().replace("/", "_")
            if not os.path.exists(file_path ):
                os.makedirs(file_path)
            save_file(os.path.join(file_path, txt_title + ".txt"), text_title + "\n")
        #保存研报的正文
        pid = soup.findAll('div', {'class': 'YBText'})
        for p in pid:
            text_part = html2text.html2text( str(p) ).strip()
            text_part_list = text_part.split("\n")
            new_text_part_list = []
            for x in text_part_list:
                if len(x) <= 2:
                    continue
                new_text_part_list.append(x)
            # print("\n".join(new_text_part_list))
            if not os.path.exists(file_path ):
                os.makedirs( file_path )
            save_file(os.path.join(file_path, txt_title + ".txt"), "\n".join(new_text_part_list))
            # print(text_part)


# def get_code_list():
#     """
#     得到所有股票列表
#     """
#     df = ts.get_stock_basics()
#     df["code"] = df.index
#     return df["code"].values.tolist()


if __name__ == '__main__':
    #当前日期
    target_date = datetime.datetime.now()
    now_date = target_date.strftime( "%Y-%m-%d" )
    #股票代码列表
    # code_list = get_code_list()
    code_list = crawler_config.code_list
    #保存txt文本文件路径
    file_path = crawler_config.research_report_file_dir
    #保存txt文件
    save_html_txt(code_list, file_path)
