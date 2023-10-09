from assembler.token_set import token_set

# Parse a mnemonic into binary code (essentially just an index-of)
def parse_mnemonic(token : str, token_type : str) -> tuple(bool, any):

    if token_type not in token_set:
        return False, f"Token type {token_type} does not exist."
        
    token_list = token_set[token_type]
    if token.lower() in token_list:
        token_index = token_list.index(token.lower())
        return True, token_index
    elif token == "":
        return False, f"Expected a {token_type} before newline."
    else:
        return False, f"Unrecognized {token_type} '{token}'."

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
        if token == "":
            return False, f"Expected a {bit_size}-bit immediate before newline."
        else:
            return False, f"Invalid immediate '{token}'."

    if result.bit_length() > bit_size:
        return False, f"Immediate value '{token}' too big for {bit_size} bits."

    return True, result

# Parses a line of assembly to binary code
def parse_instruction(asmline : str) -> list[int]:

    # split but also add some empty padding tokens for safe indexing
    tokens = asmline.split() + [""] * 4

    # firstly, parse the opcode and destination register
    status, opcode = parse_mnemonic(tokens[0], "instruction")
    if not status: return status, opcode
    status, rd = parse_mnemonic(tokens[1], "register") 
    if not status: return status, rd
    
    # next, parse the operands
    operands = 0
    # parsing operands are finicky since syntax is specific to opcode
    if opcode == 0: # start with conditional move "cmove"
        operands += parse_mnemonic(tokens[2], "register") << 4
        operands += parse_mnemonic(tokens[3], "condition")
    elif opcode == 1: # count leading zeros 
        operands += parse_mnemonic(tokens[2], "register") << 4
        if tokens[3] != "": 
            return False, f"Unexpected operand '{tokens[3]}'"
    elif opcode in [2, 3]: # memory instructions ("load" and "store")
        operands += parse_mnemonic(tokens[2], "register") << 4
        operands += parse_immediate(tokens[3], 4)
    elif opcode == 4: # insert instruction takes 8-bit immediate
        operands += parse_immediate(tokens[2], 8)
        if tokens[3] != "": 
            return False, f"Unexpected operand '{tokens[3]}'"
    elif opcode == 5: # shift instruction takes a special "shift operation" token type
        operands += parse_mnemonic(tokens[2], "shift operation") << 4
        operands += parse_mnemonic(tokens[3], "register")
    else: # rest ALU instructions take registers
        operands += parse_mnemonic(tokens[2], "register") << 4
        operands += parse_mnemonic(tokens[3], "register")

    if tokens[4] != "": 
        return False, f"Unexpected operand '{tokens[4]}'"
    
    return [(opcode << 4) + rd, operands]

def parse(asmlines : list[str]) -> dict[str: int]:

    bytecodes = []

    for i, asmline in enumerate(asmlines):
        # remove comments and empty lines
        asmline = asmline.strip().split("//")[0]
        if asmline == "": continue

        # split, but also add some empty padding tokens for safe indexing
        tokens = asmline.split() + [""] * 4

        # try parsing the code
        if tokens[0].lower() == "move":
            if tokens[3] != "":
                return False, f"Unexpected token '{tokens[3]}'"
            bytecodes += parse_instruction(f"cmove {tokens[1]} {tokens[2]} always") 
        elif tokens[0].lower() == "flag":
            if tokens[2] != "":
                return False, f"Unexpected token '{tokens[2]}'"
            if tokens[1].lower() == "on":
                bytecodes += parse_instruction("nor zero zero zero")
            elif tokens[1].lower() == "reset":
                bytecodes += parse_instruction("xor zero zero zero")
            else:
                return False, f"Unrecognized flag directive {tokens[1]}"
        else:
            bytecodes += parse_instruction(asmline)

        return False, f"Assembler error at line {i+1}: {ve.args[0]}"

            

    return { i: v for i, v, in enumerate(bytecodes) }
