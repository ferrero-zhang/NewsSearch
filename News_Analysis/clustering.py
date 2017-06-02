#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import uuid
import jieba
import jieba.posseg as pseg
from gensim import corpora, models

CLUTO_INPUT_FOLDER = './cluto'
try:
    os.mkdir(CLUTO_INPUT_FOLDER)
except:
    pass

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
# CLUSTERING_CLUTO_EXECUTE_PATH = os.path.join(AB_PATH, './cluto-2.1.2/Linux-x86_64/vcluster')

CLUSTERING_CLUTO_EXECUTE_PATH = os.path.join(AB_PATH, './cluto-2.1.2/MSWIN-x86_64/vcluster.exe')

# 名词集合
NOUNSET = set(['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng'])

#----------------可调参数开始--------------#
# 聚类个数
CLUSTER_NUM = 10

# 分词时是否保留名词
IF_NOUN = False # True

# 分词时是否去掉单个词
IF_REMOVE_SINGLE = False # True

# 是否保留按照词频排序前TOPK个词
IF_TOP = False # True
TOPK = 10000
#----------------可调参数结束--------------#


def cluto_kmeans_vcluster(k, input_file, vcluster=None):
    '''
    cluto kmeans聚类
    input：
        k: 聚簇数
        input_file: cluto输入文件绝对路径
        vcluster: cluto vcluster可执行文件路径
    output：
        cluto聚类结果, list
    '''
    # handle default
    # 聚类结果文件, result_file
    result_file = input_file + '.clustering.%s' % k

    if not vcluster:
        vcluster = os.path.join(AB_PATH, CLUSTERING_CLUTO_EXECUTE_PATH)

    command = "%s -niter=20 %s %s" % (vcluster, input_file, k)
    os.popen(command)

    results = [line.strip() for line in open(result_file)]

    # if os.path.isfile(result_file):
    #    os.remove(result_file)

    #if os.path.isfile(input_file):
    #    os.remove(input_file)

    return results


def label2uniqueid(labels):
    '''
        为聚类结果不为其他类的生成唯一的类标号
        input：
            labels: 一批类标号，可重复
        output：
            label2id: 各类标号到全局唯一ID的映射
    '''
    label2id = dict()
    for label in set(labels):
        label2id[label] = str(uuid.uuid4())
    return label2id


def kmeans(items, k, process_for_cluto_func):
    """kmeans聚类
       input:
           cluto要求至少输入两条文本
           items: [{"text": u"新闻"}], 以unicode 编码
           process_for_cluto_func: 预处理的方法
       output:
           items: [{"label": "簇标签"}]
    """
    if len(items) < 2:
        raise ValueError("length of input items must be larger than 2")

    input_file = process_for_cluto_func(items)
    labels = cluto_kmeans_vcluster(k, input_file) # cluto聚类，生成文件，每行为一条记录的簇标签
    label2id = label2uniqueid(labels)

    for idx, item in enumerate(items):
        label = labels[idx]
        if int(label) != -1:
            item['label'] = label2id[label]
        else:
            # 将-1类归为其它
            item['label'] = 'other'

    return items


def process_for_cluto(inputs, cluto_input_filepath=None, ifreserveNoun=IF_NOUN, ifremoveSingleWord=IF_REMOVE_SINGLE, ifreserveTopWord=IF_TOP, topk=TOPK):
    """
    数据预处理函数
    input：
        inputs: 新闻数据, 示例：[{'text': u'新闻'}]
        ifreserveNoun： 分词时是否去掉非名词
        ifremoveSingleWord： 分词时是否去掉单个词
    output:
        cluto输入文件路径
    """
    # handle default
    if not cluto_input_filepath:
        cluto_input_filepath = os.path.join(CLUTO_INPUT_FOLDER, "cluto_input.txt")

    feature_set = set() # 不重复的词集合
    words_list = [] # 所有新闻分词结果集合
    fw = open(os.path.join(CLUTO_INPUT_FOLDER, "news_words.txt"), "w")
    for input in inputs:
        text = input['text'].encode("utf-8")
        words = pseg.cut(text)
        if ifreserveNoun:
            words = [[word, flag] for word, flag in words if flag in NOUNSET]

        if ifremoveSingleWord:
            words = [[word, flag] for word, flag in words if len(word) > 1]

        words = [w.encode("utf-8") for w, f in words]
        fw.write("%s\n" % " ".join(words))
        #print words
        words_list.append(words)
    fw.close()

    # 特征词字典
    dictionary = corpora.Dictionary(words_list)

    # 参考http://radimrehurek.com/gensim/corpora/dictionary.html
    if ifreserveTopWord:
        dictionary.filter_extremes(no_below=0, no_above=1.0, keep_n=topk)

    # Save this Dictionary to a text file, in format: id[TAB]word_utf8[TAB]document frequency[NEWLINE]. 
    # Sorted by word, or by decreasing word frequency.
    dictionary.save_as_text(os.path.join(CLUTO_INPUT_FOLDER, "feature_dict.txt"))
    print "特征词集合大小为： ", len(dictionary)

    corpus = [dictionary.doc2bow(words) for words in words_list]

    # 将feature中的词转换成列表
    feature_set = set(dictionary.keys())

    row_count = len(inputs) # documents count
    column_count = len(feature_set) # feature count
    nonzero_count = 0 # nonzero elements count

    file_name = cluto_input_filepath

    with open(file_name, 'w') as fw:
        lines = []

        for words in words_list:
            doc_bow = dictionary.doc2bow(words)
            nonzero_count += len(doc_bow)
            line = ' '.join(['%s %s' % (w + 1, c) for (w, c) in doc_bow]) + '\n'
            lines.append(line)

        fw.write('%s %s %s\n' % (row_count, column_count, nonzero_count))
        fw.writelines(lines)

    return file_name


