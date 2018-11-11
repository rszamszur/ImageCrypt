import click
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
    pass


cli.add_command(encrypt)
cli.add_command(decrypt)
