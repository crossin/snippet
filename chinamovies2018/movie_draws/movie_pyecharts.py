
# coding: utf-8

# In[8]:


import pymongo
import numpy as np
from pyecharts import Scatter, Bar, Grid, Overlap

client = pymongo.MongoClient()
db = client.chinamovies
collections = db.movies
collections_detail = db.moviesdetail
col_casts = db.casts
col_directors = db.directors


# In[9]:


genre = {}
other_list = ['武侠', '悬疑', '儿童', '历史', '家庭', '古装', '传记', '纪录片', '音乐', '歌舞', '恐怖', '灾难', '运动', '同性', '西部', '戏曲']
for i, element in enumerate(collections_detail.find({'boxoffice_num':{'$exists':True}})):
    if element['rating']['average'] == 0 or element['rate_quantity'] == '0' or not element['boxoffice_num']:
        continue
    for index, gen in enumerate(element['genres'], start=1):
        if gen not in other_list:
            break
        if index == len(element['genres']):
            gen = '其它'
    if not genre.get(gen):
        genre[gen] = {'title': [], 'rate': [], 'boxoffice': [], 'rate_quantity': []}
    genre[gen]['title'].append(element['title'])
    genre[gen]['rate'].append(element['rating']['average'])
    genre[gen]['boxoffice'].append(round(element['boxoffice_num']/10000,2))
    genre[gen]['rate_quantity'].append(element['rate_quantity'])

scatter = Scatter("电影评分-票房")
other_setting = {
    'legend_orient': 'vertical',
    'legend_pos': 'right',
    'legend_top': 'center',
    'is_datazoom_show': True,
    'datazoom_type': 'both',
    'datazoom_range':[0,40],
}
total_num = 0
for i in genre:
    total_num += len(genre[i]['rate'])
#     print(i)
#     print(len(genre[i]['boxoffice']), genre[i]['boxoffice'])
#     print(len(genre[i]['rate']), genre[i]['rate'])
#     print(len(genre[i]['title']), genre[i]['title'])
#     print(len(genre[i]['rate_quantity']), genre[i]['rate_quantity'])
#     print('===============================')
    scatter.add(i, genre[i]['boxoffice'], genre[i]['rate'], **other_setting, extra_name=genre[i]['title'], 
                xaxis_name='票房（亿）', yaxis_name='评分', yaxis_name_gap=20,yaxis_min=2, symbol_size=5, 
                label_formatter='{c}', is_label_emphasis=True, is_toolbox_show=False)#  xaxis_name_gap=80, 
print('该图电影总数',total_num)
scatter#.render('电影评分-票房.html')


# 上图是 电影豆瓣评分-票房 散点图，用点的颜色表现了不同电影类型，包括了2018年国内上映电影中同时有豆瓣评分和票房数据的291部。
# 
# 由于很多类型的电影数量较少，因此将部分类型定为‘其它’。一部电影通常具有多个类型，在分析时，电影类型的确定方法为：按照每一部电影豆瓣上类型的先后顺序，选择顺序最前且不是‘其它’类型的类型；若该电影所有类型都在‘其它’类型中，将此电影归类为其它。
# 
# 电影票房较高，超过10亿时，其豆瓣评分都在五分及以上；而电影票房较少的电影（小于1亿）豆瓣评分和票房基本无关。

# In[10]:


count = 0
title = []
maoyan = []
mtime = []
imdb = []
douban = []
for i, element in enumerate(collections_detail.find({'boxoffice_num':{'$exists':True}})):
    if element.get('猫眼') and element.get('时光') and element.get('imdb'):
        # [ int(i) for i in [element['猫眼']['rank'], element['时光']['rank'], element['imdb']['rank']] if int(i)>0]
        if float(element['猫眼']['rank']) > 0 and float(element['时光']['rank']) > 0 and float(element['imdb']['rank']) > 0 and float(element['rate_score']) > 0:
            title.append(element['title'])
            maoyan.append(element['猫眼']['rank'])
            mtime.append(element['时光']['rank'])
            imdb.append(element['imdb']['rank'])
            douban.append(element['rate_score'])
            # print(i, element['title'], element['猫眼']['rank'], element['时光']['rank'], element['imdb']['rank'], 'count', count)
            count += 1
