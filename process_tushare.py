# -*- coding:utf-8 -*-

import time
import random
from multiprocessing import Process

import datetime
import tushare as ts

conns = ts.get_apis()


def get_tick_data_df(adj_code, trading_date):
    """
    type:买卖方向，0-买入 1-卖出 2-集合竞价成交
    change：价格变动(元)
    volume：成交手
    amount：成交金额(元)
    """
    df = ts.tick(adj_code, conn=conns, date=trading_date)
    return df


class Piao(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.trading_date = "2018-06-19"
        self.start_date = "2015-01-02"
        self.end_date = "2018-01-02"

    def run(self):
        print("---------------------------")
        nowTime = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )
        print(nowTime)
        print('开始下载股票：%s ' % self.name)
        datestart = datetime.datetime.strptime( self.start_date, '%Y-%m-%d' )
        dateend = datetime.datetime.strptime( self.end_date, '%Y-%m-%d' )
        while datestart <= dateend:
            get_tick_data_df(self.name, self.trading_date)
            datestart += datetime.timedelta( days=1 )
        time.sleep(random.randrange(1, 5))
        print('下载股票：%s，结束--' % self.name)


if __name__ == '__main__':
    p1 = Piao('000002')
    p2 = Piao('601012')
    p3 = Piao('600893')
    p4 = Piao('603993')

    p1.start() #start会自动调用run
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    for connection in conns:
        connection.disconnect()