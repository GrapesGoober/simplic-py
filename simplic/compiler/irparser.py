class SimplicIRParser:
    def from_file(self, filename: str) -> list[tuple]:
        with open(filename, 'r') as file:
            for linenum, line in enumerate(file):
                line = line.split("#")[0].lower()
                if line.strip() == "": continue
                tokens = tokenize_ir(line)

def psuedo_ir_instruction(operator, dest, operand1, operand2):
    if operand1 != None:    print(f'load from {operand1}')
    if operator != None:    print(f'{operator} with {operand2}')
    if dest != None:        print(f'store to {dest}')


import re

# Define regular expression patterns for different components

# function is a func-keyword then funcname followed by optional arguments
func =  r'func\s+(?P<FUNC>[\w.%]+)'
args =  r'\((?P<ARGS>(\s*[\w.%]+\s*,?\s*)*)\)'
funcdef = rf"{func}\s*({args})?\s*"

# label is a label name with colon
label = r'(?P<LABEL>[\w.%]+)\s*:'

# TODO: define return

# parsing operation is finicky
dest =  r'(?P<DEST>[\w.%]+)\s*=\s*'
op =    r'\s*(?P<OP>\+|-|\*|\/|<<|>>|&|\||~)\s*'
var1 =  r'\s*(?P<VAR1>[\w.%]+)\s*'
var2 =  r'\s*(?P<VAR2>[\w.%]+)\s*'
operation = rf"({var1})?({op}{var2})?"

instr = rf'({dest})?({operation})'

pattern = f"\s*(({funcdef})|({label})|({instr}))"

# syntax idea: 
# an IF statement is defined as
# if <cond>, label
# then cond can be defined as
# either    <var> <compare> <var>    or  <var>

print(funcdef)

def tokenize_ir(ir_string):

    # Tokenize the IR string
    print(ir_string, end='')
    match = re.match(pattern, ir_string)
    if match == None: print('cant parse')
    else: print('\t\t', match.groupdict())

SimplicIRParser().from_file("test_codes\\fib.ir")
