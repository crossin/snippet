# python 2
import os
from collections import Counter
import jieba

all_words = []
for filename in os.listdir('lyrics'):
    with open('lyrics/' + filename) as f:
        lyrics = f.read()
        data = jieba.cut(lyrics)
        all_words.extend(set(data))

count = Counter(all_words)
result = sorted(count.items(), key=lambda x: x[1], reverse=True)

for word in result:
    print word[0], word[1]

