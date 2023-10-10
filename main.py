import sys, assembler

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception("Requires second argument for file path")
    
    assembler.to_hexfile(sys.argv[1])

