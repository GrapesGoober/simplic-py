# (Internal) Defining instruction set with their instruction type
instructions = {
    "condition" : [ "move", "cadd" ],
    "memory" : [ "load", "store" ],
    "insert" : [ "insert" ],
    "shift" : [ "shift" ],
    "alu" : [ 
        "add", "sub", "mul", "longmul", "div", "mod", 
        "and", "or", "xor", "nor"
    ]
}

# (Internal) Defining a set of operand tokens (excluding instructions)
token_set = {
    "register" : [
        # A special zero value for resetting registers
        "zero",
        # General purpose registers
        "r1", "r2", "r3", "r4",
        "r5","r6", "r7", "r8", "r9",

        # Dedicated registers
        "buffer",   # Buffer register   - immediate values
        "return",   # Return register   - values from previous call
        "stack",    # Stack pointer     - keep track the current top of the stack
        "address",  # Address register  - for memory and jumps
        "link",     # Link register     - keep progc addresses to return to
        "progc"     # Program counter   - current instruction to execute
    ],
    "condition" : [

    ],
    "shift-op" : [
        "left",
        "right",
        "arith",
        "rotate"
    ]
}

# (Internal) Returns a function to parse token with a specified type
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


# (Internal) Parses an instruction token and returns instruction index and type
def parse_instr(token : str) -> (int, str):
    
    instr_index = 0
    for instr_type in instructions:
        if token.lower() in instructions[instr_type]:
            instr_index += instructions[instr_type].index(token.lower())
            return instr_index, instr_type
        else:
            instr_index += len(instructions[instr_type])

    # If did not return within loop, then assume it wasn't found
    raise Exception(f"Unrecognized instruction '{token}'")


# Parses a line of assembly to binary code
def parse_line(asmline : str) -> int:
    asmline = asmline.strip()
    tokens = asmline.split()

    # firstly, iterate to get the instruction index and operand parsers
    instr, instr_type = parse_instr(tokens[0])
    operand_parsers = operands[instr_type]
    
    if instr_type == "condition":
        pass
    elif instr_type == "memory":
        pass
    elif instr_type == "insert":
        pass
    elif instr_type == "shift":
        pass
    elif instr_type == "alu":
        pass
    else:
        raise Exception("Undefined instruction type")
