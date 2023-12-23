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
    assembler.file_to_file(source, destination)

def count_lz():
    clz = lambda: len(f"{V1:016b}".split('1')[0])

    A = 0
    V1 = 0x00F1
    A = clz()
    print(f"{V1:016b}")

    V2 = 0x0001
    A -= V2
    V3 = A
    A = V2
    A <<= V3

    V4 = A
    A = ~V4 & 0xFFFF
    A &= V1
    print(f"{A:016b}")

if __name__ == '__main__':
    assemble_instructions()
    run_microcontroller()
    # count_lz()

