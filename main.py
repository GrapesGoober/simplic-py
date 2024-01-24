from simplic import SimplicVM, SimplicIR, SimplicAsm, SimplicErr, error_print

if __name__ == '__main__':

    from test_codes.IRtests import func_main, func_add_ten, fibbonaci
    ir = SimplicIR(fibbonaci, 'fibbonaci')
    asmcode = ir.compile()
    # ir = SimplicIR(func_add_ten, 'func_add_ten')
    # asmcode += ir.compile()
    
    asm = SimplicAsm()
    asm.from_list(asmcode)
    bytecodes = asm.compile()
    
    # # write to file
    # with open("test_codes\\test.hex", 'w') as f:
    #     for i, bytecode in enumerate(bytecodes):
    #         f.write(f'{bytecode:02x} ' + ('\n' if (i + 1) % 16 == 0 else ''))

    # # handle error using
    # # error_print(asmfile, asm.iter, e.message)
    # [print(l) for l in asmcode]
    # [print(f"{b:02x}", end=' ') for b in bytecodes]

    import subprocess
    exe_path = "simplic\\virtualmachine\\virtualmachine.exe"
    process = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    process.stdin.write(' '.join([f'{i:02x}' for i in bytecodes]))
    process.stdin.close() 

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Process the output as needed
            print(output.strip())

    # Wait for the process to finish
    process.wait()

