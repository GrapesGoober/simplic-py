# Add the parent directory to the Python path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simplic.microcontroller.core import SimplicCore

if __name__ == '__main__':
    # c = SimplicCore()

    # c.execute(0xFFFF, 0xFFFF)
    # print(c.ctrl_bus)

    match 2:
        case 1:
            result = "A"
        case 2:
            result = "B"
        case 3:
            result = "C"

    print(result)
