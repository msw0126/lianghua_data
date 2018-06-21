# -*- coding:utf-8 -*-

import os, sys
import pandas as pd
from jqdatasdk import *
# from datetime import datetime, timedelta
import datetime

auth('15355402003', '111111')
# auth('15558150270', '111111')

#最新下载数据的时间
target_date = datetime.datetime.now()
target_date = target_date.strftime("%Y-%m-%d")

source_folder = "./data/hs300/"
# output_folder = "./data/output_folder/"


def preprocess(df):
    """
    股票代码预处理，如果不是6位数字，则过滤掉
    """
    df["code"] = df.apply(lambda row: str(int(row["code"])).zfill(6), axis=1)
    return df


def get_adj_code(code):
    """
    为股票代码添加沪、深标签
    """
    if code.find("0")==0 or code.find("3")==0:
        code_adj = code + ".XSHE"
    elif code.find("6") == 0:
        code_adj = code + ".XSHG"
    else:
        print("name %s not find, exit." %(code))
        sys.exit(-1)
    return code_adj


def read_source_csv(csv_file_path):
    """
    读取现在已经存在的沪深300股票csv文件
    """
    df = pd.read_csv( csv_file_path )
    df["code"] = df.apply( lambda row: str( row["code"] ).zfill( 6 ), axis=1 )
    df = df.sort_values( by=["date"], ascending=[True] )
    df.index = range( len( df ) )
    return df


def get_df_start_date(df):
    """
    获取csv文件最后一天数据的加一天，作为接口的开始时间
    """
    last_date = df.at[len( df ) - 1, "date"]
    last_date = datetime.datetime.strptime( last_date, "%Y-%m-%d" )
    start_date = last_date + datetime.timedelta( days=1 )
    start_date = start_date.strftime( "%Y-%m-%d" )
    return start_date


def get_price_df(code_adj, start_date, target_date):
    """
    获取价格接口
    """
    code = code_adj.split(".")[0]
    df_tmp = get_price( code_adj, start_date=start_date, end_date=target_date, frequency="daily",
                        fields=["open", "high", "low", "close", "volume", "money", "factor"], skip_paused=True )
    if len( df_tmp ) < 1:
        return df_tmp
    else:
        df_tmp = df_tmp.rename( columns={"money": "amount"} )
        df_tmp["date"] = df_tmp.index
        df_tmp["date"] = df_tmp.apply( lambda row: row["date"].strftime( "%Y-%m-%d" ), axis=1 )
        df_tmp["code"] = [code] * len( df_tmp )
        df_tmp["vwap"] = df_tmp.apply( lambda row: (row["high"] + row["low"] + row["close"]) / 3, axis=1 )
        return df_tmp.sort_values(by=["date"], ascending=[True])


def get_fundamentals_df(code_adj, date):
    """
    获取基本面接口
    """
    df_tojoin = pd.DataFrame()
    df_new = get_fundamentals( query( valuation ).filter( valuation.code == code_adj ), date )
    df_tojoin = pd.concat( [df_tojoin, df_new] )
    del df_tojoin["id"]
    del df_tojoin["code"]
    df_tojoin = df_tojoin.rename( columns={"day": "date", "market_cap": "cap"} )
    # cap的单位是 亿元，把它乘以1e8, https://www.joinquant.com/data/dict/fundamentals
    df_tojoin["cap"] = df_tojoin.apply( lambda row: row["cap"] * 1e8, axis=1 )
    return df_tojoin.sort_values(by=["date"], ascending=[True])


