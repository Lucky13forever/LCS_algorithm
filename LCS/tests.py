unu = '( ( P and Q ) => ( not R ) )'

doi = '( ( ( P and Q ) and ( B and C ) ) => ( not R ) )'

a = '( ( ( P => Q ) or S ) <=> T )'

b = '( ( P => ( Q and ( S => T ) ) ) )'

c = '( not ( B ( not Q ) ) and R )'

d = '( P and ( ( not Q ) and ( not ( not ( Q <=> ( not R ) ) ) ) ) )'

e = '( ( P or Q ) => not ( P or Q ) ) and ( P or ( not ( not Q ) ) )'

f = 'P and Q'

g = '( P'

h = '( not A B )'

i = '( R => ( A and B ) ) )'

# relaxed strings 

j = 'P and Q => not B or G'
j_strong = '( ( P and Q ) => ( ( not B ) or G ) )'
# '( ( P and Q ) => ( ( not B ) or G ) )'

hw_5_ex_1_a = 'P and Q => R not B or G'

hw_5_ex_1_b = 'P => not not not not not B <=> Q and S'


homework_5 = {
    'SUP' : '( ( A and B ) => C ) and ( not A => D ) and ( not B => E ) and not C and ( F => ( not D and not E ) )',
    '1_a)' : 'P and Q => R not B or G',
    '1_b)' : 'P => not not not not not B <=> Q and S',
    '3_a)' : '( ( ( P => Q ) or S ) <=> T )',
    '3_b)' : '( ( P => ( Q and ( S => T ) ) ) )',
    '3_c)' : '( not ( B ( not Q ) ) and R)',
    '3_d)' : '( ( P => Q ) and ( ( not Q ) and P ) )',
    '3_e)' : '( ( P => Q ) => ( Q => P ) )',
    '3_f)' : '( ( not ( P or Q ) ) and ( not Q ) )',
    '4_a)' : '( P => Q ) and not Q and not P',
    '4_b)' : '( P => Q ) => ( ( Q => S ) => ( ( P or Q ) => R ) )',
    '4_c)' : 'not ( P => Q ) <=> ( ( P or R ) and ( not P => Q ) )',
    '4_d)' : '( P <=> Q ) <=> ( not ( P => not Q ) )'
}


#  bottom:   '_|_'

#  top:   '‾|‾'

homework_6 = {

    'True and False' : {
        'a)' : 'not ‾|‾ ~ _|_' 
    },
    'Reduction Laws' : {
        'a)' : '¬ F',
    }

}


# '¬', '∧', '∨', '⇒' ,'⇔'