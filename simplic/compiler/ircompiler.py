class SimplicIR:

    def __init__(self, ircode: list, name: str) -> None:
        self.alloc = {v:i+1 for i, v in enumerate(ircode[0])}
        self.name = name
        self.ircode = ircode[1]
        self.asm = [('label', self.name)]
        self.current_window = 0
    
    # Slide current window to the target variable location
    def slide(self, location: str) -> list[tuple[str]]:
        delta = location // 16 - self.current_window
        self.current_window += delta
        if   delta < 0: return [('stack', 'pop')] * -delta
        elif delta > 0: return [('stack', 'push')] * delta
        else:           return []
    
    # Slide window and returns the allocation for variables or frame headers
    def take(self, operand: int | str) -> int:
        # handle 3 seperate cases, 
        # 1) operand is variable
        if isinstance(operand, str):  
            self.asm += self.slide(self.alloc[operand])
            return self.alloc[operand] % 16
        # 2) operand is overhead of the next frame
        elif operand >= 0: 
            # TODO: the bug with "args" is to slide to fresh window
            # slide to a fresh widow and offset from there
            self.asm += self.slide((len(self.alloc) // 16 + 1) * 16 + operand)
            return operand % 16
        # 3) operand is an negative (header value or absolute address)
        elif operand < 0: 
            self.asm += self.slide(-operand - 1)
            return (-operand - 1) % 16
    
    # Compile entire IR code to ASM
    def compile(self) -> list[tuple[str]]:
        for tokens in self.ircode:
            match tokens[0]:
                case 'label':
                    self.asm += ('label', f"{self.name}.{tokens[1]}"),
                case 'if':
                    self.asm += ('if', tokens[1], f"{self.name}.{tokens[2]}"),
                case 'call':
                    # TODO: the bug with "call" is to slide to fresh window
                    # OLD CODE: self.asm += self.slide(len(self.alloc) + 16)
                    self.asm += self.slide((len(self.alloc) // 16 + 1) * 16)
                    self.asm += ('if', 'always', tokens[1]),
                case 'return':
                    self.asm += self.slide(0)
                    # this uses dynamic jumping to return, which requires a -1 offset
                    self.asm += ('load', 0), ('set', 0, 1), ('sub', 0), ('set', 0, 0), ('storem', 0)
                    # alternative is to have a buffer instruction in the middle (say, null instruction) 
                    # or modify VM to not do *PC += 1
                case 'loadm' | 'storem':
                    self.asm += ('load', self.take(tokens[2])), 
                    self.asm += (tokens[0], self.take(tokens[1])),
                case 'set':     
                    self.asm += ('set', self.take(tokens[1]), tokens[2]),
                case 'move':
                    self.asm += ('load', self.take(tokens[2])), 
                    self.asm += ('store', self.take(tokens[1])),
                case 'cmp':
                    self.asm += ('load', self.take(tokens[1])), 
                    self.asm += ('sub', self.take(tokens[2])),
                case _:
                    self.asm += ('load', self.take(tokens[2])),
                    self.asm += (tokens[0], self.take(tokens[3])),
                    self.asm += ('store', self.take(tokens[1])),

        return self.asm