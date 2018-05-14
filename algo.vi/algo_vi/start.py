#coding=utf-8
import random

import fire

from api import bubble_sort, select_sort, insert_sort, quick_sort, merge_sort

all_sort_funcs = [bubble_sort, select_sort, insert_sort, quick_sort, merge_sort]


class Algorithm(object):

    def __init__(self):
        
        self.sort_func_map = self._init_map(all_sort_funcs)

    def _init_map(self, funcs):
        dct = {}
        for f in funcs:
            f_name = f.__name__
            dct[f_name] = f

        return dct        

    def sortex(self, algo, data=None, **kw):

        sort_func = self.sort_func_map.get(algo)
        if not sort_func:
            raise NotImplementedError

        if data == None:
            data = self._random_generate(20)

        return sort_func(data, **kw)

    def _random_generate(self, num):

        lst = list(range(1,41))
        random.shuffle(lst)
        return lst

if __name__ == '__main__':
    fire.Fire(Algorithm())
    