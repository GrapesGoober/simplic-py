from compiler.exceptions import AsmException

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

STACK_OP = ['pop', 'push']

def file_to_file(source: str, dest: str) -> None:
    asm = Assembler()
    with open(source, 'r') as f:
        for line_num, line in enumerate(f):
            # read line and exclude comments
            line = line.lower().strip().split('#')[0]
            cursor = source, line_num
            try: 
                asm.parse_line(line, cursor)
            except AsmException as e: 
                e.print()
                return
    
    try: 
        asm.to_file(dest)
    except AsmException as e: 
        e.print()
        return

class Assembler():
    def __init__(self) -> None:
        self.bytecodes = []
        self.labels = {}
        self.label_points = []

    def parse_line(self, line: str, cursor: tuple = None) -> None:
        if ':' in line: self.parse_label(line, cursor)
        elif line: self.parse_instr(line, cursor)
        else: return

    def parse_label(self, line: str, cursor: tuple = None) -> None:
        if line[-1] != ':':
            raise AsmException("Expect a line to end after colon", cursor)
        elif len(line[:-1].split()) != 1:
            raise AsmException("Expect a only a single label", cursor)
        label = line[:-1].split()[0]
        if label in self.labels:  
            raise AsmException("Duplicate label", cursor)
        self.labels[label] = len(self.bytecodes)

    def parse_instr(self, line: str, cursor: tuple = None):
        tokens = line.split()
        if tokens[0] not in OPCODES:
            raise AsmException("Invalid opcode.", cursor)
        OP  = OPCODES.index(tokens[0])
        
        match tokens[0]:
            case 'set': 
                if len(tokens) != 3:
                    raise AsmException("'SET' expects only variable and value.", cursor)
                I   = self.parse_literal(tokens[1], 4, cursor)
                Imm = self.parse_literal(tokens[2], 16, cursor)
                self.bytecodes.append(f"{OP:x}{I:x}")
                self.bytecodes.append(f"{( Imm >> 8 ):02x}")
                self.bytecodes.append(f"{( Imm & 0xFF ):02x}")

            case 'if': 
                if len(tokens) != 3: 
                    raise AsmException("'IF' expects only condition and label.", cursor)
                if tokens[1] not in CONDITIONS:
                    raise AsmException("Invalid condition.", cursor)
                COND = CONDITIONS.index(tokens[1]) 
                self.bytecodes.append(f"{OP:x}{COND:x}")
                label_point = len(self.bytecodes), tokens[2], cursor
                self.label_points.append(label_point)
                self.bytecodes.append('--')
                self.bytecodes.append('--')

            case 'stack': 
                if len(tokens) != 2: 
                    raise AsmException("'STACK' expects either 'PUSH' or 'POP'.", cursor)
                if tokens[1] not in STACK_OP:
                    raise AsmException("'STACK' expects either 'PUSH' or 'POP'.", cursor)
                m = STACK_OP.index(tokens[1])
                self.bytecodes.append(f"{OP:x}{m:x}")
                
            case _:
                caps = tokens[0].capitalize()
                if len(tokens) != 2: 
                    raise AsmException(f"'{caps}' expects variable index", cursor)
                I = self.parse_literal(tokens[1], 4, cursor) 
                self.bytecodes.append(f"{OP:x}{I:x}")

    def parse_literal(self, token: str, bitsize: int, cursor: tuple = None) -> int:
        try:
            if token.startswith("0x"): 
                result = int(token, 16)
            elif token.startswith("0b"): 
                result = int(token, 2)
            else: 
                result = int(token, 10)
        except ValueError:
            raise AsmException("Invalid immediate syntax.", cursor)

        if result.bit_length() > bitsize: 
            raise AsmException(f"Immediate value too big for {bitsize} bits.", cursor)
        
        return result

    def to_file(self, dest: str) -> None:
        for i, label, cursor in self.label_points:
            if label not in self.labels: 
                raise AsmException("Unknown label", cursor)
            address = self.labels[label]
            self.bytecodes[i] = f'{(address >> 8):02x}'
            self.bytecodes[i + 1] = f'{(address & 0xFF):02x}'

        max_width, width = 16, 0
        with open(dest, 'w') as f:
            for b in self.bytecodes:
                f.write(b + ' ')
                width += 1
                if width == max_width:
                    width = 0
                    f.write('\n')