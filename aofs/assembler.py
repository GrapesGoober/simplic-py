import asm_tokens

# (Internal) Parses a token to hex value
def parse_token(token : str, token_type : str) -> int:
    if token.lower() not in token_set[token_type]:
        raise Exception(f"Unrecognized {token_type} '{token}'")
    else:
        return token_set[token_type].index(token.lower())

# (Internal) Parse an immediate with the specified bitsize limitation
def parse_imm(token : str, bit_size : int) -> int:
    result = 0
    try:
        if token.startswith("0x"):
            result = int(token, 16)
        elif token.startswith("0b"): 
            result = int(token, 2)
        else:
            result = int(token, 10)
    except:
        raise Exception(f"Invalid immediate '{token}'")

    if result.bit_length() > bit_size:
        raise Exception(f"Immediate value '{token}' too big for {bit_size} bits.")
    
    return result

# Parses a line of assembly to binary code
def parse_line(asmline : str) -> int:
    asmline = asmline.strip()
    tokens = asmline.split()

    # firstly, iterate to get the instruction index and operand parsers
    instr, instr_type = parse_token(tokens[0], instructions)
    operand_parsers = operands[instr_type]
    
    if instr_type == "condition":
        pass
    elif instr_type == "memory":
        pass
    elif instr_type == "insert":
        pass
    elif instr_type == "shift":
        pass
    else:
        raise Exception("Undefined instruction type")
