# to do

from os import close
import re
from typing import Pattern, final

from tabulate import tabulate

fout = open(r'Programming_I\LCS\output.txt', 'a', encoding='utf-8')

nod = 0#nodul curent in care lucrez
symbol = ['not', 'and', 'or', '=>', '<=>', '¬', '∧', '∨', '⇒' ,'⇔' ,'~', '∼', '⊨', '|=']

passed = []


split = []

all_nodes = set()

def initialize(prop: str):
    # firslty, format the string
    # give space after every char
    new_prop = ''
    for char in prop:
        new_prop += char + ' '
        
    # be aware that and is now written as a n d
    new_prop = new_prop.replace('a n d', 'and')
    new_prop = new_prop.replace('n o t', 'not')
    new_prop = new_prop.replace('o r', 'or')
    new_prop = new_prop.replace('= >', '=>')
    new_prop = new_prop.replace('< =>', '<=>')
    new_prop = new_prop.replace('| =', '|=')

    new_prop = new_prop.split()
    
    new_prop = ' '.join(new_prop)


    new_prop = relaxed_to_strong(new_prop, False)

    # replace unicode with normal chars
    new_prop = new_prop.replace('¬', 'not')
    new_prop = new_prop.replace('∧', 'and')
    new_prop = new_prop.replace('∨', 'or')
    new_prop = new_prop.replace('⇒', '=>')
    new_prop = new_prop.replace('⇔', '<=>')
    new_prop = new_prop.replace('∼', '~')
    

    #REGEX has a problem with |=

    new_prop = new_prop.replace('⊨', '|=')


    return new_prop

# create the split proposition, a list of all variables and connectives
def create_proposition(prop: str):
    # create the list of every symbol and connective

    # replace ~ with <=>
    # fout.write(prop)
    # prop = prop.replace('~', '<=>')


    global split
    global passed
    split = prop.split(' ')

    # keep track of what symbols or connective i already appended to the tree
    passed = [0 for a in split]



# create the abstract tree
def create_tree(rez: list, index: int, steps: bool) -> str:
    # indications
    # proposition.split(' ') = ['(', '(', 'P', 'and', 'Q', ')', '=>', '(', 'not', 'R', ')', ')']

    # first ( means create a list
    # proposition = '( P and Q )'
    # result =  [ 'and', [P], [Q] ]


    right = -1
    global split
    global nod
    
    for i in range(index, len(split) ):
        var = split[i]

        passed[i] += 1 #keep track if i crossed this index before
        if passed[i] == 1: #if it's the first time, it means i need to add to tree
            if var == '(' or var == ')':
                if var == '(': #append to current list
                    
                    if nod == 0:
                        nod = 1
                    else:
                        nod *= 2 
                    
                    if nod not in all_nodes:
                        all_nodes.add(nod)
                    else:
                        # means that this node is already in my tree, so i go next to it's brother
                        nod += 1
                    if steps == True:
                        fout.write(f"'{var}'  Create node {nod}\n")
                    
                    rez.append([]) 
                    create_tree(rez[-1], i + 1, steps)#continue creation in the list i just appended
                else:
                    if steps == True:
                        nod = nod // 2
                        fout.write(f"'{var}'  Return to node {nod}\n")#return to father
                    #i need to step out and get to the father list of rez
                    break
            elif var in symbol:
                # because i always return to the father now the var nod holds the right working node
                # no changes required for the var nod
                if steps == True:
                    fout.write(f"'{var}'  Update node {nod} to {[var]}\n")

                rez.insert(0, var) #i need to insert the symbol
            else:
                

                nod *= 2

                if nod not in all_nodes:
                    all_nodes.add(nod)
                else:
                    nod += 1 

                if steps == True:
                    fout.write(f"'{var}'  Update node {nod} to {[var]}\n")

                nod = nod // 2
                # return to father
                
                
                rez.append([var]) # insert the proposition


