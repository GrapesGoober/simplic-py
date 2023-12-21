
def file_error_print(source: str, line_num: int, message: str):
    err_string = "\n"
    with open(source, 'r') as f:
        for i, line in enumerate(f):
            if line_num - 3 < i < line_num + 2: 
                err_string += f"  {i+1}:\t{line}"

    err_string += f"Error at line {line_num + 1}: {message}\n"
    raise Exception(err_string)

class AsmException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)