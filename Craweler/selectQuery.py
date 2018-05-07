# encoding:utf-8
import pymssql
from config import *

class Query:

    def __init__(self):
        self.link_dics = []
        self.details_dics = []

    def query_ms_schools(self,schools_collection):
        conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
        cursor = conn.cursor()
        
        cur_sql = 'SELECT * FROM '+schools_collection
        print(cur_sql)
        cursor.execute(cur_sql)  
        schools = cursor.fetchall() 
        for collection in schools:
            link_dic = {
                'school':collection[1],
                'link':collection[0],
                'local':collection[2],
                '_985':collection[3],
                '_211': collection[4]
            }
            self.link_dics.append(link_dic)
 
        return  self.link_dics
    
    def query_schools(self,schools_collection):
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        schools_collection = db[schools_collection]
        for collection in schools_collection.find():
            link_dic = {
                'school':collection['school'][7:],
                'link':collection['link'],
                '_985':collection['_985'],
                '_211': collection['_211']
            }
            self.link_dics.append(link_dic)

        return  self.link_dics
    
    def query_details(self,details_collection_db):
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        majors_collection = db[details_collection_db]

# "_id" : ObjectId("5ada9ea0326ffe1f905d5724"),
#     "school" : "北京大学",
#     "_985" : true,
#     "_211" : true,
#     "department" : "(017)软件与微电子学院",
#     "marjor" : "(083500)软件工程",
#     "direction" : "(01)软件工程技术与环境",
#     "zhaosheng_number" : 810,
#     "tuimian_number" : 138,
#     "example_scope" : "(101)思想政治理论,(201)英语一,(301)数学一,(911)计算机专业基础,;"
        for collection in majors_collection.find():
            details_dic = {
                'school':collection['school'],
                '_985':collection['_985'],
                '_211': collection['_211'],
                'department':collection['department'],
                'marjor':collection['marjor'],
                'direction':collection['direction'],
                'zhaosheng_number':collection['zhaosheng_number'],
                'tuimian_number':collection['tuimian_number'],
                'example_scope':collection['example_scope']
            }
            self.details_dics.append(details_dic)
            print(details_dic)
        return  self.details_dics
    
    def query_ms_majors(self,majors_collection_db):
        conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
        cursor = conn.cursor()
        
        cur_sql = 'SELECT * FROM '+ majors_collection_db
        print(cur_sql)
        cursor.execute(cur_sql)  
        majors = cursor.fetchall() 
#           SELECT TOP 1000 [id]
#               ,[school]
#               ,[_985]
#               ,[_211]
#               ,[department]
#               ,[major]
#               ,[direction]
#               ,[details_link]
#           FROM [yanzhao].[dbo].[majors]

        for collection in majors:
            link_dic = {
                'school':collection[1],
                '_985':collection[2],
                '_211': collection[3],
                'department':collection[4],
                'major':collection[5],
                'direction': collection[6],
                'details_link': collection[7]
            }
            self.details_dics.append(link_dic)
 
        return  self.details_dics
    
    def main(self):
        # majors = self.query_majors()
#         majors_collection_db = MAJORS_COLLECTION_P
        schools_collection = SCHOOLS_COLLECTION
        schools = self.query_schools(schools_collection)
        print(schools)
        
        
if __name__ == '__main__':
    query = Query()
#     query.main()

    #查询招生详情数据
    majors_collection_db = MAJORS_COLLECTION
    print(query.query_ms_majors(majors_collection_db))