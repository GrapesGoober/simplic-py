from compiler.exceptions import SimplicErr, error_print

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

STACK_OP = ['pop', 'push']

def file_to_file(source: str, destination: str) -> None:
    sasm = SimplicAsm()
    with open(source, 'r') as f: file = list(f)
    try: 
        for linenum, line in enumerate(file):
            sasm.parse_label(line.strip().split('#')[0])
        for linenum, line in enumerate(file):
            sasm.parse_instr(line.strip().split('#')[0])
    except SimplicErr as se:
        error_print(source, linenum, se.message)
        return 
                
    with open(destination, 'w') as f:
        for i, b in enumerate(sasm.bytecodes):
            newline = '\n' if ((i + 1) % 16 == 0) else ''
            f.write(f'{b:02x} {newline}')

class SimplicAsm:
    def __init__(self) -> None:
        self.bytecodes = []
        self.labels = {}
        self.PC = 0

    def parse_label(self, line: str) -> None:
        if ':' in line:
            if line[-1] != ':':
                raise SimplicErr("Expect a line end after colon")
            elif len(line[:-1].split()) != 1:
                raise SimplicErr("Expect only a single label")
            label = line[:-1].split()[0]
            if label in self.labels:  
                raise SimplicErr(f"Duplicate label '{label}'")
            self.labels[label] = self.PC
        elif line:
            opcode = line.split()[0]
            if opcode == ('set' or 'if'):
                self.PC += 3
            else:
                self.PC += 1

    def parse_instr(self, line: str) -> None:
        if not line or ':' in line: return
        tokens = line.split()
        if tokens[0] not in OPCODES:
            raise SimplicErr( f"Invalid opcode '{tokens[0]}'")
        opcode = OPCODES.index(tokens[0])
        operand, immediate = 0, None
        match tokens[0]:
            case 'set':
                if len(tokens) != 3:
                    raise SimplicErr("Expects a variable and a value")
                operand = self.parse_literal(tokens[1], 4)
                immediate = self.parse_literal(tokens[2], 16)
            case 'if':
                if len(tokens) != 3: 
                    raise SimplicErr("Expects only condition and label")
                if tokens[1] not in CONDITIONS:
                    raise SimplicErr(f"Invalid condition '{tokens[1]}'")
                if tokens[2] not in self.labels:
                    raise SimplicErr(f"Undeclared label '{tokens[2]}'")
                operand = CONDITIONS.index(tokens[1]) 
                immediate = self.labels[tokens[2]] 
            case 'stack':
                if len(tokens) != 2: 
                    raise SimplicErr("Expects either 'PUSH' or 'POP'")
                if tokens[1] not in STACK_OP:
                    raise SimplicErr("Expects either 'PUSH' or 'POP'")
                operand = STACK_OP.index(tokens[1])
            case _:
                if len(tokens) != 2: 
                    raise SimplicErr("Expects variable operand")
                operand = self.parse_literal(tokens[1], 4) 

        self.bytecodes.append(opcode << 4 | operand & 0xF)
        if immediate != None:
            self.bytecodes += immediate >> 8, immediate & 0xFF
                    
    def parse_literal(self, token: str, bitsize: int) -> int:
        try:
            if token.startswith("0x"): 
                result = int(token, 16)
            elif token.startswith("0b"): 
                result = int(token, 2)
            else: 
                result = int(token, 10)
        except ValueError:
            raise SimplicErr("Invalid immediate syntax")
        if result.bit_length() > bitsize: 
            raise SimplicErr(f"Immediate value too big for {bitsize} bits.")
        return result
