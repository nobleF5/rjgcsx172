'''
Created on 2018年5月21日

@author: Administrator
'''

import pymssql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from config import *
from bs4 import BeautifulSoup
from yanzhao.selectQuery import *

class AcceptStuInfo:
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
    cursor = conn.cursor()
    
    def index_page(self,url,dep_id,detail_collection_save):
        """
        抓取索引页
        """
        try:
            AcceptStuInfo.browser.get(url)
            html = AcceptStuInfo.browser.page_source
            doc = pq(html)
            soup = BeautifulSoup(str(doc), 'html.parser')

            zsml_condition = soup.select('.zsml-condition')
            zsml_summmary = BeautifulSoup(str(zsml_condition), 'html.parser').find_all('tr')[4]
            number = BeautifulSoup(str(zsml_summmary), 'html.parser').find_all('td')[1].get_text()

            zhaosheng_number = 0
            tuimian_number = 0
            if (len(number.split(',')) > 1):
                zhaosheng_number = int(number.split(',')[0].split('：')[1])
                tuimian_number = int(number.split(',')[1].split('：')[1])

            example_scope =  ''
            zsml_result = soup.select('.zsml-result')
            zsml_result_items = BeautifulSoup(str(zsml_result), 'html.parser').select('.zsml-res-items')
            
            for zsml_result_item in zsml_result_items:
                
                zsml_result_item_tds = BeautifulSoup(str(zsml_result_item), 'html.parser').find_all('td')

                for zsml_result_item_td in zsml_result_item_tds:
                    example_scope += zsml_result_item_td.get_text() + ','

                example_scope = example_scope.replace('\n','').replace(' ','').replace('见招生简章','')
                example_scope += ';'
#             details = {
#                 'school':school,
#                 '_985':_985,
#                 '_211':_211,
#                 'department':department,
#                 'major': major,
#                 'direction': direction,
#                 'zhaosheng_number': zhaosheng_number,
#                 'tuimian_number': tuimian_number,
#                 'example_scope':example_scope
#             }
#             print(details)
            
#              insert into [yanzhao].[dbo].[details] (school,_985,_211,department,major,direction,zhaosheng_number,tuimian_number,example_scope)
#         values('jxufe',1,1,'aa','bb','cc',12,12,'scope')
            print('example_scope:\n',example_scope)
            cur_sql_users_value ="('" + str(dep_id) + "','" + str(zhaosheng_number) + "','"+ str(tuimian_number) + "','"+ example_scope + "')"
            cur_sql_users= "insert into " + detail_collection_save + "(dep_id,acce_stu_num,acce_stu_recommend_nu,acce_stu_exam_scop) values"  + cur_sql_users_value
            print("sql语句为:" + cur_sql_users)
            AcceptStuInfo.cursor.execute(cur_sql_users)
            AcceptStuInfo.conn.commit()

        except TimeoutException:
            print("爬取院校失败")

    def main(self,query_db_num,detail_collection_save):
        query = Query()
        majors_collection_db = ''
        if query_db_num == 0:
            majors_collection_db = DepartmentInfo_COLLECTION
        if query_db_num != 0:
            majors_collection_db = DepartmentInfo_COLLECTION
        #从major中查出数据给details
        details_link = query.query_ms_majors(majors_collection_db)
        print(details_link)
        for detail_link in list(details_link):
            dep_id = detail_link['dep_id']
            acce_stu_url = detail_link['acce_stu_url']
            self.index_page(acce_stu_url,dep_id,detail_collection_save)

        
if __name__ == '__main__':
    acceptStuInfo = AcceptStuInfo()
    
#     acceptStuInfo.index_page('http://yz.chsi.com.cn//zsml/kskm.jsp?id=1014021018085212001','1',AcceptStuInfo_COLLECTION);

    #爬取学硕
#     detail_collection_save = AcceptStuInfo_COLLECTION
#     spider.main(0,detail_collection_save)

    #爬取专硕
    detail_collection_save_p = AcceptStuInfo_COLLECTION
    acceptStuInfo.main(1, detail_collection_save_p)

    # number = '专业：12,其中推免：4'
    # zhaosheng_number = number.split(',')[0].split('：')[1]
    # tuimian_number = number.split(',')[1].split('：')[1]
    # print(zhaosheng_number)
    # print(tuimian_number)
