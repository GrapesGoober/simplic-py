from simplic import SimplicVM, assembler

if __name__ == '__main__':
    
    source = "test_codes\\fib.asm"
    destination = "test_codes\\fib.hex"
    assembler.file_to_file(source, destination)
    vm = SimplicVM()
    vm.load_program(destination)
    vm.run()

