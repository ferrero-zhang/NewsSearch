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
    	url = item["news_url"] # 新闻URL
    	title = item["news_title"] # 新闻标题
        content = item["news_content"] # 新闻内容
        source = item["news_source"] # 新闻来源
        date = item["news_date"] # 日期
        print url, title, content, source, date
        count += 1
        print count
    except:
    	continue

    # 建索引的代码从这里开始写
f.close()
