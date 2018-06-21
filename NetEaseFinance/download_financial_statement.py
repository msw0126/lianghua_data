# -*- coding:utf-8 -*-

import tushare as ts
import requests


def code_list():
    """
    得到所有股票列表
    """
    df = ts.get_stock_basics()
    df["code"] = df.index
    return df["code"].values.tolist()


def download_file(url, file_path):
    """
    下载文件
    """
    r = requests.get(url) # create HTTP response object
    with open(file_path, 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    #所有股票列表
    code_list = code_list()
    for code in code_list:
        #下载文件的URL地址
        financial_indexes_url = "http://quotes.money.163.com/service/zycwzb_{}.html?type=report".format( code )
        profit_statement_url = "http://quotes.money.163.com/service/lrb_{}.html".format( code )
        chart_of_cash_flow_url = "http://quotes.money.163.com/service/xjllb_{}.html".format( code )
        #保存路径
        financial_indexes_file_path = "./data/financial_indexes/{}.csv".format(code)
        profit_statement_file_path = "./data/profit_statement/{}.csv".format(code)
        chart_of_cash_flow_file_path = "./data/chart_of_cash_flow/{}.csv".format(code)
        try:
            #下载
            download_file(financial_indexes_url, financial_indexes_file_path)
            download_file( profit_statement_url, profit_statement_file_path )
            download_file( chart_of_cash_flow_url, chart_of_cash_flow_file_path )
        except Exception as e:
            raise e
