import aofs_mnemonics

instructions = [
    # Conditional instructions
    ("move", 	parse_conditional_operands),
    ("cadd", 	parse_conditional_operands),
    
    # Memory instructions, with 4-bit immediate post indexing
    ("load", 	parse_indexing_operands),
    ("store", 	parse_indexing_operands),
    
    ("insert",	parse_insert_operands),
    
    # ALU instructions
    ("shift", 	parse_alu_operands),
    ("add", 	parse_alu_operands),
    ("sub", 	parse_alu_operands),
    ("mul", 	parse_alu_operands),
    ("longmul",	parse_alu_operands),
    ("divide", 	parse_alu_operands),
    ("mod", 	parse_alu_operands),
    ("and", 	parse_alu_operands),
    ("or", 		parse_alu_operands),
    ("xor", 	parse_alu_operands),
    ("nor" 		parse_alu_operands)
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

    # parse each type differently
    
def parse_conditional_operands(tokens : list) -> int:
    pass
    
def parse_indexing_operands(tokens : list) -> int:
    pass
    
def parse_insert_operands(tokens : list) -> int:
    pass
    
def parse_alu_operands(tokens : list) -> int:
	pass
