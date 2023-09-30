token_set = {
    "instruction" : [
        # General purpose instructions
        "move", "cadd", "load", "store", "insert", 
        # Arithmatic instructions
        "shift", "add", "sub", "mul", "longmul", "divide", "mod", 
        # Logic instructions
        "and", "or", "xor", "nor" 
    ],
    "register" : [
        # A special zero value for resetting registers
        "zero",
        # General purpose registers
        "r1", "r2", "r3", "r4",
        "r5","r6", "r7", "r8", "r9",
    
        # Dedicated registers
        "buffer",   # Buffer register   - immediate values
        "return",   # Return register   - values from previous call
        "stack",    # Stack pointer     - pointer to base of the stack
        "address",  # Address register  - for memory and jumps
        "link",     # Link register     - keep progc addresses to return to
        "progc"     # Program counter   - current instruction to execute
    ],
    "condition" : [
        "zero",
        "notzero",
        "carry",
        "notcarry",
        "negative",
        "positive",
        "overflow",
        "notoverflow",
        "ulesser",      # unsigned, Z or C
        "ugreater",     # unsigned, !Z and !C
        "lesser",       # signed, N != V
        "greater",      # signed, !Z and (N == V)
        "lesserequal",  # signed, Z or (N != V)
        "greaterequal", # signed, N == V
        "flagclear",    # Z and !N and !C and !V
        "always"
    ],
    "shift operation" :  [
        "left",
        "right",
        "arith",
        "rotate"
    ]
}
