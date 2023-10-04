import aofs, intelhex, os

def to_hexfile(asm_filepath : str) -> None:

    bincodes_list = []
    with open(asm_filepath, mode = "r") as asm_file:
        for asm_line in asm_file:
            asm_line = asm_line.strip().split("//")[0]
            if asm_line == "": continue
            bincode = aofs.parse_line(asm_line)
            bincodes_list.append(bincode >> 8)
            bincodes_list.append(bincode & 0xFF)

    hex_filepath = os.path.splitext(asm_filepath)[0] + ".hex"
    ih = intelhex.IntelHex()
    bincodes_dict = { i: v for i, v, in enumerate(bincodes_list) }
    ih.fromdict(bincodes_dict)
    ih.tofile(hex_filepath, "hex")
    


