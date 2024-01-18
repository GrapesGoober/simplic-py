from simplic import SimplicVM, SimplicIR, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    from test_codes.IRtests import func_main, func_add_ten, fibbonaci
    ir = SimplicIR(func_main, 'func_main')
    asmcode = ir.compile()
    # ir = SimplicIR(func_add_ten, 'func_add_ten')
    # asmcode += ir.compile()

    
    asm = SimplicAsm()
    asm.from_list(asmcode)
    bytecodes = asm.compile()
    
    # handle error using
    # error_print(asmfile, asm.iter, e.message)
    [print(l) for l in asmcode]
    [print(f"{b:02x}", end=' ') for b in bytecodes]

    vm = SimplicVM()
    vm.from_list(bytecodes)
    vm.run()

    # import subprocess
    # # Step 2: Executing the Exe Program
    # exe_path = "test_codes\\test.exe"
    # process = subprocess.Popen([exe_path, "a", "b", "c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # # Step 3: Reading Continuous Output from the Exe Program
    # while True:
    #     output = process.stdout.readline()
    #     if output == '' and process.poll() is not None:
    #         break
    #     if output:
    #         # Process the output as needed
    #         print("Output:", output.strip())

    # # Wait for the process to finish
    # process.wait()

