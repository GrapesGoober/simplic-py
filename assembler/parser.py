from assembler.token_set import token_set

# Parse a mnemonic into integer code (essentially just an index-of)
def parse_mnemonic(token : str, token_type : str) -> int:

    if token_type not in token_set:
        raise Exception(f"Token type {token_type} does not exist.")
        
    token_list = token_set[token_type]
    if token.lower() in token_list:
        token_index = token_list.index(token.lower())
        return token_index
    else:
        raise Exception(f"Unrecognized {token_type} '{token}'.")

# Parse an immediate into integer with the specified bitsize
def parse_immediate(token : str, bit_size : int) -> int:

    result = 0
    try:
        if token.lower().startswith("0x"):
            result = int(token, 16)
        elif token.lower().startswith("0b"): 
            result = int(token, 2)
        else:
            result = int(token, 10)
    except ValueError:
        raise Exception(f"Invalid immediate '{token}'.")

    if result.bit_length() > bit_size:
        raise Exception(f"Immediate value '{token}' too big for {bit_size} bits.")

    return result

# Parses a line of assembly to integer code
def parse_line(asmline : str) -> int:

    # firstly, handle comma split into header and operands
    asmline = asmline.strip()
    tokens = asmline.split()

    # next, parse the header (the opcode and destination register)
    opcode = parse_mnemonic(tokens[0], "instruction")
    rd = parse_mnemonic(tokens[1], "register") << 8

    # next, parse the operands
    # parsing operands are finicky; syntax is specific to opcode

    # start with conditionals ("move" and "cadd")
    if opcode in [0, 1]:
        rn = parse_mnemonic(tokens[2], "register")
        cnd = parse_mnemonic(tokens[3], "condition")
        operands = (rn << 4) + cnd
    # next, do memory instructions ("load" and "store")
    elif opcode in [2, 3]:
        rn = parse_mnemonic(tokens[2], "register")
        imm4 = parse_immediate(tokens[3], 4)
        operands = (rn << 4) + imm4
    # insert instruction takes 8-bit immediate
    elif opcode == 4:
        imm8 = parse_immediate(tokens[2], 8)
        operands = imm8
    # shift instruction takes a special "shift operation" token type
    elif opcode == 5:
        shiftop = parse_mnemonic(tokens[2], "shift operation")
        distance = parse_mnemonic(tokens[3], "register")
        operands = (shiftop << 4) + distance
    # rest ALU instructions take registers
    else:
        rn = parse_mnemonic(tokens[2], "register")
        rm = parse_mnemonic(tokens[3], "register")
        operands = (rn << 4) + rm

    bincode = (opcode << 12) + (rd << 8) + operands

    return bincode
