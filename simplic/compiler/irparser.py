class SimplicIRParser:
    def from_file(self, filename: str) -> list[tuple]:
        with open(filename, 'r') as file:
            for linenum, line in enumerate(file):
                line = line.split("#")[0].lower()
                if line.strip() == "": continue
                print(list(parse_ir(line)))

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

# What should be code output structure? How about tuple (not key-val pairs)?
(
    'INSTR',        # type
    '+',            # operator
    ('PTR', 'a'),   # destination
    ('VAR', 'b'),   # L-operand
    ('IMM', '3'),   # R-operand
)

# IDEA: a 'GOTO' destination specifier? 
(
    '<',            # operator is defaulted to subtract
    ('GOTO', 'a'),  # DEST now uses special conditional GOTO specifier
    ('VAR', 'b'), 
    ('VAR', 'c'), 
)
# This specifier should also not be available for syntax use, using if-goto only
# This technique frees up 'type' field. Is this a good tradeoff?
# In this case, the 'RETURN' would now be unary operator with no DEST field

sample_code = """
    x = 3
    y = 2
    ptr a = b + c
    arg 3 = b + c
    goto loop_point_1
    if x > 3 goto return_point_1
    call somefunc
    return x
"""

def parse_ircode(ircode: str):
    GOTO_PATTERN = r'(?:\s*if\s*(.*))?\s*goto\s*(.*)'
    RETURN_PATTERN = r'return\s*(.*)'
    INSTR_PATTERN = r'(?:(.*)\s*=\s*)?(.*)'

    if m := re.match(GOTO_PATTERN, ircode):
        return 'GOTO',  m.group(2), m.group(1)
    elif m := re.match(RETURN_PATTERN, ircode):
        return 'RETURN', None, m.group(1)
    elif m := re.match(INSTR_PATTERN, ircode):
        if m.group(1) == None: dest = None
        else: dest = parse_dest(m.group(1))
        return 'INSTR',  dest, m.group(2)
    raise Exception("Invalid syntax")

def parse_dest(ircode: str):
    DEST_PATTERN = r'(\w*\s+)?\s*([\w.%]+)'
    if m := re.match(DEST_PATTERN, ircode):
        specifier, identifier = m.groups('')
        specifier = specifier.upper().strip()
        if specifier == '': specifier = 'VAR'

        if specifier not in ('ARG', 'PTR', 'VAR'):
            raise Exception("Invalid destination specifier")
        elif specifier == 'ARG' and not identifier.isdigit():
            raise Exception("Argument destination only accepts numbers")
        elif specifier == 'VAR' and identifier.isdigit():
            raise Exception("Variable destination cannot accept numbers")
        return specifier, identifier
    raise Exception("Invalid destination syntax")

# these two expects different operators!
def parse_arith_expr():
    pass

def parse_cmp_expr():
    pass

for linenum, line in enumerate(sample_code.split('\n')):
    line = line.split("#")[0].lower()
    if line.strip() == "": continue
    print(parse_ircode(line.strip()))