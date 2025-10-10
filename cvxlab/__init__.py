"""CVXlab - Open-source Python laboratory for convex algebraic modeling.

This module provides shortcuts to the main functionalities of CVXlab, including 
Model class and a set of utility functions for managing model directories.
The module also includes metadata about the package such as authorship and 
licensing information.
"""

from cvxlab.backend.model import Model
from cvxlab.support.model_directory import (
    create_model_dir,
    transfer_setup_info_xlsx,
    handle_model_instance
)
from .version import __version__

__authors__ = "'Matteo V. Rocco'"
__collaborators__ = """
    'Lorenzo Rinaldi', 'Debora Ghezzi', 'Valeria Baiocco', 'Camilla Citterio', 
    'Emanuela Colombo'
    """
__license__ = "Apache License Version 2.0, (January 2004) <http://www.apache.org/licenses/>"
