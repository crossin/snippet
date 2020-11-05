# 把1~52放入4个盒子，是的每个盒子任意一个数都不等于该盒子里任意两个数之和

import itertools

nums = list(range(1, 53))
boxes = [[], [], [], []]

for num in nums:    # 遍历 1~52
    for box in boxes:   # 依次选盒子
        valid = True
        # 从盒子里取所有2个数的组合，判断是否“可放”
        for two in itertools.combinations(box, 2):
            if sum(two) == num:
                valid = False
                break
        # 如果不符合，就选下一个盒子
        if not valid:
            continue
        # 没有不符合，就放入盒子，跳出循环，选择下一个数
        box.append(num)
        break

print(boxes)
