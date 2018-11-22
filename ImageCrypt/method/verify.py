import tempfile
import shutil
import time
import hashlib
import sys
from ImageCrypt.data.factory import DataFactory
from ImageCrypt.method.lsb import LSBImageCrypt
from ImageCrypt.logger import LoggerFactory


class VerifyImageCrypt(object):

    def __init__(self, image_path, data_path, data_type):
        self._logger = LoggerFactory.create_logger(self.__class__.__name__)
        self._data_path = data_path
        self._logger.info("Creating temporary directory.")
        self._temp_dir = tempfile.mkdtemp()
        self._temp_file = "{0:s}/{1:f}.{2:s}".format(
            self._temp_dir,
            time.time(),
            self._data_path.split(".")[-1],
        )
        self._data = DataFactory.create(
            action="decrypt",
            data_type=data_type,
            path=self._temp_file,
        )
        self._image = LSBImageCrypt(
            image_path,
            self._data,
        )

    def verify(self):
        self._logger.info("Running transaction check.")
        self._image.decrypt()
        self._image.data.save()

        self._logger.info(
            "Calculating checksums for original and decrypted data."
        )
        original_md5 = hashlib.md5()
        original_sha1 = hashlib.sha1()
        original_sha256 = hashlib.sha256()
        with open(self._data_path, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                original_md5.update(data)
                original_sha1.update(data)
                original_sha256.update(data)

        self._logger.debug(
            "Original file MD5: {0:s}".format(original_md5.hexdigest())
        )
        self._logger.debug(
            "Original file SHA1: {0:s}".format(original_sha1.hexdigest())
        )
        self._logger.debug(
            "Original file SHA256: {0:s}".format(original_sha256.hexdigest())
        )

        decrypted_md5 = hashlib.md5()
        decrypted_sha1 = hashlib.sha1()
        decrypted_sha256 = hashlib.sha256()
        with open(self._temp_file, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                decrypted_md5.update(data)
                decrypted_sha1.update(data)
                decrypted_sha256.update(data)

        self._logger.debug(
            "Decrypted file MD5: {0:s}".format(decrypted_md5.hexdigest())
        )
        self._logger.debug(
            "Decrypted file SHA1: {0:s}".format(decrypted_sha1.hexdigest())
        )
        self._logger.debug(
            "Decrypted file SHA256: {0:s}".format(decrypted_sha256.hexdigest())
        )

        self._logger.info("Verifying checksums.")
        if decrypted_md5.hexdigest() != original_md5.hexdigest() or \
                decrypted_sha1.hexdigest() != original_sha1.hexdigest() or \
                decrypted_sha256.hexdigest() != original_sha256.hexdigest():
            self._logger.error("Checksum mismatch!")
            self._logger.error(
                "An error must have occurred during encryption!"
            )
            self._logger.info(
                "Decrypted data is most likely to be incomplete "
                "or irrecoverable."
            )
            self._logger.error(
                "Please create defect at "
                "https://github.com/rszamszur/ImageCrypt/issues/new "
                "issues providing necessary data to reproduce this case."
            )
            self.cleanup()
            sys.exit(1)

        self._logger.info("Checksums verified. Image is encrypted correctly.")

    def cleanup(self):
        self._logger.info(
            "Removing temporary directory: {0:s}".format(self._temp_dir)
        )
        shutil.rmtree(self._temp_dir)
