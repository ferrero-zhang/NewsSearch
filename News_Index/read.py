#-*-coding: utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

from mapping import es
from time_utils import datehour2ts, datetime2ts
import json

f = open("news.json")
count = 0
bulk_action = []
index_count = 0
for line in f:
    item = json.loads(line.strip())
    print "---------------"
    print item.keys()
    try:
        url = item["news_url"] # 新闻URL
        title = item["news_title"] # 新闻标题
        content = item["news_content"] # 新闻内容
        source = item["news_source"] # 新闻来源
        date = item["news_date"].strip() # 日期
        #print url, title, content, source, date
        count += 1
        print count
    except:
        continue

    # 建索引的代码从这里开始写
    index_dict = dict()
    index_dict["url"] = url
    index_dict["title"] = title
    index_dict["content"] = content
    index_dict["source"] = source
    try:
        index_dict["timestamp"] = datehour2ts(date)
    except:
        index_dict["timestamp"] = datetime2ts(date)
    bulk_action.extend([{"index":{"_id":url}}, index_dict])
    index_count += 1

    if index_count !=0 and index_count % 100 == 0:
        es.bulk(bulk_action, index="news", doc_type="text")
        bulk_action = []
        print "finish index: ", index_count

if bulk_action:
    es.bulk(bulk_action, index="news", doc_type="text")
print "total index: ", index_count

f.close()
