import pymongo
from Craweler.config import *

class Query:

    def __init__(self):
        self.link_dics = []
        self.details_dics = []

    def query_majors(self,schools_collection):
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

    def query_details(self,majors_collection_db):
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        majors_collection = db[majors_collection_db]

        for collection in majors_collection.find():
            details_dic = {
                'url':collection['details_link'],
                '_985':collection['_985'],
                '_211': collection['_211'],
                'school':collection['school'],
                'department':collection['department'],
                'marjor':collection['marjor'],
                'direction':collection['direction']
            }
            self.details_dics.append(details_dic)
        return  self.details_dics

    def main(self):
        # majors = self.query_majors()
        major = self.query_details()
if __name__ == '__main__':
    query = Query()
    query.main()