def kmeans_clustering(docs, cluster_num):
    """kmeans长文本聚类
       input:
            docs 长文本集 示例：[{'text': u'长文本'}]
    """
    # 最小聚类输入信息条数，少于则不聚类
    MIN_CLUSTERING_INPUT = 20

    if len(docs) == 0:
        raise ValueError("docs length equals zero")
    elif 'text' not in docs[0]:
        raise ValueError("docs have no key named text")
    elif not isinstance(docs[0]["text"], unicode):
        raise ValueError("docs[0] text's encoding is not unicode")

    if len(docs) >= MIN_CLUSTERING_INPUT:
        results = kmeans(docs, cluster_num, process_for_cluto)
    else:
        # 如果信息条数小于MIN_CLUSTERING_INPUT,则直接归为其他类
        results = []
        for doc in docs:
            doc["label"] = "other"
            results.append(doc)
    return results

class DocCluster:  
    def __init__(self):
        self.index = dict()

    def add(self, clus_id, input):
        if clus_id in self.index:
            self.index[clus_id].append(input)
        else:
            d = []
            d.append(input)
            self.index[clus_id] = d

def output_docs_cluster(doc_cluster, features):
    """ 以可读形式输出聚类结果
    """
    index = docCluster.index
    fw_content = ""

    total_docs_num = sum([len(v) for k, v in index.iteritems()])
    clus_docs_num = dict([(k, len(v)) for k, v in index.iteritems()])

    cluster_idx = 0
    for k, docs in index.iteritems():
        if len(docs) < 3:
            continue

        clu_ratio = float(clus_docs_num.get(k))/float(total_docs_num)

        fw_content += '聚簇' + str(cluster_idx) + ':  (' + features.get(k, "") + ')  比例：'+str(round(clu_ratio, 4))+'\n'

        for doc in docs:
            fw_content += '      【' + doc["news_title"].replace("\n", "") + '】' + doc["news_content"].replace("\n", "") + '\n'
        fw_content += '\n\n'
        cluster_idx += 1

    return fw_content

def extract_features(doc_cluster, keyword_topk=10):
    """ 为类簇提取关键词，每个类提取排名前10的词语作为该类的主题词
        inputs: topk，每个类提取的主题词数量，根据frequency值由大到小提取
    """
    index = docCluster.index
    cluster_feature = dict()
    for label, docs in index.iteritems():
        features = freq_word(docs, keyword_topk)
        cluster_feature[label] = features

    return cluster_feature

def freq_word(docs, topk):
    from collections import Counter
    
    allwords = []
    for doc in docs:
        text = doc["text"].encode("utf-8")
        words = pseg.cut(text)
        words = [[word, flag] for word, flag in words if flag in NOUNSET and len(word) > 1]
        words = [w.encode("utf-8") for w, f in words]
        allwords.extend(words)

    ct = Counter(allwords)
    result = ct.most_common()[:topk]

    return ",".join([r[0] for r in result])


if __name__ == '__main__':
    # 加载数据
    from preprocess import final_input as news_items
    print "新闻总条数： ", len(news_items) 

    # 对新闻进行聚类
    documents = kmeans_clustering(news_items, CLUSTER_NUM)

    # 构造docCluster
    docCluster = DocCluster()
    for doc in documents:
        docCluster.add(doc.get("label", "other"), doc)

    # 获取每个类的topk代表词
    cluster_feature = extract_features(docCluster, keyword_topk=10)

    # 输出聚类结果到文件
    content = output_docs_cluster(docCluster, cluster_feature)
    with open(os.path.join(CLUTO_INPUT_FOLDER, "output_result.txt"), "w") as fw:
        fw.write(content)
