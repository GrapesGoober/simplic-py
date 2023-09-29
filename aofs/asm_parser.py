from math import ceil
import asm_token_set

# Get the token index in unprefixed hex
def __hexify_token(token : str, token_type : str) -> str:
    if token_type not in token_set:
        raise Exception(f"Token type {token_type} does not exist.")
        
    token_list = token_set[token_type]
    if token.lower() in token_list:
        indexof = token_list.index(token.lower())
        return hex(indexof)[2:]
    else:
        raise Exception(f"Unrecognized {token_type} '{token}'.")

# Parse an immediate into integer value with the specified bitsize
def __hexify_imm(token : str, bit_size : int) -> str:
    result = 0
    try:
        if token.startswith("0x"):
            result = int(token, 16)
        elif token.startswith("0b"): 
            result = int(token, 2)
        else:
            result = int(token, 10)
    except ValueError:
        raise Exception(f"Invalid immediate '{token}'.")

    if result.bit_length() > bit_size:
        raise Exception(f"Immediate value '{token}' too big for {bit_size} bits.")

    # must return hex of the proper digits for bitsize
    zeros = (bitcount  - intvalue.bit_length()) // 4
    return ("0" * zeros) + hex(result)[2:]

# Parses a line of assembly to binary code
def parse_line(asmline : str) -> int:
    asmline = asmline.strip()
    tokens = asmline.split()

    # firstly, iterate to get the instruction index and operand parsers
    instr = parse_token(tokens[0], instructions)
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
