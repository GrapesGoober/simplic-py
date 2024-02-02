from simplic.compiler.exceptions import SimplicErr

OPCODES = [
    "load", "store", "loadm", "storem", "add", "sub", "lsl", "lsr",
    "mul", "div", "and", "or", "not", "stack", "set", "if"
]

CONDITIONS = [
    "always", "less", "more", "equal", "nequal", "eqless", "eqmore"
]

STACK_OP = ['pop', 'push']

class SimplicAsm:
    def __init__(self) -> None:
        self.asm = []
        self.bytecodes = []
        self.labels = {'#halt': 0xFFFE}
        self.PC = 0
        self.iter = 0

    # load ASM from file
    def from_file(self, filename: str) -> None:
        with open(filename, 'r') as f: 
            for self.iter, line in enumerate(f):
                tokens = line.strip().split('#')[0].split()
                self.asm.append(tokens)
        self.from_list(self.asm)

    # load ASM from list
    def from_list(self, asm: list) -> None:
        self.asm = asm
        for self.iter, tokens in enumerate(self.asm):
            if not tokens: continue
            match tokens[0]:
                case 'label':
                    label, = self.get_operands(tokens, 1)
                    if label in self.labels:  
                        raise SimplicErr(f"Duplicate label '{label}'")
                    if label in OPCODES + CONDITIONS + STACK_OP:
                        raise SimplicErr(f"Cannot use reserved keyword as label")
                    self.labels[label] = self.PC - 1
                case 'if' | 'set':  self.PC += 3
                case _:             self.PC += 1

    # compile current ASM to hex file
    def compile(self) -> list[int]:
        for self.iter, tokens in enumerate(self.asm):
            if not tokens or tokens[0] == 'label': continue
            self.bytecodes += self.parse_instr(tokens)
        return self.bytecodes
    
    def to_hexfile(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for i, b in enumerate(self.bytecodes):
                newline = '\n' if ((i + 1) % 16 == 0) else ''
                f.write(f'{b:02x} {newline}')
                
    # parse current opcode & instruction
    def parse_instr(self, tokens: list[str]):
        if tokens[0] not in OPCODES:
            raise SimplicErr( f"Invalid opcode '{tokens[0]}'")
        opcode = OPCODES.index(tokens[0])
        match tokens[0]:
            case 'set' | 'if':
                operand, immediate = self.parse_operands(tokens, 2)
                yield opcode << 4 | operand & 0xF
                yield ( immediate >> 8 )    & 0xFF
                yield   immediate           & 0xFF
            case _:
                operand, = self.parse_operands(tokens, 1)
                yield opcode << 4 | operand & 0xF

    # parses operands from tokens list
    def parse_operands(self, tokens: list[str], count: int):
        for _, tok in enumerate(self.get_operands(tokens, count)):
            if tok in CONDITIONS:           yield CONDITIONS.index(tokens[1])
            elif tok in STACK_OP:           yield STACK_OP.index(tokens[1])
            elif tok in self.labels:        yield self.labels[tok]
            else:
                if isinstance(tok, int):    yield tok
                elif tok.startswith("0x"):  yield int(tok, 16)
                elif tok.startswith("0b"):  yield int(tok, 2)
                elif tok.isdigit():         yield int(tok, 10)
                else: raise SimplicErr(f"Invalid token '{tok}'")
                    

    # tokenizes operands from tokens list, does invalid cases check
    def get_operands(self, tokens: list[str], count: int):
        if len(tokens[1:]) > count:
            raise SimplicErr(f"Unexpected token '{tokens[count]}'")
        if len(tokens[1:]) < count:
            raise SimplicErr(f"Expected {count} operands")
        return tokens[1:]

    
