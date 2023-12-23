IR = {
    "myfunc" : {
        "return" : "r",
        "args": [
            "a", "b", "c", "d" 
        ],
        "body": {
            "start" : [
                # IR should seemlessly handle 
                # - immediate operands
                # - single assignment with multiple operations
                # - recognizing variable lifetimes
                # - variables that are used consecutively are checked

                # ( (assignee), op,  (operands) )
                (('var', 'y'), 'set', (3,)),        # direct assignment (using set instruction)
                (('var', 'y'), 'set', ('a',)),      # moving assignment
                (('var', 'y'), 'mul', ('a', 'b')),  # ALU opcodes add sub lsl lsr mul div and or not
                (('var', 'y'), 'add', ('y', 3)),    #   handle immediate values as well

                (('var', 'y'), 'mem', ('c',)),      # memory load
                (('var', 'y'), 'mem', (0x20,)),     #   handle immediate values as well
                (('mem', 'c'), 'mem', ('b',)),      # memory store using memory load
                (('mem', 420), 'set', (3,)),        # can index using immediate

                (('var', 'y'), 'call', ('funcname', 'a', 'b')),
                ((None, None), 'call', ('funcname2',)),

                ((None, None), 'if', ('less', 'label')),
            ]
        }
    }
}

code = [
    (('var', 'prev'),   'set', (1,)),
    (('var', 'curr'),   'set', (1,)),
    (('var', 'next'),   'set', (0,)),
    (('var', 'cntr'),   'set', (2,)),
    (('var', 'incr'),   'set', (1,)),
    (('var', 'max'),    'set', (25,)),

    (('var', 'next'),   'add', ('prev', 'curr')),
    (('var', 'prev'),   'set', ('curr',)),
    (('var', 'curr'),   'set', ('next',)),
    (('var', 'cntr'),   'add', ('cntr', 'incr')),
    ((None, None),      'sub', ('cntr', 'max')),
    ((None, None),      'if', ('less', 'loop')),
]

lifetimes = {}
for i, (assignee, op, operands) in enumerate(code):
    variables = []
    if isinstance(assignee[1], str):
        variables.append(assignee[1])
    if op == 'call': operands = operands[1:]
    for operand in operands:
        if isinstance(operand, str):
            variables.append(operand)
    for v in variables:
        if v in lifetimes: lifetimes[v][1] = i
        else: lifetimes[v] = [i, i]

alloc = {}
avail = [0]
for t in range(10):
    for v, (start, end) in lifetimes.items():
        if t == start: # entering lifespan of a variable
            alloc[v] = avail[0]
            if len(avail) == 1: avail[0] += 1
            else: avail.pop(0)
        elif t == end + 1:  # exiting lifespan of a variable
            avail.insert(0, alloc[v])
            alloc.pop(v)
        if v in alloc:
            print(f'{v}:{alloc[v]}\t\t', end='')
        else: print('\t\t', end='')
    print()
