import struct
from ImageCrypt.data.binary import BaseBinaryData


class DecodeBinaryData(BaseBinaryData):

    def __init__(self):
        super(DecodeBinaryData, self).__init__()

    @property
    def string(self):
        if self._string is None:
            self._string = struct.pack(
                "{0:d}B".format(len(self.bytes)),
                *tuple(self.bytes)
            )
        return self._string

    @property
    def bytes(self):
        if self._bytes is None:
            self._bytes = []
            for char in self.group_bits(8):
                self._bytes.append(
                    int(
                        "".join(str(c) for c in char),
                        2
                    )
                )
        return self._bytes

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        self._bits = value
