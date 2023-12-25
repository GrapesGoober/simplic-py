IR = {
    "somefunc" : [
        [
            "x", "y", "z"
        ],
        [
            ('label',   'start'),
            ('set',     'a', 0),
            ('set',     'b', 1),
            ('label',   'loop'),
            ('add',     'a', 'a', 1),
            ('set',     'i', 2),
            ('add',     'j', 'b', 'a'),
            ('add',     'a', 'j', 'i'),
            ('cmp',     'a', 20),
            ('if',      'less', 'loop'),
            ('return',  'b'),

            # memory load IS AN OPERATION, since it can take either stack variable or ANOTHER IMMEDIATE
            # ('loadm', 'b', 'c'),
            # ('storem', 12, 'c')

            # ('setarg', 'a', 'b', 'c'),
            # ('call', 'otherfunc')
        ]
    ]
}

code = IR['somefunc'][1]

labels = {}
lifetimes = {}
for i, tokens in enumerate(code):
    match tokens[0]:
        case 'call': continue
        case 'label':
            labels[tokens[1]] = i
        case 'if':
            if tokens[2] in labels:
                for v, (start, end) in lifetimes.items():
                    address = labels[tokens[2]]
                    if start <= address <= end: lifetimes[v][1] = i
        case _:
            variables = []
            for var in tokens[1:]:
                if isinstance(var, str):
                    variables.append(var)
            for v in variables:
                if v in lifetimes: lifetimes[v][1] = i
                else: lifetimes[v] = [i, i]


alloc = {}
avail = [0]
for i in range(len(code)):
    print(f'{i}\t', end='')
    for v, (start, end) in lifetimes.items():
        if i == start: # entering lifespan of a variable
            alloc[v] = avail[0]
            if len(avail) == 1: avail[0] += 1
            else: avail.pop(0)
        elif i == end + 1:  # exiting lifespan of a variable
            avail.insert(0, alloc[v])
            alloc.pop(v)

        if v in alloc:
            print(f'{v}:{alloc[v]}\t', end='')
        else: print('\t', end='')
    print()
