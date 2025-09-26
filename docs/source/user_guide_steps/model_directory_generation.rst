.. _generation-of-model-directory:

Generation of model directory
-----------------------------

This step initializes a new model workspace by creating a dedicated directory 
containing all the necessary configuration template files required to create and
handle an instance of the :py:class:`cvxlab.Model`.
All files related to the model instance will be stored in this directory (settings 
files, data input files, database, etc.).
It is possible to choose between YAML (*.yml*) or Excel (*.xlsx*) templates for 
setup files, depending on user's workflow preferences.
Optionally, a Jupyter notebook can be included to guide the user through the 
modeling process interactively.
Refer to the API documentation for details on available arguments and customization 
options:`cvxlab.create_model_dir`.

**Typical usage:**

.. code-block:: python

    import cvxlab 

    cvxlab.create_model_dir(
        model_dir_name="my_model",
        main_dir_path="path/to/parent",
        template_file_type="yml",  # or "xlsx"
        export_tutorial=True
    )
