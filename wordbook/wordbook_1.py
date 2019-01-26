# coding: utf8
import datetime

f = open('words.txt', 'a+')
f.seek(0)
lines = f.readlines()
words = [line.split('      ')[0] for line in lines if line.strip()]

while True:
    word = input('请输入你要记录的单词（直接回车退出程序）：\n').strip()
    if not word:
        break
    if word in words:
        print('单词已存在')
    else:
        words.append(word)
        t = datetime.date.today()
        line = word + '      ' + str(t) + '\n'
        lines.append(line)
        f.write(line)
        f.flush()
    print('已记录', len(words) ,'个单词/词组\n')
f.close()
