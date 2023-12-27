IR = {
    "fibbonaci" : [
        [
            'a', 'b', 'c'
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
        self.args = funcdef[0]
        self.code = funcdef[1]
        self.alloc = {v:i for i, v in enumerate(self.args)}
        self.top_of_stack = len(self.args) 
        self.asm = []

    def get_alloc_mapping(self, variable: str):
        if variable not in self.alloc:
            self.alloc[variable] = self.top_of_stack
            self.top_of_stack += 1
        return self.alloc[variable]

    def take_operand(self, token: str, op: str):
        if isinstance(token, str): 
            location = self.get_alloc_mapping(token)
            self.asm.append((op, location))
        elif isinstance(token, int):
            self.asm.append(('set', self.top_of_stack, token))
            self.asm.append((op, self.top_of_stack))

    def set_variable(self, assignee: str, value: any):
        if isinstance(value, str): 
            self.asm.append(('load', self.get_alloc_mapping(value)))
            self.asm.append(('store', self.get_alloc_mapping(assignee)))
        elif isinstance(value, int):
            self.asm.append(('set', self.get_alloc_mapping(assignee), value))

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
                    self.asm.append(('store', self.get_alloc_mapping(tokens[1])))

ir = SimplicIR(IR['fibbonaci'])
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


