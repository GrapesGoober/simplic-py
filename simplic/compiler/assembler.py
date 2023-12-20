from .error_print import ErrorPrint
import re

INSTRUCTIONS = [
    "load", "store", "loadp", "storep", "insert", "compare", "jump", "clz",
    "?", "add", "sub", "mul", "div", "and", "or", "not"
]

def literal_to_int(token: str) -> int:
    BITSIZE = 4
    try:
        if token.startswith("0x"): 
            result = int(token, 16)
        elif token.startswith("0b"): 
            result = int(token, 2)
        else: 
            result = int(token, 10)
    except ValueError:
        raise Exception(f"Invalid immediate syntax.")

    assert result.bit_length() < BITSIZE, "Immediate value too big for {BITSIZE} bits."
    return result

def asm_to_dict(source: str) -> dict:
    asm, labels, address = [], {}, 0
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            report = ErrorPrint(i, source).report

            # read line and exclude comments
            line = line.lower().strip().split('#')[0]
            if not line: continue

            # capture current label
            if ':' in line:
                match = re.match(r'^\s*(\w\w*)\s*:\s*$', line)
                if not match:
                    report("Invalid label syntax")
                l = match.group(1)
                if l in labels:
                    report(f"Duplicate label '{l}'")
                labels[l] = address
                continue

            # split code into individual tokens and parse
            tokens = line.split()
            if tokens[0] == INSTRUCTIONS[6]: 
                address += 3
            else: address += 1

            asm.append(tokens)
            
    return asm, labels

def asm_to_hex(source: str, destination: str) -> None:
    import json
    asm = asm_to_dict(source)
    print(json.dumps(asm, indent=4))
                
