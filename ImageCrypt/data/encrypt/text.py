from ImageCrypt.data.base import BaseData
from ImageCrypt.data.encrypt.binary import EncodeBinaryData


class EncodeTextData(BaseData):

    def __init__(self, path):
        super(EncodeTextData, self).__init__(
            path,
        )
        with open(path, "rb") as f:
            self._data = f.read()
        self.binary = EncodeBinaryData(
            self._data.encode("utf-8"),
        )

    @property
    def data(self):
        return self._data

    def validate(self, size, sp, e):
        available_space = (size[0] * size[1] * 3)
        if available_space < len(self.binary.bytes):
            raise DataToBigException(
                "This image can only store {0:d} bytes of data. "
                "Your message is {1:d} bytes".format(
                    available_space,
                    len(self.binary.bytes),
                )
            )


class DataToBigException(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)