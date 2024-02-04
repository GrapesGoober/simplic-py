# TODO: Check for valid opcodes
# TODO: Handle "NOT" unary instruction
ARITHMATIC_OPCODES = [
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

class SimplicIR:

    def __init__(self, alloc: list, ircode: list) -> None:
        self.alloc = {v:i+1 for i, v in enumerate(alloc)}
        self.ircode, self.asm = ircode, []
        self.current_window = 0
    
    # Compile the IR code to ASM
    def compile(self) -> list[tuple[str]]:
        for tokens in self.ircode:
            match tokens[0]:
                case 'call':
                    self.asm += ('if', 'always', tokens[1]),
                case 'return':
                    self.asm += ('load', 0), ('set', 0, 0), ('storem', 0),
                case 'label':
                    self.asm += ('label', tokens[1]),
                case 'if':
                    self.asm += ('if', tokens[1], tokens[2]),
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

    # TODO: implement a "instr" function? where it slides the variables and append to asm for us
    # the idea is to reduce the clutter of "self.asm += " and the trailing colon "," readability problem

    # TODO: merge the slide function with take function, into a "slide_and_alloc"
    # Slide current window to the target variable location
    def slide(self, location: str) -> list[tuple[str]]:
        delta = location // 16 - self.current_window
        self.current_window += delta
        if   delta < 0: return [('stack', 'pop')] * -delta
        elif delta > 0: return [('stack', 'push')] * delta
        else:           return []
    
    # Slide window and returns the allocation for variables or frame headers
    def take(self, operand: int | str) -> int:
        if isinstance(operand, str):  
            self.asm += self.slide(self.alloc[operand])
            return self.alloc[operand] % 16
        elif operand >= 0: 
            fresh_window = len(self.alloc) // 16 + 1
            self.asm += self.slide(fresh_window * 16 + operand)
            return operand % 16
        elif operand < 0: 
            self.asm += self.slide(-operand - 1)
            return (-operand - 1) % 16
