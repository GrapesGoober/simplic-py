
class ErrorPrint:
    def __init__(self, lineNo: int, filename: str) -> None:
        self.lineNo = lineNo
        self.filename = filename

    def report(self, message: str) -> None:
        print()
        with open(self.filename, 'r') as f:
            for i, line in enumerate(f):
                if self.lineNo - 3 < i < self.lineNo + 2: 
                    print(f"  {i+1}:\t{line}", end='')
        print()
        print(f"Error at line {self.lineNo+1}:", message)
        print()
        exit(-1)