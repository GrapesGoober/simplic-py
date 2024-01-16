class SimplicVM:

    def __init__(self) -> None:
        self.instr  = {i: 0 for i in range(0x10000)}
        self.mem    = {i: 0 for i in range(0x10000)}
        self.mem[2] = 0xFFFF    # Stack Pointer count reverses

    # load program from hex file
    def from_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for i, v in enumerate(f.read().split()):
                self.instr[i] = int(v, 16) & 0xFF
    
    # load program from a list of bytecodes
    def from_list(self, bytecodes: list[int]) -> None:
        for i, v in enumerate(bytecodes): self.instr[i] = v

    # execute the current instruction
    def execute(self) -> None:
        mem, instr = self.mem, self.instr
        PC, A, SP = mem[0], mem[1], mem[2]
        OP, I = instr[PC] >> 4, instr[PC] & 0xF
        V = mem[SP - I]
        
        I16 = instr[PC + 1] << 8 | instr[PC + 2]
        memOUT = None
        Z, N = A == 0, A >> 15
        cond = [True, N, not (Z or N), Z, not Z, N or Z, not N]

        match OP:
            case 0x0: A = V             # Load
            case 0x1: V = A             # Store
            case 0x2: A = mem[V]        # Load Memory
            case 0x3: memOUT = A        # Store Memory
            case 0x4: A +=  V           # Add
            case 0x5: A -=  V           # Sub
            case 0x6: A <<= V           # LSL
            case 0x7: A >>= V           # LSR
            case 0x8: A *=  V           # Mul
            case 0x9: A //= V           # Div
            case 0xA: A &=  V           # And
            case 0xB: A |=  V           # Or
            case 0xC: A =  ~V           # Not  
            case 0xD:                   # Stack slide
                if I: SP += 0xFFF0
                else: SP += 0x10
            case 0xE:                   # Set value to V
                V, PC = I16, PC + 2     
            case 0xF:                   # If condition
                if cond[I]: PC = I16 - 1 
                else:       PC += 2

        mem[0]      = PC + 1    & 0xFFFF
        mem[1]      = A         & 0xFFFF
        mem[2]      = SP        & 0xFFFF
        mem[SP - I] = V         & 0xFFFF
        if memOUT != None: 
            mem[V]  = memOUT    & 0xFFFF

    # run program
    def run(self) -> None:
        while self.mem[0x0] < 0xFFFF:
            self.execute()
        print("internal state")
        print(f"  PC\t{self.mem[0]}")
        print(f"  A\t{self.mem[1]}")
        print(f"  SP\t{self.mem[2]}")

        print("stack")
        for i in range(0x10):
            P = self.mem[2]
            print(f"  {i:0x}\t{self.mem[P - i]}")

            



        
