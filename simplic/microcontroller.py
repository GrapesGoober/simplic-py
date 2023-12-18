class SimplicMicrocontroller:

    def __init__(self, word_size: int = 16) -> None:
        self.MASK           = 2 ** word_size - 1
        self.instructions   = {i: 0 for i in range(2 ** word_size)}
        self.memory         = {i: 0 for i in range(2 ** word_size)}
        self.memory[2]      = self.MASK    # Stack Pointer count reverses

    def load_program(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for i, v in enumerate(f.read().split()):
                self.instructions[i] = int(v, 16) & 0xFF

    def execute(self) -> None:
        mem, instr = self.memory, self.instructions
        PC, A, P = mem[0], mem[1], mem[2]
        opcode, I = instr[PC] >> 4, instr[PC] & 0xF
        V = mem[P - I]

        def set_data():
            data = instr[PC + 1]
            data = data << 8 | instr[PC + 2]
            PC += 2
            return data
        
        def countlz():
            bin = f"{V:016b}"
            count = len(bin.split('1')[0])
            return count

        match opcode:
            case 0x0: A = V             # Load
            case 0x1: V = A             # Store
            case 0x2: A = mem[V]        # Load Pointer
            case 0x3: mem[V] = A        # Store Pointer
            case 0x4: V = set_data()    # Set
            case 0x5: pass              
            case 0x6: pass              
            case 0x7: pass             
            case 0x8: A = countlz()
            case 0x9: A +=  V           # Add
            case 0xA: A -=  V           # Sub
            case 0xB: A *=  V           # Mul
            case 0xC: A //= V           # Div
            case 0xD: A &=  V           # And
            case 0xE: A |=  V           # Or
            case 0xF: A =  ~V           # Not           

        mem[0]      = PC + 1    & self.MASK
        mem[1]      = A         & self.MASK
        mem[2]      = P         & self.MASK
        mem[P - I]  = V         & self.MASK

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



        
