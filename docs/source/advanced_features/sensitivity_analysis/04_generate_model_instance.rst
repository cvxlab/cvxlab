.. _generate-model-class-instance-gsa:

Generate Model class instance
===============================

The ``Model`` class instance should be generated following the standard procedure
described in :ref:`Generate Model class instance <generate-model-class-instance>`.

For GSA, uncertainty functionalities must also be enabled when creating the model
instance by setting ``uncertainty=True``.

API: :py:meth:`cvxlab.Model.__init__`

Typical usage
--------------

.. code-block:: python

   model = cvxlab.Model(
       ...,
       uncertainty=True,
   )

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
:ref:`Generate Model class instance <generate-model-class-instance>`.
