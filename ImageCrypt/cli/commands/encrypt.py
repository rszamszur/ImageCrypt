import click
from ImageCrypt.method.base import BaseImageCrypt
from ImageCrypt.method.lsb import LSBImageCrypt
from ImageCrypt.method.verify import VerifyImageCrypt
from ImageCrypt.data.encrypt.text import EncodeTextData
from ImageCrypt.data.encrypt.file import EncodeFileData


@click.group()
@click.option(
    "--verify/--skip-verify",
    help="Transaction check to make sure nothing went wrong.",
    default=True,
)
def encrypt(**options):
    """Encrypt data into image."""
    if options['verify']:
        BaseImageCrypt.verify = True
    else:
        BaseImageCrypt.verify = False


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
    if image.verify:
        verify = VerifyImageCrypt(
            image_path=image.output_path,
            data_path=options['file'],
            data_type="file",
        )
        verify.verify()
        verify.cleanup()
