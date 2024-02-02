fibbonaci = [
    [
        'previous', 'current', 'next', 'counter', 'incr', 'max',

        "exit", "address",

        "7", "8", "9", "A", "B", "C", "D", 'E', "F", "11", '12',
        "X", "Y", 
        
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

        # halt condition
        ('set', 'exit', 0xFFFE),
        ('set', 'address', 0),
        ('storem', 'address', 'exit'),

        # ('loadm', 'b', 'c'),
        # ('storem', 12, 'c')

        # # handling function calls
        # ('setargs', 'a', 'b', 'c'),
        # ('call', 'otherfunc'),
        # ('setrets', 'a'),

        # dynamic jump
        # ('set', 'exit', 0xFFFE),
        # ('set', 'address', 0),
        # ('storem', 'address', 'exit'),
    ]
]

add_til_ten = [
    [
        "arg", "result", "ten", "step"
    ],
    [
        ("set",         "ten", 10),
        ("cmp",         "arg", "ten"),
        ("if", "less", "recurse"),
        ('move',         -2, 'arg'),                # simply return the argument
        ("return",),

        ("label", "recurse"),
        ("set",         "step", 1),
        ("add",         "result", "arg", "step"),
        ('set',         0, 'add_til_ten.return_0'), # assign return address
        ('move',        1, 'result'),               # argument
        ('call',        'add_til_ten'),             # call the function
        ('label',       'return_0'),                # determine return address
        ('move',        -2, 1),                     # return the result of the recursive call

        ("return",)
    ]
]

func_main = [
    [
        "result", "number"
    ],
    [
        ('set', 'number', 3),

        # prepare call overhead (return address & function argument)
        ('set',     0, 'func_main.return_0'),  # assign return address
        ('move',    1, 'number'),    # argument
        ('call',    'add_til_ten'), # call the function
        ('label',   'return_0'),     # determine return address

        # recieve return value
        ('move',    'result', 1),

        # halt the program
        ('set', -1, '#halt'),
        ('return',),
    ]
]

func_add_ten = [
    [
        "arg", "ten", "result"
    ],
    [
        ('set',     'ten', 10),
        ('add',     'result', 'arg', 'ten'),
        ('move',    -2, 'result'),    # set return value
        ('return',),
    ]
]