# coding: utf-8

# 1.分词
import jieba
with open('report19.txt') as f:
    s = f.read()
word_list = list(jieba.cut(s))
print('分词总数:', len(word_list))
print('示例:', word_list[:20])

# 2.统计词频
from collections import Counter
words_count = Counter(word_list)
most_words = words_count.most_common(128)
print(most_words)

# 去除符号和助词、介词等
# 这一步我们做了人工干预，手动选出一些忽略词
most_words = [words for words in most_words if words[0] not in ' ，、。“”（）！；的和是在要为以把了对中到有上不等更二从大\n']
print(most_words)

# 3.生成词云
# 生成词频 dict
dict_words = {}
for words in most_words:
    dict_words[words[0]] = words[1]

from wordcloud import WordCloud, ImageColorGenerator

# 读入图片
from scipy.misc import imread
bg_pic = imread('party.png')
# 配置词云参数
wc = WordCloud(
    # 因为中文显示，这里必须提供中文字体文件
    font_path = 'zhaozi.ttf',
    # 设置背景色
    background_color='red',
    # 词云形状
    mask=bg_pic,
    # 最大号字体
    max_font_size=100,
)
# 生成词云
wc.generate_from_frequencies(dict_words)
image_colors = ImageColorGenerator(bg_pic)
wc.recolor(color_func=image_colors)

# 画图
# import matplotlib.pyplot as plt
# plt.figure()
# plt.imshow()
# plt.axis('off')
# plt.show()

# 保存图片
wc.to_file('word_freq.jpg')

# 3.绘制条状图
# 生成 ECharts 配置数据，拼接出 HTML
# 也可直接通过 ECharts 官网生成图表

words_list = []
count_list =[]
for word in most_words[:32]:
    words_list.append(word[0])
    count_list.append(word[1])

# 指定图表的配置项和数据
option = """
var option = {
    title: {
        text: '十九大工作报告',
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['报告词频']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data: """ + str(words_list[::-1]) + """
    },
    series: [
        {
            name: '报告词频',
            type: 'bar',
            data: """ + str(count_list[::-1]) + """
        }
    ]
};
"""

head = """
<html>
<head>
    <meta charset="utf-8">
    <title>ECharts</title>
    <!-- 引入 echarts.js -->
    <script src="echarts.js"></script>
</head>
<body>
    <div id="showhere" style="width:800px; height:600px;"></div> 
    <script> 
    var myChart = echarts.init(document.getElementById('showhere'));
"""

tail = """
myChart.setOption(option);
</script>
</body>
</html>
"""

with open('word_freq.html', 'w') as f:
    f.write(head + option + tail)

