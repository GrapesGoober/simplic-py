class SimplicIRParser:
    def from_file(self, filename: str) -> list[tuple]:
        with open(filename, 'r') as file:
            for line in file:
                print(line, end='')
