"""
Helper script to create a Sphinx conf.py.
This can mostly be done with jupyter-book, but we need to add the local extensions path.

This script should be run from the root of the book's repository.
"""
import os
import subprocess

# Path to the local extensions
path_extensions = '_ext'

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
if 'import sys' not in conf and os.path.exists(path_extensions):
    with open('conf.py', 'w') as f:
        conf = '\n'.join([
            '###############################################################################',
            '# Auto-generated with create_conf.py.',
            '# Add local extensions directory to the path.',
            '###############################################################################',
            'import sys, os',
            f'sys.path.append(os.path.abspath(\'{path_extensions}\'))',
            '',
            conf
        ])
        f.write(conf)
        print('Updated conf.py to include local extensions path.')
