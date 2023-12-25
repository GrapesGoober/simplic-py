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
            ('set',     'k', 'j'),   # variable k should recycle i
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

# capture labels and determine variable live ranges
labels = {}
live_range = {}
for i, tokens in enumerate(code):
    match tokens[0]:
        case 'call': continue
        case 'label': labels[tokens[1]] = i
        case 'if':
            if tokens[2] not in labels: continue
            for v, (start, end) in live_range.items():
                address = labels[tokens[2]]
                if start <= address <= end: live_range[v][1] = i
        case _:
            variables = []
            for var in tokens[1:]:
                if isinstance(var, str):
                    variables.append(var)
            for v in variables:
                if v in live_range: live_range[v][1] = i
                else: live_range[v] = [i, i]

# allocates variables and immediates
alloc = {} # stores the variable mappings
immediates = [] # stores the immediate value mappings
avail = [0] # local variable, stores the current available usage
for i, tokens in enumerate(code):
    # if the current line uses variables, have to allocate/deallocate them
    if tokens[0] in ('call', 'label', 'if'): continue
    for v in tokens[1:]:
        if not isinstance(v, str): continue
        start, end = live_range[v]
        if i == start: # entering lifespan of a variable
            alloc[v] = avail[0]
            if len(avail) == 1: avail[0] += 1
            else: avail.pop(0)
        elif i == end:  # exiting lifespan of a variable
            avail.insert(0, alloc[v])






import json
print(json.dumps(alloc, indent=2))    

for i, tokens in enumerate(code):
    if tokens[0] in ('call', 'label', 'if'): 
        print('---')
        continue
    for v in tokens[1:]:
        if not isinstance(v, str): continue
        print(f"{v} : {alloc[v]}", end='\t')
    print()



