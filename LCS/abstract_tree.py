import re
from tabulate import tabulate

from propositional_logic import *
from tests import *

      

# How to use
# call relaxed_to_strong() to get the strong syntax of a relaxed syntax
# call create_proposition() in order to create the required arguments
# steps_check_new_wff() if u want to see how to verify if it's a wff
# steps_abstract_tree() if u want to create the abstract tree


truth_table(homework_5['SUP'], 
    [
        {
            'A' : 1, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 1, 'F' : 0,  
        },
        {
            'A' : 1, 'B' : 0, 'C' : 0, 'D' : 1, 'E' : 1, 'F' : 0,
        },
        {
            'A' : 0, 'B' : 1, 'C' : 0, 'D' : 1, 'E' : 1, 'F' : 0,
        },
        {
            'A' : 0, 'B' : 1, 'C' : 0, 'D' : 1, 'E' : 0, 'F' : 0,
        },
        {
            'A' : 0, 'B' : 0, 'C' : 0, 'D' : 1, 'E' : 1, 'F' : 0,
        },
    ]

)
    











        

