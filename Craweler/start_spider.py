from Craweler.spiderSchool import *
from Craweler.spiderMajor import *
from Craweler.spiderDetails import *

spiderSchool = SpiderSchool()
spiderMajor = SpiderMajor()
spider = SpiderDetails()

# spiderSchool.main(1)# 爬取专硕学校信息
# db_p = spiderMajor.MAJOR_COLLECTION_P
# spiderMajor.main(db_p,1)#爬取专硕院校信息
# detail_collection_save_p = DETAILS_COLLECTION_P# 爬取专硕招生详情
# spider.main(1, detail_collection_save_p)

spiderSchool.main(0)# 爬取学硕学校信息
db = spiderMajor.MAJOR_COLLECTION
spiderMajor.main(db,0)#爬取学硕院校信息
detail_collection_save = DETAILS_COLLECTION# 爬取学硕招生详情
spider.main(0,detail_collection_save)



