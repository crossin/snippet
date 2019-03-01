# coding: utf8
import datetime
import requests
import sqlite3

# 建立数据库连接
conn = sqlite3.connect('words.db')
cursor = conn.cursor()
# 如果不存在表则新建
create_tb_cmd='''
    CREATE TABLE IF NOT EXISTS WORD
    (english TEXT,
     date DATE,
     phonetic TEXT,
     chinese TEXT);
'''
cursor.execute(create_tb_cmd)
cursor.execute('select english from WORD;')
words = [w[0] for w in cursor.fetchall()]
print(words)
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
            return '', ''
        # 拼接音标和释义
        means_str = []
        for m in means:
            means_str.append(m['part'] + ';'.join(m['means']))
        all_mean = ' | '.join(means_str)
        return ph, all_mean
    except:
        # 请求异常
        print('获取中文失败')
        return '', ''

while True:
    word = input('请输入你要记录的单词（直接回车退出程序）：\n').strip()
    if not word:
        break

    if word in words:
        print('单词已存在')
    else:
        words.append(word)
        # 获取并增加翻译
        ph, chs = get_chs(word)
        print( '[' + ph + '] ' + chs)
        t = datetime.date.today()
        print(t)
        # 插入数据库
        insert_cmd = '''
            INSERT INTO WORD
            (english, date, phonetic, chinese)
            VALUES (?, ?, ?, ?);
        '''
        cursor.execute(insert_cmd, (word, t, ph, chs))
        conn.commit()
    print('已记录', len(words) ,'个单词/词组\n')
cursor.close()
conn.close()
