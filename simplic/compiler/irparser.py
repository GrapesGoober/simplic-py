class SimplicIRParser:
    def from_file(self, filename: str) -> list[tuple]:
        with open(filename, 'r') as file:
            for linenum, line in enumerate(file):
                tokens = line.split('#')[0].split()
                if tokens == []: continue

                match tokens[0]:
                    case 'func':
                        print('\nDefining a new function')
                        print('Name:', tokens[1])
                    case 'label':
                        print('label', tokens[1])
                    case _:
                        dest = None
                        if '=' in tokens: dest = tokens[0]

                        print('\t', ' '.join(tokens))
                        psuedo_ir_instruction('add', 'result', 'x', 'y')


# SimplicIRParser().from_file("test_codes\\fib.ir")

def psuedo_ir_instruction(operator, dest, operand1, operand2):
    if operand1 != None:    print(f'load from {operand1}')
    if operator != None:    print(f'{operator} with {operand2}')
    if dest != None:        print(f'store to {dest}')


import re

word = r'(\w|%|\$|.)+'
destination = rf'{word}\s*=\s*'
operators = r'\+|-|\*|\/|<<|>>|&|\||~|cmp'
operation = rf'\s*({operators})\s*{word}'

def tokenize_ir(ir_string):
    # Define regular expression patterns for different components
    patterns = [
        (r'(?P<destination>[a-zA-Z_][a-zA-Z0-9_]*)?\s*=\s*', 'DESTINATION'),
        (r'(?P<variable1>[a-zA-Z_][a-zA-Z0-9_]*)', 'VARIABLE1'),
        (r'\s*(?P<operator>[+\-*/<<>>&|!cmp]*)\s*', 'OPERATOR'),
        (r'(?P<variable2>[a-zA-Z_][a-zA-Z0-9_]*)?', 'VARIABLE2'),
    ]

    # Combine patterns into a single regular expression
    combined_pattern = '|'.join('(?:%s)' % pattern for pattern, _ in patterns)

    # Tokenize the IR string
    tokens = []
    for match in re.finditer(combined_pattern, ir_string):
        for name, value in match.groupdict().items():
            if value is not None:
                tokens.append((name, value))

    return tokens