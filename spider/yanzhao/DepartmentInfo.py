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
import re

class DepartmentInfo:
    
    options = webdriver.ChromeOptions()
    options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"')
    
    browser = webdriver.Chrome(chrome_options=options)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
    cursor = conn.cursor()
    def index_page(self,aca_id,url,db):
        """
        抓取索引页
        """
        cookies = ''
        try:
            DepartmentInfo.browser.get(url)
#             cookies = SpiderMajor.browser.get_cookies()
#             if cookies == '' or cookies == None:
#                 SpiderMajor.browser.add_cookie(cookies)
            html = DepartmentInfo.browser.page_source
            doc = pq(html)

            soup = BeautifulSoup(str(doc), 'html.parser')
            tbodyRaw = soup.find('tbody')
            trs = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            for item in trs:

                major = {
                    'aca_id':aca_id,
                    'department':item.find_all('td')[0].get_text(),
                    'dep_specialty': item.find_all('td')[1].get_text(),
                    'dep_direction': item.find_all('td')[2].get_text(),
                    'acce_stu_url': 'http://yz.chsi.com.cn/'+ item.find_all('td')[6].find('a').get('href')
                }
                print("major in item:")
                print(major)
                
                
#                 sc = school['school']
#                 aca_no_start = sc.index(')')+1
#                 
#                 link = school['link']
#                 aca_name = re.findall('\((.*?)\)', sc)[0]
#                 aca_no = sc[aca_no_start:]
                
                dep_no_name = major['department']
                dep_no_name_start = dep_no_name.index(')')+1
                dep_direction_raw = major['dep_direction']
                dep_direction_raw_start = dep_direction_raw.index(')')+1
                dep_specialty_raw = major['dep_specialty']
                dep_specialty_raw_start = dep_specialty_raw.index(')')+1
                
                dep_no = re.findall('\((.*?)\)', dep_no_name)[0]
                dep_name = dep_no_name[dep_no_name_start:]
                aca_id = major['aca_id']
                acce_stu_url = major['acce_stu_url']
                dep_specialty = dep_specialty_raw[dep_specialty_raw_start:]
                dep_direction = dep_direction_raw[dep_direction_raw_start:]
                
                cur_sql_users_value ="('" + str(aca_id) + "','" + dep_no + "','"+ dep_name + "','"+ dep_specialty + "','"+ dep_direction + "','"+ acce_stu_url + "')"
                cur_sql_users= "insert into " + db + "(aca_id,dep_no,dep_name,dep_specialty,dep_direction,acce_stu_url) values"  + cur_sql_users_value
                print("sql语句为:" + cur_sql_users)
                DepartmentInfo.cursor.execute(cur_sql_users)
                DepartmentInfo.conn.commit()

        except TimeoutException:
            print("爬取专业信息失败")


    def main(self,db,major_type):
        query = Query()
        schools_collection = ''
        if major_type == 0 :
            pass
#             schools_collection = AcademyInfo_COLLECTION
        if major_type != 0 :
            schools_collection = AcademyInfo_COLLECTION
        major_links = query.query_ms_schools(schools_collection)
        print("返回爬取major要用到的school表")
        print(major_links)

        for major_link in list(major_links):
            aca_id = major_link['aca_id']
            url = major_link['link']
            self.index_page(aca_id,url,db)


if __name__ == '__main__':
    departmentInfo = DepartmentInfo()
    db = DepartmentInfo_COLLECTION
#     db_p = spiderMajor.MAJOR_COLLECTION_P

#     departmentInfo.main(db, 0)#爬取学硕
    departmentInfo.main(db,1)#爬取专硕
