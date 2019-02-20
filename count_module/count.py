import os
from collections import Counter

modules = set()
all_modules = {}
for root, dirs, files in os.walk("..", topdown=False):
    # print('========', root,dirs
    for name in files:
        # print('--', name)
        if name.endswith('.py'):
            with open(root + os.path.sep + name) as f:
                for line in f:
                    line = line.lstrip()
                    if line.startswith('from') or line.startswith('import'):
                        # print('--------',line)
                        module = line.split()[1]
                        module = module.split('.')[0]
                        if module:
                            # print(module)
                            modules.add(module)
    if root.count(os.path.sep) <= 1:
        # print(modules)
        for m in modules:
            all_modules[m] = all_modules.get(m, 0) + 1
        modules = set()
# print(all_modules)
c = Counter(all_modules).most_common()
for i in c:
    if i[1] > 1:
        print(i)