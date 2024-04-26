"""
Simple command line to help with generating a Sphinx configuration file and updating translations.
"""
import os
import subprocess
from pathlib import Path
from typing import Iterable

import click

# Path to the local extensions
_local_extensions_path = '_ext'

# Build directory for languages
_locale_build_dir = 'locales/_build/gettext'


def create_sphinx_config(overwrite=False):
    """
    Create a Sphinx configuration file from this project's Jupyter Book configuration file.
    This can mostly be done with jupyter-book, but we need to add the local extensions path.
    """

    # Check if we should overwrite an existing conf.py file
    if os.path.exists('conf.py') and not overwrite:
        raise FileExistsError('A conf.py file already exists. Use --overwrite to replace it.')

    # Check we have a _config.yml file
    if not os.path.exists('_config.yml'):
        raise FileNotFoundError('No _config.yml file found. Run this script from the root of your book.')

    # Create the Sphinx configuration with jupyter-book
    subprocess.run(["jupyter-book", "config", "sphinx", "."])
    with open('conf.py', 'r') as f:
        conf = f.read()

    # Include instruction to add local extensions to the path if needed
    # See https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions
    # We optimistically assume that, if conf.py already contains 'import sys', then it has been written by
    # a newer version of jupyter-book that already includes the local extensions path.
    if 'import sys' not in conf and os.path.exists(_local_extensions_path):
        with open('conf.py', 'w') as f:
            conf = '\n'.join([
                '###############################################################################',
                '# Auto-generated with create_conf.py.',
                '# Add local extensions directory to the path.',
                '###############################################################################',
                'import sys, os',
                f'sys.path.append(os.path.abspath(\'{_local_extensions_path}\'))',
                '',
                conf
            ])
            f.write(conf)
            click.secho('Updated conf.py to include local extensions path.', fg='green')


def _update_catalog_template():
    """
    Update the .pot file using sphinx-build.
    """
    subprocess.run(["sphinx-build", "-b", "gettext", ".", _locale_build_dir])


def _update_translations(add_languages: Iterable[str] = ()):
    """
    Update the .po files using sphinx-intl.
    Optionally add new languages specified by their code (usually two letters).
    See https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language
    """
    cmd = ["sphinx-intl", "update", "-p", _locale_build_dir]
    if isinstance(add_languages, str):
        add_languages = [add_languages]
    for lang in add_languages:
        cmd += ["-l", lang]
    subprocess.run(cmd)


@click.command()
@click.option('--update/--no-update', default=True, help=
'Update the main language and translations')
@click.option('--lang', '-l', default=(), help=
'Add the specified language to the list of translations, given the two-letter code',
              multiple=True)
@click.option('--config/--no-config', default=True, help=
'Create a conf.py file from the _config.yml file')
@click.option('--overwrite/--no-overwrite', default=False, help=
'Overwrite an existing conf.py file if it exists')
def cli(update: bool, lang: str, config: bool, overwrite: bool):
    """
    Simple command line to create a Sphinx configuration file or update translations (.pot and .po files).
    """
    # Create a conf.py if requested; this won't be deleted
    if config:
        create_sphinx_config(overwrite=overwrite)

    # Update the translations if requested, creating a temporary conf.py if needed
    if update or lang:
        # Create a conf.py file if it doesn't exist
        conf_exists = os.path.exists('conf.py')
        if not conf_exists:
            click.echo('Creating temporary conf.py file')
            create_sphinx_config(overwrite=overwrite)
        elif overwrite and not config:
            click.echo('Overwriting conf.py file')
            create_sphinx_config(overwrite=overwrite)

        # Update the translations
        _update_catalog_template()
        _update_translations(add_languages=lang)

        # Remove the conf.py file if we created it
        if not conf_exists:
            click.echo('Removing temporary conf.py file')
            os.remove('conf.py')


if __name__ == '__main__':
    # Switch to the base directory for the project
    os.chdir(Path(__file__).parent.parent)
    cli()
