#-*-coding: utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import json

f = open("news.json")
count = 0
for line in f:
    item = json.loads(line.strip())
    print "---------------"
    print item.keys()
    try:
    	url = item["news_url"]
    	title = item["news_title"]
        content = item["news_content"]
        source = item["news_source"]
        date = item["news_date"]
        news_key = item["news_key"]
        print url, title, content, source, date, news_key
        count += 1
        print count
    except:
    	pass
f.close()
