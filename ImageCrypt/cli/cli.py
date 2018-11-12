import click
from logging import DEBUG, INFO
from ImageCrypt.logger import LoggerFactory
from .commands.encrypt import encrypt
from .commands.decrypt import decrypt


@click.group()
@click.option(
    "-v",
    "--verbose",
    help="Enable verbose logging.",
    is_flag=True,
    default=False,
)
def cli(**options):
    """Choose action Encrypt or Decrypt"""
    if options['verbose']:
        LoggerFactory.level = DEBUG
    else:
        LoggerFactory.level = INFO


cli.add_command(encrypt)
cli.add_command(decrypt)
