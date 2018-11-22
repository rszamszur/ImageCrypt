import sys
from abc import ABCMeta, abstractmethod
from PIL import Image
from ImageCrypt.logger import LoggerFactory


class BaseImageCrypt(object):

    __metaclass__ = ABCMeta
    _verify = None
    _add_noise = None

    def __init__(self, path, data):
        self._image = Image.open(path)
        self._logger = LoggerFactory.create_logger(self.__class__.__name__)
        if self._image.format not in ["PNG", "TTIF"]:
            self._logger.error(
                "Invalid image format: {0:s}".format(self._image.format)
            )
            sys.exit(1)
        if self._image.width < 20 or self._image.height < 20:
            self._logger.error("Invalid image size! Minimum is 20x20 pixels.")
            sys.exit(1)
        self._data = data
        self._extension = self._image.format.lower()
        if self._image.mode in ["RGB", "YCbYCr"]:
            self.lsbs = 3
        elif self._image.mode in ["RGBA", "CMYK"]:
            self.lsbs = 4
        else:
            self._logger.error("Unsupported image color mode!")
            sys.exit(1)
        self._output_path = None

    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass

    @property
    def verify(self):
        return self.verify

    @verify.setter
    def verify(self, value):
        self._verify = value

    @property
    def add_noise(self):
        return self.add_noise

    @add_noise.setter
    def add_noise(self, value):
        self._add_noise = value

    @property
    def output_path(self):
        return self._output_path

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
        self._output_path = "{0:s}/encrypted.{1:s}".format(
            directory,
            self._extension,
        )
        self._logger.info(
            "Saving image under path: {0:s}".format(self._output_path)
        )
        self._image.save(
            self._output_path,
            format=self._image.format
        )
