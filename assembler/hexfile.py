import assembler, intelhex, os

def to_hexfile(asm_filepath : str) -> None:

    asmcodes = []
    with open(asm_filepath, mode = "r") as asm_file:
        asmcodes = asm_file.readlines()
    bytecodes = assembler.parse(asmcodes)

    hex_filepath = os.path.splitext(asm_filepath)[0] + ".hex"
    ih = intelhex.IntelHex()
    ih.fromdict(bytecodes)
    ih.tofile(hex_filepath, "hex")
    


