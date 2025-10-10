.. _conceptual-model-definition:

Conceptual model definition
---------------------------

The CVXlab modeling process must be grounded on a solid conceptualization and 
mathematical definition of the problem to be solved. 

CVXlab numerical problems can be formulated as 


**What is a linear optimization model?**

A **linear optimization model** (also known as a linear programming model) is a 
mathematical problem used to find the best outcome (such as maximum profit or 
minimum cost) in a system described by linear relationships.

**General formulation**

A linear optimization problem can be written as:

.. math::

   \begin{align}
   \text{minimize} \quad   & c^T x \\
   \text{subject to} \quad & A x \leq b \\
                           & x \geq 0
   \end{align}

where:

- :math:`x` is the vector of **decision variables** (endogenous variables),
- :math:`c` is the vector of **objective coefficients**,
- :math:`A` is the matrix of **constraint coefficients**,
- :math:`b` is the vector of **right-hand side values** (exogenous data).

**Endogenous vs. Exogenous variables**

- **Endogenous variables** are the decision variables whose values are determined 
  by solving the optimization problem (e.g., :math:`x` above).
- **Exogenous variables** are parameters or data provided to the model, not determined 
  by the optimization (e.g., :math:`c`, :math:`A`, :math:`b`).


**References**

Fundational knowledge of Opearations Research can be found in the following references: 

- `Introduction to Operations Research, Frederick Hillier and Gerald Lieberman, McGraw Hill Education, 2024
  <https://www.mheducation.com/highered/product/Introduction-to-Operations-Research-Hillier.html>`_
