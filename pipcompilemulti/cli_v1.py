"""First version of command line interface"""

import logging

import click

from .options import OPTIONS, DEFAULT
from .actions import recompile
from .verify import verify_environments


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--compatible', '-c', multiple=True,
              help='Glob expression for packages with compatible (~=) '
                   'version constraint. Can be supplied multiple times.')
@click.option('--forbid-post', '-P', multiple=True,
              help="Environment name (base, test, etc) that cannot have "
                   'packages with post-release versions (1.2.3.post777). '
                   'Can be supplied multiple times.')
@click.option('--generate-hashes', '-g', multiple=True,
              help='Environment name (base, test, etc) that needs '
                   'packages hashes. '
                   'Can be supplied multiple times.')
@click.option('--directory', '-d', default=DEFAULT['directory'],
              help='Directory path with requirements files.')
@click.option('--in-ext', '-i', default=DEFAULT['in_ext'],
              help='File extension of input files.')
@click.option('--out-ext', '-o', default=DEFAULT['out_ext'],
              help='File extension of output files.')
@click.option('--header', '-h', default='',
              help='File path with custom header text for generated files.')
@click.option('--only-name', '-n', multiple=True,
              help='Compile only for passed environment names and their '
                   'references. Can be supplied multiple times.')
@click.option('--upgrade/--no-upgrade', default=True,
              help='Upgrade package version (default true)')
def cli(ctx, compatible, forbid_post, generate_hashes, directory,
        in_ext, out_ext, header, only_name, upgrade):
    """Recompile"""
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    OPTIONS.update_from_dict({
        'compatible': compatible,
        'forbid_post': set(forbid_post),
        'generate_hashes': set(generate_hashes),
        'directory': directory,
        'in_ext': in_ext,
        'out_ext': out_ext,
        'header': header or None,
        'only_names': only_name,
        'upgrade': upgrade,
    })
    if ctx.invoked_subcommand is None:
        recompile()


@cli.command()
@click.pass_context
def verify(ctx):
    """
    For each environment verify hash comments and report failures.
    If any failure occured, exit with code 1.
    """
    ctx.exit(0
             if verify_environments()
             else 1)
