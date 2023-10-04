from aofs.token_set import token_set

# Parse a token into integer code (i.e. index of token)
def parse_token(tokens : list, token_type : str) -> int:

    # reads from the first token
    if tokens == []:
        raise Exception(f"Expected a {token_type} token.")
    token = tokens[0]
    tokens.pop(0)

    if token_type not in token_set:
        raise Exception(f"Token type {token_type} does not exist.")
        
    token_list = token_set[token_type]
    if token.lower() in token_list:
        token_index = token_list.index(token.lower())
        return token_index
    else:
        raise Exception(f"Unrecognized {token_type} '{token}'.")

# Parse an immediate into integer with the specified bitsize
def parse_imm(tokens : list, bit_size : int) -> int:

    # reads from the first token
    if tokens == []:
        raise Exception(f"Expected a {bit_size}-bit immediate value.")
    token = tokens[0]
    tokens.pop(0)

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
    asmline = asmline.strip()
    tokens = asmline.split()

    # firstly, get the opcode and rd code
    opcode = parse_token(tokens, "instruction")

    # parsing operands are finicky; syntax is specific to opcode
    # nevertheless, it always starts with Destination Register
    rd = parse_token(tokens, "register")
    operands = rd << 8

    # start with conditionals ("move" and "cadd")
    if opcode in [0, 1]:
        rn = parse_token(tokens, "register")
        cnd = parse_token(tokens, "condition")
        operands += (rn << 4) + cnd
    # next, do memory instructions ("load" and "store")
    elif opcode in [2, 3]:
        rn = parse_token(tokens, "register")
        imm4 = parse_imm(tokens, 4)
        operands += (rn << 4) + imm4
    # insert instruction takes 8-bit immediate
    elif opcode == 4:
        imm8 = parse_imm(tokens, 8)
        operands += imm8
    # shift instruction takes a special "shift operation" token type
    elif opcode == 5:
        shiftop = parse_token(tokens, "shift operation")
        distance = parse_token(tokens, "register")
        operands += (shiftop << 4) + distance
    # rest ALU instructions take registers
    else:
        rn = parse_token(tokens, "register")
        rm = parse_token(tokens, "register")
        operands += (rn << 4) + rm

    bincode = (opcode << 12) + operands

    return bincode
