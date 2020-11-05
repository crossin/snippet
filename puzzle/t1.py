#  111
#  333
#  555
#  777
# +999
# ----
# 1111
# 从上面去掉9个数字，使竖式结果为1111成立

import itertools

nums = [111, 333, 555, 777, 999]

# 分解数字
real_nums = []
for n in nums:
    real_nums.append(n // 100 * 100)     # 百位数
    real_nums.append(n % 100 // 10 * 10) # 十位数
    real_nums.append(n % 10)             # 个位数
# print(real_nums)

# 从中选取6个数
for answer in itertools.combinations(real_nums, 6):
    # print(answer)
    # 判断是否符合
    if sum(answer) == 1111:
        print(answer)

