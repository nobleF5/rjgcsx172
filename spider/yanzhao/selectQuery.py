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
                'aca_id':collection[0],
                'link':collection[6]
            }
            self.link_dics.append(link_dic)
 
        return  self.link_dics
    
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
                'dep_id': collection[0],
                'acce_stu_url':collection[2]
            }
            self.details_dics.append(link_dic)
 
        return  self.details_dics
    
    def query_acaIdByacaName(self, aca_name):
        conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
        cursor = conn.cursor()
        cur_sql = "SELECT aca_id FROM "+ AcademyInfo_COLLECTION + " WHERE aca_name = '"+ aca_name+"'"
        print(cur_sql)
        cursor.execute(cur_sql)  
        acaId = cursor.fetchone()
        return acaId[0]
    
    def main(self, major_type):
        # majors = self.query_majors()
#         majors_collection_db = MAJORS_COLLECTION_P
        collection = ""
        result = []
        if major_type == 0 :
            collection = AcademyInfo_COLLECTION
            result = self.query_ms_schools(collection)
        if major_type != 0 :
            collection = DepartmentInfo_COLLECTION
            result = self.query_ms_majors(collection)
       
        print(result)
        
        
if __name__ == '__main__':
    query = Query()
#     query.main(1)
    print(query.query_acaIdByacaName('北京大学'))

    #查询招生详情数据
#     majors_collection_db = MAJORS_COLLECTION
#     print(query.query_ms_majors(majors_collection_db))