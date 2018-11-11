from abc import ABCMeta, abstractmethod


class BaseBinaryData(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self._bytes = None
        self._bits = []
        self._string = None
        self._length = None

    @property
    @abstractmethod
    def string(self):
        pass

    @property
    @abstractmethod
    def bytes(self):
        pass

    @property
    @abstractmethod
    def bits(self):
        pass

    @bits.setter
    @abstractmethod
    def bits(self, value):
        pass

    @property
    def length(self):
        if self._length is None:
            self._length = len(self.bits)
        return self._length

    def group_bits(self, step):
        return [self.bits[i:i + step] for i in range(0, len(self.bits), step)]
