
# Add the parent directory to the Python path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simplic.microcontroller.memory import Memory

import json, random
def generate_random_dict():
    bytes_dict = {i: random.randint(0, 2**16) for i in range(300)}
    with open("test\sample.json", 'w') as f:
        json.dump(bytes_dict, f, indent=2)

if __name__ == '__main__':

    # generate_random_dict()

    m = Memory("test\sample.json")
    print(m.read(296))