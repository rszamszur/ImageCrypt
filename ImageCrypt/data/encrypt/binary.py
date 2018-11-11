import struct
from ImageCrypt.data.binary import BaseBinaryData


class EncodeBinaryData(BaseBinaryData):

    def __init__(self, string):
        super(EncodeBinaryData, self).__init__()
        self._string = string

    @property
    def string(self):
        return self._string

    @property
    def bytes(self):
        if self._bytes is None:
            self._bytes = struct.unpack(
                "{0:d}B".format(len(self.string)),
                self.string
            )
        return self._bytes

    @property
    def bits(self):
        if len(self._bits) == 0:
            for byte in self.bytes:
                for bit in format(byte, "08b"):
                    self._bits.append(bit)
        return self._bits
