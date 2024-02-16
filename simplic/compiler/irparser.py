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

# syntax idea: 
# an IF statement is defined as
# if <cond>, label
# then cond can be defined as
# either    <var> <compare> <var>    or  <var>

# try experimenting unnamed capture group
word = r'\s*([\w.%]+)\s*'
args = r'\(%s(?:,%s)*,?\)' % (word, word)

patterns = [
    ("FUNC",    r'func\s+([\w.%]+)'),
    ("ARGS",    r'\(((\s*[\w.%]+\s*,?\s*)*)\)'),
    ("LABEL",    r'([\w.%]+)\s*:'),
    ("FUNC",    r'return\s+([\w.%]+)'),
    ("FUNC",    r'([\w.%]+)\s*='),
    ("FUNC",    r'call\s+([\w.%]+)'),
    ("FUNC",    r'(\+|-|\*|\/|<<|>>|&|\||~)'),
    ("FUNC",    r'(>|<|>=|<=|==|!=)'),
    ("FUNC",    r'([\w.%]+)'),
]
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

# we have 2 unparsed subtokens: IF's comparison and ARGS items
# [('IF', 'n > %i0'), ('OPERAND', 'recurse')]
# [('FUNC', 'test_arg_parser'), ('ARGS', 'a, b, c')]

# also should group generic "operations" together as one unit
'''
"FUNC": {
    "NAME" : "funcname",
    "ARGS" : [] | None
}

"LABEL": {
    "NAME": "start"
}

"OPERATION": {
    "LEFT" : None | str
    "OPERATOR" : None | both binary, unary, and comparison
    "RIGHT" : None | str
}


'''

def tokenize_ir(ir_string: str):
    index = 0
    while index < len(ir_string):
        token = None
        for pattern in patterns:

            # # testing out setargs
            # match_args = re.findall(word, ir_string[index:])
            # for m in match_args:
            #     print("\targs", m)

            matched = re.match(f"\s*{pattern}\s*", ir_string[index:])
            if matched != None:
                index += matched.end()
                token = list(matched.groupdict().items())[0]
                break
        if token: yield token
        else: raise Exception(f'Unexpected token "{ir_string[index:]}"')

SimplicIRParser().from_file("test_codes\\fib.ir")
