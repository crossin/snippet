# 图形见图2
# 数字对应相邻和：1->26, 2->8, 3->19, 4->13, 5->17, 6->10, 7->4, 8->19, 9->24

import itertools
import time

# 相邻和列表
checksum = [26, 8, 19, 13, 17, 10, 4, 19, 24]

# 节点类
class node():
    def __init__(self):
        self.num = 0    # 节点值
        self.link = []  # 相邻节点

    # 计算相邻节点和
    def get_sum(self):
        return sum(l.num for l in self.link)

    # 判断是否符合条件
    def is_valid(self):
        if self.get_sum() == checksum[self.num - 1]:
            return True
        else:
            return False

    # 判断周围是否填满（递归方法使用）
    def all_filled(self):
        for l in self.link:
            if l.num == 0:
                return False
        return True

    # 显示
    def __repr__(self):
        # return str(self.num) + ':' + ','.join([str(l.num) for l in self.link])
        return str(self.num)

# 初始化图和节点
graph = []
for i in range(9):
    graph.append(node())

# 定义相邻关系
graph[0].link.extend([graph[2]])
graph[1].link.extend([graph[2], graph[3]])
graph[2].link.extend([graph[0], graph[1], graph[3], graph[4]])
graph[3].link.extend([graph[1], graph[2], graph[5], graph[6], graph[8]])
graph[4].link.extend([graph[2], graph[5], graph[7]])
graph[5].link.extend([graph[3], graph[4], graph[8]])
graph[6].link.extend([graph[3], graph[8]])
graph[7].link.extend([graph[4], graph[8]])
graph[8].link.extend([graph[3], graph[5], graph[6], graph[7]])

nums = list(range(1, 10))

# 枚举法
count = 0
t1 = time.time()

for answer in itertools.permutations(nums, 9):
    # print(answer)
    count+=1
    for i in range(9):
        graph[i].num = answer[i]
    # print(graph)
    valid = True
    for i in range(9):
        if not graph[i].is_valid():
            valid = False
            break
    if valid:
        print(graph)
        # break
t2=time.time()
print(count)
print(t2-t1)

# 递归法
for i in range(9):
    graph[i].num = 0
count = 0
t1 = time.time()
# 检测全部符合
def all_passed():
    for i in range(9):
        if not graph[i].is_valid():
            return False
    print(graph)
    return True

count=0
def fill(index, available):
    global count
    for num in available:
        count+=1
        # print(index, available, num)
        # print(checksum[num-1], graph[index].get_sum(), graph)
        # 如果当前值符合填入条件
        if (graph[index].all_filled() and checksum[num-1] == graph[index].get_sum()) or (
            not graph[index].all_filled() and checksum[num-1] > graph[index].get_sum()):
            graph[index].num = num
            # 判断是否会破坏条件
            valid = True
            for i in graph[index].link:
                if i.num > 0 and i.get_sum() > checksum[i.num-1]:
                    valid = False
                    break
            if not valid:
                graph[index].num = 0
                continue
            # 将剩余递归调用
            rest = available[:]
            rest.remove(num)
            if len(rest):
                if fill(index + 1, rest):
                    return True
                else:
                    # 退回，清除当前值
                    graph[index].num = 0
            else:
                # 如果没有剩余，且全部符合，返回True（得到结果）
                if all_passed():
                    return True
                else:
                    # 不符合，清除当前值
                    graph[index].num = 0

fill(0, nums)

t2=time.time()
print(count)
print(t2-t1)