# verify with propositional variables if a proposition is a wff
def new_wff(prop: str, steps: bool):

    prop = initialize(prop)
    #rules
    # A
    # ( not A )
    # ( A and B) 
    # ( A or B ) 
    # ( A => B ) 
    # ( A <=> B )
    #Goal: replace every good wff with only one Letter: ( A and B) change to A
    rules = [
        '[(] not [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] and [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] or [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] => [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] <=> [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ~ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] [|]= [A-Z⊤⊥] [)]',

        #ISSUE WITH |=

        # '¬', '∧', '∨', '⇒' ,'⇔', '∼', '⊨'

        # REGEX HAS ISSUES WITH UNICODE

        '[(] ¬ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ∧ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ∨ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ⇒ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ⇔ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ∼ [A-Z⊤⊥] [)]',
        '[(] [A-Z⊤⊥] ⊨ [A-Z⊤⊥] [)]',
        


    ]
    last = []

    while prop != last: 
        
        # if i made at least one change
        show = 'After changes:  '
        if len(last) == 0:
            show = ''
        if steps == True:
            fout.write(show + prop + '\n')
        
        
        last = prop
        total = []
        # prop = '( not A ) and ( not B )' # -> A and B
        for rule in rules:
            pattern = re.compile(rule)
            result = pattern.findall(prop)
            total += result

        for change in total:
            if steps == True:
                fout.write(f'Replace {change} with propositional variable A\n')
            prop = prop.replace(change, 'A')
    #in the end if end up with just one letter it means i have a wff
    if prop >= 'A' and prop <= 'Z':
        if steps == True:
            fout.write('i finished with a propositonal variable => i have a wff\n')
        return True
    return False


# choose if to show steps in creating the tree
# and show the steps if it's a wff
def steps(prop: str, answer: bool):


    if new_wff(prop, answer) == True:
        fout.write('This is a wff\n')
    else:
        fout.write('This is not a wff\n')
        return

    tree = []
    
    fout.write('\n')
    if answer == True:
        fout.write('!!!Remainder!!!\n')
        fout.write("In a binary tree, \nif the father's node is F then \nit's left child is placed at F * 2 and \nit's right child is placed at F * 2 + 1 \n")
        fout.write('\n')
        fout.write('Instructions:')
    fout.write('\n')
    create_tree(tree, 0, answer)
    #i have an extra parathesis when i create my tree
    tree = tree[0]

    fout.write('\n')
    fout.write('Tree but in list representation:\n')
    fout.write(f'{tree}\n')

# show steps in checking if it's a wff
def steps_check_new_wff(prop: str, answer: bool):
    if new_wff(prop, answer) == True:
        fout.write('This is a wff\n')
        return True
    else:
        fout.write('This is not a wff\n')
        return False
 
# show steps in creating the abstract tree
def steps_abstract_tree(prop: str, answer: bool):
    prop = initialize(prop)
    
    if new_wff(prop, False) == False:
        fout.write('This is not an wff, cannot create tree\n')
        return

    create_proposition(prop)
    
    tree = []
    
    fout.write('\n')
    if answer == True:
        fout.write('!!!Remainder!!!\n')
        fout.write("In a binary tree, \nif the father's node is F then \nit's left child is placed at F * 2 and \nit's right child is placed at F * 2 + 1\n")
        fout.write('\n')
        fout.write('Instructions:')
    fout.write('\n')
    create_tree(tree, 0, answer)
    #i have an extra parathesis when i create my tree
    tree = tree[0]

    fout.write('\n')
    fout.write('Tree but in list representation:\n')
    fout.write(f'{tree}\n')


# verify if it's a wff by checking the tree creation
def wff(step):

    #if my step at some point has 4 elements in, it's not a wff
    #because the maximum of elements should be 3
    # the connector, prop, prop
    # negation, prop
    if len(step) > 3 or (len(step) >= 2 and step[0] not in symbol):
        return False

    #the bottom case, only a letter, a letter is a wff
    if len(step) == 1:
        if type(step[0]) == type([]):
            return wff(step[0])
        if (step[0] >= 'A' and step[0] <= 'Z'):
            return True
        return False
    

    #normal layer, step[0] should have the connector and, or, not, ->, <->
    if step[0] in symbol:
        if step[0] == 'not' or step[0] == '¬':
            if len(step) != 2:#not should have one more prop
                return False
            return wff(step[1])
        else:
            if len(step) != 3:#connctor should have 2 more prop
                return False
            return wff(step[1]) and wff(step[2])


