import aofs_mnemonics

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
    
