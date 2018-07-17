import urllib
import hashlib
import base64
import random
import string
import time
import requests
from django.shortcuts import render

APPID = 1234567890  # your appid!!!
APPKEY = 'abcdefghijk'  # your appkey!!!

def get_sign(data):
    lst = [i[0]+'='+urllib.parse.quote_plus(str(i[1])) for i in data.items()]
    params = '&'.join(sorted(lst))
    s = params + '&app_key=' + APPKEY
    h = hashlib.md5(s.encode('utf8'))
    return h.hexdigest().upper()

def face(img_file, model):
    img = base64.b64encode(img_file.read())
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
    r = requests.post(url_face, data=data)
    pic = r.json()['data']['image']
    return pic

def index(request):
    image = ''
    if request.method == 'POST':
        image = request.FILES.get("photo")
        if image:
            m = request.POST.get('model', 1)
            image = 'data:image/png;base64,'+face(image, m)
    return render(request, 'face/index.html', {'image':image})

