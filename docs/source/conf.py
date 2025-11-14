# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from importlib.metadata import version as pkg_version

project = 'CVXlab'
copyright = '2025, Matteo V. Rocco'
author = 'Matteo V. Rocco'
github_url = "https://github.com/cvxlab/cvxlab"

# Avoid importing the package; read version from metadata
try:
    version = pkg_version("cvxlab")
except Exception:
    version = "nd"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",   # For Google or NumPy style
    "sphinx.ext.viewcode",   # Link to source code
    "sphinx.ext.mathjax",    # Add this for math rendering
    "sphinxcontrib.mermaid",  # For mermaid diagrams
    # 'myst_parser',           # For Markdown files (.md)
    'myst_nb',             # For Jupyter Notebook support
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

# Do not execute notebooks during doc build
nb_execution_mode = "off"

# Mock optional/heavy deps that are not available on RTD
autodoc_mock_imports = ["gurobipy"]

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
