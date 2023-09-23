import aofs_mnemonics

def asmfile_to_hexfile(filename : str) -> None:
    with open(filename, mode = "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("//"): continue
            print(hex(parse_line(line)))

def parse_line(asmline : str) -> int:
    tokens = asmline.split()

    instr_token = tokens[0]
    if instr_token.lower() not in aofs_mnemonics.instructions:
        raise Exception(f"Unrecognized instruction: {instr_token}")
    bincode = aofs_mnemonics.instructions.index(instr_token.lower()) << 12
    
    rd_token = tokens[1]
    if rd_token.lower() not in aofs_mnemonics.registers:
        raise Exception(f"Unrecognized Rd register: {rd_token}")
    bincode = aofs_mnemonics.registers.index(rd_token.lower()) << 8

    return bincode

    # parse each type differently
    
