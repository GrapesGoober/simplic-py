from simplic import SimplicVM, SimplicIR, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    from test_codes.IRtests import fibbonaci
    ir = SimplicIR(fibbonaci, 'fibbonaci')
    asmcode = ir.compile()

    asm = SimplicAsm()
    asm.from_list(asmcode)
    bytecodes = asm.compile()
    # handle error using
    # error_print(asmfile, asm.iter, e.message)

    vm = SimplicVM()
    vm.from_list(bytecodes)
    vm.run()

