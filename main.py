from simplic import SimplicVM, SimplicIR, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    from test_codes.IRtests import func_main, func_add_ten, fibbonaci
    ir = SimplicIR(func_main, 'func_main')
    asmcode = ir.compile()
    # ir = SimplicIR(func_add_ten, 'func_add_ten')
    # asmcode += ir.compile()

    for l in asmcode:
        [print(tok, end='\t') for tok in l]
        print()
    print()
    asm = SimplicAsm()
    asm.from_list(asmcode)
    bytecodes = asm.compile()
    # handle error using
    # error_print(asmfile, asm.iter, e.message)

    vm = SimplicVM()
    vm.from_list(bytecodes)
    vm.run()

