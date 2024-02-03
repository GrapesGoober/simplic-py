from simplic import SimplicIR, SimplicAsm, SimplicErr, error_print

def compile() -> list[int]:
    from test_codes.IRtests import func_main, add_til_ten, fib_iterative, fib_recursive
    
    ir = SimplicIR(func_main[0], func_main[1])
    asmcode = ir.compile()
    ir = SimplicIR(add_til_ten[0], add_til_ten[1])
    asmcode += ir.compile()
    ir = SimplicIR(fib_iterative[0], fib_iterative[1])
    asmcode += ir.compile()
    ir = SimplicIR(fib_recursive[0], fib_recursive[1])
    asmcode += ir.compile()
    
    # # handle error using
    # # error_print(asmfile, asm.iter, e.message)
    # [print(l) for l in asmcode]
    # [print(f"{b:02x}", end=' ') for b in bytecodes]
    
    sa = SimplicAsm()
    sa.from_list(asmcode)
    bytecodes = sa.compile()
    return bytecodes
    
def run_vm(bytecodes: list[int]):

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
            print(output, end='')

    # Wait for the process to finish
    process.wait()
    
if __name__ == '__main__':
    bytecodes = compile()
    run_vm(bytecodes)
    

