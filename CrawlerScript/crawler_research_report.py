# -*- coding:utf-8 -*-
import urllib.request as urllib2

import datetime
import html2text
import os
from bs4 import BeautifulSoup
import tushare as ts


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
    ua_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
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


def save_html_txt(code_list, file_path, now_date):
    """
    保存html解析出的txt文本
    """
    for code in code_list:
        try:
            url_list = get_url_list( code.strip() )
            save_report_txt(url_list, file_path, now_date, code.strip())
            print("正在保存股票：{}，相关的研报...".format(code))
        except Exception as e:
            raise e


def save_report_txt(url_list, file_path, now_date, code):
    """
    保存研报的txt文本
    """
    file_path = os.path.join(file_path, now_date, code)
    for url in url_list:
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
            # print(text_title)
        #保存研报的正文
        pid = soup.findAll('div', {'class': 'YBText'})
        for p in pid:
            text_part = html2text.html2text( str(p) ).strip()
            if not os.path.exists(file_path ):
                os.makedirs( file_path )
            save_file(os.path.join(file_path, txt_title + ".txt"), text_part)
            # print(text_part)


def get_code_list():
    """
    得到所有股票列表
    """
    df = ts.get_stock_basics()
    df["code"] = df.index
    return df["code"].values.tolist()


if __name__ == '__main__':
    #当前日期
    target_date = datetime.datetime.now()
    now_date = target_date.strftime( "%Y-%m-%d" )
    #股票代码列表
    code_list = get_code_list()
    #保存txt文本文件路径
    file_path = "./data/research_report"
    #保存txt文件
    save_html_txt(code_list, file_path, now_date)
