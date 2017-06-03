
一、演示说明

1. Python

(1)双击python-2.7.13.msi，即可安装

(2)安装完成之后在计算机系统属性中加入python可执行路径，将C:\Python27和C:\Python27\Scripts加入系统PATH变量中，加入过程可参考https://jingyan.baidu.com/article/48206aeafdcf2a216ad6b316.html

(3)win + R键运行CMD命令行，输入python，回车，看到python的shell即视为python安装成功，输入easy_install确认可以安装python的包

(4)python运行，两种方式：1）命令行运行参考http://www.cnblogs.com/simon-c/p/4562080.html；2）IDLE运行

(5)（可选）必要时安装Anaconda（该安装包将python和许多常用的package如numpy科学计算包等打包，方便python初学者直接使用），双击Anaconda2-4.4.0-Windows-x86_64.exe即可安装

2、执行install.bat，安装完polyglot之后需要把C:\Python27\Lib\site-packages\polyglot\downloader.py中261行前加入path.sep = "/"，保存，把polyglot_data拷贝到C:\Users\***\AppData\Roaming目录下，安装完毕

3、运行News_Scrapy文件夹下的crawl_news.bat，抓取163网易新闻数据，大概需要运行二十分钟

4、运行News_Index文件夹下相关脚本，进行新闻索引构建（袁昆说明）

5、进入News_Analysis文件夹下，python clustering.py 执行新闻聚类，同时可以调参，查看效果；执行python sentiment.py 选定某个子话题，进行实体情感分析


二、作业说明

1. 新闻检索子任务：查询标题中含有“龙卷风”时间是在2015年12月1日至31日之间的所有新闻，并写入文件

2. 新闻聚类子任务：通过调整参数（包括设置聚类个数、是否去除单个词、是否保留名词、是否保留高频词等），对新闻聚类效果进行调优 

3. 实体情感分析子任务：从聚类结果中找一个比较感兴趣的子话题，对子话题的所有新闻进行命名实体识别，并分析新闻报道中实体的极性走势