from exceptions import AsmException, file_error_print

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

def file_to_file(source: str, dest: str) -> None:
    asm = Assembler()
    with open(source, 'r') as f:
        for line_num, line in enumerate(f):
            # read line and exclude comments
            line = line.lower().strip().split('#')[0]
            
            try: 
               asm.parse_line(line)
            except AsmException as e:
                file_error_print(source, line_num, e.message)
    
    try: 
        asm.to_file(dest)
    except AsmException as e:
        # There might need to be a stronger error handling system than this
        # currently there isn't a mechanism to show the current linenum when trying to assemble
        file_error_print(source, 0, e.message)

class Assembler():
    def __init__(self) -> None:
        self.bytecodes = []
        self.labels = {}
        self.label_points = []

    def parse_line(self, line: str) -> None:
        if ':' in line: self.parse_label(line)
        elif line: self.parse_instr(line)
        else: return

    def parse_label(self, line: str) -> None:
        if line[-1] != ':':
            raise AsmException("Expect a line to end after colon")
        elif line[:-1].split() != 1:
            raise AsmException("Expect a only a single label")
        label = line[:-1].split()[0]
        if label in self.labels:  
            raise AsmException("Duplicate label")
        self.labels[label] = len(self.bytecodes) - 1

    def parse_instr(self, line: str):
        tokens = line.split()
        match tokens[0]:
            case 'set': 
                if len(tokens) != 3:
                    raise AsmException("'SET' expects only 2 operands: variable and value.")
                _, var, val = tokens

            case 'if': 
                if len(tokens) != 3: 
                    raise AsmException("'IF' expects only 2 operands: condition and label.")

            case 'stack': 
                if len(tokens) != 2: 
                    raise AsmException("'STACK' expects only 1 operand: either 'PUSH' or 'POP'.")
                
            case _:
                pass

    def parse_literal(token: str, bitsize: int) -> int:
        try:
            if token.startswith("0x"): 
                result = int(token, 16)
            elif token.startswith("0b"): 
                result = int(token, 2)
            else: 
                result = int(token, 10)
        except ValueError:
            raise AsmException("Invalid immediate syntax.")

        if result.bit_length() < bitsize: 
            raise AsmException(f"Immediate value too big for {bitsize} bits.")
        
        return result

    # Need a stronger exception handling, 
    # currently the linenum is lost; it cannot be passed along to the exception to be pretty printed
    def to_file(self, dest: str) -> None:
        for i, label in self.label_points:
            if label not in self.labels: 
                raise AsmException("Unknown label")
            address = self.labels[label] - 1
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