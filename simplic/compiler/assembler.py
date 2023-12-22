from compiler.exceptions import SimplicErr, error_print

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

STACK_OP = ['pop', 'push']

# These two will use parse_label and parse_instr to build this intermediate representation
# however, the 'from_list' will not populate 'source' and 'linenum'
def file_to_file(source: str, destination: str) -> None:
    sasm = SimplicAsm()
    with open(source, 'r') as f:
        sasm.load(list(f))
        try:
            sasm.compile()
        except SimplicErr as se:
            error_print(source, sasm.linenum, se.message)
    [print(i) for i in sasm.bytecodes]

class SimplicAsm:
    def __init__(self) -> None:
        self.bytecodes = []
        self.labels = {}
        self.linenum = 0
        self.asm = []
    
    def load(self, asm: list[str]) -> None:
        self.asm = asm

    def compile(self) -> None:
        while self.asm:
            line = self.asm[0].strip().split('#')[0]
            if ':' in line:
                self.compile_label(line)
            elif line:
                self.compile_instr(line)

            self.asm.pop(0)
            self.linenum += 1

    def compile_label(self, line: str) -> None:
        if line[-1] != ':':
            raise SimplicErr("Expect a line end after colon")
        elif len(line[:-1].split()) != 1:
            raise SimplicErr("Expect only a single label")
        label = line[:-1].split()[0]
        if label in self.labels:  
            raise SimplicErr(f"Duplicate label '{label}'")
        self.labels[label] = len(self.bytecodes)

    def compile_instr(self, line: str) -> None:
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
                self.bytecodes.append(f'{opcode:x}{operand:x}')
                self.bytecodes.append(f'{( immediate >> 8 ):02x}')    
                self.bytecodes.append(f'{( immediate & 0xFF ):02x}')    
            case 'if':
                if len(tokens) != 3: 
                    raise SimplicErr("Expects only condition and label")
                if tokens[1] not in CONDITIONS:
                    raise SimplicErr(f"Invalid condition '{tokens[1]}'")
                operand = CONDITIONS.index(tokens[1]) 
                self.bytecodes.append(f'{opcode:x}{operand:x}')
                if tokens[2] not in self.labels:
                    index = len(self.bytecodes)
                    self.bytecodes.append('')    
                    self.bytecodes.append('')
                    self.compile()
                    if tokens[2] not in self.labels:
                        raise SimplicErr(f"Undeclared label '{tokens[2]}'")
                    immediate = self.labels[tokens[2]]
                    self.bytecodes[index] = f'{( immediate >> 8 ):02x}'    
                    self.bytecodes[index + 1] = f'{( immediate & 0xFF ):02x}'    
                else:
                    immediate = self.labels[tokens[2]]
                    self.bytecodes.append(f'{( immediate >> 8 ):02x}')    
                    self.bytecodes.append(f'{( immediate & 0xFF ):02x}')  

            case 'stack':
                if len(tokens) != 2: 
                    raise SimplicErr("Expects either 'PUSH' or 'POP'")
                if tokens[1] not in STACK_OP:
                    raise SimplicErr("Expects either 'PUSH' or 'POP'")
                operand = STACK_OP.index(tokens[1])
                self.bytecodes.append(f'{opcode:x}{operand:x}')
            case _:
                if len(tokens) != 2: 
                    raise SimplicErr("Expects variable operand")
                operand = self.parse_literal(tokens[1], 4) 
                self.bytecodes.append(f'{opcode:x}{operand:x}') 
            
                    
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

# this function compiles to destination
# if the source and linenum is set, will print error message and exit
# otherwise, raise exception
def parse(asm: list[str], destination: str) -> tuple[bool, str, int]:
    bytecodes = []
    for tokens, line_num in asm['code']:
        status, codes = parse_instr(tokens, asm['labels'])
        if not status:
            return status, codes, line_num
        bytecodes += codes

    max_width, width = 16, 0
    with open(destination, 'w') as f:
        for b in bytecodes:
            f.write(b + ' ')
            width += 1
            if width == max_width:
                width = 0
                f.write('\n')
    return True, '', None



