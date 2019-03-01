# -*- coding: UTF-8 -*-
import datetime,requests,peewee

db = peewee.SqliteDatabase("words.db")

#创建表
class Word(peewee.Model):
    #将表和数据库连接
    class Meta:
        database = db
    word = peewee.CharField()
    ph_en = peewee.CharField()
    means = peewee.CharField()
    date = peewee.DateTimeField()
Word.create_table()
    
t_list = Word.select()
words = [t.word for t in t_list]

# 接口地址，替换成你的key
key = '1234567'
url = "http://dict-co.iciba.com/api/dictionary.php?w={}&type=json&key=" + key       # api构造

def get_chs(word):
    try:
        r = requests.get(url.format(word))
        d = r.json()
        if not d.get("word_name"):          #　分析json的格式，当word不存在时，key"word_name"也不存在
            print("单词/词组不存在")
        else:
            words.append(word)              #实时更新单词列表
            ph_en = d["symbols"][0]["ph_en"]
            parts = d["symbols"][0]["parts"]
            means = "".join([i["part"] + "".join(i["means"]) for i in parts])
            t = Word()
            t.word = word
            t.ph_en = ph_en
            t.means = means
            t.date = datetime.date.today()
            t.save()
            print(t.word+'    ['+t.ph_en+']    '+t.means+'    '+str(t.date)+'\n')
            
    except:
        print("获取中文失败")
    
while 1:
    word=input("请输入你要记录的单词(1:打印现有单词;Enter:退出):").strip()
    if not word:                  #回车退出循环
        break
    elif word == '1':
        t_list = Word.select()
        for w in ((t.word+'    ['+t.ph_en+']    '+t.means+'    '+str(t.date)+'\n') for t in t_list):
            print(w)
    elif word in words:
        print("单词已存在")
# 打出存在的单词和解释
        t = Word.get(word=word)
        print(t.word+'    ['+t.ph_en+']    '+t.means+'    '+str(t.date)+'\n')
    else:
        get_chs(word)
        
    print("已记录{}个单词/词组".format(len(words)))
    print()


   
  