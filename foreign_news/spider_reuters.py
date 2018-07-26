# -*- coding:utf-8 -*-
import random

import chardet
import re
import json
import requests
import urllib.request as urllib2
import urllib.error, urllib.request, urllib.parse
import http.cookiejar

import datetime
import time
import html2text
import os
from bs4 import BeautifulSoup


ZERO_TIME = time.mktime(time.strptime( str(datetime.datetime.now().strftime( "%Y%m%d" )) + "0000", '%Y%m%d%H%M%S' ))


def get_timestamp(news_date):
    """
    新闻日期转为时间戳
    :param news_date:
    :return:
    """
    def trun_date(s):
        if len( s ) == 1:
            return "0" + s
        return s
    json_date = news_date.\
        replace( "月", "" ).\
        replace( "日", "" ).\
        replace( "BJT", "" ).\
        replace( "年", "" ).\
        replace( ":", "" )
    new_json_date = ""
    for x in json_date.split( " " ):
        new_json_date += str( trun_date( x ) )
    return time.mktime( time.strptime( new_json_date, '%Y%m%d%H%M%S' ) )

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
    """代理访问"""
    proxy = urllib2.ProxyHandler( {'https': '127.0.0.1:1080'} )
    # 尝试带上cookie
    # cookie_filename = 'cookie.txt'
    # cookie_aff = http.cookiejar.MozillaCookieJar( cookie_filename )
    # handler = urllib.request.HTTPCookieProcessor( cookie_aff )
    # opener = urllib.request.build_opener( handler )
    opener = urllib2.build_opener( proxy )
    request = urllib2.Request( url, headers=ua_headers )
    html = opener.open( request).read().decode( 'utf-8' )

    """正常访问"""
    # request = urllib2.Request( url, headers=ua_headers )
    # response = urllib2.urlopen( request )
    # html = response.read().decode( 'utf-8' )
    soup = BeautifulSoup( html, "html.parser" )
    return soup

def get_more_news_url_list(BASE_URL, more_news_url):
    """添加查询更多的方法"""
    # 检查最早的新闻是否是大于当天零点的时间，如果不是，需要拿到更多的新闻
    # last_news_time = get_timestamp(news_date_list[-1])
    # if last_news_time - ZERO_TIME > 0:
    more_news_soup = get_html( more_news_url )
    # print(more_news_soup)
    res_tr = r'addMoreNewsResults\((.*?)\)\;'
    json_data = re.findall( res_tr, str( more_news_soup ), re.S )
    json_data = re.sub( "[A-Z|a-z]\"[A-Z|a-z]", '',
                        json_data[0].strip()
                        .replace( "blob:", "\"blob\":" )
                        .replace( "sortBy:", "\"sortBy\":" )
                        .replace( "dateRange:", "\"dateRange\":" )
                        .replace( "totalResultNumber:", "\"totalResultNumber\":" )
                        .replace( "totalResultNumberStr:", "\"totalResultNumberStr\":" )
                        .replace( "news:", "\"news\":" )
                        .replace( "id: \"", "\"id\": \"")
                        .replace( "headline:", "\"headline\":" )
                        .replace( "date:", "\"date\":" )
                        .replace( "href:", "\"href\":" )
                        .replace( "blurb:", "\"blurb\":" )
                        .replace( "mainPicUrl:", "\"mainPicUrl\":" )
                        .replace("'trade+war+China',", "\"trade+war+China\",")
                        .replace("'date',", "\"date\",")
                        .replace("'pastYear',", "\"pastYear\","))
    print( json_data )
    more_news_dicts = json.loads(json_data)['news']
    print("===========================")
    print(len(more_news_dicts))
    print("===========================")
    more_news_url_list = []
    if not len(more_news_dicts) > 0:
        return
    else:
        for news_dict in more_news_dicts:
            news_url = BASE_URL + news_dict['href']
            # news_time = get_timestamp(news_dict['date'])
            more_news_url_list.append(news_url)
    return more_news_url_list



def get_url_list(url, BASE_URL, more_news_url=None):
    """
    得到相关新闻的url地址
    """
    news_url_list = []
    news_date_list = []
    soup = get_html( url )
    # 得到新闻URL和时间
    news_titles = soup.findAll( 'div', {'class': 'search-result-content'} )
    for news_title in news_titles:
        news_title_soup = BeautifulSoup( str(news_title), "html.parser" )
        news_date = news_title_soup.get_text().split("\n")[-2]
        news_url_a_tag = news_title_soup.find_all('a')
        news_url = BASE_URL + news_url_a_tag[0].get('href')
        news_url_list.append(news_url)
        news_date_list.append(news_date)
    return news_url_list#, news_date_list


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


