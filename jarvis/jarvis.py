
# coding: utf-8

# In[381]:


import requests as rq
import time
import random
import string
import urllib
import hashlib


# In[423]:


APPKEY = 'abcdefghijk'  # 替换成你的appkey！！！
APPID = 1234567890  # 替换成你的appid！！！

def get_sign(data):
    lst = [i[0]+'='+urllib.parse.quote_plus(str(i[1])) for i in data.items()]
    params = '&'.join(sorted(lst))
    s = params + '&app_key=' + APPKEY
    h = hashlib.md5(s.encode('utf8'))
    return h.hexdigest().upper()


# In[424]:


import pyaudio
import wave
import base64

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 8000#44100
CHUNK = 1024
RECORD_SECONDS = 3

def record():
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("listening...")
    frames = [] 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # stop Recording
    stream.stop_stream()
    stream.close()

    voice = b''.join(frames)
    b64voice = base64.b64encode(voice)

    url_asr = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    data = {
        'app_id': APPID,
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str,
        'format': 1,
        'speech': b64voice.decode(),
    }
    data['sign'] = get_sign(data)
    r = rq.post(url_asr, data=data)
    question = r.json()['data']['text']
    return question


# In[384]:


def chat(question):    
    url_chat = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    data = {
        'app_id': APPID,
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str,
        'session': '10000',
        'question': question,
    }
    data['sign'] = get_sign(data)
    r = rq.post(url_chat, data=data)
    answer = r.json()['data']['answer']
    return answer


# In[385]:


def playsound(voice):
    stream = audio.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        output = True)
    stream.write(voice)
    stream.close()


# In[386]:


def speak(text):
    text = text[:50]
    url_speak = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    data = {
        'app_id': APPID,
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str,
        'text': text,
        'speaker': 1,
        'format': 2,
        'volume': 0,
        'speed': 100,
        'aht': 0,
        'apc': 58,
    }
    data['sign'] = get_sign(data)
    r = rq.post(url_speak, data=data)
    voice = r.json()['data']['speech']
    voice = base64.b64decode(voice)
    playsound(voice)


# In[394]:


def face(img_file, model):
    with open(img_file, 'rb') as f:
        img = base64.b64encode(f.read())
    url_face = 'https://api.ai.qq.com/fcgi-bin/ptu/ptu_facemerge'
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    data = {
        'app_id': APPID,
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str,
        'model': model,
        'image': img.decode(),
    }
    data['sign'] = get_sign(data)
    r = rq.post(url_face, data=data)
    pic = r.json()['data']['image']
    return pic


# In[ ]:


import time
audio = pyaudio.PyAudio()
for i in range(5):
    question = record()
    print(question)
    answer = chat(question)
    print(answer)
    speak(answer)
#     time.sleep(1)
audio.terminate()


# In[ ]:


import io
from PIL import Image
p = face('head.jpg', 22)
image=io.BytesIO(base64.b64decode(p))
img = Image.open(image)
img.show()
# img

