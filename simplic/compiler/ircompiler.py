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
            ('add',     'j', 'b', 3),
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
            for tok, (start, end) in live_range.items():
                address = labels[tokens[2]]
                if start <= address <= end: live_range[tok][1] = i
        case _:
            variables = [v for v in tokens[1:] if isinstance(v, str)]
            for tok in variables:
                if tok in live_range: live_range[tok][1] = i
                else: live_range[tok] = [i, i]

# allocates variables and immediates
alloc = {} # stores the variable mappings
immediates = [] # stores the immediate value mappings
avail = [0] # local variable, stores the current available usage
for i, tokens in enumerate(code):
    # if the current line uses variables, have to allocate/deallocate them
    if tokens[0] in ('call', 'label', 'if'): continue
    for tok in tokens[1:]:
        # using variable: allocate variable locations onto frame
        if isinstance(tok, str):
            start, end = live_range[tok]
            if i == start: # entering lifespan of a variable
                alloc[tok] = avail[0]
                if len(avail) == 1: avail[0] += 1
                else: avail.pop(0)
            elif i == end:  # exiting lifespan of a variable
                avail.insert(0, alloc[tok])
        # using immediate: allocate immediate values onto frame
        elif isinstance(tok, int):
            immediates += avail[0],

# print(f"{tok} : {alloc[tokens[1]]}", end='\t')

# Translate
parent_funcname = 'func'
asm = []
for i, tokens in enumerate(code):
    tokenstring = " ".join([str(t) for t in tokens])
    asm.append((f'# {str(tokenstring)}',))
    match tokens[0]:
        case 'setarg':
            # prepare call overhead
            asm.append(('---',))
        case 'call':
            # prepare call overhead
            asm.append(('if', 'always', tokens[1]))
        case 'return':
            # prepare return overhead
            asm.append(('---',))
        case 'label':
            asm.append(('label', f"func.{tokens[1]}"))
        case 'if':
            asm.append(('if', tokens[1], f"func.{tokens[2]}"))
        case 'set':
            if isinstance(tokens[2], str): 
                asm.append(('load', alloc[tokens[2]]))
                asm.append(('store', alloc[tokens[1]]))
            elif isinstance(tokens[2], int):
                asm.append(('set', alloc[tokens[1]], tokens[2]))
                immediates.pop(0)
        case 'cmp':
            op = tokens[0]

            if isinstance(tokens[1], str): 
                asm.append(('load', alloc[tokens[1]]))
            elif isinstance(tokens[2], int):
                asm.append(('set', immediates[0], tokens[2]))
                asm.append(('load', immediates[0]))
                immediates.pop(0)

            if isinstance(tokens[2], str): 
                asm.append((op, alloc[tokens[2]]))
            elif isinstance(tokens[2], int):
                asm.append(('set', immediates[0], tokens[2]))
                asm.append((op, immediates[0]))
                immediates.pop(0)

        case _:
            op = tokens[0]

            if isinstance(tokens[2], str): 
                asm.append(('load', alloc[tokens[2]]))
            elif isinstance(tokens[2], int):
                asm.append(('set', immediates[0], tokens[2]))
                asm.append(('load', immediates[0]))
                immediates.pop(0)

            if isinstance(tokens[3], str): 
                asm.append((op, alloc[tokens[3]]))
            elif isinstance(tokens[3], int):
                asm.append(('set', immediates[0], tokens[3]))
                asm.append((op, immediates[0]))
                immediates.pop(0)

            asm.append(('store', alloc[tokens[1]]))
            
                

for line in asm:
    for tok in line:
        print(tok, end='\t')
    print()


# for i, tokens in enumerate(code):
#     print(f"{tokens[0]},\t", end='')
#     if tokens[0] in ('call', 'label', 'if'): 
#         print('---')
#         continue
#     for tok in tokens[1:]:
#         if isinstance(tok, str): 
#             print(f"{tok} : {alloc[tok]}", end='\t')
#         elif isinstance(tok, int):
#             print(f"{tok} : {immediates[0]}", end='\t')
#             immediates.pop(0)
#     print()


