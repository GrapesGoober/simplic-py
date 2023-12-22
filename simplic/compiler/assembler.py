from compiler.exceptions import SimplicErr

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

STACK_OP = ['pop', 'push']

# These two will use parse_label and parse_instr to build this intermediate representation
# however, the 'from_list' will not populate 'source' and 'linenum'
def file_to_file(source: str, destination: str) -> None:
    asm = { 'source': source, 'labels': {}, 'code': [], 'current pc': 0 }
    with open(source, 'r') as f:
        for line_num, line in enumerate(f):
            line = line.lower().strip().split('#')[0]
            status, msg = parse_line(line, asm, line_num)
            if not status: 
                error_print(source, line_num, msg)
                return
    status, msg, line_num = compile(asm, destination)
    if not status:
        error_print(source, line_num, msg)

def list_to_file(asm_list: list[str], destination: str) -> None:
    asm = { 'source': None, 'labels': {}, 'code': [], 'current pc': 0}
    for line in asm_list:
        status, msg = parse_line(line, asm)
        if not status: raise Exception(msg)
    status, msg, _ = compile(asm, destination)
    if not status: raise Exception(msg)

def parse_line(line: str, asm: dict, line_num: int = None) -> tuple[bool, str]:
    if ':' in line:
        if line[-1] != ':':
            return False, "Expect a line to end after colon"

        elif len(line[:-1].split()) != 1:
            return False, "Expect a only a single label"
        label = line[:-1].split()[0]
        if label in asm['labels']:  
            return False, f"Duplicate label '{label}'"
        asm['labels'][label] = asm['current pc']
    elif line:
        tokens = line.split()
        if tokens[0] == ('set' or 'if'):
            asm['current pc'] += 3
        else: asm['current pc'] += 1
        asm['code'].append(( line.split(), line_num ))
    return True, None

# this function compiles to destination
# if the source and linenum is set, will print error message and exit
# otherwise, raise exception
def compile(asm: dict, destination: str) -> tuple[bool, str, int]:
    bytecodes = []
    for tokens, line_num in asm['code']:
        status, codes = compile_instr(tokens, asm['labels'])
        if not status:
            return status, codes, line_num
        bytecodes += codes

    max_width, width = 16, 0
    with open(destination, 'w') as f:
        for b in bytecodes:
            f.write(b + ' ')
            width += 1
            if width == max_width:
                width = 0
                f.write('\n')
    return True, '', None

def compile_instr(tokens: list, labels: dict) -> tuple[bool, list]:
    
    if tokens[0] not in OPCODES:
        raise SimplicErr( f"Invalid opcode '{tokens[0]}'")
    
    opcode = OPCODES.index(tokens[0])
    operand, immediate = 0, None
    match tokens[0]:
        case 'set':
            if len(tokens) != 3:
                raise SimplicErr("Expects a variable and a value")
            operand = parse_literal(tokens[1], 4)
            immediate = parse_literal(tokens[2], 16)
        case 'if':
            if len(tokens) != 3: 
                raise SimplicErr("Expects only condition and label")
            if tokens[1] not in CONDITIONS:
                raise SimplicErr(f"Invalid condition '{tokens[1]}'")
            if tokens[2] not in labels:
                # TODO do the recursive jump
                if eqfwef
                raise SimplicErr(f"Undeclared label '{tokens[2]}'")
            operand = CONDITIONS.index(tokens[1]) 
            immediate = labels[tokens[2]]
        case 'stack':
            if len(tokens) != 2: 
                raise SimplicErr("Expects either 'PUSH' or 'POP'")
            if tokens[1] not in STACK_OP:
                raise SimplicErr("Expects either 'PUSH' or 'POP'")
            operand = STACK_OP.index(tokens[1])
        case _:
            if len(tokens) != 2: 
                return False, "Expects variable operand"
            operand = parse_literal(tokens[1], 4) 

    if immediate == None:
        return [f'{opcode:01x}{operand:01x}']
    else:
        return [
            f'{opcode:01x}{operand:01x}',
            f'{( immediate >> 8 ):02x}',
            f'{( immediate & 0xFF ):02x}',
        ]

def parse_literal(token: str, bitsize: int) -> int:
    try:
        if token.startswith("0x"): 
            result = int(token, 16)
        elif token.startswith("0b"): 
            result = int(token, 2)
        else: 
            result = int(token, 10)
    except ValueError:
        raise SimplicErr("Invalid immediate syntax")
    if result.bit_length() > bitsize: 
        raise SimplicErr(f"Immediate value too big for {bitsize} bits.")
    return result