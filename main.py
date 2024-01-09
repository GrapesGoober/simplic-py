from simplic import SimplicVM, SimplicIR, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    hexfile = "test_codes\\fib.hex"
    
    from test_codes.IRfib import fibbonaci
    ir = SimplicIR(fibbonaci, 'fibbonaci')
    ir.compile()

    asm = SimplicAsm()
    asm.from_list(ir.asm)
    asm.compile(hexfile)
    # handle error using
    # error_print(asmfile, asm.iter, e.message)

    vm = SimplicVM()
    vm.load_program(hexfile)
    vm.run()

