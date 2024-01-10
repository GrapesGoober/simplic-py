fibbonaci = [
    [
        'previous', 'current', 'next', 'counter', 'incr', 'max'

        ,"7", "8", "9", "A", "B", "C", "D", 'E', "F", "11", '12',
        "X", "Y"
    ],
    [
        ('label', 'start'),
        ('set',     'previous',     1),
        ('set',     'current',      1),
        ('set',     'next',         0),
        ('set',     'counter',      2),
        ('set',     'incr',         1),
        ('set',     'max',          24),
        ('label', 'loop'),
        ('add',     'next',         'previous', 'current'),
        ('move',    'previous',     'current'),
        ('move',    'current',      'next'),
        ('add',     'counter',      'counter', 'incr'),
        
        # some rando assignment junk to test the variables X Y
        ('move',    'X',            'counter'),
        ('add',     'Y',            'Y', 'X'),

        ('cmp',     'counter',      'max'),
        ('if', 'less', 'loop'),

        # assign X Y to E F
        ('move',    'D',            'X'),
        ('move',    'E',            'Y'),

        # ('loadm', 'b', 'c'),
        # ('storem', 12, 'c')

        # # handling function calls
        # ('setargs', 'a', 'b', 'c'),
        # ('call', 'otherfunc'),
        # ('setrets', 'a'),
    ]
]

add_til_ten = [
    [
        "arg", "result", "ten", "step"
    ],
    [
        ("set", "ten", 10),
        ("set", "step", 1),
        ("cmp", "arg", "ten"),
        ("if", "less", "recurse"),
        ("return", "arg"),
        ("label", "recurse"),
        ("add", "result", "arg", "step"),
        ("setargs", "result"),
        ("call", "add_till_ten"),
        ("setrets", "result"),
        ("return", "result")
    ]
]