import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from config import *
from bs4 import BeautifulSoup
from selectQuery import *

class SpiderMajor:
    MAJOR_COLLECTION = "majors"
    MAJOR_COLLECTION_P = "majors_p"
    
    options = webdriver.ChromeOptions()
    options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"')
    
    browser = webdriver.Chrome(chrome_options=options)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
    cursor = conn.cursor()
    def index_page(self,schoolName,url,_985,_211,db):
        """
        抓取索引页
        """
        cookies = ''
        try:
            SpiderMajor.browser.get(url)
#             cookies = SpiderMajor.browser.get_cookies()
#             if cookies == '' or cookies == None:
#                 SpiderMajor.browser.add_cookie(cookies)
            html = SpiderMajor.browser.page_source
            doc = pq(html)

            soup = BeautifulSoup(str(doc), 'html.parser')
            tbodyRaw = soup.find('tbody')
            trs = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            for item in trs:

                major = {
                    'school':schoolName,
                    '_985':_985,
                    '_211': _211,
                    'department':item.find_all('td')[0].get_text(),
                    'major': item.find_all('td')[1].get_text(),
                    'direction': item.find_all('td')[2].get_text(),
                    'details_link': 'http://yz.chsi.com.cn/'+ item.find_all('td')[6].find('a').get('href')
                }
                print("major in item:")
                print(major)
                
                sc = major['school']
                _985 = str(major['_985'])
                _211 = str(major['_211'])
                department = major['department']
                mj = major['major']
                direction = major['direction']
                details_link = major['details_link']
                
                cur_sql_users_value ="('" + sc + "','" + _985 + "','"+ _211 + "','"+ department + "','"+ mj + "','"+ direction+ "','"+ details_link+ "')"
                cur_sql_users= "insert into " + db + "(school,_985,_211,department,major,direction,details_link) values"  + cur_sql_users_value
                print("sql语句为:" + cur_sql_users)
                SpiderMajor.cursor.execute(cur_sql_users)
                SpiderMajor.conn.commit()

        except TimeoutException:
            print("爬取专业信息失败")


    def main(self,db,major_type):
        query = Query()
        schools_collection = ''
        if major_type == 0 :
            schools_collection = SCHOOLS_COLLECTION
        if major_type != 0 :
            schools_collection = SCHOOLS_COLLECTION_P
        major_links = query.query_ms_schools(schools_collection)
        print("返回爬取major要用到的school表")
        print(major_links)

        for major_link in list(major_links):
            url = major_link['link']
            schoolName = major_link['school']
            _985 = major_link['_985']
            _211 = major_link['_211']
            self.index_page(schoolName,url,_985,_211,db)


if __name__ == '__main__':
    spiderMajor = SpiderMajor()
    db = spiderMajor.MAJOR_COLLECTION
    db_p = spiderMajor.MAJOR_COLLECTION_P

    spiderMajor.main(db,0)#爬取学硕
#     spiderMajor.main(db_p,1)#爬取专硕
