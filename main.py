import sys, aofs_assembler

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception("Requires second argument for file path")
    
    aofs_assembler.asmfile_to_hexfile(sys.argv[1])


