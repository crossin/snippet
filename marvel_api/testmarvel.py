
# coding: utf-8

# In[42]:


import marvel
from IPython.display import Image, HTML, display
PUBLIC_KEY = '25b558c56c28ea8839370f72250e7c31'
PRIVATE_KEY = '0929fdf08c3134b73388825d209cc712b4657eda'
m = marvel.Marvel(PUBLIC_KEY, PRIVATE_KEY)


# In[96]:


# 模糊搜索英雄（名字开头）
characters = m.characters
# all_characters = characters.all()
name = input('请输入要查询的英雄（英文，可只输入开头）：')
print('搜索中...')
all_characters = characters.all(nameStartsWith=name)
for c in all_characters['data']['results']:
    print(c['id'], c['name'])
    pic = c['thumbnail']
    display(Image(url=pic['path']+'/portrait_small.'+pic['extension']))


# In[97]:


hid = input('请输入要查询的英雄ID：')
print('搜索中...')
character = characters.get(hid)
# 英雄信息
for c in character['data']['results']:
    display(HTML('<a href="'+c['urls'][0]['url']+'" target="_blank">'+c['name']+'</a>'))
    print(c['description'])
    pic = c['thumbnail']
    display(Image(url=pic['path']+'/detail.'+pic['extension']))
print('搜索中...')
# 漫画信息
comics = characters.comics(hid)
print(comics['data']['total'], '本相关漫画')
for c in comics['data']['results']:
    display(HTML('<a href="'+c['urls'][0]['url']+'" target="_blank">'+c['title']+'</a>'))
    print(c['id'], '$%.2f'%c['prices'][-1]['price'])
    pic = c['thumbnail']
    display(Image(url=pic['path']+'/portrait_xlarge.'+pic['extension']))

