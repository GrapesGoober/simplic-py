from simplic import SimplicVM, SimplicIR, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    hexfile = "test_codes\\fib.hex"
    
    from test_codes.IRfib import fib_ir_code
    ir = SimplicIR(fib_ir_code['fibbonaci'])
    ir.map_variables(fib_ir_code['fibbonaci'][0])
    ir.compile_function('fibbonaci')

    asm = SimplicAsm()
    asm.from_list(ir.asm)
    asm.compile(hexfile)
    # handle error using
    # error_print(asmfile, asm.iter, e.message)

    vm = SimplicVM()
    vm.load_program(hexfile)
    vm.run()

