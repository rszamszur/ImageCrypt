from ImageCrypt.data.encrypt.text import EncodeTextData
from ImageCrypt.data.encrypt.file import EncodeFileData
from ImageCrypt.data.decrypt.text import DecodeTextData
from ImageCrypt.data.decrypt.file import DecodeFileData


class DataFactory(object):

    __data = {
        "encrypt": {
            "text": EncodeTextData,
            "file": EncodeFileData,
        },
        "decrypt": {
            "text": DecodeTextData,
            "file": DecodeFileData,
        },
    }

    @classmethod
    def create(cls, action, data_type, **cls_params):
        return cls.__data[action][data_type](**cls_params)