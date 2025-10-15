.. _conceptual-model-definition:

Conceptual model definition
===========================

The CVXlab modeling process must be grounded on a solid conceptualization and 
mathematical definition of the problem to be solved. As its name suggests, CVXlab 
is primarily designed for **convex optimization problems**.

Definition of convex optimization problems and related mathematical concepts
lies outside the scope of this documentation. Fundational knowledge of Opearations 
Research and can be found in several references. Among others, we suggest the textbook:
`Introduction to Operations Research (F.Hillier and G.Lieberman, McGraw Hill Education, 
2024) <https://www.mheducation.com/highered/product/Introduction-to-Operations-Research-Hillier.html>`_

Since numerical problem generation and solution in CVXlab is grounded on the CVXPY
package, we also recommend referring to the `CVXPY documentation <https://www.cvxpy.org/
tutorial/intro/index.html>`_ for a comprehensive description of supported problem 
types.


Defining problem Sets
----------------------

*Sets* represent the dimensions of the model, defining its scope. 

As example, a production planning model may be defined over a set of *products* 
and a set of *time periods*. An energy system optimization model may be defined 
over a set of *technologies*, *energy carriers*, *locations* and *time periods*.

Each set is identified by a name, and its elements are 




defined by a list of elements (*coordinates*, in the following), used to 
identify model variables. 


Defining model sets and coordinates:

- *Sets* are defined in model setup file/s.
- *Coordinates* of each sets are defined in a dedicated Excel file, automatically
  generated once CVXlab Model instance is generated (see :ref:`Fill sets data (model 
  coordinates) <fill-sets-data>`).

Defining problem expressions
----------------------------

ttt