# transform a relaxed string to a strong one
# apply paranthesis after the folloswing precedence
#  1       2       3        4          5
# not     and      or      =>         <=> 
def relaxed_to_strong(prop: str, answer: bool):
    # ---------- the logic behind -------
    # when i encounter a symbol
    # if i go the left
    # i count the number of ) and ( paranthesis
    # when i encounter an atomic proposition and the diff between ) and ( is 0, then 
    # i put a ( at the left index I stopped
    # i do the same to the right part
    # and put a ) to the right index I stopped
    # by doing these over and over for every symbol i should end up with a strong syntax
    # keep in mind !!!
    # propositional connectives are right associative
    # if I have
    # P -> A -> B in strong syntax should be ( P -> ( A -> B ) )
    # always add the set of paranthesis to the most right symbol
    


    create_proposition(prop)
    global split
    
    def update_right(start: int, action: bool):
        d = {
            '(' : 0,
            ')' : 0
        }
        i = start + 1
        prop_var = 0
        while i < len(split):
            if ( split[i] >= 'A' and split[i] <= 'Z' ) or split[i] in '⊤⊥':
                prop_var = 1
            if split[i] == '(':
                d['('] += 1
            if split[i] == ')':
                d[')'] += 1
            
            if (d[')'] == d['(']) and prop_var:
                try:
                    if split[i + 1] == ')' and action == False: #there's no need to do it again
                        return 0
                except:
                    pass
                split.insert(i + 1, ')')
                break

            i += 1
        return 1

    def update_left(start: int, symb: str, action: bool):
        if symb == 'not' or symb == '¬':
            try:
                if split[start - 1] == '(' and action == False:
                    return 0
            except:
                pass
            split.insert(start, '(')
            return 1
        else:
            
            d = {
            '(' : 0,
            ')' : 0
            }

            i = start - 1
            prop_var = 0
            while i >= 0:

                if ( split[i] >= 'A' and split[i] <= 'Z' ) or split[i] in '⊤⊥':
                    prop_var = 1
                if split[i] == '(':
                    d['('] += 1
                if split[i] == ')':
                    d[')'] += 1
                
                if (d[')'] == d['(']) and prop_var:
                    try:
                        if split[i-1] == '(' and action == False: #no need to add this again
                            return 0
                    except:
                        pass
                    split.insert(i, '(')
                    break

                i -= 1
            return 1
            
            




    for symb in symbol:

        
        if answer == True:
            fout.write(f'{symbol.index(symb) + 1}.Aplying paranthesis to \'{symb}\' symbol\n')

        i = len(split) - 1

        while i >= 0:
            
            # if i have a not, i insert ( before it, and ) using the normal rule above
            if split[i] == symb:
                rez_update = update_left(i, symb, False)
                if rez_update != 1:
                    rez_update = 0
                i += rez_update
                right = update_right(i, False)

                # if one of them is 0 and the other is 1, i need to aply paranthesis
                if rez_update != right:
                    
                    if rez_update == 0:
                        update_left(i, symb, True)
                    if right == 0:
                        update_right(i, True)
                    
                
                if answer == True:
                    fout.write(' '.join(split) + '\n')

            i -= 1
        
        if answer == True:
            fout.write('\n')

    rez = ' '.join(split)
    if answer == True:
        show = 'Strong syntax is: \n' + rez
        fout.write(show + '\n')

    return rez


def relaxed_sense(prop: str, answer: bool):
    fout.write(prop + '\n')
    prop = initialize(prop)
    prop = relaxed_to_strong(prop, answer)
    rez = steps_check_new_wff(prop, answer)
    if rez == False:
        fout.write('This is not a proposition in the relaxed sense\n')
        return None
    else:
        fout.write('This is a proposition in the relaxed sense\n')
        return prop


