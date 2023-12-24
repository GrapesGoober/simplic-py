from simplic import SimplicVM, assembler

if __name__ == '__main__':

    hexfile = "test_codes\\fib.hex"

    # # compiling asm to file
    # source = "test_codes\\fib.asm"
    # assembler.file_to_file(source, hexfile)

    # vm = SimplicVM()
    # vm.load_program(hexfile)
    # vm.run()

    k = input()
    match k:
        case 'a': print('a')
        case 'b': print('b')
        case k if k != 'c': print('c')

