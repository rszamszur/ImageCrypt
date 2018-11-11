import sys
import time
from abc import ABCMeta, abstractmethod
from PIL import Image


class BaseImageCrypt(object):

    __metaclass__ = ABCMeta

    def __init__(self, path, data):
        self._image = Image.open(path)
        if self._image.format not in ["PNG", "TTIF"]:
            print("Invalid image format: {0:s}".format(self._image.format))
            sys.exit(1)
        if self._image.width < 20 or self._image.height < 20:
            print("Invalid image size! Minimum is 20x20 pixels.")
            sys.exit(1)
        self._data = data
        self._extension = self._image.format.lower()
        if self._image.mode in ["RGB", "YCbYCr"]:
            self.lsbs = 3
        elif self._image.mode in ["RGBA", "CMYK"]:
            self.lsbs = 4
        else:
            raise RuntimeError("Unsupported image color mode!")

    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass

    @property
    def data(self):
        return self._data

    def show(self):
        self._image.show()

    def save(self, directory):
        # path = "{0:s}/encrypted-{1:f}.{2:s}".format(
        #     directory,
        #     time.time(),
        #     self._extension,
        # )
        path = "{0:s}/encrypted.{1:s}".format(
            directory,
            self._extension,
        )
        self._image.save(
            path,
            format=self._image.format
        )
