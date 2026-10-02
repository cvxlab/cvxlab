.. _generation-of-model-directory-gsa:

Generation of model directory
==============================

The model directory should be generated following the standard procedure described in
:ref:`Generation of model directory <generation-of-model-directory>`.

Adittionally, for GSA, uncertainty functionalities must be enabled when generating the model
directory by setting ``uncertainty=True``.

API: :py:func:`cvxlab.create_model_dir`

Typical usage
--------------
.. code-block:: python

   cvxlab.create_model_dir(
       ...,
       uncertainty=True,
   )

This generates the model setup templates including the additional settings
required to define uncertainty-enabled data tables and model outputs of interest.

Parameters description
-----------------------
.. list-table::
   :header-rows: 1
   :align: center

   * - Parameter
     - Description
     - Default
   * - ``uncertainty``
     - If ``True`` enables the generation of the additional model setup fields required by
       the GSA workflow. It must be set to ``True`` when preparing a model for GSA.
     - ``False``

For the description of all other parameters, refer to
:ref:`Generation of model directory <generation-of-model-directory>`.