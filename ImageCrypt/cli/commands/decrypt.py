from six import text_type
import click
from ImageCrypt.method.lsb import LSBImageCrypt
from ImageCrypt.data.decrypt.text import DecodeTextData
from ImageCrypt.data.decrypt.file import DecodeFileData


@click.group()
def decrypt():
    pass


@decrypt.command()
@click.option(
    "--path",
    help="Path to image",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--method",
    help="Method of decryption",
    required=True,
    type=click.Choice(["LSB", "DCT"]),
)
@click.option(
    "--save-dir",
    help="Directory to save encrypted image in.",
    required=False,
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "--filename",
    help="Output filename.",
    required=False,
    default="decrypted.txt",
    type=text_type,
)
def text(**options):
    path = "{0:s}/{1:s}".format(
        options["save_dir"],
        options["filename"],
    )
    image = LSBImageCrypt(
        path=options['path'],
        data=DecodeTextData(path),
    )
    image.decrypt()
    image.data.save()


@decrypt.command()
@click.option(
    "--path",
    help="Path to image",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--method",
    help="Method of encryption",
    required=True,
    type=click.Choice(["LSB", "DCT"]),
)
@click.option(
    "--save-dir",
    help="Directory to save encrypted image in.",
    required=False,
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "--filename",
    help="Output filename.",
    required=True,
    type=text_type,
)
def file(**options):
    path = "{0:s}/{1:s}".format(
        options["save_dir"],
        options["filename"],
    )
    image = LSBImageCrypt(
        path=options['path'],
        data=DecodeFileData(path),
    )
    image.decrypt()
