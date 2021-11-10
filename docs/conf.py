# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'Elpis'
copyright = '2020, The University of Queensland'
author = 'Ben Foley, Nicholas Lambourne, Nay San'

# The full version, including alpha/beta/rc tags
release = '0.96.12'

master_doc = 'index'
# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx_autodoc_typehints',
    'recommonmark'
]

# Show undocumented members in docs
autodoc_default_options = {
    'undoc-members': True,
}

# Mock to get RTD docs to compile
autodoc_mock_imports = ["pytest"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# We also exclude the "ugly" auto-generated elpis.rst file and replace it with our own.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'elpis/elpis.rst']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = '_static/img/logo.png'
html_theme_options = {
    'logo_only': True,
}
github_url = 'https://github.com/CoEDL/elpis'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'style.css',
]

# -- Extension configuration -------------------------------------------------
