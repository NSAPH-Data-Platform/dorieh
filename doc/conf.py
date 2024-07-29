# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

add_module_names = False
autoclass_content = 'both'
autodoc_member_order = 'bysource'
sys.path.insert(0, os.path.abspath('../src/python'))
sys.path.insert(0, os.path.abspath('src/python'))
sys.setrecursionlimit(2500)


# -- Project information -----------------------------------------------------

project = 'Dorieh Data Platform'
copyright = '2021-2024, Harvard University'
author = 'Michael A Bouzinier'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx_paramlinks',
    'sphinx.ext.autosectionlabel',
    'myst_parser',
]
myst_heading_anchors = 5

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.nsaph', 'notes', 'venv']
include_patterns = ['**']

html_static_path = ['_static']
html_css_files = [
    'css/dorieh.css',
]

#
#html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.cwl': 'cwl',
}

suppress_warnings = ['autosectionlabel.*']