def merge_concat_df(adj_code, source_df, start_date, end_date, csv_file_path): #,
    """
    合并保存文件
    """
    datestart = datetime.datetime.strptime( start_date, '%Y-%m-%d' )
    dateend = datetime.datetime.strptime( end_date, '%Y-%m-%d' )
    #使用csv文件的最新日期加一天的数据，更新数据
    source_df = replace_fundamentals( adj_code, start_date, source_df )
    df_concat = source_df
    #对从csv最后一天加一天，到昨天的数据处理
    while datestart < dateend:
        date = datestart.strftime( '%Y-%m-%d' )
        price_df = get_price_df( adj_code, date, date )
        fundamentals_df = get_fundamentals_df( adj_code, date )
        if len( price_df ) > 0:
            df_merge = pd.merge( price_df, fundamentals_df, on="date", how="outer" )
            df_concat = pd.concat( [source_df, df_merge] ).sort_values(by=["date"], ascending=[True])
            source_df = df_concat
        datestart += datetime.timedelta( days=1 )

    source_df = df_concat
    print( df_concat['date'].tolist()[-10:] )
    #获取当天的数据
    today_price_df = get_price_df( adj_code, end_date, end_date )
    today_fundamentals_df = get_fundamentals_df( adj_code, end_date )
    if len( today_price_df ) > 0:
        # 当天只能拿到昨天的数据，对cap字段单独处理
        today_fundamentals_df["cap"] = today_fundamentals_df.apply(
            lambda row: (row["capitalization"] * 10000 * today_price_df['close']) / today_price_df['factor'], axis=1 )
        #拿到的数据是昨天的，需要把日期换成今天的
        today_fundamentals_df["date"] = today_fundamentals_df.apply(lambda row: today_price_df['date'], axis=1)
        today_df_merge = pd.merge( today_price_df, today_fundamentals_df, on="date", how="outer" )
        df_concat = pd.concat( [source_df, today_df_merge] ).sort_values( by=["date"], ascending=[True] )
    print(df_concat['date'].tolist()[-10:])
    #保存
    df_concat.to_csv(csv_file_path, index=False)


def replace_fundamentals(adj_code, target_date, source_df):
    """
    把csv文件最新日期的财务数据与加一天的数据进行更新
    """
    fundamentals_df = get_fundamentals_df( adj_code, target_date )
    pe_ratio = fundamentals_df['pe_ratio'].values[-1]
    turnover_ratio = fundamentals_df['turnover_ratio'].values[-1]
    pb_ratio = fundamentals_df['pb_ratio'].values[-1]
    ps_ratio = fundamentals_df['ps_ratio'].values[-1]
    pcf_ratio = fundamentals_df['pcf_ratio'].values[-1]
    capitalization = fundamentals_df['capitalization'].values[-1]
    cap = fundamentals_df['cap'].values[-1]
    circulating_cap = fundamentals_df['circulating_cap'].values[-1]
    circulating_market_cap = fundamentals_df['circulating_market_cap'].values[-1]
    pe_ratio_lyr = fundamentals_df['pe_ratio_lyr'].values[-1]
    #替换
    source_df['pe_ratio'].values[-1] = pe_ratio
    source_df['turnover_ratio'].values[-1] = turnover_ratio
    source_df['pb_ratio'].values[-1] = pb_ratio
    source_df['ps_ratio'].values[-1] = ps_ratio
    source_df['pcf_ratio'].values[-1] = pcf_ratio
    source_df['capitalization'].values[-1] = capitalization
    source_df['cap'].values[-1] = cap
    source_df['circulating_cap'].values[-1] = circulating_cap
    source_df['circulating_market_cap'].values[-1] = circulating_market_cap
    source_df['pe_ratio_lyr'].values[-1] = pe_ratio_lyr
    return source_df


if __name__ == '__main__':
    count = 1
    for name in os.listdir( source_folder ):
        print("------------------------------------------------------------------------------------")
        print("第{}个文件".format(count), "，文件名是{}".format(name))
        code = name[:6]
        csv_file_path = os.path.join( source_folder, name )
        count += 1
        source_df = read_source_csv(csv_file_path)
        source_df = preprocess(source_df)
        #准备获取价格接口参数
        adj_code = get_adj_code(code)
        start_date = get_df_start_date(source_df)
        print("开始时间：{}".format(start_date))
        #合并保存
        merge_concat_df(adj_code, source_df, start_date, target_date, csv_file_path) #



