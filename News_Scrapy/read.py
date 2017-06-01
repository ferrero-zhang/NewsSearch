#-*-coding: utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import json

f = open("news.json")
for line in f:
    item = json.loads(line.strip())
    print item.keys()
    print type(item["news_title"]), item["news_title"]
    #print item["news_key"]
f.close()