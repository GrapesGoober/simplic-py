from .error_print import ErrorPrint

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
    asm, jump_points = {}, []
    current_label, current_PC = "start", 0
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            report = ErrorPrint(i, source).report

            # read line and exclude comments
            line = line.lower().strip().split('#')[0]
            if not line: continue

            # capture current label
            if ':' in line:
                if len(line.split()) != 1: 
                    report("Expect only one name for label")
                current_label = line[:-1]
                if current_label not in asm:
                    asm[current_label] = [f"at PC = {current_PC}"]
                continue

            # split code into individual tokens and parse
            tokens = line.split()
            if len(tokens) != 2:
                report("Expect only an opcode and immediate")
            if tokens[0] == INSTRUCTIONS[6]: 
                current_PC += 3
            else: current_PC += 1

            asm[current_label].append(tokens)
            
    return asm

def asm_to_hex(source: str, destination: str) -> None:
    import json
    asm = asm_to_dict(source)
    print(json.dumps(asm, indent=4))
                
