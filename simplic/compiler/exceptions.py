
class AsmException(Exception):
    def __init__(self, message: str, cursor: tuple = None) -> None:
        self.message = message
        self.cursor = cursor
        super().__init__(self.message)
    
    def print(self) -> None:
        if self.cursor != None:
            err_string = "\n"
            source, line_num = self.cursor
            with open(source, 'r') as f:
                for i, line in enumerate(f):
                    if line_num - 3 < i < line_num + 2: 
                        err_string += f"  {i+1}:\t{line}"
            err_string += f"Error at line {0 + 1}: {self.message}\n"
            print(err_string)
        else:
            print(self.message)