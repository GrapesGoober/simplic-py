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
    asm = { "start": [] }
    current_label = "start"
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            
            # read line
            line = line.lower().strip().split('#')[0]
            if not line: continue

            # capture current label
            if ':' in line:
                assert line[-1] == ':', f"Line {i}, Expect only a colon after label"
                assert len(line.split()) == 1, f"Line {i}, Expect only 1 label"
                current_label = line[:-1]
                continue

            # split code into individual tokens
            assert len(line.split()) == 2, f"Line {i}, Expect identifier followed by value"
            tokens = line.split()
            
            # parse
            if current_label not in asm:
                asm[current_label] = []

            asm[current_label].append(tokens)
            
    return asm

def asm_to_hex(source: str, destination: str) -> None:
    import json
    asm = asm_to_dict(source)
    print(json.dumps(asm, indent=4))
                