if __name__ == '__main__':
    # 中文
    url = "https://cn.reuters.com/search/news?sortBy=date&dateRange=pastDay&blob=trade+war+China"
    more_news_url = "https://cn.reuters.com/assets/searchArticleLoadMoreJson?blob=trade+war+China&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastDay&numResultsToShow=10&pn=2&callback=addMoreNewsResults"
    BASE_URL = "https://cn.reuters.com"
    # more_news_url = "https://cn.reuters.com/assets/searchArticleLoadMoreJson?blob=trade+war+China&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastYear&numResultsToShow=10&pn=1100&callback=addMoreNewsResults"

    # 英文
    # url = "https://www.reuters.com/search/news?sortBy=date&dateRange=pastDay&blob=trade+war+China"
    # more_news_url = "https://www.reuters.com/assets/searchArticleLoadMoreJson?blob=trade+war+China&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastDay&numResultsToShow=10&pn=2&callback=addMoreNewsResults"
    # BASE_URL = "https://www.reuters.com"
    # url = "https://www.baidu.com"
    # url = "https://www.google.com"
    news_url_list = get_url_list( url, BASE_URL )
    # 爬最近一年的新闻
    # for n in range(2, 141):
    #     print("--------------------------------------------")
    #     more_news_url = "https://cn.reuters.com/assets/searchArticleLoadMoreJson?blob=trade+war+China&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastYear&numResultsToShow=10&pn={}&callback=addMoreNewsResults".format(n)
    #     # more_news_url = "https://cn.reuters.com/assets/searchArticleLoadMoreJson?blob=trade+war+China&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastYear&numResultsToShow=10&pn=131&callback=addMoreNewsResults"
    #     print( more_news_url )
    #     more_news_url_list = get_more_news_url_list(BASE_URL, more_news_url)
    #     if more_news_url_list == None:
    #         break
    #     news_url_list += more_news_url_list

    for news_url in news_url_list:
        print("------------------------------")
        print(news_url)
        # news_url = "https://www.reuters.com/article/us-global-oil/oil-edges-lower-set-for-big-weekly-decline-idUSKBN1K306Z"
        try:
            news_html_data = get_html(news_url)
            title = news_html_data.findAll('h1', {'class': 'ArticleHeader_headline'})
            title_name = title[0].get_text()
            # print(title_name)
            c = ClassifyTableTxt()
            news_text = c.html_into_text( str(news_html_data ))
            # print(news_text)
            n = 0
            if os.path.exists(
                    "./data/news/{}.txt".format( str( title_name ).strip().replace( " ", "_" ).replace( "/", "_" ) ) ):
                continue
            for text in news_text.split("\n"):
                if " / " not in text and n == 0:
                    continue
                if "Min Read" in text or "分钟阅读" in text:
                    continue
                if "Our Standards:The Thomson Reuters Trust Principles" in text or "我们的标准：" in text:
                    break
                if " / " in text and n == 0:
                    text = text.replace("/ 更新于", "/ Updated")
                print(text.replace("‘", "\'")
                          .replace("’", "\'")
                          .replace("”", "\"")
                          .replace("“", "\"")
                          .replace("，", ",")
                          .replace("。", ".")
                          .replace("（", "(")
                          .replace("）", ")"))
                save_file("./data/news/{}.txt".format(str(title_name).strip().replace(" ", "_").replace("/", "_")), text
                          .replace("\‘", "\'")
                          .replace("’", "\'")
                          .replace("”", "\"")
                          .replace("“", "\"")
                          .replace("，", ",")
                          .replace("。", ".")
                          .replace("（", "(")
                          .replace("）", ")") + "\n")
                n += 1
        except Exception as e:
            print(str(e).strip())
        continue

    # more_news_url = "https://cn.reuters.com/assets/searchArticleLoadMoreJson?blob=trade+war+China&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastYear&numResultsToShow=10&pn=1100&callback=addMoreNewsResults"

    # more_news_soup = get_html( more_news_url )
    # print(more_news_soup)