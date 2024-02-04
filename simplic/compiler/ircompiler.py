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
                    self.to_asm('load', tokens[2])
                    self.to_asm(tokens[0], tokens[1])
                case 'set':     
                    self.to_asm('set', tokens[1], tokens[2])
                case 'move': 
                    # self.to_asm(('load', tokens[2]), ('store', tokens[1]))
                    self.to_asm('load', tokens[2])
                    self.to_asm('store', tokens[1])
                case 'cmp':
                    self.to_asm('load', tokens[1])
                    self.to_asm('sub', tokens[2])
                case _:
                    if tokens[2] != None: # in case of unary op, ignore operand
                        self.to_asm('load', tokens[2])
                    self.to_asm(tokens[0], tokens[3])
                    self.to_asm('store', tokens[1])
        
                    # self.to_asm((tokens[0], tokens[3]), ('store', tokens[1]))
        return self.asm

    # resolve variable address and write assembly code to self.asm
    def to_asm(self, opcode: str, operand: str|int, imm: str|int = None):

        # handle 3 separate operand cases
        if isinstance(operand, str):  
            location = self.alloc[operand]
        elif operand < 0: 
            location = (-operand - 1)
        elif operand >= 0: 
            fresh_window = len(self.alloc) // 16 + 1
            location = fresh_window * 16 + operand
        
        # slide window to target location
        delta = location // 16 - self.current_window
        self.current_window += delta
        if   delta < 0: self.asm += [('stack', 'pop')] * -delta
        elif delta > 0: self.asm += [('stack', 'push')] * delta

        # append to assembly code
        if imm == None: self.asm += (opcode, location % 16),
        else: self.asm += (opcode, location % 16, imm),
