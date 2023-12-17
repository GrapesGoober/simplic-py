
class ErrorPrint:
    def __init__(self, lineNo: int, filename: str) -> None:
        self.lineNo = lineNo
        self.filename = filename

    def report(self, message: str):
        print()
        with open(self.filename, 'r') as f:
            for i, line in enumerate(f):
                if self.lineNo - 3 < i < self.lineNo + 2: 
                    print(f"  {i+1}:\t{line}", end='')
        print()
        print(f"Error at line {self.lineNo+1}:", message)
        print()
        exit(-1)
## 
# IDEA for error checking system!
# Pretty print class, which can be reinstantiated every iteration
# 
#   for i, v in enumerate(f):
#       p = PrettyPrint(i, source)
#
#       p.check(x == y, "Expect x and y to be equals")
#
#   the class encapsulates those two info, which can then be opened later (circumvent the SEEK_CUR problem)
#

