from simplic.compiler.exceptions import SimplicErr
from typing import Iterator 
import re

OPCODES = [
    "load", "store", "loadm", "storem", "add", "sub", "lsl", "lsr",
    "mul", "div", "and", "or", "not", "stack", "set", "if"
]

CONDITIONS = [
    "always", "less", "more", "equal", "nequal", "eqless", "eqmore"
]

STACK_OP = ['pop', 'push']

class SimplicAsm:
    labels, iter, label_PC = {r'%halt': 0xFFFE}, 0, 0

    # Iterator function to tokenize each line of asm using regex
    def tokenize(self, asmcodes: list[str]) -> Iterator[dict]:
        # Define the regular expression patterns
        label = r'(?P<LABEL>[\w.%]*)\s*:'
        instr = r'(?P<OPCODE>\w+)\s+(?P<OPERAND>\w+)'
        imm16 = r'(?:\s*,\s*(?P<IMMEDIATE>[\w.%]+))?'
        pattern = rf'\s*(({label})|({instr}{imm16}))'

        for self.iter, line in enumerate(asmcodes):
            line = line.split("#")[0].lower()
            if line.strip() == "": continue
            
            # Tokenize using regex
            re_match = re.match(pattern, line)
            if re_match:    yield re_match.groupdict()
            else:           raise SimplicErr("Invalid syntax; cannot parse")

    # Iterator function to compile asmcodes to bytecodes
    def compile(self, asmcodes: Iterator[str]) -> Iterator[int]:
        asmcodes = list(asmcodes)
        # count the PC address to build label table
        for tokens in self.tokenize(asmcodes):
            self.build_label_table(tokens)
            
        # with a label table, now compile the assembly
        for tokens in self.tokenize(asmcodes):
            if tokens['LABEL']: continue
            yield from self.compile_instr(tokens)

    # scan the code to construct the label table
    def build_label_table(self, tokens: dict[str, str]) -> None:
        label, opcode = tokens['LABEL'], tokens['OPCODE']
        if label != None:
            if label in self.labels:  
                raise SimplicErr(f"Duplicate label '{label}'")
            if label in OPCODES + CONDITIONS + STACK_OP:
                raise SimplicErr(f"Cannot use reserved keyword as label")
            self.labels[label] = (self.label_PC - 1) & 0xFFFF
        elif opcode in ('if', 'set'): 
            self.label_PC += 3
        else: self.label_PC += 1

    # generator function to compile a single asm line to bytecodes
    def compile_instr(self, tokens: dict[str, str]) -> Iterator[int]:
        # parse opcode and operand to yield the first bytecode
        if tokens['OPCODE'] not in OPCODES: 
            raise SimplicErr(f"Invalid opcode '{tokens['OPCODE']}'")
        opcode = OPCODES.index(tokens['OPCODE'])
        if tokens['OPERAND'] == None: 
            raise SimplicErr(f"Expects an operand")
        operand = self.parse_operand(tokens['OPERAND'])
        yield opcode << 4 | operand & 0xF 

        # handle case of optional immediate value
        if tokens['OPCODE'] in ('if', 'set'):
            if tokens['IMMEDIATE'] == None:
                raise SimplicErr(f"Expects an immediate value")
            immediate = self.parse_operand(tokens['IMMEDIATE'])
            yield ( immediate >> 8 )    & 0xFF
            yield   immediate           & 0xFF
        elif tokens['IMMEDIATE'] != None:
            raise SimplicErr(f"Unexpected immediate value")

    # parses a token operand to integer value
    def parse_operand(self, tok: str) -> int:
        if tok in CONDITIONS:       return CONDITIONS.index(tok)
        elif tok in STACK_OP:       return STACK_OP.index(tok)
        elif tok in self.labels:    return self.labels[tok]
        elif tok.startswith("0x"):  return int(tok, 16)  & 0xFFFF
        elif tok.startswith("0b"):  return int(tok, 2)   & 0xFFFF
        elif tok.isdigit():         return int(tok, 10)  & 0xFFFF
        else:                       raise SimplicErr(f"Invalid operand '{tok}'")

