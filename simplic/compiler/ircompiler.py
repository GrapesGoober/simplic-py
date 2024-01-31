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
        # 2) operand is a header field of the next frame
        elif operand >= 0: 
            self.asm += self.slide(len(self.alloc) + operand)
            return (len(self.alloc) + operand) % 16
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
                case 'loadm' | 'storem':
                    self.asm += ('load', self.take(tokens[2])), (tokens[0], self.take(tokens[1])),
                case 'set':     
                    self.asm += ('set', self.take(tokens[1]), tokens[2]),
                case 'move':
                    self.asm += ('load', self.take(tokens[2])), ('store', self.take(tokens[1])),
                case 'cmp':
                    self.asm += ('load', self.take(tokens[1])), ('sub', self.take(tokens[2])),
                case _:
                    self.asm += [
                        ('load', self.take(tokens[2])),
                        (tokens[0], self.take(tokens[3])),
                        ('store', self.take(tokens[1])),
                    ]

        return self.asm