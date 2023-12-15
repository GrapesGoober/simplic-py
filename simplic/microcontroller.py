class SimplicMicrocontroller:

    def __init__(self, word_size: int = 16) -> None:
        self.WORDSIZE = word_size
        self.MASK = 2 ** word_size - 1
        self.instructions = {i: 0 for i in range(2 ** word_size)}
        self.memory = {i: 0 for i in range(2 ** word_size)}
        self.PC, self.ACC, self.P, self.BSP = 0, 0, 0, self.MASK

    def load_program(self, filename: str) -> None:
        with open(filename, 'r') as f:
            instructions = f.read().split()
            for i, v in enumerate(instructions):
                v = int(v, 16)
                if i > self.MASK or v > 0xFFFF:
                    raise Exception("Can't load program; exceeded size limit")
                self.instructions[i] = v

    def execute(self) -> None:
        instruction = self.instructions[self.PC]
        opcode = instruction >> 12

        match instruction:
            case 0x1:
                pass

        self.PC += 1


        
