# Add the parent directory to the Python path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simplic.microcontroller import SimplicMicrocontroller
import random, math

filename = "test\sample.hex"

def generate_random_hex():
    width = 16
    WORDSIZE = 8
    with open(filename, 'w') as f:
        hex_digit = math.ceil(WORDSIZE / 4)
        for i in range(300):
            r = random.randint(0, 2**WORDSIZE)
            f.write(f"{r:0{hex_digit}x} ")
            if (i + 1) % width == 0:
                f.write("\n")


if __name__ == '__main__':

    mc = SimplicMicrocontroller()
    mc.load_program(filename)
    mc.run()

    # number = 0
    # incremented = number + 0xFFFE
    # masked = incremented & 0xFFFF
    # print(masked)
