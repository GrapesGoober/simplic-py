# dynamic jump
# ('set', 'exit', 0xFFFE),
# ('set', 'address', 0),
# ('storem', 'address', 'exit'),


func_main = [
    [
        "result", "number"
    ],
    [
        ('set', 'number', 24),

        # prepare call overhead (return address & function argument)
        ('set',     0, 'func_main.return_0'), 
        ('move',    1, 'number'),
        ('call',    'fib_recursive'), 
        ('label',   'return_0'),

        # recieve return value
        ('move',    'result', 1),

        # halt the program
        ('set', -1, '#halt'),
        ('return',),
    ]
]

fib_iterative = [
    [
        'previous', 'current', 'next', 'counter', 'incr', 'max',
        
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
        ('cmp',     'counter',      'max'),
        ('if', 'less', 'loop'),

        # return the current value
        ('move',    -2, 'current'),
        ('return',)
    ]
]

fib_recursive = [
    [
        'n', 'result', '#i0', '#i1', '#i2', '#i3'
    ],
    [
        ('set',     '#i0', 1),
        ('cmp',     'n', '#i0'),
        ('if', 'more', 'recurse'),
        ('move',    -2, 'n'),
        ('return',),

        ('label', 'recurse'),
        # recursively call fib_recursive(n-1), set to #i2
        ('set',     '#i0', 1),
        ('sub',     '#i1', 'n', '#i0'),
        ('set',     0, 'fib_recursive.return_0'),  
        ('move',    1, '#i1'), 
        ('call',    'fib_recursive'), 
        ('label',   'return_0'),
        ('move',    '#i2', 1),
        # recursively call fib_recursive(n-2), set to #i3
        ('set',     '#i0', 2),
        ('sub',     '#i1', 'n', '#i0'),
        ('set',     0, 'fib_recursive.return_1'),  
        ('move',    1, '#i1'), 
        ('call',    'fib_recursive'), 
        ('label',   'return_1'),
        ('move',    '#i3', 1),

        ('add',     'result', '#i2', '#i3'),
        ('move',    -2, 'result'),
        ('return',)
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