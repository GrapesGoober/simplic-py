from assembler.token_set import token_set

# Parse a mnemonic into binary code (essentially just an index-of)
def parse_mnemonic(token : str, token_type : str) -> int:

    if token_type not in token_set:
        print(f"Error: Token type {token_type} does not exist.")
        return False
        
    token_list = token_set[token_type]
    if token.lower() in token_list:
        token_index = token_list.index(token.lower())
        return token_index
    elif token == "":
        print(f"Error: Expected a {token_type} before newline.")
        return False
    else:
        print(f"Error: Unrecognized {token_type} '{token}'.")
        return False

# Parse an immediate into integer with the specified bitsize
def parse_immediate(token : str, bit_size : int) -> int:

    result = 0
    if token == "":
        print(f"Error: Expected a {bit_size}-bit immediate.")
        return False
    try:
        if token.lower().startswith("0x"):
            result = int(token, 16)
        elif token.lower().startswith("0b"): 
            result = int(token, 2)
        else:
            result = int(token, 10)
    except ValueError:
        print(f"Error: Invalid immediate '{token}'.")
        return False

    if result.bit_length() > bit_size:
        print(f"Error: Immediate value '{token}' too big for {bit_size} bits.")
        return False
    
    return result

# Parses a line of assembly to binary code
def parse_instruction(asmline : str) -> list[int]:

    # split but also add some empty padding tokens for safe indexing
    tokens = asmline.split() + [""] * 4

    # firstly, parse the opcode and destination register
    opcode = parse_mnemonic(tokens[0], "instruction")
    rd = parse_mnemonic(tokens[1], "register") 
    
    # next, parse the operands
    operandA, operandB = 0, 0
    # parsing operands are finicky since syntax is specific to opcode
    if opcode == 0: # start with conditional move "cmove"
        operandA = parse_mnemonic(tokens[2], "register")
        operandB = parse_mnemonic(tokens[3], "condition")
    elif opcode == 1: # count leading zeros 
        operandB += parse_mnemonic(tokens[2], "register")
        if tokens[3] != "": 
            print(f"Error: Unexpected operand '{tokens[3]}'")
            return False
    elif opcode in [2, 3]: # memory instructions ("load" and "store")
        operandA = parse_mnemonic(tokens[2], "register")
        operandB = parse_immediate(tokens[3], 4)
    elif opcode == 4: # insert instruction takes 8-bit immediate
        operandB += parse_immediate(tokens[2], 8)
        if tokens[3] != "": 
            print(f"Error: Unexpected operand '{tokens[3]}'")
            return False
    elif opcode == 5: # shift instruction takes a special "shift operation" token type
        operandA = parse_mnemonic(tokens[2], "shift operation")
        operandB = parse_mnemonic(tokens[3], "register")
    else: # rest ALU instructions take registers
        operandA = parse_mnemonic(tokens[2], "register")
        operandB = parse_mnemonic(tokens[3], "register")

    if tokens[4] != "": 
        print(f"Error: Unexpected operand '{tokens[4]}'")
        return False
    
    if any(i is False for i in [opcode, rd, operandA, operandB]):
        return False

    return [(opcode << 4) + rd, (operandA << 4) + operandB]

def parse(asmlines : list[str]) -> dict[str: int]:

    bytecodes = []

    for i, asmline in enumerate(asmlines):
        # remove comments and empty lines
        asmline = asmline.strip().split("//")[0]
        if asmline == "": continue

        # split, but also add some empty padding tokens for safe indexing
        tokens = asmline.split() + [""] * 4

        # try parsing the code onto "result"
        result = None
        if tokens[0].lower() == "move":
            result = parse_instruction(f"cmove {tokens[1]} {tokens[2]} always") 
            if tokens[3] != "":
                print(f"Error: Unexpected token '{tokens[3]}'")
                return False
        elif tokens[0].lower() == "flag":
            if tokens[1].lower() == "on":
                result = parse_instruction("nor zero zero zero")
            elif tokens[1].lower() == "reset":
                result = parse_instruction("xor zero zero zero")
            else:
                print(f"Error: Unrecognized flag directive '{tokens[1]}'")
                return False
            if tokens[2] != "":
                print(f"Error: Unexpected token '{tokens[3]}'")
                return False
        else:
            result = parse_instruction(asmline)

        if result:
            bytecodes += result
        else:    
            print(f"Error: Assembler error at line {i+1}\n\t {asmline}")
            return False
        
    return { i: v for i, v, in enumerate(bytecodes) }
