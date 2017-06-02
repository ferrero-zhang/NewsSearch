#-*-coding: utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import json

def load_news():
    news_url_set = set()
    items = []
    f = open("../News_Scrapy/news.json")
    count = 0
    for line in f:
        item = json.loads(line.strip())
        print "---------------"
        try:
            url = item["news_url"] # 新闻URL
            title = item["news_title"] # 新闻标题
            content = item["news_content"] # 新闻内容
            source = item["news_source"] # 新闻来源
            date = item["news_date"] # 日期
            print url, title, content, source, date
            count += 1
            if url not in news_url_set:
                news_url_set.add(url)
                items.append(item)
        except:
            continue
    f.close()

    return items

def weight_title_content():
    items = load_news()
    for item in items:
        item["text"] = item["news_title"] + item["news_content"]

    return items

final_input = weight_title_content()
