import assembler, intelhex, os

def to_hexfile(asm_filepath : str) -> None:

    bytecodes = []
    with open(asm_filepath, mode = "r") as asm_file:
        for asm_line in asm_file:
            # remove comments
            asm_line = asm_line.strip().split("//")[0]
            if asm_line == "": continue
            
            # start parsing
            bincode = assembler.parse_line(asm_line)

            # intel hex format expects a single byte for each entries
            bytecodes.append(bincode >> 8)
            bytecodes.append(bincode & 0xFF)

    hex_filepath = os.path.splitext(asm_filepath)[0] + ".hex"
    ih = intelhex.IntelHex()
    ih.fromdict({ i: v for i, v, in enumerate(bytecodes) })
    ih.tofile(hex_filepath, "hex")
    


