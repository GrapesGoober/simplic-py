from compiler.exceptions import AsmException

OPCODES = [
    "set",  "if", "stack", "load", "store", "loadm", "storem",  
    "add", "sub", "lsl", "lsr", "mul", "div", "and", "or", "not"
]

CONDITIONS = [
    "always", "less", "high", "equal", "nequal", "lesseq", "higheq"
]

STACK_OP = ['pop', 'push']

# using intermediate object { source: null, label: { address: 0, code: [ [["unparsed", "tokens"], linenum] ] } }
{
    # using source here
    'source': None,
    'labels': {
        'start': 0
    },
    'code': [                   # Using linenum here
        (["unparsed", "tokens"], None),
        (["unparsed", "tokens"], None),
    ]
}

# These two will use parse_label and parse_instr to build this intermediate representation
# however, the 'from_list' will not populate 'source' and 'linenum'
def file_to_file(source: str, destination: str) -> None:
    asm = { 'source': source, 'labels': {}, 'code': [] }
    current_pc = 0
    with open(source, 'r') as f:
        for line_num, line in enumerate(f):
            line = line.lower().strip().split('#')[0]
            if ':' in line:
                result, label = parse_label(line, asm['labels'])
                if not result: 
                    error_print(source, line_num, label)
                    return
                asm['labels'][label] = current_pc
            elif line:
                tokens = line.split()
                if tokens[0] == ('set' or 'if'):
                    current_pc += 3
                else: current_pc += 1
                asm['code'].append(( line.split(), line_num ))
                
    status, msg, line_num = compile(asm, destination)
    if not status:
        error_print(source, line_num, msg)

def list_to_file(asm_list: list[str], destination: str) -> None:
    asm = { 'source': None, 'labels': {}, 'code': []}
    current_pc = 0
    for line in asm_list:
        if ':' in line:
            result, label = parse_label(line, asm['labels'])
            if not result: 
                raise Exception(label)
            asm['labels'][label] = current_pc
        else:
            tokens = line.split()
            if tokens[0] == ('set' or 'if'):
                current_pc += 3
            else: current_pc += 1
            asm['code'].append(( line.split(), None ))
    status, msg, _ = compile(asm, destination)
    if not status:
        raise Exception(msg)

# These two returns (false, msg) when failed, otherwise (true, result)
# returns a label
def parse_label(line: str, labels: dict) -> tuple[bool, str]:
    if line[-1] != ':':
        return False, "Expect a line to end after colon"
    elif len(line[:-1].split()) != 1:
        return False, "Expect a only a single label"
    label = line[:-1].split()[0]
    if label in labels:  
        return False, "Duplicate label"
    return True, label

# this function compiles to destination
# if the source and linenum is set, will print error message and exit
# otherwise, raise exception
def compile(asm: dict, destination: str) -> tuple[bool, str]:
    bytecodes = []
    for tokens, line_num in asm['code']:
        if tokens[0] not in OPCODES:
            return False, "Invalid opcode"
        match tokens[0]:
            case 'set':
                status, operands = compile_set_operands(tokens)
            case 'if':
                status, operands = compile_if_operands(tokens, asm['labels'])
            case 'stack':
                status, operands = compile_stack_operands(tokens)
            case _:
                status, operands = compile_default_operands(tokens)
        if not status:
            return status, operands, line_num
        opcode = OPCODES.index(tokens[0])
        bytecodes.append(f'{opcode:x}{operands[0]}')
        if len(operands) == 3:
            bytecodes += operands[1], operands[2]

    max_width, width = 16, 0
    with open(destination, 'w') as f:
        for b in bytecodes:
            f.write(b + ' ')
            width += 1
            if width == max_width:
                width = 0
                f.write('\n')
    return True, '', None

def compile_set_operands(tokens: list) -> tuple[bool, any]:
    if len(tokens) != 3:
        return False, "Expects only variable and value"
    
    status, I = parse_literal(tokens[1], 4)
    if not status:
        return status, I
    status, Imm = parse_literal(tokens[2], 16)
    if not status:
        return status, Imm
    
    return True, (
        f"{I:x}",
        f"{( Imm >> 8 ):02x}", 
        f"{( Imm & 0xFF ):02x}"
    )

def compile_if_operands(tokens: list, labels: dict) -> tuple[bool, any]:
    if len(tokens) != 3: 
        return False, "Expects only condition and label"
    if tokens[1] not in CONDITIONS:
        return False, "Invalid condition"
    if tokens[2] not in labels:
        return False, "Undeclared label"

    cond = CONDITIONS.index(tokens[1]) 
    label = labels[tokens[2]]

    return True, (
        f'{cond:x}',
        f'{( label >> 8 ):02x}',
        f'{( label & 0xFF ):02x}',
    )

def compile_stack_operands(tokens: list) -> tuple[bool, any]:
    if len(tokens) != 2: 
        return False, "Expects either 'PUSH' or 'POP'"
    if tokens[1] not in STACK_OP:
        return False, "Expects either 'PUSH' or 'POP'"
    m = STACK_OP.index(tokens[1])
    return True, (f'{m:x}')

def compile_default_operands(tokens: list) -> tuple[bool, any]:
    if len(tokens) != 2: 
        return False, "Expects variable index"
    status, I = parse_literal(tokens[1], 4) 
    if not status:
        return status, I
    return True, (f"{I:x}")

def parse_literal(token: str, bitsize: int) -> int:
    try:
        if token.startswith("0x"): 
            result = int(token, 16)
        elif token.startswith("0b"): 
            result = int(token, 2)
        else: 
            result = int(token, 10)
    except ValueError:
        return False, "Invalid immediate syntax"

    if result.bit_length() > bitsize: 
        return False, f"Immediate value too big for {bitsize} bits."
    
    return True, result

def error_print(source, line_num, message) -> None:
    err_string = "\n"
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            if line_num - 3 < i < line_num + 2: 
                err_string += f"  {i+1}:\t{line}"
    print(err_string)
    print(f"Error at line {line_num + 1}: {message}", end='\n\n')