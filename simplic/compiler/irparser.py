class SimplicIRParser:
    def from_file(self, filename: str) -> list[tuple]:
        with open(filename, 'r') as file:
            for linenum, line in enumerate(file):
                line = line.split("#")[0].lower()
                if line.strip() == "": continue
                print(list(tokenize_ir(line)))

def psuedo_ir_instruction(operator, dest, operand1, operand2):
    if operand1 != None:    print(f'load from {operand1}')
    if operator != None:    print(f'{operator} with {operand2}')
    if dest != None:        print(f'store to {dest}')


import re

patterns = [
    r'func\s+(?P<FUNC>[\w.%]+)',
    r'if\s+(?P<IF>[\w.%]+\s*(>|<|>=|<=|==|!=)\s*[\w.%]+)',
    r'\((?P<ARGS>(\s*[\w.%]+\s*,?\s*)*)\)',
    r'(?P<LABEL>[\w.%]+)\s*:',
    r'return\s+(?P<RETURN>[\w.%]+)',
    r'(?P<DEST>[\w.%]+)\s*=',
    r'call\s+(?P<CALL>[\w.%]+)',
    r'(?P<OP>\+|-|\*|\/|<<|>>|&|\||~)',
    r'(?P<CMP>>|<|>=|<=|==|!=)',
    r'(?P<OPERAND>[\w.%]+)',
]

goto_pattern = r'(if\s*(?P<COMPARISON>.*))?\s*goto\s*(?P<GOTO>.*)'
return_pattern = r'return\s*(?P<OPERATION>.*)'
instr_pattern = r'((?P<DEST>.*)\s*=\s*)?(?P<OPERATION>.*)'

sample_code = [
    "x = 3",
    "y = 2",
    "ptr a = b + c",
    "goto label",
    "if x > 3 goto label",
    "call somefunc",
    "return x"
]

def tokenize_ir(ir_string: str):
    m = re.match(goto_pattern, ir_string)
    if not m: m = re.match(return_pattern, ir_string)
    if not m: m = re.match(instr_pattern, ir_string)

    if m: return m.groupdict()
    else: return {}
    

for linenum, line in enumerate(sample_code):
    line = line.split("#")[0].lower()
    if line.strip() == "": continue
    print(tokenize_ir(line))