from simplic.compiler.exceptions import SimplicErr, error_print

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "more", "equal", "nequal", "eqless", "eqmore"
]

STACK_OP = ['pop', 'push']

class SimplicAsm:
    def __init__(self) -> None:
        self.asm = []
        self.bytecodes = []
        self.labels = {}
        self.PC = 0
        self.iter = 0

    def from_file(self, filename: str):
        with open(filename, 'r') as f: 
            for self.iter, line in enumerate(f):
                tokens = line.strip().split('#')[0].split()
                self.asm.append(tokens)
        self.from_list(self.asm)

    def from_list(self, asm: list):
        self.asm = asm
        for self.iter, tokens in enumerate(self.asm):
            if not tokens: continue
            match tokens[0]:
                case 'label':
                    label, = self.get_operands(tokens, 1)
                    if label in self.labels:  
                        raise SimplicErr(f"Duplicate label '{label}'")
                    self.labels[label] = self.PC
                    self.asm[self.iter] = [] # remove labels from asm list
                case 'if' | 'set':
                    self.PC += 3
                case _:
                    self.PC += 1

    def compile(self, filename: str):
        for self.iter, tokens in enumerate(self.asm):
            if not tokens: continue
            self.bytecodes += self.parse_instr(tokens)
        with open(filename, 'w') as f:
            for i, b in enumerate(self.bytecodes):
                newline = '\n' if ((i + 1) % 16 == 0) else ''
                f.write(f'{b:02x} {newline}')

    # get operands and check for operand count
    def get_operands(self, tokens: list[str], count: int) -> list[str]:
        if len(tokens[1:]) > count:
            raise SimplicErr(f"Unexpected token '{tokens[count]}'")
        if len(tokens[1:]) < count:
            raise SimplicErr(f"Expected {count} operands")
        return tokens[1:]

    def parse_instr(self, tokens: list[str]) -> list[int]:
        if tokens[0] not in OPCODES:
            raise SimplicErr( f"Invalid opcode '{tokens[0]}'")
        opcode = OPCODES.index(tokens[0])
        operand, immediate = 0, None
        match tokens[0]:
            case 'set':
                operand, immediate = self.get_operands(tokens, 2)
                operand = self.parse_literal(tokens[1], 4)
                immediate = self.parse_literal(tokens[2], 16)
            case 'if':
                operand, immediate = self.get_operands(tokens, 2)
                if operand not in CONDITIONS:
                    raise SimplicErr(f"Invalid condition {operand}")
                operand = CONDITIONS.index(tokens[1]) 
                immediate = self.labels[tokens[2]] 
            case 'stack':
                operand = self.get_operands(tokens, 1)
                if operand not in STACK_OP:
                    raise SimplicErr(f"Invalid stack operation {operand}")
                operand = STACK_OP.index(tokens[1])
            case _:
                operand = self.get_operands(tokens, 1)
                operand = self.parse_literal(tokens[1], 4) 

        ret = [opcode << 4 | operand & 0xF]
        if immediate != None: ret += immediate >> 8, immediate & 0xFF
        return ret
                    
    def parse_literal(self, token: str, bitsize: int) -> int:
        try:
            if token.startswith("0x"): 
                result = int(token, 16)
            elif token.startswith("0b"): 
                result = int(token, 2)
            else: 
                result = int(token, 10)
        except ValueError:
            raise SimplicErr("Invalid literal syntax")
        if result.bit_length() > bitsize: 
            raise SimplicErr(f"Literal value too big for {bitsize} bits.")
        return result
