
class SimplicCore:

    def __init__(self, word_size: int = 16) -> None:
        self.WORDSIZE = word_size
        self.MASK = 2 ** word_size - 1
        self.ACC, self.BSP, self.PC = 0, 0, 0
        self.flags = {}
        self.ctrl_bus = {}
    
    def execute(self, instruction: int, memory_word: int):
        opcode = (instruction >> 12) & 0xF
        control = (instruction >> 8) & 0xF
        imm8 = (instruction >> 0) & 0xFF
        
        self.decode(opcode, control)

    def decode(self, opcode: int, control: int) -> None:
        # conditions bits (for jump) are the same as the control bits
        self.ctrl_bus["COND"] = control

        # unpack individual control bits from MSB to LSB
        self.ctrl_bus["CARRY"]  = (control >> 3) & 0b1
        self.ctrl_bus["SIGN"]   = (control >> 3) & 0b1
        self.ctrl_bus["NEG"]    = (control >> 3) & 0b1
        self.ctrl_bus["SFT"]    = (control >> 2) & 0b11
        self.ctrl_bus["BSP/P"]  = (control >> 2) & 0b1
        self.ctrl_bus["IMM8"]   = (control >> 0) & 0b1

        # decode the flag control signals (c & v flags only enabled for ADD 0x7 and SUB 0x8)
        # note that 
        f = (control >> 1) & 0b1
        self.ctrl_bus["ZN EN"] = f and opcode > 0x3
        self.ctrl_bus["CV EN"] = f and opcode in (0x7, 0x8) 
        self.ctrl_bus["CV CLEAR"] = f and opcode not in (0x7, 0x8)

        # decode operand A/P control signal

    def compute(self, opcode: int, A: int, B: int) -> None:
        match opcode:
            case 0x0:
                pass
            case 0x1:
                pass
            case 0x2:
                pass
            case 0x3:
                pass
            case 0x4:
                pass
            case 0x5:
                pass
            case 0x6:
                pass
            case 0x7: result = A + B
            case 0x8: result = A - B
            case 0x9: result = A * B
            case 0xA: result = A * B >> self.WORDSIZE
            case 0xB: result = A // B
            case 0xC: result = A % B
            case 0xD: result = A & B
            case 0xE: result = A | B
            case 0xF: result = ~A + self.ctrl_bus["NEG"]

        
