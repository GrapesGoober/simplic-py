import aofs_mnemonics

instructions = [
    # Conditional instructions
    ("move", "cond" ), ("cadd", "cond" ),
    
    # Memory instructions, with 4-bit post indexing
    ("load", "memory" ), ("store", "memory" ),
    
    # Insert instruction with 8-bit immediate
    ("insert", "insert" ),
    
    # ALU instructions
    ("shift", "alu" ),
    ("add", "alu" ),		("sub", "alu" ),
    ("mul", "alu" ),		("longmul", "alu" ),
    ("divide", "alu" ), 	("mod", "alu" ),
    ("and", "alu" ), 		("or", "alu" ),
    ("xor", "alu" ),		("nor", "alu" )
]

operands = {
	"cond" : [ parse_reg, parse_cond ],
    "memory" : [ parse_reg, parse_imm4 ],
    "insert" : [ parse_imm8 ],
    "alu" : [ parse_reg, parse_reg, parse_reg ]
}


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

