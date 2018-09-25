
# coding: utf-8

# In[1]:


# Crossin的编程教室
# 微信公众号：crossincode
import requests as rs
uid = 94763945245
url = 'https://api.amemv.com/aweme/v1/aweme/post/?max_cursor=0&user_id=%d&count=20&aid=1128' % uid
h = {'user-agent': 'mobile'}
req = rs.get(url, headers=h, verify=False)
data = req.json()
print(data)


# In[9]:


import urllib.request
for video in data['aweme_list']:
    name = video['desc'] or video['aweme_id']    
    url_v = video['video']['download_addr']['url_list'][0]
    print(name, url_v, '\n')
    urllib.request.urlretrieve(url_v, name + '.mp4')