def value_interpretation_proposition(prop: str, itp: dict, answer: bool):
    
    prop = initialize(prop)

    def give_new_value(change: str):
        change_split = change.split()
        # index
        # normally on index 0 and -1 i have ( and )
        # the connective is usually at index 2, the values at 1 and 3
        # exception, not is at index 1, and the value is 2

        # if i have parathesis in plus
        try:
            if change_split[0] == '(' and (change_split[1] in '01' ) and change_split[2] == ')':
                return change_split[1]
        except:
            pass 
        
        # '¬', '∧', '∨', '⇒' ,'⇔' , '⊨'

        if change_split[1] == 'not' or change_split[1] == '¬':
            # fout.write('I have not')
            connective = change_split[1]
            a = change_split[2]

            # by having not, just negate a
            if a == '0':
                return '1'
            else:
                return '0'    
        else:
            # fout.write(f'I have {change_split[2]}')
            connective = change_split[2]
            a, b = change_split[1], change_split[3]
            
            # and, just return a and b
            if connective == 'and' or connective == '∧':
                if (a == b) and a == '1':
                    return '1'
                else:
                    return '0'

            if connective == 'or' or connective == '∨':
                if (a == '1') or (b == '1'):
                    return '1'
                else:
                    return '0'

            if connective == '=>' or connective == '⇒' or connective == '⊨' or connective == '|=':
                if (a == '1') and (b == '0'):
                    return '0'
                else:
                    return '1'

            if connective == '<=>' or connective == '⇔' or connective == '~' or connective == '∼':
                if a == b:
                    return '1'
                else:
                    return '0' 
            
    
    
    
    
    # change every atomic proposition to it's truth interpretation
    
    itr_prop = prop

    if answer == True or answer == False:

        fout.write('Starting proposition is\n')
        fout.write(itr_prop + '\n')

        fout.write('Interpretation is:\n')

    for key, value in itp.items():

        if answer == True or answer == False:
            fout.write(f'{key} = {value}\n')

        if value == True:
            value = '1'
        else:
            value = '0'

        itr_prop = itr_prop.replace(key, value)
    
    if answer == True:
        fout.write('\n')
    # itr_prop now has 1 where atomic propsitions are True
    # has 0 where atomic propositions are False


    search_patterns = [
        '[(] not [0-1] [)]',
        '[(] [0-1] and [0-1] [)]',
        '[(] [0-1] or [0-1] [)]',
        '[(] [0-1] => [0-1] [)]',
        '[(] [0-1] <=> [0-1] [)]',
        '[(] [0-1] [)]',
        '[(] [0-1] ~ [0-1] [)]',
        '[(] [0-1] [|]= [0-1] [)]',        

        # '¬', '∧', '∨', '⇒' ,'⇔', '∼', '⊨'

        # REGEX HAS ISSUES WITH UNICODE

        # '[(] ¬ [0-1] [)]',
        # '[(] [0-1] ∧ [0-1] [)]',
        # '[(] [0-1] ∨ [0-1] [)]',
        # '[(] [0-1] ⇒ [0-1] [)]',
        # '[(] [0-1] ⇔ [0-1] [)]', 
        # '[(] [0-1] ∼ [0-1] [)]',
        # '[(] [0-1] ⊨ [0-1] [)]',

    ]

    find = 1
    while find == 1:
        find = 0

        total = []
        for s_p in search_patterns:
            pattern = re.compile(s_p)
            rez = pattern.findall(itr_prop)
            total += rez

        for change in total:
            find = 1
            # ------------ requires changes -------------
            new_value = give_new_value(change)

            if answer == True:
                fout.write(f'proposition becomes: {itr_prop}\n')
                fout.write(f'{change} will get evaluated to {new_value}\n')

            itr_prop = itr_prop.replace(change, new_value)

    fout.write(itr_prop + '\n')
    if itr_prop == '0':
        rez = False
    elif itr_prop == '1':
        rez = True
    else:
        rez = None
     
    fout.write(f'Truth value of this interpretation is: {rez}\n')
    fout.write('-' * 60 + '\n')
    fout.write('\n')

    return rez



def value_interpretation_abstract(tree: list, itp: dict, answer: bool):

    fout.write('Starting tree is:\n')
    fout.write(f'{tree}\n')
    fout.write('\n')

    fout.write('Interpretation is:\n')
    for key, value in itp.items():
        fout.write(f'{key} = {value}\n')

    fout.write('\n')

    # transform the current tree with 0 and 1's

    def transform(my_list: list):
        for i in range(len(my_list)):
            if type(my_list[i]) == type([]):
                if len(my_list[i]) == 1:
                    var =  my_list[i][0]
                    my_list[i] = itp[var]
                else:
                    transform(my_list[i])


    def evaluate(my_list: list, original: list):
        a = my_list[0] #connector
        b = my_list[1] #proposition
        c = True
        if a != 'not' and a != '¬':
            c = my_list[2]#proposition


        if type(b) != bool:
            b = evaluate(b, original[1])
            my_list[1] = b
        if type(c) != bool:
            c = evaluate(c, original[2])
            my_list[2] = c
            

        rez = None
        if type(a) == str and type(b) == bool and type(c) == bool:
            # replace this list with a truth value
            # '¬', '∧', '∨', '⇒' ,'⇔', '⊨'

            if a == 'not' or a == '¬':
                rez = not b
            
            if a == 'and' or a == '∧':
                rez = b and c

            if a == 'or' or a == '∨':
                rez = b or c

            if a == '=>' or a == '⇒' or a == '⊨' or a == '|=':
                if b == True and c == False:
                    rez = False
                else:
                    rez = True
            
            if a == '<=>' or a == '⇔' or a == '~' or a == '∼':
                rez = b == c
         
        original = rez
        if answer == True: 
            fout.write(f'Tree becomes {tree}\n')
            fout.write(f'{my_list} gets evaluated to {rez}\n')
            fout.write('\n')
        return rez


    transform(tree)
    
    fout.write('\n')

    final_result = evaluate(tree, tree)
    fout.write(f'Value after interpretation: {final_result}\n')
    return final_result


