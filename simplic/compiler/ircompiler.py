class SimplicIR:

    def __init__(self, ircode: list, name: str) -> None:
        self.alloc = {v:i+1 for i, v in enumerate(ircode[0])}
        self.name = name
        self.code = ircode[1]
        self.asm = []
        self.current_window = 0
        self.return_count = 0
    
    def get_alloc(self, variable) -> int:
        return self.alloc[variable] % 16
    
    def slide_to(self, variable) -> list[tuple[str]]:
        distance = self.alloc[variable] // 16 - self.current_window
        self.current_window += distance
        if distance < 0:
            return [('stack', 'pop')] * -distance
        elif distance > 0:
            return [('stack', 'push')] * distance
        else: return []
    
    def slide_to_new(self, offset) -> list[tuple[str]]:
        offset_slide = [('stack', 'push')] * (offset // 16 + 1)
        return self.slide_to(self.alloc.keys()[-1]) + offset_slide
    
    def take_var(self, op: str, variable: str) -> list[tuple[str]]:
        return self.slide_to(variable) + [(op, self.get_alloc(variable))]

    def compile(self) -> list[tuple[str]]:
        for tokens in self.code:
            match tokens[0]:
                case 'setargs':
                    for i, arg in enumerate(tokens[1:]):
                        self.asm += self.take_var('load', arg)
                        self.asm += self.slide_to_new(i) + ('store', i % 16 + 1),
                case 'setrets':
                    for i, arg in enumerate(tokens[1:]):
                        self.asm += self.take_var('load', arg)
                        self.asm += self.slide_to_new(i) + ('store', i % 16 + 1),
                case 'call':
                    return_label = f"{self.name}.ret{self.return_count}"
                    self.asm += self.slide_to_new(0)
                    self.asm += ('set', 0, return_label),
                    self.asm += ('if', 'always', tokens[1]),
                    self.asm += ('label', return_label),
                    self.return_count += 1
                case 'return':
                    # prepare return overhead
                    # load return value, set to return location
                    # load return address, set to PC
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
