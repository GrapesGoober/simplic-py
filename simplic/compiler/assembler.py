import re

class Assembler:
    def __init__(self) -> None:
        self.opcodes = [
            "set",  "if", "stack", "load", "store", "loadm", "storem",  
            "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
        ]
        self.conditions = [
            "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
        ]
        self.source = ""
        self.bytecodes = []
        self.labels = {}
        self.label_points = []

    def load(self, source: str) -> None:
        self.source = source
        with open(source, 'r') as f:
            for line_num, line in enumerate(f):
                # read line and exclude comments
                line = line.lower().strip().split('#')[0]
                if not line: continue
                status = self.parse_line(line)
                if status:
                    self.print_error(line_num, status)
                    return
        for i, label in self.label_points:
            address = self.labels[label] - 1
            self.bytecodes[i] = f'{(address >> 8):02x}'
            self.bytecodes[i+1] = f'{(address & 0xFF):02x}'

    def store(self, dest: str) -> None:
        max_width, width = 16, 0
        with open(dest, 'w') as f:
            for b in self.bytecodes:
                f.write(b + ' ')
                width += 1
                if width == max_width:
                    width = 0
                    f.write('\n')

    def parse_line(self, line: str) -> str:

        word, comma = r'(\w+)\s*', r',\s*'

        label = re.match(f'^{word}:$', line)
        instr = re.match(f'^{word}{word}(?:{comma}{word})?$', line)

        if label:
            l = label.group(1)
            if l in self.labels: return f"Duplicate label '{l}'"
            self.labels[l] = len(self.bytecodes)
        elif instr:
            opcode, var, imm = instr.groups()
            
            if opcode == "set":
                if imm is None: return "Expect an immediate"

                opcode = self.opcodes.index(opcode)
                var = self.parse_literal(var)
                imm = self.parse_literal(imm)
                self.bytecodes.append(f'{opcode:x}{var:x}')
                self.bytecodes.append(f'{(imm >> 8):02x}')
                self.bytecodes.append(f'{(imm & 0xFF):02x}')

            elif opcode == "if":
                if imm is None: return "Expect a label"
                self.label_points.append((len(self.bytecodes)+1, imm))
                opcode = self.opcodes.index(opcode)
                var = self.conditions.index(var)
                self.bytecodes.append(f'{opcode:x}{var:x}')
                self.bytecodes.append('--')
                self.bytecodes.append('--')

            elif opcode == "stack":
                if imm is not None: return "Unexpected token"
                opcode = self.opcodes.index(opcode)
                var = ['pop', 'push'].index(opcode)
                self.bytecodes.append(f'{opcode:x}{var:x}')

            elif opcode in self.opcodes:
                if imm is not None: return "Unexpected token"
                opcode = self.opcodes.index(opcode)
                var = self.parse_literal(var)
                self.bytecodes.append(f'{opcode:x}{var:x}')

            else: return "Invalid opcode"


        else: "Invalid syntax"
        
    def print_error(self, line_num, message):
        err_string = "\n"
        with open(self.source, 'r') as f:
            for i, line in enumerate(f):
                if line_num - 3 < i < line_num + 2: 
                    err_string += f"  {i+1}:\t{line}"
        print(err_string, f"Error at line {line_num + 1}:", message)

    def parse_literal(self, token: str) -> int:
        BITSIZE = 16
        try:
            if token.startswith("0x"): 
                result = int(token, 16)
            elif token.startswith("0b"): 
                result = int(token, 2)
            else: 
                result = int(token, 10)
        except ValueError:
            raise Exception(f"Invalid immediate syntax.")

        assert result.bit_length() < BITSIZE, "Immediate value too big for {BITSIZE} bits."
        return result
