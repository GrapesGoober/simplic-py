# Add the parent directory to the Python path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simplic import SimplicCore

if __name__ == '__main__':
    c = SimplicCore()

    c.decode(0x0, 0b0100)
    for i, v in c.ctrl_bus.items():
        print(i, "\t", int(v))
