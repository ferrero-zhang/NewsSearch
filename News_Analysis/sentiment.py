#-*-coding: utf-8-*-
"""使用如下NLP工具进行entity level sentiment analysis，进而对实体的新闻极性进行分析

   可参考如下资源：
   http://blog.csdn.net/qsc0624/article/details/50357518
   https://site.douban.com/146782/widget/notes/15462869/note/355625387/
   https://github.com/aboSamoor/polyglot
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import polyglot
from polyglot.text import Text

from polyglot.downloader import downloader
print downloader.download("sentiment2.zh")
print downloader.download("sentiment2.en")
print downloader.download("ner2.zh")
print downloader.download("ner2.en")
print downloader.download("embeddings2.zh")
print downloader.download("embeddings2.en")

if __name__ == '__main__':
    # 加载一个子话题的数据
    news_items = []
    f = open("./sentiment/sentiment_input.txt")
    for line in f:
    	item = dict()
        data = line.strip().split("datetextsplit")
        date = data[0]
        text = data[1].decode("utf-8")
        item["text"] = text
        item["news_date"] = date
        news_items.append(item)
    f.close()

    entity_sentiment_dict = dict()

    # 参考http://polyglot.readthedocs.io/en/latest/Sentiment.html#entity-sentiment进行entity level sentiment的提取
    fw1 = open("./sentiment/entity_sentiment_detail.txt", "w")
    for news in news_items:
    	# get each document
        text = news["text"]
        date = news["news_date"]
        text = Text(text)

        # First, we need split the text into sentneces, this will limit the words tha affect the sentiment of 
        # an entity to the words mentioned in the sentnece.
        for sent in text.sentences:
            print "\n句子: ", sent
            # Second, we extract the entities
            try:
                entities = sent.entities
                if len(entities) > 0:
                    fw1.write("\n%s\n" % sent)
            except:
            	continue
            for entity in entities:
                try:
                    entity_type = entity.tag
                    entity_name = entity[0]
                    # Finally, for each entity we identified, we can calculate the strength of the positive 
                    # or negative sentiment it has on a scale from 0-1
                    entity_pos = entity.positive_sentiment
                    entity_neg = entity.negative_sentiment
                    print "情感： ", entity_type, entity_name, "负面强度： ", entity_pos, "正面强度： ", entity_neg
                    fw1.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (entity_type, entity_name, "负面强度： ", entity_pos, "正面强度： ", entity_neg))
                except:
                    continue
                
                try:
                    entity_sentiment_dict[entity_type + entity_name].append([date, entity_pos, entity_neg])
                except KeyError:
                	entity_sentiment_dict[entity_type + entity_name] = [[date, entity_pos, entity_neg]]

    fw1.close()

    target_entity = "I-PER寅"
    vis_data = []

    fw = open("./sentiment/entity_sentiment.txt", "w")
    for ent, sent in entity_sentiment_dict.iteritems():
    	if ent == target_entity:
    		vis_data = sent
    	fw.write("%s\t%s\n" % (ent, sent))
    fw.close()
    
    # 合并相同的日期
    vis_data_dict = dict()
    for d in vis_data:
    	try:
            vis_data_dict[d[0]].append([d[1], d[2]])
        except KeyError:
        	vis_data_dict[d[0]] = [[d[1], d[2]]]

    vis_data_final = []
    for k, v in vis_data_dict.iteritems():
    	finalv = [k]
    	for v_ in zip(*v):
            finalv.append(float(sum(v_)) / len(v_))
        vis_data_final.append(finalv)

    sorted_data = sorted(vis_data_final, key=lambda (k1, k2, k3): k1, reverse=False)
    import numpy as np
    import matplotlib.pyplot as plt
    from pylab import *  
    mpl.rcParams[u'font.sans-serif'] = ['YouYuan']

    x_names = [k1 for k1, k2, k3 in sorted_data]
    x = np.arange(len(x_names))
    y1 = [k2 for k1, k2, k3 in sorted_data]
    y2 = [k3 for k1, k2, k3 in sorted_data]

    fig, ax = plt.subplots()
    line1, = ax.plot(x, y1, label='positive sentiment')
    line2, = ax.plot(x, y2, label='negative sentiment')
    ax.set_xticklabels(x_names)
    ax.legend(loc='up left')
    ax.set_title(target_entity)
    plt.show()
