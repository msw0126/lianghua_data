# -*- coding:utf-8 -*-
import os

#当前日期
import datetime

# 获得当前时间
target_date = datetime.datetime.now()
now_date = target_date.strftime( "%Y-%m-%d" )

# 需要爬取得股票列表
code_list = ['600519',
             '002372',
             '002032',
             '300401',
             '000333',
             '300700']

# 需要标题时间的股票列表
title_date_code_list = ['300700',
                        '603773',
                        '603897',
                        '603301']

# 上市公司公告保存地址
notice_file_dir = os.path.join("../data/", now_date, "notice")
# 上市公司新闻保存地址
news_file_dir = os.path.join("./data", now_date, "news")
# 上市公司研报保存地址
research_report_file_dir = os.path.join("./data", now_date, "research_report")
# 上市公司标题、时间保存路径
title_date_dir = os.path.join("./data/", now_date)
# 东方财富个股研报，保存路径
eastmoney_stocks_research_report_dir = os.path.join("./data", now_date, "stocks_research_report")
# 东方财富行业研报，保存路径
eastmoney_industry_research_report_dir = os.path.join("./data", now_date, "industry_research_report")
# 东方财富上市公司公告，保存路径
eastmoney_notice_dir = os.path.join("./data", now_date, "notice")
# 东方财富上市公司新闻，保存路径
eastmoney_company_news_dir = os.path.join("./data", now_date, "company_news")
# 东方财富上市公司行业新闻，保存路径
eastmoney_industry_news_dir = os.path.join("./data", now_date, "industry_news")