.. _fill-model-setup-files:

Fill model setup file/s
-----------------------

text


.. admonition:: Example

    Consider a model defined by two sets: 
    
    **time periods**
        as a list of years.

    **products**
        as a list of energy products (*e.g. electricity, gas, oil, ...*), where each 
        product is classified by a category (*e.g. renewable, fossil, ...*), the 
        latter defined as filters.

    A data table **energy demand** can be defined, collecting exogenous
    data identified by the two sets above *time periods* and *products*. The data 
    table includes a number of data entries equal to the linear combination of the 
    coordinates of the two sets.

    Definition of variables shapes and filtering criteria depends on the ultimate 
    purpose of the variables in the mathematical expressions of the model. As 
    an example, two different variables may stem from data in **energy demand** 
    data table: 
    
    **E_renewable** 
        points to a sub-set of data in the *energy demand* data table, filtering only 
        the values related to the products *renewable* category in all time periods, 
        and of shape (number of technologies as rows, number of time periods as
        columns). 
    
    **E_all** 
        points to all entries in the *energy demand* data table, and of shape 
        (number of time periods as rows, number of products as columns). 