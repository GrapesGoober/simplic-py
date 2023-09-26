import aofs_mnemonics

instructions = [
    # Conditional instructions
    ("move", 		parse_Rd, parse_Rn, parse_CND ),
    ("cadd", 		parse_Rd, parse_Rn, parse_CND ),
    
    # Memory instructions, with 4-bit post indexing
    ("load", 		parse_Rd, parse_Rn, parse_imm4 ),
    ("store", 		parse_Rd, parse_Rn, parse_imm4 ),
    
    # Insert instruction with 8-bit immediate
    ("insert",		parse_Rd, parse_imm8 ),
    
    # ALU instructions
    ("shift", 		parse_Rd, parse_Rn, parse_Rm ),
    ("add", 		parse_Rd, parse_Rn, parse_Rm ),
    ("sub", 		parse_Rd, parse_Rn, parse_Rm ),
    ("mul", 		parse_Rd, parse_Rn, parse_Rm ),
    ("longmul",		parse_Rd, parse_Rn, parse_Rm ),
    ("divide", 		parse_Rd, parse_Rn, parse_Rm ),
    ("mod", 		parse_Rd, parse_Rn, parse_Rm ),
    ("and", 		parse_Rd, parse_Rn, parse_Rm ),
    ("or", 			parse_Rd, parse_Rn, parse_Rm ),
    ("xor", 		parse_Rd, parse_Rn, parse_Rm ),
    ("nor" 			parse_Rd, parse_Rn, parse_Rm )
]


def asmfile_to_hexfile(filename : str) -> None:
    with open(filename, mode = "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("//"): continue
            print(hex(parse_line(line)))

def parse_line(asmline : str) -> int:
    tokens = asmline.split()

    if tokens[0].lower() not in aofs_mnemonics.instructions:
        raise Exception(f"Unrecognized instruction: {tokens[0]}")
    bincode = aofs_mnemonics.instructions.index(tokens[0].lower()) << 12
    
    if tokens[1].lower() not in aofs_mnemonics.registers:
        raise Exception(f"Unrecognized Rd register: {tokens[0]}")
    bincode = aofs_mnemonics.registers.index(tokens[1].lower()) << 8

