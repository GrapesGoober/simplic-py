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

goto_pattern = r'(if\s*(?P<COMPARISON>.*))?\s*goto\s*(?P<GOTO>.*)'
return_pattern = r'return\s*(?P<OPERATION>.*)'
instr_pattern = r'((?P<DEST>.*)\s*=\s*)?(?P<OPERATION>.*)'

# What should be code output structure? How about tuple (not key-val pairs)?
(
    ('var', 'a'), # destination
    (   # operation
        ('var', 'b'),
        ('+'),
        ('var', 'c'),
    )
)

sample_code = [
    "x = 3",
    "y = 2",
    "ptr a = b + c",
    "arg 3 = b + c",
    "goto label",
    "if x > 3 goto label",
    "call somefunc",
    "return x"
]

def parse_ir(ircode: str):
    m = re.match(goto_pattern, ircode)
    if not m: m = re.match(return_pattern, ircode)
    if not m: m = re.match(instr_pattern, ircode)

    m = m.groupdict()
    if 'DEST' in m and m['DEST']:
        m['DEST'] = parse_dest(m['DEST'])

    if m: return m
    else: return {}

# NOTE: using named captures & groupdict is funky
# might be better to do case-by-case, and name the DEST TYPE as tuples
# ex: ('VAR': 'x')  ('PTR', '3')
dest_pattern = [
    (r'arg\s*([\w.%]+)', 'ARG'),
    (r'ptr\s*([\w.%]+)', 'PTR'),
    (r'([\w.%]+)', 'VAR')
]

dest_pattern = r'(?P<SPECIFIER>\w*)\s*(?P<ADDRESS>[\w.%]+)'

def parse_dest(dest_str: str):

    m = re.match(dest_pattern, dest_str)
    if not m:
        raise Exception("Invalid destination syntax")
    m = m.groupdict()

    match m['SPECIFIER'].upper():
        case 'ARG':
            if not m['ADDRESS'].isdigit():
                raise Exception("Argument specifier only accepts numbers")
            return m
        case 'PTR': 
            return m
        case '':
            if m['ADDRESS'].isdigit():
                raise Exception("Cannot assign values to number") 
            return m
        case _:
            raise Exception("Invalid specifier") 
    

for linenum, line in enumerate(sample_code):
    line = line.split("#")[0].lower()
    if line.strip() == "": continue
    print(parse_ir(line))