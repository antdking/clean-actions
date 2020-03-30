import click

from .api import process


@click.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"))
def cli(input, output):
    contents = input.read()
    processed = process(contents)
    output.write(processed)
    output.flush()
