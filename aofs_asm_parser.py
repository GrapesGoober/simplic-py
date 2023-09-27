# Defining a set of instruction types and their instructions
instructions = {
    "cond" : [ "move", "cadd" ],
    "memory" : [ "load", "store" ],
    "insert" : [ "insert" ],
    "shift" : [ "shift" ],
    "alu" : [ 
        "add", "sub", "mul", "longmul", "div", "mod", 
        "and", "or", "xor", "nor"
    ]
}

# Defining a set of operand tokens (excluding instructions)
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

# Returns a function to parse token with a specified type
def parse_token(token_type : str) -> int:

    def parser(token : str) -> int:
        if token.lower() not in token_set[token_type]:
            raise Exception(f"Unrecognized {token_type} '{token}'")
        else:
            return token_set[token_type].index(token.lower())
    
    return parser

# Returns a function to parse immediate valuue with the specified bitsize limitation
def parse_imm(bit_size : int):

    def parser(token : str) -> int:
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
    
    return parser

# Defining how each types of instruction recieve operands
# Key   : Instruction type
# Value : A list of parser functions specific to that function type
operands = {
    "cond" : [ 
        parse_token("register"), # Rd   - Destination Register
        parse_token("register"), # Rn   - Input Register 1
        parse_token("condition") # CND  - Condition
    ],
    "memory" : [ 
        parse_token("register"), # Rd   - Destination Register
        parse_token("register"), # Rn   - Address
        parse_imm(4)             # Imm4 - Post Addressing
    ],
    "insert" : [ 
        parse_token("register"), # Rd   - Destination Register
        parse_imm(8)             # Imm8 - Immediate value to insert
    ],
    "shift" : [ 
        parse_token("register"), # Rd   - Destination Register
        parse_token("shift-op"), # Op   - Shifting operation
        parse_token("register")  # Rm   - Distance to shift
    ],
    "alu" : [ 
        parse_token("register"), # Rd - Destination Register
        parse_token("register"), # Rn - Input Register 1
        parse_token("register"), # Rm - Input Register 2
    ]
}

