# -*-coding:utf-8-*-

import json
from mapping import es
from time_utils import ts2datetime, datetime2ts

# example 1
# 查询“新华社”发布的，时间在2017-3-1到2017-5-1的新闻
# 并写入 “xinhuashe.txt”的文件中

def query_body_1():
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term": {"source": "新华社"}}, # 消息来源是新华社
                    {"range":{
                        "timestamp":{
                            "gte": datetime2ts("2017-3-1"), # 时间大于等于3.1
                            "lt": datetime2ts("2017-5-1") # 时间小于5.1
                        }
                    }}
                ]
            }
        },
        "size": 100, # 最多返回100个
        "sort": {"timestamp":{"order": "desc"}} # asc，按照时间先后顺序返回
    }

    ff = open("xinhuashe.txt","w")
    results = es.search(index="news", doc_type="text", body=query_body)["hits"]["hits"]
    for item in results:
        ff.write(json.dumps(item["_source"])+"\n")
        print item["_source"]

    print "finish"

    ff.close()


##example 2
# 查询“新华社”发布的内容中包括“萨德”的所有新闻

def query_body_2():
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term":{"source":"新华社"}}, # 消息来源是新华社
                    {"wildcard":{ "content":"*萨德*"}} # 内容中包含萨德关键词
                ]
            }
        },
        "size": 10
    }


    ff = open("sade.txt","w")
    results = es.search(index="news", doc_type="text", body=query_body)["hits"]["hits"]
    for item in results:
        ff.write(json.dumps(item["_source"])+"\n")
        print item["_source"]

    print "finish"

    ff.close()


if __name__ == "__main__":
    query_body_1()
    query_body_2()

