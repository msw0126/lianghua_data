# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import random
import urllib.request as urllib2

import datetime
import html2text
import os
from bs4 import BeautifulSoup
import pandas as pd
import tushare as ts

from CrawlerScript import crawler_config
from CrawlerScript.crawler_config import title_date_code_list


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
    html = response.read().decode( 'gbk' )
    soup = BeautifulSoup( html, "html.parser" )
    return soup


if __name__ == '__main__':
    code = "SZ300700"
    data_new = []
    if not os.path.exists( crawler_config.title_date_dir ):
        os.makedirs( crawler_config.title_date_dir )
    title_date_file_path = os.path.join( crawler_config.title_date_dir, "titel_date_from_eastmoney.csv" )
    # for code in title_date_code_list:
    url = "http://quote.eastmoney.com/{}.html".format(code)
    code = code[2:]
    soup = get_html(url)
    # 公司新闻与公告
    share_html_data = soup.findAll('div', {'class': 'nlist'})
    # 个股与行业研报
    research_report_html_data = soup.findAll('div', {'class': 'fz14'})
    #个股研报
    Stocks_research_report_list = []
    Stocks_research_report = []
    # 行业研报
    Industry_research_report_list = []
    Industry_research_report = []
    research_n = 0
    for x in research_report_html_data:
        new_soup = BeautifulSoup( str( x ), "html.parser" )
        td_tag = new_soup.find_all( 'td' )
        a_tag = new_soup.find_all( 'a' )
        for x in a_tag:
            if "class=\"lightBlue\""  not in str(x):
                print( "-----------------------------------" )
                print(x)
    #     for t in td_tag:
    #         print("------------------------------")
    #         print(t)
    #         for text_ in BeautifulSoup(str(t).replace("<a", "\n<a"), "html.parser").get_text().strip().split("\n"):
    #             if text_ == "机构" or text_ == "评级" or text_ == "研报":
    #                 continue
    #             if len(text_) == 0:
    #                 text_ = "Null"
    #             if research_n == 0:
    #                 Stocks_research_report.append(text_)
    #             if research_n == 1:
    #                 Industry_research_report.append(text_)
    #     research_n += 1
    # Stocks_split_list = [Stocks_research_report[i:i+4] for i in range(0, len(Stocks_research_report), 4)]
    # for lst in Stocks_split_list:
    #     lst.insert(0, code)
    #     lst.append("个股研报")
    #     Stocks_research_report_list.append(lst)
    # print(Stocks_research_report_list)
    #
    # Industry_split_list = [Industry_research_report[i:i + 4] for i in range( 0, len( Industry_research_report ), 4 )]
    # for lst in Industry_split_list:
    #     lst.insert( 0, code )
    #     lst.append( "行业研报" )
    #     Industry_research_report_list.append( lst )
    # print( Industry_research_report_list )

#     # 公司新闻
#     news_list = []
#     news = []
#     # 行业新闻
#     industry_news_list = []
#     industry_news = []
#     # 公司公告
#     notice_list = []
#     notice = []
#     share_n = 0
#     for x in share_html_data:
#         new_soup = BeautifulSoup( str( x ), "html.parser" )
#         td_tag = new_soup.find_all( 'li' )
#         for t in td_tag:
#             for text_ in BeautifulSoup( str( t ).replace( "<a", "\n<a" ), "html.parser" ).get_text().strip().split( "\n" ):
#                 if share_n == 0:
#                     news.append(text_)
#                 if share_n == 1:
#                     industry_news.append(text_)
#                 if share_n == 2:
#                     notice.append(text_)
#         share_n += 1
#
#     news_split_list = [news[i:i+2] for i in range(0, len(news), 2)]
#     for lst in news_split_list:
#         lst.insert(0, code)
#         lst.insert(1, "Null")
#         lst.insert( 2, "Null" )
#         lst.append("个股要闻")
#         news_list.append(lst)
#     print(news_list)
#
#     industry_news_split_list = [industry_news[i:i + 2] for i in range( 0, len( industry_news ), 2 )]
#     for lst in industry_news_split_list:
#         lst.insert( 0, code )
#         lst.insert( 1, "Null" )
#         lst.insert( 2, "Null" )
#         lst.append( "行业要闻" )
#         industry_news_list.append( lst )
#     print( industry_news_list )
#
#     notice_split_list = [notice[i:i + 2] for i in range( 0, len( notice ), 2 )]
#     for lst in notice_split_list:
#         lst.insert( 0, code )
#         lst.insert( 1, "Null" )
#         lst.insert( 2, "Null" )
#         lst.append( "公司公告" )
#         notice_list.append( lst )
#     print( notice_list )
#
#
#     data_new += news_list
#     data_new += industry_news_list
#     data_new += notice_list
#     data_new += Stocks_research_report_list
#     data_new += Industry_research_report_list
# sum_data_new = []
# sum_data_new += data_new
# columns = ['code', 'organization', 'grade', 'date', 'title', 'type']
# df = pd.DataFrame( columns=columns, data=data_new )
# df.to_csv( title_date_file_path, index=False )