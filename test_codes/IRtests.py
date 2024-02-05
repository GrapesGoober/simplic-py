# dynamic jump
# ('set', 'exit', 0xFFFE),
# ('set', 'address', 0),
# ('storem', 'address', 'exit'),


func_main = [
    [
        "result", "number"
    ],
    [
        ('label', 'func_main'),
        ('set', 'number', 24),

        # prepare call overhead (return address & function argument)
        ('set',     0, 'func_main.return_0'), 
        ('move',    1, 'number'),
        ('call',    'fib_recursive'), 
        ('label',   'func_main.return_0'),

        # recieve return value
        ('move',    'result', 1),

        # halt the program
        ('set', -1, '%halt'),
        ('return',),
    ]
]

fib_iterative = [
    [
        'previous', 'current', 'next', 'counter', 'incr', 'max',
        
    ],
    [
        ('label', "fib_iterative"),
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
        ('cmp',     'counter',      'max'),
        ('if', 'less', 'loop'),

        # return the current value
        ('move',    -2, 'current'),
        ('return',)
    ]
]

fib_recursive = [
    [
        'n', 'result', r'%i0', r'%i1', r'%i2', r'%i3'
    ],
    [
        ('label', "fib_recursive"),
        ('set',     r'%i0', 1),
        ('cmp',     'n', r'%i0'),
        ('if', 'more', 'fib_recursive.recurse'),
        ('move',    -2, 'n'),
        ('return',),

        ('label', 'fib_recursive.recurse'),
        # recursively call fib_recursive(n-1), set to #i2
        ('set',     r'%i0', 1),
        ('sub',     r'%i1', 'n', r'%i0'),
        ('set',     0, 'fib_recursive.return_0'),  
        ('move',    1, r'%i1'), 
        ('call',    'fib_recursive'), 
        ('label',   'fib_recursive.return_0'),
        ('move',    r'%i2', 1),
        # recursively call fib_recursive(n-2), set to #i3
        ('set',     r'%i0', 2),
        ('sub',     r'%i1', 'n', r'%i0'),
        ('set',     0, 'fib_recursive.return_1'),  
        ('move',    1, r'%i1'), 
        ('call',    'fib_recursive'), 
        ('label',   'fib_recursive.return_1'),
        ('move',    r'%i3', 1),

        ('add',     'result', r'%i2', r'%i3'),
        ('move',    -2, 'result'),
        ('return',)
    ]
]


add_til_ten = [
    [
        "arg", "result", "ten", "step"
    ],
    [
        ('label', "add_til_ten"),
        ("set",         "ten", 10),
        ("cmp",         "arg", "ten"),
        ("if", "less", "add_til_ten.recurse"),
        ('move',         -2, 'arg'),                # simply return the argument
        ("return",),

        ("label", "add_til_ten.recurse"),
        ("set",         "step", 1),
        ("add",         "result", "arg", "step"),
        ('set',         0, 'add_til_ten.return_0'), # assign return address
        ('move',        1, 'result'),               # argument
        ('call',        'add_til_ten'),             # call the function
        ('label',       'add_til_ten.return_0'),    # determine return address
        ('move',        -2, 1),                     # return the result of the recursive call

        ("return",)
    ]
]