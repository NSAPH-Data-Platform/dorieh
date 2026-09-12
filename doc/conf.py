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
# local documentation-build extensions (doc/_ext)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/_ext')
sys.setrecursionlimit(2500)

# -- Project information -----------------------------------------------------

project = 'Dorieh Data Platform'
copyright = '2021-2026, Harvard University'
author = 'Michael A Bouzinier'

# The full version, including alpha/beta/rc tags.
# The documentation is built from this checkout, so the version is parsed
# from ../setup.py; if that fails (e.g. docs built outside a full source
# tree), fall back to the installed package metadata.
try:
    import re as _re
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '..', 'setup.py')) as _f:
        release = _re.search(r'version\s*=\s*["\']([^"\']+)["\']',
                             _f.read()).group(1)
except Exception:
    from importlib.metadata import version as _pkg_version
    release = _pkg_version('dorieh')


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
    'sphinx.ext.graphviz',
    'sphinxcontrib.mermaid',
    'myst_parser',
    'sphinx_togglebutton',
    # local shim: guarantees <outdir>/_static exists before build-finished
    # handlers run (sphinx_paramlinks crashes on Sphinx 8.2 without it)
    'ensure_static',
]
myst_heading_anchors = 5
# Enable MyST extensions
myst_enable_extensions = [
    "colon_fence",
    # other extensions...
]


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

# Render nested toctree entries in the sidebar on every page (by default the
# RTD theme collapses branches until the reader navigates into them, which
# hides e.g. the list of data domains from the main pages).
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
}

# Mock optional/heavy dependencies during autodoc imports, so API pages build
# in any environment: rpy2 (FST support, requires a matching R installation),
# pyspark/pyhive (the [spark] extra) and memory_profiler (used by memtest).
# Without this, a missing — or broken, e.g. linked against an uninstalled R —
# dependency leaves the affected module pages empty and spams the build log.
autodoc_mock_imports = [
    "rpy2",
    "pyspark",
    "pyhive",
    "memory_profiler",
    "pympler",
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext'
}

# ,
#     '.cwl': 'cwl',

suppress_warnings = [
    'autosectionlabel.*',
    # Pygments cannot lex the {identifiers} placeholders and plpgsql $body$
    # blocks embedded in generated lineage pages; it retries in relaxed mode
    # and renders correctly, so these warnings are purely cosmetic.
    'misc.highlighting_failure',
]
