# Add the parent directory to the Python path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simplic.microcontroller import SimplicMicrocontroller
import random, math

filename = "test\sample.hex"

if __name__ == '__main__':

    mc = SimplicMicrocontroller()
    mc.load_program(filename)
    mc.run()
