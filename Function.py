from abc import ABCMeta, abstractmethod


class Function:
    __metaclass__ = ABCMeta

    @abstractmethod
    def exec(self, **kwargs):
        pass

    def get_name(self):
        return self.__class__.__name__


