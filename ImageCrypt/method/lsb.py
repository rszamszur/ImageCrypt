import random
from collections import namedtuple
from ImageCrypt.method.base import BaseImageCrypt


class LSBImageCrypt(BaseImageCrypt):

    def __init__(self, path, data):
        super(LSBImageCrypt, self).__init__(
            path,
            data,
        )
        self.header_map = {
            "vbs": {
                2: 7,
                3: 10,
                4: 14,
            },
            "c2b": {
                1: "00",
                2: "01",
                3: "10",
                0: "11",
            },
            "b2c": {
                "00": 1,
                "01": 2,
                "10": 3,
                "11": 0,
            }
        }
        self.header = None
        self.start_pixel = None
        self.end_pixel = None

    def _get_header(self):
        self._logger.info("Reading headers.")
        hl = self._calculate_header_len()
        self.header = []

        index = 0
        for x in range((hl/self.lsbs) + 1):
            for color in self._image.getpixel((x, 0)):
                self.header.append(color & 1)
                index += 1
                if index == hl:
                    break

        sx = self.header[0:self.header_map['vbs'][len(str(self._image.width))]]
        del self.header[0:self.header_map['vbs'][len(str(self._image.width))]]
        sy = self.header[0:self.header_map['vbs'][len(str(self._image.height))]]
        del self.header[0:self.header_map['vbs'][len(str(self._image.height))]]
        ex = self.header[0:self.header_map['vbs'][len(str(self._image.width))]]
        del self.header[0:self.header_map['vbs'][len(str(self._image.width))]]
        ey = self.header[0:self.header_map['vbs'][len(str(self._image.height))]]
        del self.header[0:self.header_map['vbs'][len(str(self._image.height))]]
        ec = "".join(str(c) for c in self.header)

        start_pixel = namedtuple("StartPixel", "x y")
        self.start_pixel = start_pixel(
            int(
                "".join(str(c) for c in sx),
                2
            ),
            int(
                "".join(str(c) for c in sy),
                2
            )
        )

        end_pixel = namedtuple("EndPixel", "x y color")
        self.end_pixel = end_pixel(
            int(
                "".join(str(c) for c in ex),
                2
            ),
            int(
                "".join(str(c) for c in ey),
                2
            ),
            self.header_map['b2c'][ec],
        )
        self._logger.debug(
            "Start pixel x: {0:d}, y: {1:d}".format(
                self.start_pixel.x,
                self.start_pixel.y,
            )
        )
        self._logger.debug(
            "End pixel x: {0:d}, y: {1:d}, color: {2:d}".format(
                self.end_pixel.x,
                self.end_pixel.y,
                self.end_pixel.color,
            )
        )

    def _set_header(self):
        self._logger.info("Generating headers.")
        hl = self._calculate_header_len()
        start_pixel = namedtuple("StartPixel", "x y")
        sx = (hl / self.lsbs) + 1
        self.start_pixel = start_pixel(sx, 0)

        dl = self._data.binary.length
        end_pixel = namedtuple("EndPixel", "x y color")
        x = ((dl / self.lsbs) + self.start_pixel.x) % (self._image.width - 1)
        y = ((dl / self.lsbs) + self.start_pixel.x) / (self._image.width - 1)
        color = dl % self.lsbs
        self.end_pixel = end_pixel(x=x, y=y, color=color)

        h_sx = format(
            self.start_pixel.x,
            "0{0:d}b".format(
                self.header_map['vbs'][len(str(self._image.width))]
            )
        )
        h_sy = format(
            self.start_pixel.y,
            "0{0:d}b".format(
                self.header_map['vbs'][len(str(self._image.height))]
            )
        )
        h_ex = format(
            self.end_pixel.x,
            "0{0:d}b".format(
                self.header_map['vbs'][len(str(self._image.width))]
            )
        )
        h_ey = format(
            self.end_pixel.y,
            "0{0:d}b".format(
                self.header_map['vbs'][len(str(self._image.height))]
            )
        )
        h_pc = self.header_map['c2b'][self.end_pixel.color]
        hs = list(
            "{0:s}{1:s}{2:s}{3:s}{4:s}".format(h_sx, h_sy, h_ex, h_ey, h_pc)
        )
        self._logger.debug(
            "Start pixel x: {0:s}, y: {1:s}".format(
                h_sx,
                h_sy,
            )
        )
        self._logger.debug(
            "End pixel x: {0:s}, y: {1:s}, color: {2:s}".format(
                h_ex,
                h_ey,
                h_pc,
            )
        )
        self.header = [hs[i:i + self.lsbs] for i in range(0, len(hs), self.lsbs)]
        self._logger.debug("Generated Headers: {0:s}".format(self.header))

    def _calculate_header_len(self):
        self._logger.info("Calculating headers length.")
        x_len = self.header_map['vbs'][len(str(self._image.width))]
        y_len = self.header_map['vbs'][len(str(self._image.height))]
        return (2 * x_len) + (2 * y_len) + 2

    @staticmethod
    def _set_lsb(value, lsb):
        if lsb == "0":
            value = value & ~1
        else:
            value = value | 1
        return value

    @staticmethod
    def _read_lsb(value):
        return value & 1

    def encrypt(self):
        self._logger.info("Begin encrypting {0:s}".format(self._data.path))
        self._set_header()
        self._data.validate(
            self._image.size,
            self.start_pixel,
            self.end_pixel,
        )

        x = 0
        y = 0
        self._logger.info("Encrypting headers into image.")

        while len(self.header) > 0:
            colors = []

            for index, color in enumerate(self._image.getpixel((x, y))):
                try:
                    if (color & 1) != self.header[0][index]:
                        color = self._set_lsb(color, self.header[0][index])
                        colors.append(color)
                except IndexError:
                    colors.append(color)

            self._image.putpixel((x, y), tuple(colors))
            self.header.pop(0)
            x += 1

        x = self.start_pixel.x
        y = self.start_pixel.y
        data = self._data.binary.group_bits(self.lsbs)
        self._logger.info("Encrypting data into image.")

        while len(data) > 0:
            colors = []

            for index, color in enumerate(self._image.getpixel((x, y))):
                try:
                    if (color & 1) != data[0][index]:
                        color = self._set_lsb(color, data[0][index])
                        colors.append(color)
                except IndexError:
                    colors.append(color)

            self._image.putpixel((x, y), tuple(colors))
            data.pop(0)
            x += 1
            if x == self._image.width - 1:
                x = 0
                y += 1
                if y == self._image.height:
                    raise RuntimeError("End of image!")

        self._logger.info("Message successfully encrypted.")
        self._logger.debug(
            "Ending point: {0:d},{1:d}".format(x, y)
        )

        if self.add_noise:
            self._logger.info("Filling rest image with random noise.")

            while True:
                colors = []

                for color in self._image.getpixel((x, y)):
                    color = self._set_lsb(
                        color,
                        random.randint(0, 1),
                    )
                    colors.append(color)

                self._image.putpixel((x, y), tuple(colors))

                x += 1
                if x == self._image.width - 1:
                    x = 0
                    y += 1
                    if y == self._image.height:
                        break

    def decrypt(self):
        self._logger.info("Begin decrypting {0:s}.".format(
                self._image.filename
            )
        )
        self._get_header()
        x = self.start_pixel.x
        y = self.start_pixel.y
        bits = []

        while True:
            for color in self._image.getpixel((x, y)):
                bits.append(
                    self._read_lsb(color)
                )
            x += 1
            if x == self._image.width - 1:
                x = 0
                y += 1

            if x == self.end_pixel.x and y == self.end_pixel.y:
                if self.end_pixel.color != 0:
                    for i, color in enumerate(self._image.getpixel((x, y))):
                        bits.append(
                            self._read_lsb(color)
                        )
                        if i == self.end_pixel.color - 1:
                            break

                break

        self._logger.info("Data successfully decrypted.")
        self._data.binary.bits = bits
        self._data.save()
