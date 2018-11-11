import click
from ImageCrypt.method.lsb import LSBImageCrypt
from ImageCrypt.data.encrypt.text import EncodeTextData
from ImageCrypt.data.encrypt.file import EncodeFileData


@click.group()
@click.option(
    "--run-check",
    help="Transaction check to make sure nothing went wrong.",
    is_flag=True,
    default=False,
)
def encrypt(**options):
    """Encrypt data into image."""
    pass


@encrypt.command()
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
    "--text",
    help="Path to file with text to encrypt.",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--save-dir",
    help="Directory to save encrypted image in.",
    required=False,
    default=".",
    type=click.Path(exists=True),
)
def text(**options):
    image = LSBImageCrypt(
        path=options['path'],
        data=EncodeTextData(options['text']),
    )
    image.encrypt()
    image.save(options['save_dir'])


@encrypt.command()
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
    "--file",
    help="Path to file to encrypt.",
    required=False,
    type=click.Path(exists=True),
)
@click.option(
    "--save-dir",
    help="Directory to save encrypted image in.",
    required=False,
    default=".",
    type=click.Path(exists=True),
)
def file(**options):
    image = LSBImageCrypt(
        path=options['path'],
        data=EncodeFileData(options['file']),
    )
    image.encrypt()
    image.save(options['save_dir'])
