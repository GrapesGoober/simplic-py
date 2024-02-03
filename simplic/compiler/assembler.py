from simplic.compiler.exceptions import SimplicErr
from typing import Iterator

OPCODES = [
    "load", "store", "loadm", "storem", "add", "sub", "lsl", "lsr",
    "mul", "div", "and", "or", "not", "stack", "set", "if"
]

CONDITIONS = [
    "always", "less", "more", "equal", "nequal", "eqless", "eqmore"
]

STACK_OP = ['pop', 'push']

class SimplicAsm:
    asmcodes, labels = [], {'#halt': 0xFFFE}

    # loads assembly codes from tokens list and assign label addresses
    def from_list(self, asmcodes: list[tuple]) -> None:
        self.asmcodes, label_PC = asmcodes, 0
        for self.iter, tokens in enumerate(self.asmcodes):
            if not tokens: continue
            match tokens[0]:
                case 'label':
                    label, = self.get_operands(tokens, 1)
                    if label in self.labels:  
                        raise SimplicErr(f"Duplicate label '{label}'")
                    if label in OPCODES + CONDITIONS + STACK_OP:
                        raise SimplicErr(f"Cannot use reserved keyword as label")
                    self.labels[label] = (label_PC - 1) & 0xFFFF
                case 'if' | 'set':  label_PC += 3
                case _:             label_PC += 1

    # loads assembly codes from file and assign label addresses
    def from_file(self, filename: str) -> None:
        with open(filename, 'r') as f: 
            for line in f:
                tokens = []
                for tok in line.strip().split('#')[0].split():
                    if tok.startswith("0x"):    tokens += int(tok, 16),
                    elif tok.startswith("0b"):  tokens += int(tok, 2),
                    elif tok.isdigit():         tokens += int(tok, 10),
                self.asmcodes += tuple(tokens),
        self.from_list(self, self.asmcodes)

    # generator function to compile to bytecodes
    def compile(self) -> Iterator[int]:
        for self.iter, tokens in enumerate(self.asmcodes):
            if not tokens or tokens[0] == 'label': continue
            if tokens[0] not in OPCODES:
                raise SimplicErr(f"Invalid opcode '{tokens[0]}'")
            opcode = OPCODES.index(tokens[0])
            match tokens[0]:
                case 'set' | 'if': # these two instructions need 16-bit immediate
                    operand, immediate = self.parse_operands(tokens, count=2)
                    yield opcode << 4 | operand & 0xF
                    yield ( immediate >> 8 )    & 0xFF
                    yield   immediate           & 0xFF
                case _:
                    operand, = self.parse_operands(tokens, count=1)
                    yield opcode << 4 | operand & 0xF
        
    # compiles to bytecodes and writes to hexfile
    def compile_to_hexfile(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for i, b in enumerate(self.compile()):
                newline = '\n' if ((i + 1) % 16 == 0) else ''
                f.write(f'{b:02x} {newline}')

    # helper function to tokenize operands from tokens with expected token count
    def get_operands(self, tokens: tuple, count: int) -> tuple[str]:
        if len(tokens[1:]) > count:
            raise SimplicErr(f"Unexpected operand '{tokens[count]}'")
        if len(tokens[1:]) < count:
            raise SimplicErr(f"Expected {count} operands")
        return tokens[1:]
    
    # helper generator function to parse operands from tokens list
    def parse_operands(self, tokens: tuple, count: int) -> Iterator[int]:
        for opr in self.get_operands(tokens, count):
            if opr in CONDITIONS:       yield CONDITIONS.index(opr)
            elif opr in STACK_OP:       yield STACK_OP.index(opr)
            elif opr in self.labels:    yield self.labels[opr]
            elif isinstance(opr, int):  yield opr
            else: raise SimplicErr(f"Invalid operand '{opr}'")