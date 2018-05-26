'''
Created on 2018年5月23日

@author: Administrator
'''
import pymssql
from config import *
from selenium import webdriver
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from yanzhao.selectQuery import *
from yanzhao import AcademyInfo
import threading
import time

class AcademyRankInfo:
    
    baseurl = 'http://www.gaokaopai.com/paihang-otype-2.html?f=1&ly=bd&city=&cate=&batch_type='
    
    browser = webdriver.Chrome()
    browser.get(baseurl)
    
    insert_db = AcademyRankInfo_COLLECTION
    script_file = 'js/academyRankInfo_loadMore.txt'
    enough_aca_ranking = 1500
    page_aca_ranking = 25
    
    def connect_database(self):
        conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
        return conn
    
    def open_script_file(self):
        script_file = open(AcademyRankInfo.script_file, 'rb')
        script_string = script_file.read().decode('utf-8')
        return script_string
    
    def clickLoadMore(self):
        for i in range(int(AcademyRankInfo.enough_aca_ranking / AcademyRankInfo.page_aca_ranking)):
            AcademyRankInfo.browser.execute_script(self.open_script_file())
    
    def load_page(self):
        conn = self.connect_database()
        cursor = conn.cursor()
        
        try:
            
            browser = AcademyRankInfo.browser
            
            '''
                预留30s管理员手动点击///无奈///
            '''
            time.sleep(30)
            
            html = browser.page_source
            doc = pq(html)
            soup = BeautifulSoup(str(doc),'html.parser')
            tbody = soup.select('.tbody-container')
            trs = BeautifulSoup(str(tbody), 'html.parser').find_all('tr')
            print('trs长度：',trs.__len__())
    #           SELECT aca_no FROM academy_info WHERE aca_name = '北京大学'
            for tr in trs:
                try:
                    aca_ranking = int(BeautifulSoup(str(tr), 'html.parser').select('.t1')[0].get_text())
                    aca_name = BeautifulSoup(str(tr), 'html.parser').select('.t2')[0].get_text()
                    query = Query()
                    aca_id = query.query_acaIdByacaName(aca_name)
                    cur_sql_academyRank_value ="('" + aca_id + "','" + aca_name + "','" + str(aca_ranking)+ "')"
                    cur_sql_academyRank = "insert into " + AcademyRankInfo.insert_db + "(aca_id,aca_name,aca_ranking) values"  + cur_sql_academyRank_value
                    print(cur_sql_academyRank)
                    cursor.execute(cur_sql_academyRank)
                    conn.commit()
                except Exception as e:
                    print(repr(e))
                    
        except TimeoutException:
            print("爬取院校失败")

    def start_index(self):
        academyRankInfo = AcademyRankInfo()
#         clickLoadMore = threading.Thread(target=academyRankInfo.clickLoadMore)   # 定义线程 
#         load_page = threading.Thread(target=academyRankInfo.load_page)
#         academyRankInfo.clickLoadMore()
#         clickLoadMore.start()
#         load_page.start()
#         academyRankInfo.clickLoadMore()
        print('加载完毕')
        academyRankInfo.load_page()
        
if __name__ == '__main__':
    academyRankInfo = AcademyRankInfo()
    academyRankInfo.start_index()
            
            
