import re

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

bytecodes, labels, label_points = [], {}, []

def file_to_file(src: str, dest: str) -> None:
    with open(src, 'r') as f:
        for line_num, line in enumerate(f):
            # read line and exclude comments
            line = line.lower().strip().split('#')[0]
            cursor = src, line_num, line
            if not line: continue
            elif ':' in line: parse_label(cursor)
            else: parse_instr(cursor)

    for line_num, label in label_points:
        cursor = src, line_num, ''
        if label not in labels: 
            error(cursor, f"Unknown label {label}")
        address = labels[label] - 1
        bytecodes[line_num] = f'{(address >> 8):02x}'
        bytecodes[line_num + 1] = f'{(address & 0xFF):02x}'

    max_width, width = 16, 0
    with open(dest, 'w') as f:
        for b in bytecodes:
            f.write(b + ' ')
            width += 1
            if width == max_width:
                width = 0
                f.write('\n')

def parse_label(cursor: tuple) -> None:
    _,_, line = cursor
    if line[-1] != ':':
        error(cursor, "Expect a line to end with colon")
    elif line[:-1].split() != 1:
        error(cursor, "Expect a only a single label")
    label = line[:-1].split()[0]
    if label in labels:  
        error(cursor, f"Duplicate label {label}")
    labels[label] = len(bytecodes) - 1

def parse_instr(cursor: tuple) -> str:
    _,_, line = cursor
    tokens = line.split()
    match tokens[0]:
        case 'set': 
            if len(tokens) != 3:
                error(cursor, "'SET' expects only 2 operands: variable and value.") 
            _, var, val = tokens

        case 'if': 
            if len(tokens) != 3: return "'IF' expects only 2 operands: condition and label."

        case 'stack': 
            if len(tokens) != 2: return "'IF' expects only 1 operand: 'PUSH' or 'POP'."
            
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
        raise Exception(f"Invalid immediate syntax.")

    if result.bit_length() < bitsize: return "Immediate value too big for {bitsize} bits."
    return result

def error(cursor: tuple, message: str):
    source, line_num = cursor
    err_string = "\n"
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            if line_num - 3 < i < line_num + 2: 
                err_string += f"  {i+1}:\t{line}"

    err_string += f"Error at line {line_num + 1}: {message}\n"
    raise Exception(err_string)
