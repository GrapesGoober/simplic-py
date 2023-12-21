class SimplicMicrocontroller:

    def __init__(self) -> None:
        self.instructions   = {i: 0 for i in range(0x10000)}
        self.memory         = {i: 0 for i in range(0x10000)}
        self.memory[2]      = 0xFFFF    # Stack Pointer count reverses

    def load_program(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for i, v in enumerate(f.read().split()):
                self.instructions[i] = int(v, 16) & 0xFF

    def execute(self) -> None:
        mem, instr = self.memory, self.instructions
        PC, A, SP = mem[0], mem[1], mem[2]
        opcode, I = instr[PC] >> 4, instr[PC] & 0xF
        V = mem[SP - I]

        match opcode:
            case 0x0:                   # Set
                V = instr[PC + 1] << 8 | instr[PC + 2]
                PC += 2
            case 0x1:                   # If
                Z, N = A == 0, A >> 15
                dest = instr[PC + 1] << 8 | instr[PC + 2]
                # always, less, high, equal, nequal, lesseq, higheq
                cond = [True, N, not Z and not N, Z, not Z, N or Z, not N]   
                PC = dest if cond[I] else PC + 2
            case 0x2:                   # Stack - Increment/Decrement SP 
                SP += I | 0xFFF0 if I >> 3 else I            
            case 0x3: A = V             # Load
            case 0x4: V = A             # Store
            case 0x5: A = mem[V]        # Load Memory
            case 0x6: mem[V] = A        # Store Memory
            case 0x7: A +=  V           # Add
            case 0x8: A -=  V           # Sub
            case 0x9: A <<= V           # LSL
            case 0xA: A >>= V           # LSR
            case 0xB: A *=  V           # Mul
            case 0xC: A //= V           # Div
            case 0xD: A &=  V           # And
            case 0xE: A |=  V           # Or
            case 0xF: A =  ~V           # Not           

        mem[0]      = PC + 1    & 0xFFFF
        mem[1]      = A         & 0xFFFF
        mem[2]      = SP        & 0xFFFF
        mem[SP - I] = V         & 0xFFFF

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



        
