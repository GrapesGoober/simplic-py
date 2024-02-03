from simplic.compiler.exceptions import SimplicErr

OPCODES = [
    "load", "store", "loadm", "storem", "add", "sub", "lsl", "lsr",
    "mul", "div", "and", "or", "not", "stack", "set", "if"
]

CONDITIONS = [
    "always", "less", "more", "equal", "nequal", "eqless", "eqmore"
]

STACK_OP = ['pop', 'push']

# compile assembly codes to bytecodes
def compile_asm(asm: list) -> list[int]:
    labels, bytecodes = get_labels(asm), []
    for iter, tokens in enumerate(asm):
        if not tokens or tokens[0] == 'label': continue
        cursor = iter, labels, tokens
        bytecodes += parse_instr(cursor)
    return bytecodes

# scan code to get label mappings
def get_labels(asm: list) -> dict[str, int]:
    labels = {'#halt': 0xFFFE}
    label_PC = 0
    for iter, tokens in enumerate(asm):
        if not tokens: continue
        match tokens[0]:
            case 'label':
                label, = get_operands((iter, labels, tokens), count=1)
                if label in labels:  
                    raise SimplicErr(f"Line {iter+1}: Duplicate label '{label}'")
                if label in OPCODES + CONDITIONS + STACK_OP:
                    raise SimplicErr(f"Line {iter+1}: Cannot use keyword '{label}' as label")
                labels[label] = (label_PC - 1) & 0xFFFF
            case 'if' | 'set':  label_PC += 3
            case _:             label_PC += 1
    return labels
            
# parse current opcode & instruction
def parse_instr(cursor: tuple) -> list[int]:
    iter, _, tokens = cursor
    if tokens[0] not in OPCODES:
        raise SimplicErr(f"Line {iter+1}: Invalid opcode '{tokens[0]}'")
    opcode = OPCODES.index(tokens[0])
    match tokens[0]:
        case 'set' | 'if': # these two instructions need 16-bit immediate
            operand, immediate = parse_operands(cursor, count=2)
            yield opcode << 4 | operand & 0xF
            yield ( immediate >> 8 )    & 0xFF
            yield   immediate           & 0xFF
        case _:
            operand, = parse_operands(cursor, count=1)
            yield opcode << 4 | operand & 0xF

# parses operands from tokens list
def parse_operands(cursor: tuple, count: int) -> list[str|int]:
    iter, labels, _ = cursor
    for tok in get_operands(cursor, count):
        if tok in CONDITIONS:       yield CONDITIONS.index(tok)
        elif tok in STACK_OP:       yield STACK_OP.index(tok)
        elif tok in labels:         yield labels[tok]
        elif isinstance(tok, int):  yield tok
        elif tok.startswith("0x"):  yield int(tok, 16)
        elif tok.startswith("0b"):  yield int(tok, 2)
        elif tok.isdigit():         yield int(tok, 10)
        else: raise SimplicErr(f"Line {iter+1}: Invalid token '{tok}'")

# tokenizes operands from tokens with expected token count
def get_operands(cursor: tuple, count: int) -> tuple[str]:
    iter, _, tokens = cursor
    if len(tokens[1:]) > count:
        raise SimplicErr(f"Line {iter+1}: Unexpected token '{tokens[count]}'")
    if len(tokens[1:]) < count:
        raise SimplicErr(f"Line {iter+1}: Expected {count} operands")
    return tokens[1:]

# load ASM from file
def from_file(filename: str) -> list[tuple]:
    asm = []
    with open(filename, 'r') as f: 
        for line in f:
            tokens = line.strip().split('#')[0].split()
            asm.append(tuple(tokens))
    return asm
    
# write bytecodes to hexfile
def to_hexfile(bytecodes: list, filename: str) -> None:
    with open(filename, 'w') as f:
        for i, b in enumerate(bytecodes):
            newline = '\n' if ((i + 1) % 16 == 0) else ''
            f.write(f'{b:02x} {newline}')
