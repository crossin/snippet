#coding=utf-8
# =================
# author: zhouxin
# start_date： 171115
# description: apis for external
# =================

from engine import Engine
from functools import wraps


# sort algorithm decorator
def sort_algo(func):
    @wraps(func)
    def inner(lst, **kw):
        func_name = func.__name__
        kw.update({'sort_lst': lst})
        kw.setdefault('title', func_name)
        e = Engine(func_name, **kw)
        e.show()
        
    return inner

@sort_algo
def bubble_sort(lst, **kw):
    '''bubble sort api'''
    pass

@sort_algo
def select_sort(lst, **kw):
    pass

@sort_algo
def insert_sort(lst, **kw):
    pass

@sort_algo
def quick_sort(lst, **kw):
    pass

@sort_algo
def merge_sort(lst, **kw):
    pass

if __name__ == '__main__':
    import random
    lst = random.sample(range(100), 100)
    random.shuffle(lst)
    # bubble_sort(lst)
    # select_sort(lst)
    # insert_sort(lst)
    # quick_sort(lst, title='quick')
    merge_sort(lst, interval=50)
