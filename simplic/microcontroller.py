class SimplicMicrocontroller:

    def __init__(self, word_size: int = 16) -> None:
        self.WORDSIZE = word_size
        self.MASK = 2 ** word_size - 1
        self.instructions = {i: 0 for i in range(2 ** word_size)}
        self.memory = {i: 0 for i in range(2 ** word_size)}
        # setting up memory mapped registers
        self.memory[0x0] = 0            # PC - Program Counter
        self.memory[0x1] = 0            # A - Accumulator 
        self.memory[0x2] = 0            # GP - General Pointer 
        self.memory[0x3] = self.MASK    # SP - Stack Pointer

    def load_program(self, filename: str) -> None:
        with open(filename, 'r') as f:
            instructions = f.read().split()
            for i, v in enumerate(instructions):
                v = int(v, 16)
                if i > self.MASK or v > 0xFF:
                    raise Exception("Can't load program; exceeded size limit")
                self.instructions[i] = v

    def execute(self) -> None:
        instruction = self.instructions[self.memory[0x0]]
        opcode, immediate = instruction >> 5, instruction & 0x1F

        match opcode:
            case 0x1: # insert value into either accumulator or pointer
                pass

        self.memory[0x0] = self.memory[0x0] + 1 & self.MASK

    def run(self) -> None:
        while self.memory[0x0] < 100:
            self.execute()


        
