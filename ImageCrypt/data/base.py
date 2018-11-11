from abc import ABCMeta, abstractmethod


class BaseData(object):

    __metaclass__ = ABCMeta

    def __init__(self, path):
        self._path = path
        self._binary = None
        self._data = None

    @property
    def path(self):
        return self._path

    @property
    def binary(self):
        return self._binary

    @binary.setter
    def binary(self, value):
        self._binary = value

    @property
    @abstractmethod
    def data(self):
        return self._data

    @abstractmethod
    def validate(self, size, sp, ep):
        pass
