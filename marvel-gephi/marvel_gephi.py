#-*- coding:utf8 -*-
from marvel import Marvel
from marvel import exceptions
import pymongo
import time
import csv

class Marvel_gephi(object):
    '''use marvel, get name id, stories's count'''
    def __init__(self,PUBLIC_KEY,PRIVATE_KEY):
        self.PUBLIC_KEY = PUBLIC_KEY
        self.PRIVATE_KEY = PRIVATE_KEY
        self.path_c = r'name2.csv' #gephi所需角色（节点）信息
        self.path_log = r'name_storielog.txt' #故事存储log
        self.path_up = r'st11.csv' #对gephi所需角色信息更新
        self.path_edg = r'name_name_w.csv' #gephi所需边信息


    def get_ready(self, ch='characters',dbname='marvel3'):
        '''marvel及数据库调用'''
        global mycol
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[dbname]
        mycol = mydb[ch]
        m = Marvel(self.PUBLIC_KEY, self.PRIVATE_KEY)
        return m


    def store_charac(self,ch):
        '''初步储存角色及相关故事数'''
        clog =[]#请求次数较少时使用    
        m = self.get_ready(ch)  #'characters'  
        characters = m.characters
        for i in range(0,1500,100):#第一次请求,英雄数量1400多
            try:
                all_characters = characters.all(limit=100,offset=i)
                time.sleep(2)
                print('till',i,'insertbegin')
                for i2 in all_characters['data']['results']:#存入数据
                    mycol.insert_one(i2)
                print('ok',i)
            except exceptions.MarvelException as e:
                print('MarvelException:',e)
                print('bad',i,':',i+100)
                clog.append(i)
            except exceptions.BadInputException as e:
                print('BadInputException:',e)
                print('bad',i,':',i+100)
                clog.append(i)
        print('first insert,end')
        #请求出错时使用，一般出错的概率比较小，所以就不输出log.txt了
        b = 0 #请求次数
        okl2 = []
        while clog:
            for i in clog:
                try:
                    all_characters = characters.all(limit=100,offset=i)
                    time.sleep(2)
                    print('till',i,'insertbegin')
                    for i2 in all_characters['data']['results']:
                        mycol.insert_one(i2)
                    print('ok',i,',delete',i)
                    okl2.append(i) #删除列表元素
                except exceptions.MarvelException as e:
                    print('MarvelException:',e)
                    print('bad',i,':',i+100)
                except exceptions.BadInputException as e:
                    print('BadInputException:',e)
                    print('bad',i,':',i+100)          
            for i3 in okl2: #删除列表元素
                clog.remove(i3)
            b += 1
            print('second insert,end,times:',b)
    def node(self,ch):
        '''生成节点数据'''
        self.get_ready(ch)#'characters'
        characters = []
        headers = ['id','name', 'weight']#故事数量weight,角色名,id ：[1009610, 'Spider-Man', 5478]
        with open(self.path_c, 'w', encoding='utf8') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(headers)
        for q in mycol.find():
            characters.append([q['id'],q['name'],q['stories']['available']])#列表
        characters.sort(key=lambda x:x[2], reverse=True) #以相关故事数量降序排列 
        m1 = characters[0:99]#挑选故事数量前99的英雄进行分析
        for m in m1: #将前100存储起来
            with open(self.path_c, 'ab+', encoding='utf8') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(m)
    

    def store_stories(self, ch):
        '''存储英雄相关所有故事'''
        slog = []
        m = self.get_ready(ch) #集合名'stories'
        stories = m.stories
        #从存入的文件中读取数据
        m1 = []
        with open(self.path_c, 'r', encoding='utf8') as f:
            f_csv = csv.reader(f)
            for r in f:
                m1.append(r.split(',')[0:3])
        m1 = m1[1:]
        for nameid in m1:#nameid=[1009277, 'Domino', 296]角色id,角色名，相关故事数----接着从第六个角色开始
            for i in range(0,int(nameid[2]),100):   
            #第一次请求
                try:
                    all_stories = stories.all(characters=nameid[0],offset=i,limit=100)
                    time.sleep(3)
                    print('till',i,'insertbegin')
                    for i2 in all_stories['data']['results']:
                        mycol.insert_one({str(nameid[0]):i2})#保存character_id及相应stories
                    print('ok',i)
                except exceptions.MarvelException as e:
                    print('MarvelException:',e)
                    print('bad',i,':',i+100)
                    slog.append(i)#nameid及i
                except exceptions.BadInputException as e:
                    print('BadInputException:',e)
                    print('bad',i,':',i+100)
                    slog.append(i)#nameid及i
            print('first， insert, end')
            
            #差错处理
            b = 0 #总请求次数
            okl = []
            while slog and b < 5:
                for si in slog: #一次si不成功就自动进入下一个si
                    try:
                        all_stories = stories.all(characters=nameid[0],offset=si,limit=100)
                        time.sleep(3)
                        print('till',si,'insertbegin')
                        for i2 in all_stories['data']['results']:#
                            mycol.insert_one({nameid[0]:i2})
                        print('ok',si,',delete',si)
                        okl.append(si) #删除请求成功的i
                    except exceptions.MarvelException as e:
                        print('MarvelException:',e)
                        print('bad',si,':',si+100)
                    except exceptions.BadInputException as e:
                        print('BadInputException:',e)
                        print('bad',si,':',si+100)
                for ok in okl:#删除请求成功的si
                    slog.remove(ok)
                okl = [] #格式化
                b += 1
                print('try,times:',b)
            if slog: #log输出  
                with open(self.path_log, 'a+', encoding='utf8') as f:
                    f.write(str(nameid))
                    f.write(str(slog))
                    f.write('\n')
                    slog = [] #格式化


    def add_stories(self,nameid,si,ch):
        '''对log中信息手动抓取'''
        self.get_ready(ch)##'sories'
        all_stories = stories.all(characters=nameid,offset=si,limit=100)
        time.sleep(3)
        print('till',si,'insertbegin')
        for i2 in all_stories['data']['results']:#
            mycol.insert_one({nameid[0]:i2})
        print('ok',si,',delete',si)


    def update_charac(self,ch):
        '''根据实际抓取数据，进行更新前面的相关故事数'''
        m = self.get_ready(ch) #集合名#'stories'
        stories = m.stories
        counts1 = []
        headers = ['nameid','stories_c']#故事id,name1id,name2id
        with open(self.path_up, 'w', encoding='utf8') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(headers)
        #从存入的文件中读取数据
        m1 = []
        with open(self.path_c, 'r', encoding='utf8') as f:
            f_csv = csv.reader(f)
            for r in f:
                m1.append(r.split(',')[0:3])
        m1 = m1[1:]
        c = 0
        for nameid in m1:
            all_stories_count = stories.all(characters=nameid[0],offset=0,limit=5)
            time.sleep(3)
            print(nameid[0],all_stories_count['data']['total'])
            counts1 = [nameid[0],all_stories_count['data']['total']] #更新故事数
            c += 1
            print(c)
            with open(self.path_up, 'ab+', encoding='utf8') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerow(counts1)


    def edge(self,ch):
        '''生成便表格相关数据'''
        self.get_ready(ch)#'stories'
        #csv文件生成，第二个edge文件生成
        dicn_stories = {} #存储故事id元组
        headers = ['source','target','weight']#name1id,name2id，同在一个故事的数量
        with open(self.path_edg, 'w', encoding='utf8') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(headers)
        print('开始id和故事存储')
        #存储故事id与故事名
        characters_c = []
        check = '1009610'#故事数最多的id
        for q2 in mycol.find():
            ckey = [ckey for ckey in q2.keys()]
            ckey = ckey[1]
            if ckey == check:
                characters_c.append((q2[ckey]['id'],q2[ckey]['title']))#故事数据
                dicn_stories[str(ckey)] = set(characters_c)#增加键值对,及数值更新
                check = ckey #更新人物id
            else:
                characters_c =[] #根据key值清空列表
                characters_c.append((q2[ckey]['id'],q2[ckey]['title']))#故事数据
                check = ckey 
        print('存储完毕。开始获取两两角色相关数据')
        #从存入的节点文件中读取id数据
        m1 = []
        with open(self.path_c, 'r', encoding='utf8') as f:
            f_csv = csv.reader(f)
            for r in f:
                m1.append(r.split(',')[0:3])
        m1 = m1[1:]
        #两两角色相关故事数存储
        m2 = []
        for ind, chaid in enumerate(m1):#nameid=[1009277, 'Domino', 296]角色id,角色名
            pre = dicn_stories[str(chaid[0])]#获取角色对应的故事
            for ind2, chaid2 in enumerate(m1):
                if ind < ind2:
                    nex = dicn_stories[str(chaid2[0])]#获取角色对应数据
                    count = len(pre & nex)
                    if count > 0:
                        m2 = [chaid[0],chaid2[0],count]
                        with open(self.path_edg, 'ab+', encoding='utf8') as f:
                            f_csv = csv.writer(f)
                            f_csv.writerow(m2)
        print('存储结束')


PUBLIC_KEY = 'YOUR PUBLIC_KEY'
PRIVATE_KEY = 'YOUR PRIVATE_KEY'
mar = Marvel_gephi(PUBLIC_KEY,PRIVATE_KEY)

# mar.store_charac('characters1')#存储人物数据
# print('人物储存完毕')
# mar.node('characters1')#生成节点数据
# print('节点数据生成完毕')
# mar.store_stories('stories1')#存储故事数据
# print('故事存储完毕，请检查log文件')
# mar.update_charac('stories')#更新故事数
# print('人物故事更新完成')
# mar.edge('stories1')#生成边数据
# print('边数据完成')