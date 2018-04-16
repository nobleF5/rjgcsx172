import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from Craweler.config import *
from bs4 import BeautifulSoup
from Craweler.selectQuery import *

class SpiderMajor:
    MAJOR_COLLECTION = "majors"
    MAJOR_COLLECTION_P = "majors_p"
    browser = webdriver.Chrome()

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    client = pymongo.MongoClient(MONGO_URL)
    mongo_db = client[MONGO_DB]


    def index_page(self,schoolName,url,_985,_211,db):
        """
        抓取索引页
        """
        cookies = ''
        try:
            SpiderMajor.browser.get(url)
            cookies = SpiderMajor.browser.get_cookies()
            if cookies == '' or cookies == None:
                SpiderMajor.browser.add_cookie(cookies)
            html = SpiderMajor.browser.page_source
            doc = pq(html)

            soup = BeautifulSoup(str(doc), 'html.parser')
            tbodyRaw = soup.find('tbody')
            trs = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            for item in trs:
                # print('item\n', item)

                major = {
                    'school':schoolName,
                    '_985':_985,
                    '_211': _211,
                    'department':item.find_all('td')[0].get_text(),
                    'marjor': item.find_all('td')[1].get_text(),
                    'direction': item.find_all('td')[2].get_text(),
                    'details_link': 'http://yz.chsi.com.cn/'+ item.find_all('td')[6].find('a').get('href')
                }
                print(major)
                self.save_to_mongo(major,db)

        except TimeoutException:
            print("爬取院校失败")

    def save_to_mongo(self,result,db):
            """
            保存至MongoDB
            :param result: 结果
            """
            try:
                if SpiderMajor.mongo_db[db].insert(result):
                    print('存储到MongoDB成功')
            except Exception:
                print('存储到MongoDB失败')


    def main(self,db,major_type):
        query = Query()
        schools_collection = ''
        if major_type == 0 :
            schools_collection = SCHOOLS_COLLECTION
        if major_type != 0 :
            schools_collection = SCHOOLS_COLLECTION_P
        major_links = query.query_majors(schools_collection)

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

    # spiderMajor.main(db,0)#爬取学硕
    spiderMajor.main(db_p,1)#爬取专硕
