class SimplicIR:

    def __init__(self, ircode: list, name: str) -> None:
        self.name = name
        self.code = ircode[1]
        self.asm = []
        self.current_window = 0
        self.alloc = {v:i+1 for i, v in enumerate(ircode[0])}
        self.alloc['#return_ptr'] = 0
    
    def get_alloc(self, variable) -> int:
        return self.alloc[variable] % 16
    
    def slide_to(self, variable) -> list[tuple[str]]:
        window_offset = self.alloc[variable] // 16 - self.current_window
        self.current_window += window_offset
        if window_offset < 0:
            return [('stack', 'pop')] * -window_offset
        elif window_offset > 0:
            return [('stack', 'push')] * window_offset
        else: return []
    
    def take_var(self, op: str, variable: str) -> list[tuple[str]]:
        return self.slide_to(variable) + [(op, self.get_alloc(variable))]

    def compile(self) -> list[tuple[str]]:
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
                    var, value = tokens[1:]
                    self.asm += self.slide_to(var) + [('set', self.get_alloc(var), value)]
                case 'move':
                    dest, src = tokens[1:]
                    self.asm += self.take_var('load', src) + self.take_var('store', dest)
                case 'cmp':
                    a, b = tokens[1:]
                    self.asm += self.take_var('load', a) + self.take_var('sub', b)
                case _:
                    opcode, dest, a, b = tokens
                    self.asm += self.take_var('load', a) + self.take_var(opcode, b)
                    self.asm += self.take_var('store', dest)

        return self.asm
