class SimplicIR:

    def __init__(self, ircode: list, name: str) -> None:
        self.alloc = {v:i+1 for i, v in enumerate(ircode[0])}
        self.name = name
        self.code = ircode[1]
        self.asm = [('label', self.name)]
        self.current_window = 0
        self.return_count = 0
    
    # Get variable allocation relative to window
    def get_alloc(self, var: str) -> int:
        return self.alloc[var] % 16
    
    # Slide current window to the target variable location
    def slide(self, location: str) -> list[tuple[str]]:
        delta = location // 16 - self.current_window
        self.current_window += delta
        if   delta < 0: return [('stack', 'pop')] * -delta
        elif delta > 0: return [('stack', 'push')] * delta
        else:           return []
    
    def instr(self, op: str, var: str, imm: any = None) -> list[tuple[str]]:
        if imm != None: return self.slide(self.alloc[var]) + [(op, self.get_alloc(var), imm)]
        else:           return self.slide(self.alloc[var]) + [(op, self.get_alloc(var))]
    
    def instr_arg(self, op: str, offset: int, imm: any = None) -> list[tuple[str]]:
        yield self.slide(len(self.alloc) + (offset + 1))
        if imm != None: yield (op, (offset + 1) % 16, imm),
        else:           yield (op, (offset + 1) % 16),
    
    # Compile entire IR code to ASM
    def compile(self) -> list[tuple[str]]:
        for tokens in self.code:
            match tokens[0]:
                case 'setargs': 
                    for i, arg in enumerate(tokens[1:]):
                        self.asm += self.instr('load', arg) + self.instr_arg('store', i)
                case 'setrets': 
                    for i, ret in enumerate(tokens[1:]):
                        self.asm += self.instr_arg('load', i) + self.instr('store', ret)
                case 'call':    
                    return_label = f"{self.name}.return_{self.return_count}"
                    self.asm += self.instr_arg('set', -1, return_label)
                    self.asm += ('if', 'always', tokens[1]), ('label', return_label)
                    self.return_count += 1
                case 'return':  
                    for i, ret in enumerate(tokens[1:]):
                        self.asm += self.instr('load', ret)
                        self.asm += self.instr('store', list(self.alloc)[i])
                    self.asm += self.slide(0) + [('load', 0), ('set', 0, 0), ('storem', 0)]
                case 'loadm' | 'storem':
                    self.asm += self.instr('load', tokens[2])
                    self.asm += self.instr(tokens[0], tokens[1])
                case 'label':
                    self.asm += ('label', f"{self.name}.{tokens[1]}"),
                case 'if':
                    self.asm += ('if', tokens[1], f"{self.name}.{tokens[2]}"),
                case 'set':     
                    self.asm += self.instr('set', tokens[1], tokens[2])
                case 'move':
                    self.asm += self.instr('load', tokens[2]) + self.instr('store', tokens[1])
                case 'cmp':
                    self.asm += self.instr('load', tokens[1]) + self.instr('sub', tokens[2])
                case _:
                    self.asm += self.instr('load', tokens[2])
                    self.asm += self.instr(tokens[0], tokens[3])
                    self.asm += self.instr('store', tokens[1])

        return self.asm