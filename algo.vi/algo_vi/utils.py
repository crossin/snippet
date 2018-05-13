#coding=utf-8
# =================
# author: zhouxin
# start_date： 171116
# description: some common tools for the projects
#
# =================
import abc

class AutoStorage:

    _counter = 0
    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls._counter
        self.s_name = '{}#{}'.format(prefix, index)
        cls._counter += 1

    def __set__(self, instance, value):
        setattr(instance, self.s_name, value)

    def __get__(self, instance, owner):
        if not instance:
            return self

        else:
            return getattr(instance, self.s_name)

class Validated(AutoStorage, metaclass=abc.ABCMeta):

    def __set__(self, instance, value):
        value = self.validated(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validated(self, instance, value):
        '''method to inspect wheather the value is valid'''


class VaList(Validated):

    MAX_LEN = 100
    def validated(self, instance, value):

        lst = list(value)
        is_valid = all([isinstance(i, (int, float)) for i in lst])
        if not is_valid:
            raise ValueError('the sequence obj only contains int or float')

        if len(lst) > VaList.MAX_LEN:
            print('the sequence exceeds max length(10), '
                  'automatically intercepts the first {} items'.format(VaList.MAX_LEN))

            lst = lst[:VaList.MAX_LEN]

        return lst
