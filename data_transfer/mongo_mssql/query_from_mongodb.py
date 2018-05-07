# encoding:utf-8

import pymssql
import pymongo
from mongo_mssql.config import *
class Query:
    
    
   def query_details(self,details_collection_db):
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        details_collection = db[details_collection_db]

        conn=pymssql.connect(host= HOST,user= USER,password= PASSWORD
                              ,database= DATABASE,charset= UTF8)
        cursor = conn.cursor()
        for collection in details_collection.find():
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
            sc = details_dic['school']
            _985 = str(details_dic['_985'])
            _211 = str(details_dic['_211'])
            department = details_dic['department']
            mj = details_dic['marjor']
            direction = details_dic['direction']
            zhaosheng_number = str(details_dic['zhaosheng_number'])
            tuimian_number = str(details_dic['tuimian_number'])
            example_scope = details_dic['example_scope']
            
                
            cur_sql_users_value ="('" + sc + "','" + _985 + "','"+ _211 + "','"+ department + "','"+ mj + "','" + direction+ "','"+ zhaosheng_number+"','"+ tuimian_number+"','"+ example_scope+ "')"
            cur_sql_users= "insert into " + details_collection_db + "(school,_985,_211,department,major,direction,zhaosheng_number,tuimian_number,example_scope) values"  + cur_sql_users_value
            print(cur_sql_users)
            cursor.execute(cur_sql_users)
            conn.commit()
#             self.details_dics.append(details_dic)
            print(details_dic)
    
if __name__ == '__main__':
    query = Query()
#     details_collection_db = DETAILS_COLLECTION
    details_collection_db = DETAILS_COLLECTION_P
    query.query_details(details_collection_db)