from .memory import Memory

class SimplicCore:

    def __init__(self, word_size: int = 16) -> None:
        self.WORDSIZE = word_size
        self.MASK = 2 ** word_size - 1

        self.PC, self.ACC, self.P = 0, 0, 0
        self.BSP = self.MASK # call stack starts counting from 0xFF..FF, unlike heap
        self.flags = {}
        self.ctrl_bus = {}
    
    def execute(self, instructionMemory: Memory, mainMemory: Memory):

        # unpack and decode the instruction word
        instruction = instructionMemory.read(self.PC)
        opcode = (instruction >> 12) & 0xF
        control = (instruction >> 8) & 0xF
        imm8 = (instruction >> 0) & 0xFF
        self.decode(opcode, control)

        # specify addressing mode using C1 control bit, then read from memory
        usePointer = self.ctrl_bus["C1"]
        address = self.P + imm8 if usePointer else self.BSP - imm8
        memData = mainMemory.read(address & self.MASK)

    def decode(self, opcode: int, control: int) -> None:

        # conditions bits (for jump) are identical as the control bits
        self.ctrl_bus["COND"] = control

        # certain control bits can be assigned without decoding
        self.ctrl_bus["C0"] = (control >> 3) & 0b1
        self.ctrl_bus["C1"] = (control >> 2) & 0b1
        self.ctrl_bus["SFT2"] = (control >> 2) & 0b11

        # decode memory write enable for STORE instruction
        self.ctrl_bus["MEM EN"] = opcode == 0x2

        # decode the flag control signals (c & v flags only enabled for ADD/SUB instructions)
        f = (control >> 1) & 0b1
        self.ctrl_bus["ZN EN"] = f and opcode >= 0x5
        self.ctrl_bus["CV EN"] = f and opcode in (0x7, 0x8) 

        # decode immediate control bit
        i = control & 0b1
        self.ctrl_bus["IMM8"] = (i and opcode >= 0x6) or opcode in (0x0, 0x3)

        # decode destination select bit

        # decode jump enable signal
        self.ctrl_bus["JMP EN"] = opcode == 0x4

        
