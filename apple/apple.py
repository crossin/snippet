
# coding: utf-8

# In[50]:


# 获取年报文件
import requests
url = 'http://investor.apple.com/feed/SECFiling.svc/GetEdgarFilingList?apiKey=BF185719B0464B3CB809D23926182246&exchange=CIK&symbol=0000320193&formGroupIdList=1%2C4&excludeNoDocuments=true&pageSize=-1&pageNumber=0&tagList=&includeTags=true&year=-1&excludeSelection=1'
rsp = requests.get(url)
data = rsp.json()
data


# In[61]:


# 下载
import urllib.request
for year_data in data['GetEdgarFilingListResult']:
    year = year_data['FilingDate'].split()[0].split('/')[-1]
    for doc in year_data['DocumentList']:
        if doc['DocumentType'] == 'XLS':
            url_xls = doc['Url']
            break
    print(year, url_xls)
    urllib.request.urlretrieve(url_xls, str(year) + '.xls')


# In[17]:


# 从文件中搜索相关信息
import pandas as pd
for y in range(2008, 2018):
    print('\n-------------------', y)
    ex = pd.ExcelFile('data/%d.xls' % y)
    sheets = pd.read_excel(ex, None)
    for sheet in sheets:
        s = sheets[sheet]
        for index, row in s.iterrows():
            line = str(row.values)
#             if 'iphone' in line.lower() and '.' in line:
#             if 'total net sales' in line.lower() and '.' in line:
#             if 'net income' in line.lower() and '.' in line:
#             if 'gross margin percentage' in line.lower() and '.' in line:
#             if 'cash equivalents' in line.lower():
#             if 'total assets' in line.lower():
            if 'china' in line.lower():
                print(sheet)
                print(line, '\n')
    ex.close()
                


# In[187]:


# 转换数据格式
table = '''
净销售额       净利润     毛利率     现金      总资产     国行     iPhone销量    iPhone销售额
32479.0     4834.0      0.342   11875.0     36171   0           11627.0     6742.0
42905.0     8235.0      0.401   5263.0      47501   769.0       20731.0     13033.0
65225.0     14013.0     0.394   11261.0     75183   2764.0      39989.0     25179.0
108249.0    25922.0     0.405   9815.0      116371  12472.0     72293.0     47057.0
156508.0    41733.0     0.439   10746       176064  22797.0     125046.0    80477.0
170910.0    37037.0     0.376   14259       207000  25946.0     150257.0    91279.0
182795.0    39510.0     0.386   13844       231839  30638.0     169219.0    101991.0
233715.0    53394.0     0.401   21120       290479  56547.0     231218.0    155041.0
215639.0    45687.0     0.391   20484       321686  46349       211884.0    136700.0
229234.0    48351.0     0.385   20289       375319  44764       216756.0    141319.0
'''
table = table.strip().split('\n')
head = table[0].split()
body = table[1:]
data = {}
year = 2008
for line in body:
    data_year = {}
    line = line.split()
    for i in range(len(head)):
        data_year[head[i]] = line[i]
    data[year] = data_year
    year += 1
data = pd.DataFrame(data)
data


# In[239]:


from pyecharts import Bar, Line, Overlap, Grid

years = [str(i) for i in range(2008, 2018)]
net_sales = data.loc['净销售额'].values
net_income = data.loc['净利润'].values
bar = Bar("盈利能力")
bar.add("净销售额", years, net_sales)
bar.add("净利润", years, net_income, bar_category_gap=25, yaxis_name='百万美元', yaxis_name_gap=60)
gross = data.loc['毛利率'].values
line = Line()
line.add("毛利率", years, gross, line_width=3)
ol = Overlap()
ol.add(bar)
ol.add(line, is_add_yaxis=True, yaxis_index=1)
ol


# In[241]:


assets = data.loc['总资产'].values
cash = data.loc['现金'].values
bar = Bar("财务状况")
bar.add("总资产", years, assets)
bar.add("现金", years, cash, bar_category_gap=25, yaxis_name='百万美元', yaxis_name_gap=60)
bar


# In[233]:


ip_sales = data.loc['iPhone销售额'].values
ip_unit = data.loc['iPhone销量'].values
bar = Bar("iPhone销售状况")
bar.add("iPhone销售额", years, ip_sales)
bar2 = Bar()
bar2.add("iPhone销量", years, ip_unit, bar_category_gap=25)
percent = ip_sales.astype('float') / net_sales.astype('float')
line = Line()
line.add("收入占比", years, percent, line_width=3, yaxis_margin=60, yaxis_pos='left')
ol = Overlap()
ol.add(bar)
ol.add(bar2, is_add_yaxis=True, yaxis_index=1)
ol.add(line, is_add_yaxis=True, yaxis_index=2)
grid = Grid()
grid.add(ol, grid_left="15%")
grid


# In[189]:


cn_sales = data.loc['国行'].values
bar = Bar("国行销售状况")
bar.add("国行", years, cn_sales)
percent = cn_sales.astype('float') / net_sales.astype('float')
line = Line()
line.add("国行占比", years, percent, line_width=3)
ol = Overlap()
ol.add(bar)
ol.add(line, is_add_yaxis=True, yaxis_index=1)
ol


# In[191]:


price_table = '''
iPhone (2007): 499 599
iPhone 3G (2008): 599  699
iPhone 3GS (2009): 599 699
iPhone 4 (2010): 599   699
iPhone 4S (2011): 649  849
iPhone 5 (2012): 649   849
iPhone 5c (2013): 549   649
iPhone 5s (2013): 649  849
iPhone 6 (2014): 649   849
iPhone 6 Plus (2014): 749  949
iPhone 6s (2015): 649  849
iPhone 6s Plus (2015): 749 949
iPhone SE (2016): 399   499
iPhone 7 (2016): 649   849
iPhone 7 Plus (2016): 769  949
iPhone 8 (2017): 699   849
iPhone 8 Plus (2017): 799  949
iPhone X (2017): 999   1149
iPhone Xr (2018): 749   899
iPhone Xs (2018): 999   1349
iPhone Xs Max (2018): 1099  1449
'''

price_table = price_table.strip().split('\n')
products = []
price_min = []
price_max = []
for line in price_table:
    prod, ps = line.split(':')
    p_min, p_max = ps.strip().split()
    products.append(prod)
    price_min.append(p_min)
    price_max.append(p_max)

print(products,price_min,price_max)


# In[227]:


line = Line('iPhone售价')
line.add("最低", products, price_min, is_fill=True, area_opacity=0.2)
line.add("最高", products, price_max, is_fill=True, area_opacity=0.2, xaxis_interval=0, xaxis_rotate=45)
grid = Grid()
grid.add(line, grid_bottom="25%")
grid

