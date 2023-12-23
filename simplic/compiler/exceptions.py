
class SimplicErr(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
def error_print(source, line_num, message) -> None:
    err_string = "\n"
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            if line_num - 3 < i < line_num + 2: 
                err_string += f"  {i+1}:\t{line}"
    print(err_string)
    print(f"Error at line {line_num + 1}: {message}", end='\n\n')