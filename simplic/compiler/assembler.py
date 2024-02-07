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

    def compile(self, asmcodes: list[str]) -> Iterator[int]:
        # count the PC address to build label table
        for self.iter, line in enumerate(asmcodes):
            line = line.split("#")[0]
            if line.strip() == "": continue
            tokens = self.tokenize(line.lower())
            self.build_label_table(tokens)
            
        # with a label table, now compile the assembly
        for self.iter, line in enumerate(asmcodes):
            line = line.split("#")[0]
            if line.strip() == "": continue
            tokens = self.tokenize(line.lower())
            if tokens['LABEL']: continue
            yield from self.compile_instr(tokens)

    # iterates over each asm line and construct labels dict
    def build_label_table(self, tokens: dict[str, str]):
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

    # generator function to compile to bytecodes
    def compile_instr(self, tokens: dict[str, str]) -> Iterator[int]:
        
        # checks and parse opcode and operand then yield the bytecode
        if tokens['OPCODE'] not in OPCODES: 
            raise SimplicErr(f"Invalid opcode '{tokens['OPCODE']}'")
        opcode = OPCODES.index(tokens['OPCODE'])
        if tokens['OPERAND'] == None: 
            raise SimplicErr(f"Expects an operand")
        operand = self.parse_operand(tokens['OPERAND'])
        yield opcode << 4 | operand & 0xF 

        # handle case of immediate value
        if tokens['OPCODE'] in ('if', 'set'):
            if tokens['IMMEDIATE'] == None:
                raise SimplicErr(f"Expects an immediate value")
            immediate = self.parse_operand(tokens['IMMEDIATE'])
            yield ( immediate >> 8 )    & 0xFF
            yield   immediate           & 0xFF
        elif tokens['IMMEDIATE'] != None:
            raise SimplicErr(f"Unexpected immediate value")

    # use regex to tokenize a line of asm code
    def tokenize(self, line) -> dict[str, str]:
        # Define the regular expression patterns
        label = r'(?P<LABEL>[\w.%]*)\s*:'
        instr = r'(?P<OPCODE>\w+)\s+(?P<OPERAND>\w+)(?:\s*,\s*(?P<IMMEDIATE>[\w.%]++))?'
        pattern = rf'\s*(({label})|({instr}))'

        # Match to assembly to tokenize
        re_match = re.match(pattern, line)
        if re_match:    return re_match.groupdict()
        else:           raise SimplicErr("Invalid syntax; cannot parse")

    # parses a token operand
    def parse_operand(self, tok: str) -> int:
        if tok in CONDITIONS:       return CONDITIONS.index(tok)
        elif tok in STACK_OP:       return STACK_OP.index(tok)
        elif tok in self.labels:    return self.labels[tok]
        elif tok.startswith("0x"):  return int(tok, 16)  & 0xFFFF
        elif tok.startswith("0b"):  return int(tok, 2)   & 0xFFFF
        elif tok.isdigit():         return int(tok, 10)  & 0xFFFF
        else:                       raise SimplicErr(f"Invalid operand '{tok}'")
        
    # compiles to bytecodes and writes to hexfile
    def compile_to_hexfile(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for i, b in enumerate(self.old_compile()):
                newline = '\n' if ((i + 1) % 16 == 0) else ''
                f.write(f'{b:02x} {newline}')
