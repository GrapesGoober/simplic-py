from simplic import SimplicIR, SimplicAsm, SimplicErr, error_print

def compile() -> list[int]:
    from test_codes.IRtests import func_main, func_add_ten, fibbonaci, add_til_ten
    
    ir = SimplicIR(func_main, 'func_main')
    asmcode = ir.compile()
    ir = SimplicIR(add_til_ten, 'add_til_ten')
    asmcode += ir.compile()
    
    # # handle error using
    # # error_print(asmfile, asm.iter, e.message)
    # [print(l) for l in asmcode]
    # [print(f"{b:02x}", end=' ') for b in bytecodes]
    
    asm = SimplicAsm()
    asm.from_list(asmcode)
    return asm.compile()
    
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
            print(output.strip())

    # Wait for the process to finish
    process.wait()
    
if __name__ == '__main__':
    bytecodes = compile()
    run_vm(bytecodes)
    

