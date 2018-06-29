# -*- coding:utf-8 -*-

import random
import urllib.request as urllib2

import datetime
import html2text
import os
from bs4 import BeautifulSoup
import pandas as pd
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
    html = response.read()#.decode( 'gb2312' )
    soup = BeautifulSoup( html, "html.parser" )
    return soup


if __name__ == '__main__':
    columns = ['code', 'title', 'date', 'type']
    data_new = []
    if not os.path.exists( crawler_config.title_date_dir ):
        os.makedirs( crawler_config.title_date_dir )
    title_date_file_path = os.path.join( crawler_config.title_date_dir, "titel_date.csv" )
    for code in crawler_config.title_date_code_list:
        url = "http://stockpage.10jqka.com.cn/{}/".format(code)
        soup = get_html(url)
        title = soup.findAll( 'li', {'class': 'clearfix'} )
        n = 0
        sr_n = 0
        sn_n = 0
        industry_news_n = 0
        company_news_n = 0
        #研报列表
        research_report_list = []
        research_report = []
        #公告列表
        notice_list = []
        notice = []
        #行业资讯列表
        industry_news_list = []
        industry_news = []
        #公司新闻列表
        company_news_list = []
        company_news = []
        for t in title:
            soup = BeautifulSoup(str(t), "html.parser")
            a_soup = soup.find_all('a')
            # print(a_soup[0])
            url = a_soup[0].get( 'href' )
            if "http://news.10jqka.com.cn/field/sr" in url:
                # if sr_n == 0:
                #     print( "---------------------------------" )
                #     print("研报列表：")
                # # print( t )
                # print("标题：", t.text.strip().split("\n")[0])
                # print("时间：", t.text.strip().split("\n")[1])
                title = t.text.strip().split("\n")[0]
                date = t.text.strip().split("\n")[1]
                research_report.append(code)
                research_report.append(title)
                research_report.append(date)
                research_report.append('研报')
                research_report_list.append(research_report)
                research_report = []
                sr_n += 1
            elif "http://news.10jqka.com.cn/field/sn" in url:
                # if sn_n == 0:
                #     print( "---------------------------------" )
                #     print( "公告列表：" )
                # # print( t )
                # print( "标题：", t.text.strip().split( "\n" )[0] )
                # print( "时间：", t.text.strip().split( "\n" )[1] )
                title = t.text.strip().split( "\n" )[0]
                date = t.text.strip().split( "\n" )[1]
                notice.append( code )
                notice.append( title )
                notice.append( date )
                notice.append( '公告' )
                notice_list.append( notice )
                notice = []
                n += 1
                sn_n += 1
            elif n > 0:
                # if industry_news == 0:
                #     print( "---------------------------------" )
                #     print( "行业资讯列表：" )
                # # print( t )
                # print( "标题：", t.text.strip().split( "\n" )[0] )
                # print( "时间：", t.text.strip().split( "\n" )[1] )
                title = t.text.strip().split( "\n" )[0]
                date = t.text.strip().split( "\n" )[1]
                industry_news.append( code )
                industry_news.append( title )
                industry_news.append( date )
                industry_news.append( '行业资讯' )
                industry_news_list.append( industry_news )
                industry_news = []
                industry_news_n += 1
            else:
                # if company_news_n == 0:
                #     print( "---------------------------------" )
                #     print( "公司新闻列表：" )
                # # print( t )
                # print( "标题：", t.text.strip().split( "\n" )[0] )
                # print( "时间：", t.text.strip().split( "\n" )[1] )
                title = t.text.strip().split( "\n" )[0]
                date = t.text.strip().split( "\n" )[1]
                company_news.append( code )
                company_news.append( title )
                company_news.append( date )
                company_news.append( '公司新闻' )
                company_news_list.append( company_news )
                company_news = []
                company_news_n += 1
        data_new += research_report_list
        data_new += notice_list
        data_new += industry_news_list
        data_new += company_news_list
    print(len(data_new))
    print(data_new)
    df = pd.DataFrame( columns=columns, data=data_new )
    df.to_csv(title_date_file_path, index=False)