# here
# way = boolean, True, False
# way = int, 00001111
def give_all_interpretations(variables: int, way: str):
    my_list = [ [] for i in range(variables)]

    unu = 2 ** (variables - 1)
    zero = unu
    p = 1
    for i in range(variables):
        for j in range(unu):
            
            if way == 'int':
                rez = 1
            else:
                rez = True

            my_list[i].append(rez)
        for j in range(zero):

            if way == 'int':
                rez = 0
            else:
                rez = False
            
            my_list[i].append(rez)

        my_list[i] = my_list[i] * p
        
        unu //= 2
        zero //= 2
        p *= 2
        

    return my_list
        

def create_dict_interpretation(prop: str):
    prop = initialize(prop)
    
    result = []
    v = []

    variables = 0
    for char in prop.split(' '):
        if char >= 'A' and char <= 'Z':
            if char not in v:
                variables += 1
                v.append(char)

    itr = give_all_interpretations(variables, 'boolean')

    posibilities = 2 ** variables

    for posib in range(posibilities):
        d = {}
        for i in range(variables):
            key = v[i]
            value = itr[i][posib] 
            d[key] = value
        
        result.append(d)
        # fout.write(d)        

    return result   


def valid_satisfiable_unsatisfiable(prop: str, answer: bool):
    prop = initialize(prop)
    
    
    interpretatinos = create_dict_interpretation(prop)


    truth_values = []
    for inter in interpretatinos:
        val = value_interpretation_proposition(prop, inter, answer)
        truth_values.append(val)

    valid = 1
    unsatisfiable = 1
    satisfiable = 0
    for value in truth_values:
        if value == False:
            valid = 0
        if value == True:
            unsatisfiable = 0

    if valid == 0 and unsatisfiable == 0:
        satisfiable = 1

    fout.write(f'We got {truth_values}\n')
    fout.write('\n')
    fout.write('This proposition is ')
    if valid == 1:
        fout.write('valid')
    elif satisfiable == 1:
        fout.write('satisfiable')
    else:
        fout.write('unsatisfiable')

    fout.write('\n')





