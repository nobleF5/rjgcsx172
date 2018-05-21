import pymssql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from yanzhao.query_shengfen import *
from config import *
import re


class AcademyInfo:
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
    cursor = conn.cursor()

    def index_page(self,schoolCode,string3,db):

        try:
            url = 'http://yz.chsi.com.cn/zsml/zyfx_search.jsp'
            AcademyInfo.browser.get(url)

            filename_part1 = 'js/jumpToSchool_part1.txt'
            file_part1 = open(filename_part1, 'rb')
            string1 = file_part1.read().decode('utf-8')

            string = string1 + schoolCode + string3

            print("执行jumpToSchool.txt中的命令")
            AcademyInfo.browser.execute_script(string)

            html = AcademyInfo.browser.page_source
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
                
                sc = school['school']
                aca_no_start = sc.index(')')+1
                
                final_local = school['local']
                final_local_start = final_local.index(')')+1
                
                link = school['link']
                aca_name = re.findall('\((.*?)\)', sc)[0]
                aca_no = sc[aca_no_start:]
                local = final_local[final_local_start:]
                _985 = str(school['_985'])
                _211 = str(school['_211'])
                
                '''
                 insert into [yanzhao].[dbo].[academy_info](dep_url,aca_name,aca_no,aca_city,aca_985,aca_211) values('http://yz.chsi.com.cn//zsml/querySchAction.do?ssdm=11&dwmc=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&mldm=&mlmc=&yjxkdm=0835&xxfs=&zymc=','北京大学','10001','(11)北京市','True','True')
 
                '''
                cur_sql_users_value ="('" + link + "','" + aca_name + "','" + aca_no + "','"+ local + "','"+ _985 + "','"+ _211 + "')"
                cur_sql_users= "insert into " + db + "(dep_url,aca_name,aca_no,aca_city,aca_985,aca_211) values"  + cur_sql_users_value
                print(cur_sql_users)
                AcademyInfo.cursor.execute(cur_sql_users)
                AcademyInfo.conn.commit()

        except TimeoutException:
            print("爬取院校失败")


    def main(self,mldm):

        request_Spider = Request_Spider()
        filename = 'js/shengfen.txt'
        print(filename)
        lines = request_Spider.spider_reader(filename)

        string3 = ''
        db = ''
        # 爬取学硕信息
        if(mldm == 0):
            filename_part2 = 'js/jumpToSchool_part2.txt'
            file_part2 = open(filename_part2, 'rb')
            string3 = file_part2.read().decode('utf-8')
            db = AcademyInfo_COLLECTION

        # 爬取专硕信息
        if (mldm != 0):
            filename_part2 = 'js/jumpToSchool_part2_professional.txt'
            file_part2 = open(filename_part2, 'rb')
            string3 = file_part2.read().decode('utf-8')
            db = AcademyInfo_COLLECTION

        for line in lines:
            self.index_page(line,string3,db)

        # shengfencode = '46'
        # self.index_page(shengfencode)

        AcademyInfo.browser.close()



if __name__ == '__main__':
    spiderSchool = AcademyInfo()
    spiderSchool.main(1)# 爬取学硕信息

#     AcademyInfo.main(1)# 爬取专硕信息
