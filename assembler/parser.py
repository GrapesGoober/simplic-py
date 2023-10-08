from assembler.token_set import token_set

# Parse a mnemonic into binary code (essentially just an index-of)
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

# Parses a line of assembly to binary code
def parse_line(asmline : str) -> int:

    # split the line into tokens, 
    # but also add some empty padding tokens for indexing
    tokens = asmline.split() + [""] * 4

    # firstly, parse the opcode and destination register
    opcode = parse_mnemonic(tokens[0], "instruction")
    rd = parse_mnemonic(tokens[1], "register") 
    
    # next, parse the operands
    operands = 0
    # parsing operands are finicky since syntax is specific to opcode
    if opcode == 0: # start with conditional move "cmove"
        operands += parse_mnemonic(tokens[2], "register") << 4
        operands += parse_mnemonic(tokens[3], "condition")
    elif opcode == 1: # count leading zeros 
        operands += parse_mnemonic(tokens[2], "register") << 4
    elif opcode in [2, 3]: # memory instructions ("load" and "store")
        operands += parse_mnemonic(tokens[2], "register") << 4
        operands += parse_immediate(tokens[3], 4)
    elif opcode == 4: # insert instruction takes 8-bit immediate
        operands += parse_immediate(tokens[2], 8)
    elif opcode == 5: # shift instruction takes a special "shift operation" token type
        operands += parse_mnemonic(tokens[2], "shift operation") << 4
        operands += parse_mnemonic(tokens[3], "register")
    else: # rest ALU instructions take registers
        operands += parse_mnemonic(tokens[2], "register") << 4
        operands += parse_mnemonic(tokens[3], "register")

    bincode = (opcode << 12) + (rd << 8) + operands

    return bincode
