import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from Craweler.config import *
from Craweler.query_shengfen import *


class SpiderSchool:
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]

    def index_page(self,schoolCode,string3,db):
        """
        抓取索引页
        """
        try:
            url = 'http://yz.chsi.com.cn/zsml/zyfx_search.jsp'
            SpiderSchool.browser.get(url)

            filename_part1 = 'js/jumpToSchool_part1.txt'
            file_part1 = open(filename_part1, 'rb')
            string1 = file_part1.read().decode('utf-8')

            string = string1 + schoolCode + string3

            print("执行jumpToSchool.txt中的命令")
            SpiderSchool.browser.execute_script(string)

            html = SpiderSchool.browser.page_source
            doc = pq(html)

            soup = BeautifulSoup(str(doc), 'html.parser')
            tbodyRaw = soup.find('tbody')
            tbody = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            trr = BeautifulSoup(str(tbodyRaw), 'html.parser').find('tr')
            if '很抱歉' in trr.get_text():
                print('没有数据')
                return

            for item in tbody:
                # print('item\n', item)
                typeItems = item.select('.ch-table-center')[0]
                typespans = BeautifulSoup(str(typeItems), 'html.parser').find_all('span')

                types = ''
                for typespan in typespans:
                    types += typespan.get_text() + ','

                _985 = False
                _211 = False
                type_open = types.split(',')
                if (len(type_open) > 1):
                    if type_open[0] == '985':
                        _985 = True
                    if type_open[1] == '211':
                        _211 = True

                school = {
                    'link': 'http://yz.chsi.com.cn/'+ item.find('a').get('href'),
                    'school': item.find('a').get_text(),
                    'local': item.find_all('td')[1].get_text(),
                    '_985': _985,
                    '_211': _211
                }
                print(school)
                self.save_to_mongo(school,db)

        except TimeoutException:
            print("爬取院校失败")

    def save_to_mongo(self,result,db):
            """
            保存至MongoDB
            :param result: 结果
            """
            try:
                if SpiderSchool.db[db].insert(result):
                    print('存储到MongoDB成功')
            except Exception:
                print('存储到MongoDB失败')


    def main(self,mldm):

        request_Spider = Request_Spider()
        filename = 'js/shengfen.txt'
        lines = request_Spider.spider_reader(filename)

        string3 = ''
        db = ''
        # 爬取学硕信息
        if(mldm == 0):
            filename_part2 = 'js/jumpToSchool_part2.txt'
            file_part2 = open(filename_part2, 'rb')
            string3 = file_part2.read().decode('utf-8')
            db = 'schools'

        # 爬取专硕信息
        if (mldm != 0):
            filename_part2 = 'js/jumpToSchool_part2_professional.txt'
            file_part2 = open(filename_part2, 'rb')
            string3 = file_part2.read().decode('utf-8')
            db = 'schools_professional'

        for line in lines:
            self.index_page(line,string3,db)

        # shengfencode = '46'
        # self.index_page(shengfencode)

        SpiderSchool.browser.close()



if __name__ == '__main__':
    spiderSchool = SpiderSchool()
    # spiderSchool.main(0)# 爬取学硕信息

    spiderSchool.main(1)# 爬取专硕信息
