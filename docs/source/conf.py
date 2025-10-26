# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from cvxlab import __version__
import os
import sys
sys.path.insert(0, os.path.abspath('../../cvxlab/'))


project = 'CVXlab'
copyright = '2025, Matteo V. Rocco'
author = 'Matteo V. Rocco'
github_url = "https://github.com/cvxlab/cvxlab"
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",   # For Google or NumPy style
    "sphinx.ext.viewcode",   # Link to source code
    "sphinxcontrib.mermaid",  # For mermaid diagrams
    "myst_parser",           # For Markdown support
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "logo": {
        "image_light": "CVXlab_logo_light.png",
        "image_dark": "CVXlab_logo_dark.png",
    },
    "github_url": github_url,
    "navigation_with_keys": True,
    "show_toc_level": 2,
}
html_static_path = ['_static']
