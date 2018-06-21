# -*- coding:utf-8 -*-
import urllib.request as urllib2

import datetime

import os
import requests
from bs4 import BeautifulSoup
import tushare as ts
import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


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
    得到相关股票的公告URL地址
    """
    url_list = []
    title_list = []
    url = r"http://stockpage.10jqka.com.cn/ajax/code/{}/type/news/".format(code)
    soup = get_html( url )
    # 得到研报URL
    title = soup.findAll( 'a', {'class': 'client'} )
    for t in title:
        url = t.get( 'href' )
        if "news.10jqka.com.cn/field/sn" in url:
            title = t.get( 'title' )
            title_list.append( title )
            url_list.append(url)
    return url_list, title_list


def get_pdf_url(url_list):
    pdf_url_list = []
    for url in url_list:
        soup = get_html(url)
        title = soup.findAll( 'a', {'target': '_blank'} )
        for t in title:
            # print(t.get('href'))
            pdf_url_list.append(t.get('href'))
            # return t.get('href')
    return pdf_url_list


def download_file(url, file_path):
    """
    下载文件
    """
    r = requests.get(url) # create HTTP response object
    with open(file_path, 'wb') as f:
        f.write(r.content)


def parse(pdf_path, txt_path):
    fp = open(pdf_path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(txt_path, 'a') as f:
                        results = x.get_text().strip()
                        # print(results.strip())
                        f.write(results + '\n')


def get_code_list():
    """
    得到所有股票列表
    """
    df = ts.get_stock_basics()
    df["code"] = df.index
    return df["code"].values.tolist()


if __name__ == '__main__':
    # 当前日期
    target_date = datetime.datetime.now()
    now_date = target_date.strftime( "%Y-%m-%d" )
    #股票代码列表
    code_list = get_code_list()
    for code in code_list:
        # 保存文件路径
        file_path = os.path.join("./data/notice", now_date, code)
        print( "正在保存股票：{}，相关的公告...".format( code ) )
        if not os.path.exists( file_path ):
            os.makedirs( file_path )
        url_list, title_list = get_url_list(code)
        pdf_url = get_pdf_url(url_list)
        for url_list, pdf_url, txt_title in zip(url_list, pdf_url, title_list):
            # print(url_list, pdf_url, txt_title)
            pdf_path = os.path.join(file_path, txt_title.strip().replace( "/", "_" ) + ".pdf")
            download_file(pdf_url, pdf_path)
            txt_path = os.path.join( file_path, txt_title.strip().replace( "/", "_" ) + ".txt" )
            try:
                parse( pdf_path, txt_path )
            except Exception as e:
                pass
            continue
