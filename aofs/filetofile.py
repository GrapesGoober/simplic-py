import aofs

def to_hexfile(filename : str) -> None:
    with open(filename, mode = "r") as file:
        for line in file:
            line = line.strip().split("//")[0]
            if line == "": continue
            print(hex(aofs.parse_line(line)))


