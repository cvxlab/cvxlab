Installation
============

CVXlab supports **Python 3.9+** and is tested on Windows and macOS. Using an 
isolated ``conda`` environment is strongly recommended to avoid dependency 
conflicts with other projects.


Create a Conda Environment
---------------------------

Creating a dedicated conda environment ensures CVXlab and its dependencies don't 
interfere with other Python projects. This step is optional but highly recommended.

**Windows**: Open **Anaconda Prompt** or **Command Prompt** (with conda in PATH).

**macOS / Linux**: Open a terminal.

Then run:

.. code-block:: bash

   conda create -n cvxlab python=3.11
   conda activate cvxlab

.. tip::
   Replace ``python=3.11`` with your preferred Python version (3.9, 3.10, 3.12, etc.). 
   Python 3.11 is recommended for optimal performance.

Once the environment is activated, your prompt should show ``(cvxlab)`` at the 
beginning. You can now proceed to install CVXlab.


Install CVXlab (Users)
-----------------------

If you want to **use** CVXlab for modeling and solving optimization problems (without 
modifying the source code), install it via pip.

With the ``cvxlab`` conda environment active, run:

.. code-block:: bash

   pip install cvxlab

This command installs CVXlab and all required dependencies (numpy, pandas, cvxpy, 
openpyxl, pyyaml, dill, etc.).


Install from Source (Developers)
----------------------------------

If you want to **contribute** to CVXlab or modify the source code, install it in 
editable mode from the GitHub repository.

**Option 1: Clone directly (for private development)**

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/cvxgrp/cvxlab.git
      cd cvxlab

2. With the ``cvxlab`` conda environment active, install in editable mode:

   .. code-block:: bash

      pip install -e .[dev]

**Option 2: Fork (for contributing via pull requests)**

If you plan to submit changes back to the project:

1. Fork the repository on GitHub (click "Fork" at https://github.com/cvxgrp/cvxlab).

2. Clone **your fork**:

   .. code-block:: bash

      git clone https://github.com/YOUR_USERNAME/cvxlab.git
      cd cvxlab

3. Add the upstream repository as a remote:

   .. code-block:: bash

      git remote add upstream https://github.com/cvxgrp/cvxlab.git

4. With the ``cvxlab`` conda environment active, install in editable mode:

   .. code-block:: bash

      pip install -e .[dev]

5. Create a feature branch for your changes:

   .. code-block:: bash

      git checkout -b feature/my-new-feature

6. After making changes, push to your fork and open a pull request on GitHub.


**What the extras do**:

- ``[dev]``: Installs development dependencies (pytest, black, flake8, mypy, etc.).
- ``[docs]``: Installs Sphinx and related tools for building documentation.
- ``[solvers]``: Installs additional solver interfaces (e.g., ``gurobipy`` for GUROBI).

You can combine extras:

.. code-block:: bash

   pip install -e .[dev,docs,solvers]

.. tip::
   In editable mode (``-e``), changes you make to the source code are immediately 
   reflected without reinstalling. This is ideal for development and testing.


Verify Installation
-------------------

After installation, verify that CVXlab is correctly installed and importable:

.. code-block:: bash

   python -c "import cvxlab; print(cvxlab.__version__)"

Expected output (version may vary):

.. code-block:: text

   1.0.1b1

If the import succeeds and prints the version, CVXlab is ready to use.


Troubleshooting
---------------

**Commercial solver setup**

To use solvers like GUROBI, MOSEK, or CPLEX:

1. Install the solver's Python package (e.g., ``pip install gurobipy``).
2. Obtain and configure a license (see the solver's documentation).
3. Pass the solver name to CVXlab's solve methods:

   .. code-block:: python

      model.model_run(solver="GUROBI", verbose=True)

**Still having issues?**

- Check the `GitHub Issues <https://github.com/cvxgrp/cvxlab/issues>`_ page.
- Consult the `cvxpy installation guide <https://www.cvxpy.org/install/>`_ for 
  solver-specific troubleshooting.
- Reach out via email: |author_email|