# print(len(title), title)
# print(len(maoyan), maoyan)
# print(len(mtime), mtime)
# print(len(imdb), imdb)
# print(len(douban), douban)

douban = [float(i) for i in douban]
imdb = [float(i) for i in imdb]
maoyan = [float(i) for i in maoyan]
mtime = [float(i) for i in mtime]
d_imdb = np.polyfit(douban, imdb, 1)
d_maoyan = np.polyfit(douban, maoyan, 1)
d_mtime = np.polyfit(douban, mtime, 1)
c_imdb = [[0,d_imdb[1]],[10, d_imdb[0]*10 + d_imdb[1]]]
c_maoyan = [[0,d_maoyan[1]],[10, d_maoyan[0]*10 + d_maoyan[1]]]
c_mtime = [[0,d_mtime[1]],[10, d_mtime[0]*10 + d_mtime[1]]]
print('imdb',d_imdb,'maoyan',d_maoyan,'mtime',d_mtime)


# In[11]:


scatter = Scatter("电影评分对比", width=400)
mark_lines = [{'name':'平均线','coord':[2,2]},{'name':'平均线','coord':[10,10]}]
scatter.add('douban-imdb', douban, imdb, extra_name=title, is_toolbox_show=False, mark_line_coords=c_imdb, is_legend_show=False, xaxis_name='douban', yaxis_name='imdb', yaxis_name_gap=20, xaxis_min=0, yaxis_min=0, symbol_size=5, label_formatter='{c}')
scatter#.render('douban-imdb.html')


# 上图为同一部电影豆瓣评分-imdb评分对比，数据包括了同时具有豆瓣评分、imdb评分、猫眼评分、时光网评分的201部电影，可以看出豆瓣和imdb评分相关性较高。两个网站上的中外群众的审美较为一致。

# In[12]:


scatter = Scatter("电影评分对比", width=400)
scatter.add('douban-maoyan', douban, maoyan, extra_name=title, mark_line_coords=c_maoyan, is_toolbox_show=False, is_legend_show=False, xaxis_name='douban', yaxis_name='maoyan', yaxis_name_gap=20, xaxis_min=0, yaxis_min=0, symbol_size=5, label_formatter='{c}')
scatter#.render('douban-maoyan.html')


# 上图为同一部电影豆瓣评分-猫眼评分对比，数据包括了同时具有豆瓣评分、imdb评分、猫眼评分、时光网评分的201部电影，可以看出猫眼的电影评分普遍较高，除了‘地球最后的夜晚’这部电影，这部电影豆瓣上评分为6.9，而在猫眼上的评分只有2.6。

# In[13]:


scatter = Scatter("电影评分对比", width=400)
scatter.add('douban-mtime', douban, mtime, extra_name=title, mark_line_coords=c_mtime, is_toolbox_show=False, is_legend_show=False, xaxis_name='douban', yaxis_name='mtime', yaxis_name_gap=20, xaxis_min=0, yaxis_min=0, symbol_size=5, label_formatter='{c}')
scatter#.render('douban-mtime.html')


# 上图为同一部电影豆瓣评分-时光网评分对比，数据包括了同时具有豆瓣评分、imdb评分、猫眼评分、时光网评分的201部电影，可以看出时光网电影和豆瓣电影相关性也较高，若一部电影在两个网站的评分都大于6，那么其评分会较为接近，说明两个网站的观影人群对高评分电影的评价较为一致。

# In[14]:


rank_boxoffice = []
rank_element = []
from pyecharts import Bar

for i, element in enumerate(collections_detail.find({'boxoffice_num':{'$exists':True}}).sort('boxoffice_num',-1)):
    rank_boxoffice.append(round(element['boxoffice_num']/10000,2))
    rank_element.append(element['title'])
    
bar = Bar('2018总票房排名')
bar.add('', rank_element[:10], rank_boxoffice[:10], grid_bottom=0.5, xaxis_interval=0, is_toolbox_show=False, xaxis_rotate=45, is_legend_show=False, xaxis_name='名称', yaxis_name='票房（亿）', xaxis_name_gap=100, yaxis_name_gap=30)

grid = Grid()
grid.add(bar, grid_bottom="30%")
grid#.render('总排名.html')


