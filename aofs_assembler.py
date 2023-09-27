import aofs_asm_parser

def asmfile_to_hexfile(filename : str) -> None:
    with open(filename, mode = "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("//"): continue
            print(hex(parse_line(line)))

def parse_line(asmline : str) -> int:
    tokens = asmline.split()

    if tokens[0].lower() not in aofs_asm_parser.instructions:
        raise Exception(f"Unrecognized instruction: {tokens[0]}")
    bincode = aofs_asm_parser.instructions.index(tokens[0].lower()) << 12
    
    if tokens[1].lower() not in aofs_asm_parser.register_tokens:
        raise Exception(f"Unrecognized Rd register: {tokens[0]}")
    bincode = aofs_asm_parser.register_tokens.index(tokens[1].lower()) << 8

