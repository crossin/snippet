## “梅西离开巴萨”新闻评论统计分析

需安装库：**numpy、pandas、jieba、matplotlib、pyecharts、stylecloud、ipython**（建议使用 anaconda 开发包）

爬虫部分未包含在此代码中，项目中提供了抓取后的数据结果。因为抓取时间有所不同，所以项目中的数据和文章中略有偏差。

代码说明：

- messi.ipynb - 程序源代码 jupyter 版本
- messi.py - 程序源代码 py 版本
- messi.html -  jupyter 版本导出页面（包含可视化结果）
- messigowhere.csv - 抓取的评论数据
- baidu_stopwords.txt - 词云忽略词表

代码建议在 jupyter notebook 中运行；若使用 .py 版本需要自行增加导出语句，不然将看不到运行结果。

说明：本案例从体育网站“直播吧”抓取了近万条关于梅西离队的网友评论，并做了简单的文本可视化分析。

参考文章：[梅西离开巴萨？看看球迷们怎么说](https://mp.weixin.qq.com/s/FRhwwhBq2DKif0Zd9HOPkg)

作者：Scofield
来源：ImagineScofield

此代码中的疑问可在公众号 **Crossin的编程教室** （crossincode）里讨论

----

更多实用有趣的例程

欢迎关注“**Crossin的编程教室**”及同名 [知乎专栏](https://zhuanlan.zhihu.com/crossin)

![crossincode](../crossin-logo.png)