# 上图为2018年电影总票房前十名，‘红海行动’票房第一，共36.51亿票房。前十名中，国产电影占了5部，且票房前四名都是国产片。好的国产片能拿到越来越多的票房了。

# In[15]:


genres = {}
other_list = ['武侠', '悬疑', '儿童', '历史', '家庭', '古装', '传记', '纪录片', '音乐', '歌舞', '恐怖', '灾难', '运动', '同性', '西部', '戏曲']
for i, element in enumerate(collections_detail.find({'boxoffice_num':{'$exists':True}})):
    for genre in element['genres']:
        if genre in other_list:
            genre = '其它'
        if genre not in genres:
            genres[genre] = {'title':[], 'boxoffice_num':[],'score':[]}
        genres[genre]['title'].append(element['title'])
        genres[genre]['boxoffice_num'].append(element['boxoffice_num']/10000)
        genres[genre]['score'].append(element['rate_score'])

styles = []
boxoffice = []
avg_boxoffice = []
quantity = []
for i in sorted(genres.items(), key=lambda item:sum(item[1]['boxoffice_num']), reverse=True):
    styles.append(i[0])
    boxoffice.append(round(sum(genres[i[0]]['boxoffice_num']), 2))
    avg_boxoffice.append(round(np.mean(genres[i[0]]['boxoffice_num']), 2))
    quantity.append(len(genres[i[0]]['boxoffice_num']))
    
grid = Grid()
bar1 = Bar(title='类型-票房') # ,title_pos='40%'
bar2 = Bar()

bar1.add('总票房',styles, boxoffice, xaxis_name='类型', yaxis_name='总票房（亿）', yaxis_name_gap=40, is_toolbox_show=False)
bar2.add('平均票房', styles, avg_boxoffice, xaxis_name='类型', yaxis_name='平均票房（亿）', is_toolbox_show=False)

overlap = Overlap(width=1200, height=600)
overlap.add(bar1)
overlap.add(bar2, is_add_yaxis=True, yaxis_index=1)

grid.add(overlap, grid_right="20%")
grid#.render('类型-票房.html')


# 上图为2018年不同类型电影的总票房和平均票房。由于一部电影一般会有多个类型，因此在计算票房时，分别考虑了该电影的每个类型。以‘红海行动’为例，‘红海行动’为动作片、战争片，因此在动作片和战争片中，都分别考虑了‘红海行动’的票房。
# 
# 可以看出，就总票房而言，动作片总票房最高，喜剧片紧随其后。而就平均票房而言，科幻和战争片的平均票房较高，这可能是由于这些类型的电影制作用了更大的成本，制作较好，因此也回收了更多的票房。

# In[16]:


genres = {}
other_list = ['武侠', '悬疑', '儿童', '历史', '家庭', '古装', '传记', '纪录片', '音乐', '歌舞', '恐怖', '灾难', '运动', '同性', '西部', '戏曲']
for i, element in enumerate(collections_detail.find({'boxoffice_num':{'$exists':True}})):
    if element['rate_score']:
        for genre in element['genres']:
            if genre in other_list:
                genre = '其它'
            if genre not in genres:
                genres[genre] = {'title':[], 'score':[]}
            genres[genre]['title'].append(element['title'])
            genres[genre]['score'].append(float(element['rate_score']))
            
styles = []
avg_scores = []
quantity = []
for i in sorted(genres.items(), key=lambda item:np.mean(item[1]['score']), reverse=True):
    # print(i, ':', len(genres[i]['title']), len(genres[i]['score']))
    styles.append(i[0])
    avg_scores.append(round(np.mean(genres[i[0]]['score']),2))
    quantity.append(len(genres[i[0]]['title']))

grid = Grid()
bar1 = Bar(title='类型-评分') # ,title_pos='40%'
bar2 = Bar()

bar1.add('豆瓣平均分', styles, avg_scores, yaxis_min=4, xaxis_name='类型', yaxis_name='豆瓣平均分', yaxis_name_gap=30, is_toolbox_show=False)
bar2.add('电影数量', styles, quantity, xaxis_name='类型', yaxis_name='电影数量', yaxis_name_gap=40, is_toolbox_show=False)

overlap = Overlap(width=1200, height=600)
overlap.add(bar1)
overlap.add(bar2, is_add_yaxis=True, yaxis_index=1)

