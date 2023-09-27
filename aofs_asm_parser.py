

def parse_reg(token : str) -> int:
    registers = [
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
    ]

def parse_cond(token : str) -> int:
    conditions = [

    ]

def parse_imm4(token : str) -> int:
    pass

def parse_imm8(token : str) -> int:
    pass

def parse_sft(token : str) -> int:
    shift_type = [
        "left",
        "right",
        "arith",
        "rotate"
    ]

# Retrieve the instruction index and a set of functions to parse the operands
def parse_instr(token : str) -> int:
    # Define a set of instruction types and their instructions
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
    # Defining the set of functions to parse operands for each instruction type
    operands = {
        "cond" : [ parse_reg, parse_reg, parse_cond ],
        "memory" : [ parse_reg, parse_reg, parse_imm4 ],
        "insert" : [ parse_reg, parse_imm8 ],
        "shift" : [ parse_reg, parse_sft, parse_reg ],
        "alu" : [ parse_reg, parse_reg, parse_reg, parse_reg ]
    }




