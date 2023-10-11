token_set = {
    "instruction" : [
        # General purpose instructions
        "cmove", "countlz", "load", "store", "insert", 
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
        "negative",
        "positive",
        "carry",
        "notcarry",
        "overflow",
        "notoverflow",
        "usmaller",     # unsigned, Z or C
        "uhigher",      # unsigned, !Z and !C
        "smaller",      # signed, N != V
        "higher",       # signed, !Z and (N == V)
        "smallerequal", # signed, Z or (N != V)
        "higherequal",  # signed, N == V
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
