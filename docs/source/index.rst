:html_theme.sidebar_secondary.remove:

.. role:: accent
   :class: cvxlab-accent

.. rst-class:: cvxlab-home

Python :accent:`laboratory` for algebraic :accent:`modelling`
=========================================================================

.. container:: cvxlab-home-intro

   .. raw:: html

      <hr class="cvxlab-intro-divider">

   - **Define models** using symbolic expressions and *YAML* or *Excel* settings.
   - **Manage data** in *SQLite*, keeping model structure separate from numerical data.
   - **Solve models** through a *CVXPY*-based numerical engine.
   - **Connect models** with managed data exchange in *parallel*, *sequential*,
     and *integrated* solution modes.

.. container:: cvxlab-home-meta

   .. raw:: html

      <hr class="cvxlab-intro-divider">

   **Version:** |version| | **Date:** |today|

   `PyPI <https://pypi.org/project/cvxlab/>`_ |
   `Source code <https://github.com/cvxlab/cvxlab>`_ |
   `Issue tracker <https://github.com/cvxlab/cvxlab/issues>`_ |
   `GitHub discussions <https://github.com/cvxlab/cvxlab/discussions>`_


.. grid:: 1 1 2 2
   :gutter: 3
   :class-container: cvxlab-section-cards

   .. grid-item-card:: Get Started

      Set up your environment with the :doc:`installation guide <installation>`,
      then build, solve, and inspect your first model in the
      :doc:`quick start <quick_start>`.

   .. grid-item-card:: User Guide
      :link: user_guide
      :link-type: doc
      :link-alt: Read the user guide

      Follow the full modeling workflow, from conceptual definition
      to results export.

   .. grid-item-card:: API Reference
      :link: api_reference
      :link-type: doc
      :link-alt: Browse the API reference

      Look up ``cvxlab.Model``, utility functions, symbolic operators,
      constants, and defaults.

   .. grid-item-card:: Resources
      :link: resources
      :link-type: doc
      :link-alt: Explore tutorials and resources

      Learn through tutorials, explore published models, and find
      related research.

   .. grid-item-card:: :doc:`Project <project>`
      :columns: 12

      Explore release changes in the :doc:`changelog <changelog>`, or help improve
      CVXlab through the :doc:`contributing guide <contributing>`.


.. grid:: 1 1 2 2
   :gutter: 3
   :margin: 5 0 0 0
   :class-container: cvxlab-section-cards

   .. grid-item-card:: Cite CVXlab

      .. _citing:

      If you use CVXlab in your work, cite the software version you used through
      the `Zenodo record <https://doi.org/10.5281/zenodo.20644006>`_.

      .. dropdown:: BibTeX

         .. code-block:: bibtex

            @software{rocco_cvxlab_2026,
              author    = {Rocco, Matteo V.},
              title     = {{CVXlab}},
              version   = {1.1.0},
              year      = {2026},
              publisher = {Zenodo},
              doi       = {10.5281/zenodo.20644006},
              url       = {https://doi.org/10.5281/zenodo.20644006}
            }

   .. grid-item-card:: About CVXlab

      Developed by `Matteo V. Rocco <https://www.energia.polimi.it/en/people/rocco-matteo-vincenzo-2/>`_,
      Associate Professor at *SESAM group*, `Department of Energy, Politecnico di Milano
      <https://www.energia.polimi.it/en/>`_.

      Released under the `Apache License 2.0 <http://www.apache.org/licenses/>`_.


.. toctree::
  :maxdepth: 1
  :hidden:

  Installation <installation>
  Quick Start <quick_start>
  User Guide <user_guide>
  API Reference <api_reference>
  Resources <resources>
  Project <project>
