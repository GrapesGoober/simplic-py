
class SimplicCore:
    BITSIZE = 16

    # Internal registers
    ACC, BSP, PC = 0, 0, 0
    Z, N, C, V = 0, 0, 0, 0

    # Mux & Signal bus
    result_mux : dict = {i:0 for i in range(16)}
    constrol_signals : dict = {}

    def decode(self, opcode, control):
        pass

    def compute(self, data):

        self.result_mux[0x6] = self.ACC + data
        self.result_mux[0x7] = self.ACC - data
        self.result_mux[0x8] = self.ACC * data
        self.result_mux[0x9] = (self.ACC * data) >> self.BITSIZE
        self.result_mux[0xA] = self.ACC // data
        self.result_mux[0xB] = self.ACC % data
        self.result_mux[0xC] = 0 # not sure what to do here
        self.result_mux[0xD] = self.ACC & data
        self.result_mux[0xE] = self.ACC | data
        self.result_mux[0xF] = ~data

    def multiplex(self, opcode):
        opcode &= (1 << self.BITSIZE) - 1
        self.ACC = self.result_mux[opcode] if self.ACC_write_en else self.ACC
        self.BSP = self.result_mux[opcode] if self.BSP_write_en else self.BSP
        self.PC = self.result_mux[opcode] if self.PC_write_en else self.PC
    
    def execute(self, instruction):
        pass