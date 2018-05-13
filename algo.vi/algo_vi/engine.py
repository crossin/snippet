#coding=utf-8
# =================
# author: zhouxin
# start_date： 171112
# description: objs in this file performs like a hub, input a concret algorithm
#              dispatch it to corresponding visualization method 
# =================

import threading
from sortx import Bubble, SelectionSort, InsertionSort, QuickSort, MergeSort
from visualx import ViSort
import abc


class BaseEngine(metaclass=abc.ABCMeta):
    '''base engine for algo-vi project
    
    MAPPING: key-value for method: [get-data-cls, visual-cls]

    '''

    MAPPING = {
        'bubble_sort': [Bubble, ViSort],
        'select_sort': [SelectionSort, ViSort],
        'insert_sort': [InsertionSort, ViSort],
        'quick_sort': [QuickSort, ViSort],
        'merge_sort': [MergeSort, ViSort],
    }
    def __init__(self, func_name, **kw):
        
        self.g_cls, self.v_cls = BaseEngine.MAPPING.get(func_name, [None, None])
        
        self.ipt = []
        # extract relevant input data
        if func_name.endswith('sort'):
            self.ipt = kw.get('sort_lst', [])

    @abc.abstractmethod
    def show(self):
        ''''''
        
class Engine(BaseEngine):
    '''engine for algo-vi project
    this cls will automatically implements correct 'get-data' cls 
    and 'visualization' cls for incoming algorithm, no matter it is 
    a sort algo or others
    '''

    def __init__(self, func_name, **kw):
        super().__init__(func_name, **kw)
        self.kw = kw

    def _get_data(self):
        '''implement assigned cls to get data which prepared for visualization'''
        dt = self.g_cls(self.ipt, **self.kw).operate()
        return dt

    def _draw_animation(self, dt):
        '''implement assigned cls to show animation for corresponding algorithm'''
        return self.v_cls(od=dt, **self.kw).show()        

    def show(self):
        '''visualization'''
        dt = self.g_cls(self.ipt, **self.kw).operate()
        self._draw_animation(dt)

