# -*-coding:utf-8-*-

from elasticsearch import Elasticsearch

es = Elasticsearch("127.0.0.1:9200", timeout=600)
# es = Elasticsearch("219.224.134.216:9202", timeout=600)

def create_mapping(index_name):
    index_info = {
        'settings':{
            'number_of_replicas': 0,
            'number_of_shards': 5,
            'analysis':{
                'analyzer':{
                    'my_analyzer':{
                        'type': 'pattern',
                        'pattern': '&'
                    }
                }
            }
        },
        'mappings':{
            'text':{
                'properties':{
                    "url":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "title":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "content":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "source":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "timestamp":{
                        'type': 'long',
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)


if __name__=='__main__':
    create_mapping("news")
