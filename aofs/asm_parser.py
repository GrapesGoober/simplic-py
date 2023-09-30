from aofs.asm_token_set import token_set

# Parse a token into integer code (i.e. index of token)
def parse_token(token : str, token_type : str) -> int:
    if token_type not in token_set:
        raise Exception(f"Token type {token_type} does not exist.")
        
    token_list = token_set[token_type]
    if token.lower() in token_list:
        token_index = token_list.index(token.lower())
        return token_index
    else:
        raise Exception(f"Unrecognized {token_type} '{token}'.")

# Parse an immediate into integer with the specified bitsize
def parse_imm(token : str, bit_size : int) -> int:
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
    opcode = parse_token(tokens[0], "instruction")
    rd = parse_token(tokens[1], "register")

    # parsing operands are finicky; syntax is specific to opcode
    if opcode in [0, 1]:
        pass
    elif opcode in [2, 3]:
        pass
    elif opcode == 4:
        pass
    elif opcode == 5:
        pass
    else:
        raise Exception("Opcode undefined")
    
    return opcode
