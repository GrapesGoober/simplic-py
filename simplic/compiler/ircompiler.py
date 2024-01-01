IR = {
    "fibbonaci" : [
        [
            'start', 'previous', 'current', 'next', 'counter'
        ],
        [
            ('label', 'start'),
            ('set',     'previous',     1),
            ('set',     'current',      1),
            ('set',     'next',         0),
            ('set',     'counter',      2),
            ('label', 'loop'),
            ('add',     'next',         'previous', 'current'),
            ('set',     'previous',     'current'),
            ('set',     'current',      'next'),
            ('add',     'counter',      'counter', 1),
            ('cmp',     'counter',      24),
            ('if', 'less', 'loop')

            # # memory load IS AN OPERATION, since it can take either stack variable or ANOTHER IMMEDIATE
            # ('loadm', 'b', 'c'),
            # ('storem', 12, 'c')

            # # handling function calls
            # ('setargs', 'a', 'b', 'c'),
            # ('call', 'otherfunc'),
            # ('setret', 'a'),
        ]
    ]
}


class SimplicIR:

    def __init__(self, funcdef: list) -> None:
        self.code = funcdef[1]
        self.asm = []

    def map_variables(self, variables: list):
        self.alloc = {v:i for i, v in enumerate(variables)}
        self.top_of_stack = len(variables) 

    def take_operand(self, token: str, op: str):
        if isinstance(token, str): 
            location = self.alloc[token]
            self.asm.append((op, location))
        elif isinstance(token, int):
            self.asm.append(('set', self.top_of_stack, token))
            self.asm.append((op, self.top_of_stack))

    def set_variable(self, assignee: str, value: any):
        if isinstance(value, str): 
            self.asm.append(('load', self.alloc[value]))
            self.asm.append(('store', self.alloc[assignee]))
        elif isinstance(value, int):
            self.asm.append(('set', self.alloc[assignee], value))

    def compile_function(self, funcname: str) -> None:
        for tokens in self.code:
            match tokens[0]:
                case 'setarg':
                    # prepare call overhead
                    self.asm.append(('---',))
                case 'call':
                    # prepare call overhead
                    self.asm.append(('if', 'always', tokens[1]))
                case 'return':
                    # prepare return overhead
                    self.asm.append(('---',))
                case 'label':
                    self.asm.append(('label', f"{funcname}.{tokens[1]}"))
                case 'if':
                    self.asm.append(('if', tokens[1], f"{funcname}.{tokens[2]}"))
                case 'set':
                    self.set_variable(tokens[1], tokens[2])
                case 'cmp':
                    self.take_operand(tokens[1], 'load')
                    self.take_operand(tokens[2], 'sub')
                case _:
                    self.take_operand(tokens[2], 'load')
                    self.take_operand(tokens[3], tokens[0])
                    self.asm.append(('store', self.alloc[tokens[1]]))

ir = SimplicIR(IR['fibbonaci'])
ir.map_variables(IR['fibbonaci'][0])
ir.compile_function('fibbonaci')

for line in ir.asm:
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


