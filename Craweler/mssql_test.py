# encoding:utf-8
import pymssql
from config import *

class Query:

    DB_URL = '139.199.212.114'
    DB = 'yanzhao'
    DB_COLLECTION = 'schools'
    USER = 'spider'
    PASSWORD = '123456'
    def __init__(self):
        self.link_dics = []
        self.details_dics = []

#     def query_users(self):
#         conn=pymssql.connect(host=DB_URL,user=USER,password=PASSWORD
#                              ,database= DB,charset='utf8') #
#         cursor = conn.cursor()
#         #
# #         cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
# #         row = cursor.fetchone()
# #         while row:
# #             print("ID=%d, Name=%s" % (row[0], row[1]))
# #             row = cursor.fetchone()
# #         pass
#         cursor.execute('SELECT * FROM users')
#         row = cursor.fetchone()
#         while row:
#             print("%s, %s" % (row[9], row[8]))
# #             print("%s, %s" % (str(row[1]).encode('utf-8'), str(row[2]).encode('utf-8')))
#             row = cursor.fetchone()
            
#             ,link,school,local,_985,_211,db_table
    def add(self):
        conn=pymssql.connect(host='139.199.212.114',user='spider',password='123456'
                              ,database= 'yanzhao',charset='utf8')
        cursor = conn.cursor()
#         school = {
#                     'link': 'http://yz.chsi.com.cn/'+ item.find('a').get('href'),
#                     'school': item.find('a').get_text(),
#                     'local': item.find_all('td')[1].get_text(),
#                     '_985': _985,
#                     '_211': _211
#                 }
#
# INSERT INTO [yanzhao].[dbo].[schools]
#            ([link]
#            ,[school]
#            ,[local]
#            ,[_985]
#            ,[_211])
#      VALUES
#            ('www.jxufe.cn'
#            ,'caida'
#            ,'nanchang'
#            ,1
#            ,1)

#         cur_sql= "insert into" + db_table + "(link,school,local,_985,_211) value(" + link+","+ school+","+ local+","+ _985+","+ _211+"," + ",)"
        cur_sql_users= "insert into " + 'schools' + "(link,school,local,_985,_211) values("  + "'www.yubajin.cn','caida','nanchang',1,0)"
        cursor.execute('insert into schools(link,school,local,_985,_211) values("http://yz.chsi.com.cn//zsml/querySchAction.do?ssdm=11&dwmc=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&mldm=&mlmc=&yjxkdm=0835&xxfs=&zymc=","(10001)北京大学","(11)北京市","True","True")')
        conn.commit()
        pass

    def main(self):
        pass
    
if __name__ == '__main__':
    query = Query()
    query.add()