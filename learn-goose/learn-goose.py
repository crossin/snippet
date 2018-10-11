
# coding: utf-8

# In[3]:


from goose3 import Goose
from goose3.text import StopWordsChinese
# 初始化，设置中文分词
g = Goose({'stopwords_class': StopWordsChinese})
# 文章地址
url = 'https://mp.weixin.qq.com/s/zflbcF5PS06QC5YJXpiviQ'
# 获取文章内容
article = g.extract(url=url)
# 标题
print('标题：', article.title)
# 显示正文
print(article.cleaned_text)


# In[6]:


url = 'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2'
g = Goose({
    'browser_user_agent': 'Version/5.1.2 Safari/534.52.7',
    'http_timeout': 15
})
article = g.extract(url=url)
print(article.meta_description)
print(article.meta_keywords)
print(article.tags)
print(article.top_image)
print(article.infos)
print(article.raw_html)


# In[3]:


from goose3 import Goose
from goose3.text import StopWordsChinese
from bs4 import BeautifulSoup

g = Goose({'stopwords_class': StopWordsChinese})
urls = [
    'https://www.ifanr.com/',
    'https://www.leiphone.com/',
    'http://www.donews.com/'
]
url_articles = []
for url in urls:
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    links = soup.find_all('a')
    for l in links:
        link = l.get('href')
        if link and link.startswith('http') and any(c.isdigit() for c in link if c) and link not in url_articles:
            # any(c.isdigit() for c in link if c) 是筛选了标题中含有数字的网站
            url_articles.append(link)
            print(link)
        
for url in url_articles:
    try:
        article = g.extract(url=url)
        content = article.cleaned_text
        if len(content) > 200:
            title = article.title
            print(title)
            with open('homework/goose/' + title + '.txt', 'w') as f:
                f.write(content)
    except:
        pass

