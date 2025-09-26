.. _user_guide:

User Guide
==========

This section provides a comprehensive guide to using CVXlab for modeling and solving
optimization problems, including the conceptualization of the problem, the model
instance generation and setup, the data management and the model solution.
This guide is structured as a sequence of steps, each described in detail in a 
dedicated page.

In generating a model instance, two cases may occur:

- *Model generation from scratch*
   all steps included in :ref:`Preliminary activities <preliminary-activities>` and
   :ref:`CVXlab model generation <model-generation>` must be performed.

- *Model generation from existing settings and database*
   this case applies when a model has already conceptualized, and its settings and 
   database are already available (e.g. from a previous modeling exercise). 
   In this case, a model instance can be directly generated based on 
   :ref:`step 4 <generate-model-class-instance>` in :ref:`CVXlab model generation 
   <model-generation>`.

Once the model instance has generated, the following actions can be performed:

- *Model run and results export*
   Numerical model can be solved, and results exported to database based on steps 
   included in :ref:`Model solution and results export <model-solution-and-results-export>`.

- *Model data or expressions update*
   In case only a part or all exogenous data need to be updated, or in case new/existing 
   expressions in symbolic problem need to be formulated/modified, without generating 
   a new model instance, steps described in :ref:`Updating symbolic problem and data <model-update>` 
   can be performed.

- *Utilities*
   A set of :ref:`Utilities <utilities>` is provided to facilitate data
   inspection, saving and loading of model instances, refreshing model database.

A Jupyter notebook is available as a tutorial of the CVXlab modeling process. 
See: :ref:`resources-tutorial`


.. _preliminary-activities:

Preliminary activities
----------------------

Using CVXlab requires a series of preliminary activities that must be performed
before starting the actual modeling process. These activities include:

1. :ref:`conceptual-model-definition`: the whole CVXlab modeling process must be 
   grounded on a solid conceptualization and mathematical definition of the problem 
   to be solved. This step consists in defining the fundamental model 
   structure pen-on-paper (i.e. definition of objective function, constraints, 
   exogenous/endogenous variables). Once the problem is well defined, the CVXlab 
   modeling process can be started.

2. :ref:`generation-of-model-directory`: a model directory is generated based on a 
   template, which contains all the necessary files to translate the conceptual
   model into the a CVXlab model instance. 
   Setup files can be generated as *.yml* or *.xlsx* formats. Optionally, a 
   *Jupyter notebook* can be created to guide the user through the modeling process.
   
   - API: :py:func:`cvxlab.create_model_dir`


.. _model-generation:

CVXlab model generation
-----------------------

3. :ref:`fill-model-setup-files`: once the model directory is generated 
   (:ref:`step 2 <generation-of-model-directory>`), the user translates the 
   conceptual model into the setup file/s. This implies defining the following
   fundamental elements:
   
   - **Sets**
      *Sets* are the dimensions of the model, defining its scope. Each set is 
      defined by a list of elements (*coordinates*, in the following), used to 
      identify model variables. Each set (and the related coordinates) correponds 
      to a table in the model *SQLite database* that will be generated.
      Sets are defined in a dedicated yaml file (or Excel tab), while coordinates
      are defined in separate Excel spreadsheet once the model instance is generated 
      (see :ref:`step 5 <fill-sets-data>`).

   - **Data tables** and related **variables**
      *Data tables* are collections of model data identified by a list of sets. 
      They can be defined either as *exogenous* (independent variables, collecting 
      input data), *endogenous* (dependent variables), or *constants* (fixed values). 
      Each data table corresponds to a table in the model *SQLite database* that 
      will be generated, linked to the related sets tables by foreign keys. 

      *Variables* are symbolic items pointing to data in data tables: multiple 
      variables can stem from a same data table, assuming different shapes and 
      referring to different subsets of data tables values, depending on how 
      variables are defined and related coordinates are filtered.
      Both data tables and variables are defined in the same yaml file (or 
      Excel tab).

   - **Problems** and related **Expressions**
      *Problems* are collections of *expressions*, the latter defined as symbolic
      equations, inequalities or objective functions. Expressions are defined 
      relying on model *variables*, mathematical *operators* and *user-defined 
      functions*. Multiple problems can be defined in a same model, and 
      could be solved in parallel as independent or integrated problems.
      Problems and the related expressions are defined in a dedicated yaml file 
      (or Excel tab).   

4. :ref:`generate-model-class-instance`: once the model setup files are filled 
   (:ref:`step 3 <fill-model-setup-files>`), an instance of the Model class is 
   generated. This step is performed by the *Model class constructor*, which 
   translates the information provided by setup file/s into a Python object. 
   The model instance includes all the necessary information and APIs to generate 
   and to solve numerical problems, and to handle exogenous/endogeous model data.
  
   - API: :py:class:`cvxlab.Model`

5. :ref:`fill-sets-data`: text

6. :ref:`data-structures-init`: text

7. :ref:`fill-exogenous-data`: text

8. :ref:`numerical-problem-init`: text


.. _model-solution-and-results-export:

Model solution and results export
---------------------------------

9. :ref:`numerical-problem-run`: text

10. :ref:`export-model-results`: text


.. _model-update:

Updating problem and input data
-------------------------------

ttt


.. _utilities:

Utilities
---------

inspection

saving and loading model instances



.. toctree::
   :maxdepth: 1
   :hidden:

   user_guide_steps/conceptual_model_definition
   user_guide_steps/model_directory_generation
   user_guide_steps/fill_model_setup_files
   user_guide_steps/generate_model_instance
   user_guide_steps/fill_sets_data
   user_guide_steps/data_structures_init
   user_guide_steps/fill_exogenous_data
   user_guide_steps/numerical_problem_init
   user_guide_steps/numerical_problem_run
   user_guide_steps/export_model_results
























