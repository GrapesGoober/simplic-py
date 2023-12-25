from simplic import SimplicVM, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    hexfile = "test_codes\\fib.hex"

    # compiling asm to file
    asmfile = "test_codes\\fib.asm"
    asm = SimplicAsm()
    try:
        asm.from_file(asmfile)
        asm.compile(hexfile)
    except SimplicErr as e:
        error_print(asmfile, asm.iter, e.message)
        exit(-1)

    vm = SimplicVM()
    vm.load_program(hexfile)
    vm.run()

