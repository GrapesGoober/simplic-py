from microcontroller import SimplicMicrocontroller
from compiler import assembler

def run_microcontroller():
    filename = "simplic\\test_codes\\fib.hex"
    mc = SimplicMicrocontroller()
    mc.load_program(filename)
    mc.run()

def assemble_instructions():
    source = "simplic\\test_codes\\fib.asm"
    destination = "simplic\\test_codes\\fib.hex"
    assembler.asm_to_hex(source, destination)

if __name__ == '__main__':
    assemble_instructions()
    
