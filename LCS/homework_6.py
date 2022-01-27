from os import terminal_size
from re import T
from tabulate import tabulate
from propositional_logic import *
from tests import *

# to erase what i had before
f = open(r'Programming_I\LCS\output.txt', 'w')

f = open(r'Programming_I\LCS\output.txt', 'a', encoding='utf-8')

print()

prop = 'F ∨ G ~ G ∨ F'


# prop = homework_6['True a0x1nd False']['a)']
# print(prop)

# '_|_'


# '‾|‾'

# to do
# implement in code those abose


# print('¬')
# print('⊤')
# print('F ∨ ⊥ ∼ F')
# '¬', '∧', '∨', '⇒' ,'⇔', '∼'
# truth_table('¬⊤ ∼ ⊥')

# they need to be identified just the same as letters

# Ex 2 truth_table('( F ∼ G ) <=> F <=> G')
# truth_table('( F ∼ G ) <=> F <=> G')

# truth_table('Q ⊨ P ∧ Q')

# Ex 3
# truth_table('(P ⇒ Q) and Q ⊨ P ∧ Q')
# steps_check_new_wff('(Q ∨ R) and (Q ⇒ ¬P) and ¬(R ∧ P) ⊨ ¬P', True)
# ⊤⊥

# truth_table('(P ⇒ Q) and Q ⊨ (P ∧ Q)')

# steps_abstract_tree('( A and B )', True)

# steps_abstract_tree
# truth_table('( ( A => B ) => C ) => ( ( C => A ) => ( not D => A ) )') True

# truth_table("((P ∧ T) ⇒ (Q ∧ R)) and (Q ⇒ S) and (R ⇒ S) ⊨ ((P ∧ T) ⇒ S)")

# steps_check_new_wff("(¬(B(¬Q)) ∧ R)", True)

# relaxed_sense("P ⇒ ¬¬¬¬¬B ⇔ Q ∧ S", True)
# steps_abstract_tree('( ( P => ( not ( not ( not ( not ( not B ) ) ) ) ) ) <=> ( Q and S ) )', True)

# truth_table("(P ∨ A) and (¬P ∨ B) and not (A ∨ B)")

truth_table("( ((P ∧ Q) ∨ (¬P ∧ R)) ∼ ((P ⇒ Q) ∧ (¬P ⇒ R)) ) => ⊥")