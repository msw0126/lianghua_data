# -*- coding:utf-8 -*-
import datetime

import os
import tushare as ts
import pandas as pd


conns = ts.get_apis()
hs300_dir = "./data/hs300/"
tick_data_hs300 = "./data/tick_data_hs300/"

start_date = "2005-01-04"
# start_date = "2017-05-01"
end_date = "2018-06-19"


def get_tick_data_df(adj_code, trading_date):
    """
    type:买卖方向，0-买入 1-卖出 2-集合竞价成交
    change：价格变动(元)
    volume：成交手
    amount：成交金额(元)
    """
    df = ts.tick(adj_code, conn=conns, date=trading_date)
    return df


def save_file(content, file_path):
    """
    保存文件
    """
    with open( file_path, 'a+', encoding='UTF-8' ) as f:
        f.write( content + "\n" )


def get_exist_code(path):
    code_list = []
    for name in os.listdir( path):
        adj_code = name.split( "." )[0]
        code_list.append(adj_code)
    return code_list


def main():
    exist_code = get_exist_code(tick_data_hs300)
    for name in os.listdir( hs300_dir ):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        csv_file_path = os.path.join( tick_data_hs300, name )
        adj_code = name.split(".")[0]
        if adj_code in exist_code:
            continue
        if not name.startswith("6") and not name.endswith("0"):
            continue
        datestart = datetime.datetime.strptime( start_date, '%Y-%m-%d' )
        dateend = datetime.datetime.strptime( end_date, '%Y-%m-%d' )
        df_concat = pd.DataFrame()
        while datestart <= dateend:
            trading_date = datestart.strftime( '%Y-%m-%d' )
            print("-------------------------")
            print(trading_date)
            df = get_tick_data_df(adj_code, trading_date)
            if "NoneType" not in str(type(df)):
                df = df.rename(columns={"vol": "volume"})
                df['amount'] = df.apply(lambda row: row["price"] * (row["volume"] * 100), axis=1)
                #增加change字段
                # df['price_'] = df["price"].shift(1)
                # df["change"] = df["price"] - df["price_"]
                # df = df[['datetime', 'price', 'change', 'volume', 'amount', 'type']].fillna({'change': 0})
                # df['tmp'] = df.index
                df = df[['datetime', 'price', 'volume', 'amount', 'type']]
                is_null = len(df[df.isnull().values == True])
                if is_null > 0:
                    save_file("股票代码：{}，日期：{}，可能出现缺失值".format(adj_code, trading_date),
                              "./data/log/tick_data_hs300_log.txt")

                #change字段缺失值处理
                # df.fillna({'change': 0}).to_csv(csv_file_path, index=False, mode='a')
                df_concat = pd.concat( [df_concat, df] )
            datestart += datetime.timedelta(days=1)
        df_concat.to_csv( csv_file_path, index=False)


if __name__ == '__main__':
    #下载数据
    main()

    #断开连接
    for connection in conns:
        connection.disconnect()
        print("close connection %s." % (str(connection)))