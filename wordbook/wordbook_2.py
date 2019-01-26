# coding: utf8
import datetime
import requests

# 打开文件，读取已有单词
f = open('words.txt', 'a+')
f.seek(0)
lines = f.readlines()
words = [line.split('      ')[0] for line in lines if line.strip()]

# 接口地址，替换成你的key
apikey = '1234567'
apiurl = 'http://dict-co.iciba.com/api/dictionary.php?key=' + apikey + '&type=json&w='

# 获取中文翻译
def get_chs(word):
    url = apiurl + word
    try:
        # 请求并获取翻译
        r = requests.get(url)
        data = r.json()
        symbol = data['symbols'][0]
        ph = symbol.get('ph_en', '')
        means = symbol.get('parts', [])
        # 无翻译
        if not ph and not means:
            print('未找到中文翻译')
            return ''
        # 拼接音标和释义
        means_str = []
        for m in means:
            means_str.append(m['part'] + ';'.join(m['means']))
        all_mean = ' | '.join(means_str)
        return '[' + ph + '] ' + all_mean
    except:
        # 请求异常
        print('获取中文失败')
        return ''

while True:
    word = input('请输入你要记录的单词（直接回车退出程序）：\n').strip()
    if not word:
        break
    if word in words:
        print('单词已存在')
    else:
        words.append(word)
        # 获取并增加翻译
        chs = get_chs(word)
        print(chs)
        t = datetime.date.today()
        print(t)
        line = word + '      ' + str(t) + '      ' + chs + '\n'
        lines.append(line)
        f.write(line)
        f.flush()
    print('已记录', len(words) ,'个单词/词组\n')
f.close()