grid.add(overlap, grid_right="20%")
grid#.render('类型-评分.html')


# 上图为2018年不同类型电影的豆瓣平均分和拥有豆瓣评分的电影数量。由于一部电影一般会有多个类型，因此在计算平均分时，分别考虑了该电影的每个类型。以‘红海行动’为例，‘红海行动’为动作片、战争片，因此在动作片和战争片中，都分别考虑了‘红海行动’的豆瓣评分。
# 
# 可以看出，就评分而言，动画类型电影的豆瓣平均分最高，而惊悚片平均分最低。‘其它’类型的豆瓣评分也较高，这可能是由于‘其它’类型电影都较为小众，观影人群也较少，倾向于打高分。
# 
# 就电影数量而言，剧情片的数量最多，这可能是由于很多电影都会带有剧情的标签。

# In[17]:


month_tot = list(range(1,13))
other_list = ['武侠', '悬疑', '儿童', '历史', '家庭', '古装', '传记', '纪录片', '音乐', '歌舞', '恐怖', '灾难', '运动', '同性', '西部', '戏曲']
monthly_sum = {}
for i, element in enumerate(collections_detail.find({'boxoffice_num':{'$exists':True}})):
    month = int(element['releasedate'].split('(')[0].split('-')[1])
    if not element['genres']:
        # print(element['title'])
        continue
    for index, genre in enumerate(element['genres'], start=1):
        if genre not in other_list:
            break
        if index == len(element['genres']):
            genre = '其它'
    if not monthly_sum.get(genre):
        monthly_sum[genre] = [0,0,0,0,0,0,0,0,0,0,0,0]
    monthly_sum[genre][month-1] += element['boxoffice_num']

# print(monthly_sum)
bar = Bar('月份票房叠加图')
legend_setting = {
    'legend_orient': 'vertical',
    'legend_pos': 'right',
    'legend_top': 'center'
}
for type in monthly_sum:
    bar.add(type, month_tot, [round(i/10000,2) for i in monthly_sum[type]], **legend_setting, is_stack=True, xaxis_name='月份', yaxis_name='票房（亿）', yaxis_name_gap=40, is_toolbox_show=False)
bar#.render('月份票房.html')


# 上图为2018年各月电影票房总和，考虑到电影上映初期票房增加较快且缺少更加详细的月度票房数据，因此计算月度票房时，以电影上映日期所在月份作为标准。
# 
# 由于很多类型的电影数量较少，因此将部分类型定为‘其它’。一部电影通常具有多个类型，在分析时，电影类型的确定方法为：按照每一部电影豆瓣上类型的先后顺序，选择顺序最前且不是‘其它’类型的类型；若该电影所有类型都在‘其它’类型中，将此电影归类为其它。
# 
# 由图可知，2018年2月票房在全年票房中占比最多，且喜剧片贡献了大部分票房，考虑到2018年2月刚好是春节，这说明春节是一个电影票房高峰，喜剧片也在春节期间占了大头。另外，7月、8月票房在全年占比也较高，这可能是由于片商考虑到在校学生暑假，排片较多，同时学生也贡献了较多票房。

# In[19]:


casts = []
total_box = []
movie_casts = []
for i in col_casts.find().sort('total_box',-1)[:10]:
    casts.append(i['name'])
    total_box.append(round(i['total_box']/10000,2))
    movie_casts.append(i['movie'])
#     print(i)

# print(casts)
# print(total_box)
# print(movie_casts)

bar = Bar('2018年演员参演电影总票房排名')
bar.add('', casts, total_box, extra_name=movie_casts, is_legend_show=False, xaxis_name='姓名', yaxis_name='票房（亿）', yaxis_name_gap=30, xaxis_name_gap=30, xaxis_interval=0, is_toolbox_show=False)
bar#.render('演员参演电影总票房前十.html')


# 上图为2018年演员参演电影的总票房排名，计算时没有考虑演员在一部电影中所获的收入，只以该演员参演电影的总票房为准。
# 
# 由图可知，王成思2018年参演电影总票房为65.5亿，排名第一，他参演了‘唐人街探案2’，‘西虹市首富’，‘李茶的姑妈’这三部电影。
