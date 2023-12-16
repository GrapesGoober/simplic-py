class SimplicMicrocontroller:

    def __init__(self, word_size: int = 16) -> None:
        self.WORDSIZE = word_size
        self.MASK = 2 ** word_size - 1
        self.instructions = {i: 0 for i in range(2 ** word_size)}
        self.memory = {i: 0 for i in range(2 ** word_size)}
        # setting up memory mapped registers
        self.memory[0] = 0            # PC - Program Counter
        self.memory[1] = 0            # A  - Accumulator 
        self.memory[2] = self.MASK    # P  - Stack Pointer (count reverse)

    def load_program(self, filename: str) -> None:
        with open(filename, 'r') as f:
            instructions = f.read().split()
            for i, v in enumerate(instructions):
                v = int(v, 16)
                if i > self.MASK or v > 0xFF:
                    raise Exception("Can't load program; exceeded size limit")
                self.instructions[i] = v

    def execute(self) -> None:
        mem = self.memory
        instruction = self.instructions[mem[0x0]]
        opcode, I = instruction >> 4, instruction & 0xF
        A = mem[1] & self.MASK
        P = mem[2] & self.MASK
        V = mem[P - I] & self.MASK
        PC = mem[0] & self.MASK

        match opcode:
            case 0x0: A = V             # Load
            case 0x1: V = A             # Store
            case 0x2: V = mem[V]        # Load Pointer
            case 0x3: A = A << 4 | I    # Insert
            case 0x4: PC += A == V      # Compare
            case 0x5: PC = V - 1        # Jump
            case 0x9: A += V            # Add

        mem[1] = A & self.MASK
        mem[2] = P & self.MASK
        mem[P - I] = V & self.MASK
        mem[0] = PC + 1 & self.MASK

    def run(self) -> None:
        while self.memory[0x0] < 0xFFFF:
            self.execute()
        print("internal state")
        for i in range(3):
            print(f"{i}\t{self.memory[i]}")

        print("stack")
        for i in range(0xF):
            P = self.memory[2]
            print(f"{i:0x}\t{self.memory[P - i]}")



        
