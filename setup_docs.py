import os
import textwrap

def create_docs_structure():
    """Create basic Sphinx documentation structure."""
    docs_dir = "docs"
    
    # Create docs directory
    os.makedirs(docs_dir, exist_ok=True)
    
    # Create conf.py
    conf_content = textwrap.dedent("""
    # Configuration file for the Sphinx documentation builder.
    
    project = 'cvxlab'
    copyright = '2024, cvxlab'
    author = 'cvxlab'
    
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinx.ext.napoleon',
    ]
    
    templates_path = ['_templates']
    exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
    
    html_theme = 'alabaster'
    html_static_path = ['_static']
    """).strip()
    
    with open(os.path.join(docs_dir, "conf.py"), "w") as f:
        f.write(conf_content)
    
    # Create index.rst
    index_content = textwrap.dedent("""
    Welcome to cvxlab's documentation!
    ==================================
    
    .. toctree::
       :maxdepth: 2
       :caption: Contents:
    
    
    
    Indices and tables
    ==================
    
    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
    """).strip()
    
    with open(os.path.join(docs_dir, "index.rst"), "w") as f:
        f.write(index_content)
    
    # Create Makefile
    makefile_content = textwrap.dedent("""
    SPHINXOPTS    ?=
    SPHINXBUILD  ?= sphinx-build
    SOURCEDIR    = .
    BUILDDIR     = _build
    
    help:
    \t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
    
    .PHONY: help Makefile
    
    %: Makefile
    \t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
    """).strip()
    
    with open(os.path.join(docs_dir, "Makefile"), "w") as f:
        f.write(makefile_content)
    
    print(f"Documentation structure created in {docs_dir}/")
    print("To build docs: cd docs && make html")

if __name__ == "__main__":
    create_docs_structure()

    html_static_path = ['_static']
    
    # Intersphinx mapping
    intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'numpy': ('https://numpy.org/doc/stable/', None),
    }
    """).strip()
    
    with open(os.path.join(docs_dir, "conf.py"), "w") as f:
        f.write(conf_content)
    
    # Create index.rst
    index_content = textwrap.dedent("""
    Welcome to cvxlab's documentation!
    ==================================
    
    .. toctree::
       :maxdepth: 2
       :caption: Contents:
    
    
    
    Indices and tables
    ==================
    
    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
    """).strip()
    
    with open(os.path.join(docs_dir, "index.rst"), "w") as f:
        f.write(index_content)
    
    # Create Makefile
    makefile_content = textwrap.dedent("""
    SPHINXOPTS    ?=
    SPHINXBUILD  ?= python -m sphinx
    SOURCEDIR    = .
    BUILDDIR     = _build
    
    help:
    \t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
    
    .PHONY: help Makefile
    
    %: Makefile
    \t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
    """).strip()
    
    with open(os.path.join(docs_dir, "Makefile"), "w") as f:
        f.write(makefile_content)
    
    # Create Windows batch file
    batch_content = textwrap.dedent("""
    @ECHO OFF
    
    pushd %~dp0
    
    REM Command file for Sphinx documentation
    
    if "%SPHINXBUILD%" == "" (
    \tset SPHINXBUILD=python -m sphinx
    )
    set SOURCEDIR=.
    set BUILDDIR=_build
    
    if "%1" == "" goto help
    
    %SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
    goto end
    
    :help