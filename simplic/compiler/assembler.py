
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
    asm = {
        "variables": {},
        "start": []
    }
    current_label = "start"
    with open(source, 'r') as f:
        for line in f:
            
            # read line
            line = line.lower().strip().split('#')[0]
            if not line: continue

            # capture current label
            if ':' in line:
                assert line[-1] == ':', "Expect only a colon after label"
                assert len(line.split()) == 1, "Expect a single label at a time"
                current_label = line[:-1]
                continue

            # split code into individual tokens
            assert len(line.split()) == 2, "Expect identifier followed by value"
            tokens = line.split()
            
            # parse
            if current_label not in asm:
                asm[current_label] = []

            if current_label == "variables":
                asm["variables"][tokens[0]] = literal_to_int(tokens[1])
            else:
                asm[current_label].append(tokens)

    return asm

def asm_to_hex(source: str, destination: str) -> None:
    import json
    asm = asm_to_dict(source)
    print(json.dumps(asm, indent=4))
                
