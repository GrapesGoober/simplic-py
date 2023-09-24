instructions = [
    # General purpose instructions
    "move", "cadd", "load", "store", "insert", 
    # Arithmatic instructions
    "shift", "add", "sub", "mul", "longmul", "divide", "mod", 
    # Logic instructions
    "and", "or", "xor", "nor" 
]

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