def truth_table(prop: str, interpretations=None):
    prop = initialize(prop)
    
    # interpretation is a list, but if i don't receive a specific interpretation, I shall compute all of them

    if interpretations == None:
        make_conclusion = True
    else:
        make_conclusion = False

    atomic = []

    variables = 0
    head = []
    head_in_tree = []
    table = [

    ]   
    def from_list_to_prop(part: list):
        # create a proposition from the abstract tree
        # divide et impera
        conn = part[0]

        rez = ''
        if conn == 'not' or conn == '¬':
            right = part[1]
            if len(right) > 1:
                right = from_list_to_prop(right)
            else:
                right = right[0]

            rez = f'{conn} {right}'
            rez = f'( {rez} )'

        else:
            left = part[1]
            if len(left) > 1:
                left = from_list_to_prop(left)
            else:
                left = left[0]

            right = part[2]
            if len(right) > 1:
                right = from_list_to_prop(right)
            else:
                right = right[0]

            rez = f'{left} {conn} {right}'
            rez = f'( {rez} )'

        # fout.write('This: ', rez)
        head.append(rez)
        return rez
    
    def count_atomic(prop: str):
        for char in prop.split():
            if ( (char >= 'A' and char <= 'Z') or (char in '⊤⊥') ) and (char not in head):
                head.append(char)
                atomic.append(char)
    

    def create_head_in_tree():
        for elem in head:
            copac = []
            create_proposition(elem)
            create_tree(copac, 0, False)
            copac = copac[0]
            head_in_tree.append(copac)

    def design_head():
        for i in range(len(head)):
            if head[i][0] == '(' and head[i][-1] == ')':
                head[i] = head[i][2:]
                head[i] = head[i][:-2]

    def return_value(tree: list, line: int):
        conn = tree[0]


        # '¬', '∧', '∨', '⇒' ,'⇔', '⊨'
        
        if conn == 'not' or conn == '¬':
            right = tree[1]
            # search at what index in head_in_tree, i find right
            index = head_in_tree.index(right)
            
            # get the value from that index
            value_index = line[index]

            # negate the value_index
            value_index = 1 - value_index
            return value_index
        else:
            left = tree[1]
            right = tree[2]

            index_left = head_in_tree.index(left)
            value_left = line[index_left]

            index_right = head_in_tree.index(right)
            value_right = line[index_right]

            if conn == 'and' or conn == '∧':
                if value_left == 1 and value_right == 1:
                    value = 1
                else:
                    value = 0

            if conn == 'or' or conn == '∨':
                if value_left == 1 or value_right == 1:
                    value = 1
                else:
                    value = 0

            if conn == '=>' or conn == '⇒' or conn == '⊨' or conn == '|=':
                if value_left == 1 and value_right == 0:
                    value = 0
                else:
                    value = 1

            if conn == '<=>' or conn == '⇔' or conn == '~' or conn == '∼':
                if value_left == value_right:
                    value = 1
                else:
                    value = 0


            return value

    def calculate_truth_value():
        for itr in interpretations:
            row = []
            for elem in range(len(head)):
                
                if len(head[elem]) == 1:
                    # i'm interested in only atomic prop for now
                   
                    value = itr[ head[elem] ]
                    row.append(value)

                else:
                    value = return_value(head_in_tree[elem], row)
                    row.append(value)
                    pass

            
            table.append(row)
                 
        pass


    def get_all_interpretations():
        k = len(atomic)

        if '⊤' in atomic:
            k -= 1
            atomic.remove('⊤')
            atomic.append('⊤')
        if '⊥' in atomic:
            k -= 1
            atomic.remove('⊥')
            atomic.append('⊥')

        my_list = give_all_interpretations(k, 'int')
        posibilities = 2 ** k
        for posib in range(posibilities):
            d = {}
            for poz in range(k):
                value = my_list[poz][posib]
                key = atomic[poz]
                d[key] = value
            
            if '⊤' in atomic:
                d['⊤'] = 1
            if '⊥' in atomic:
                d['⊥'] = 0

            interpretations.append(d)
            # fout.write(interpretations) 
            

    def conclusion():
        if make_conclusion == False:
            return

        valid = 1
        satisfiable = 0
        for i in range(1, len(table)):
            elem = table[i] 
            val = elem[-1]
            if val == 0:
                valid = 0
            else:
                satisfiable = 1

        if valid == 1:
            fout.write('This is valid')
        elif satisfiable == 1:
            fout.write('This is satisfiable')
        else:
            fout.write('This is not satisfiable')

        fout.write('\n')

    # steps



    # go from relaxed to strong
    prop = relaxed_to_strong(prop, False)

    # verify i have a wff
    wff = new_wff(prop, False)
    if wff == False:
        fout.write('This is not a wff\n')
        return

    # fout.write the prop
    fout.write('Starting proposition is:\n')
    fout.write(prop + '\n')

    fout.write('\n')
    fout.write('Truth table is:\n')


    # append every atomic proposition to head
    count_atomic(prop)

    # create the tree
    create_proposition(prop)
    tree = []
    create_tree(tree, 0, False)
    tree = tree[0]    

    

    # create all propositions from the tree and append them to head
    from_list_to_prop(tree)


    # for every prop in head, save it's abstract syntax in head_in_tree
    create_head_in_tree()
    
    # change head so it's more appealing
    design_head()

    # append the head to table
    table.append(head)


    # if i have no user input for interpretation
    # i shall consider all of them
    if interpretations == None:
        interpretations = []
        get_all_interpretations()



    # calculate every interpretation
    calculate_truth_value()

    # make the truth table
    # grid
    fout.write(tabulate(table, tablefmt='fancy_grid', stralign='center') + '\n')
    
    # valid, satisfiable or not
    conclusion()


    return tabulate(table, tablefmt='grid')

# here
def my_print(string: str):
    fout.write(string)