# Add the parent directory to the Python path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simplic.microcontroller.memory import Memory
import random, math

filename = "test\sample.hex"
width = 16
WORDSIZE = 16

def generate_random_hex():
    with open(filename, 'w') as f:
        hex_digit = math.ceil(WORDSIZE / 4)
        for i in range(300):
            r = random.randint(0, 2**16)
            f.write(f"{r:0{hex_digit}x} ")
            if (i + 1) % width == 0:
                f.write("\n")


if __name__ == '__main__':

    #generate_random_hex()

    m = Memory()
    m.load(filename)
