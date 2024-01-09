class SimplicIR:

    def __init__(self, ircode: list, name: str) -> None:
        self.name = name
        self.code = ircode[1]
        self.asm = []
        self.current_window = 0
        self.alloc = {v:i+1 for i, v in enumerate(ircode[0])}
        self.alloc['#return_ptr'] = 0
    
    def get_var(self, variable):
        window_offset = self.alloc[variable] // 16 - self.current_window
        self.current_window += window_offset
        if window_offset < 0:
            [ self.asm.append( ('stack', 'pop') ) for i in range(-window_offset) ]
        elif window_offset > 0:
            [ self.asm.append( ('stack', 'push') ) for i in range(window_offset) ]
        return self.alloc[variable] % 16

    def compile(self) -> None:
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
                    self.asm.append(('label', f"{self.name}.{tokens[1]}"))
                case 'if':
                    self.asm.append(('if', tokens[1], f"{self.name}.{tokens[2]}"))
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
