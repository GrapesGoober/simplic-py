IR = {
    "fibbonaci" : [
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
            # ('setret', 'a'),
        ]
    ]
}


class SimplicIR:

    def __init__(self, funcdef: list) -> None:
        self.code = funcdef[1]
        self.asm = []
        self.current_window = 0

    def map_variables(self, variables: list):
        self.alloc = {v:i+1 for i, v in enumerate(variables)}
        self.alloc['#return_ptr'] = 0
    
    def get_var(self, variable):
        window_offset = self.alloc[variable] // 16 - self.current_window
        self.current_window += window_offset
        if window_offset < 0:
            [ self.asm.append( ('stack', 'pop') ) for i in range(-window_offset) ]
        elif window_offset > 0:
            [ self.asm.append( ('stack', 'push') ) for i in range(window_offset) ]
        return self.alloc[variable] % 16

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
                    self.asm.append(('set', self.get_var(tokens[1]), tokens[2]))
                case 'move':
                    self.asm.append(('load', self.get_var(tokens[2])))
                    self.asm.append(('store', self.get_var(tokens[1])))
                case 'cmp':
                    self.asm.append(('load', self.get_var(tokens[1])))
                    self.asm.append(('sub', self.get_var(tokens[2])))
                case _:
                    self.asm.append(('load', self.get_var(tokens[2])))
                    self.asm.append((tokens[0], self.get_var(tokens[3])))
                    self.asm.append(('store', self.get_var(tokens[1])))

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


