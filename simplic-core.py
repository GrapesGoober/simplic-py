from intelhex import IntelHex
import sys

ih = IntelHex(sys.argv[1])

# internal state (memory, registers, and flip-flops)
bytecodes = ih.todict()
bytecodes = {
    i:( 0 if i not in bytecodes else bytecodes[i] ) 
    for i in range(0, 2**16)
}

memory = {i:0 for i in range(0, 2**16)} 
registers = {i:0 for i in range(0, 16)} 
en_flag = False
z, n, c, v = False, False, False, False

# multiplexers
data_in = {i:0 for i in range(0, 16)} 
conditions = { i:False for i in range(0, 16) } 
shifts = { i:0 for i in range(0, 4) }

while True:
    if registers[15] == 100:
        print(memory)
        break

    # deconstructing instruction for easy use
    opcode, rd, operand1, operand2 = [
        bytecodes[registers[15] * 2] >> 4,
        bytecodes[registers[15] * 2] & 0xF,
        bytecodes[registers[15] * 2 + 1] >> 4,
        bytecodes[registers[15] * 2 + 1] & 0xF,
    ]
    print( opcode, rd, operand1, operand2 )
    print( registers )

    # handle conditions for cmove
    conditions[0x0] = z
    conditions[0x1] = not z
    conditions[0x2] = n
    conditions[0x3] = not n
    conditions[0x4] = c
    conditions[0x5] = not c
    conditions[0x6] = v
    conditions[0x7] = not v
    conditions[0x8] = z or c
    conditions[0x9] = not z and not c
    conditions[0xA] = n != v
    conditions[0xB] = not z and (n == v)
    conditions[0xC] = z or (n != v)
    conditions[0xD] = n == v
    conditions[0xE] = z and not n and not c and not v
    conditions[0xF] = True

    # cmove
    data_in[0x0] = registers[operand1] if conditions[operand2] else data_in[0x0]

    # count leading zeros
    data_in[0x1] = registers[operand1]
    data_in[0x1] = data_in[0x1] | (data_in[0x1] >> 1)
    data_in[0x1] = data_in[0x1] | (data_in[0x1] >> 2)
    data_in[0x1] = data_in[0x1] | (data_in[0x1] >> 4)
    data_in[0x1] = data_in[0x1] | (data_in[0x1] >> 8)
    data_in[0x1] = 16 - bin(data_in[0x1]).count("1")

    # memory instructions
    data_in[0x2] = memory[ (registers[operand1] + registers[operand2]) & 0xFF ]
    data_in[0x3] = data_in[0x3]
    memory[ (registers[operand1] + registers[operand2]) & 0xFF ] = registers[rd]

    # insert
    data_in[0x4] = (registers[rd] << 8) | (operand1 << 4) | operand2

    # shift
    shifts[0x0] = registers[rd] << registers[operand2]
    shifts[0x1] = registers[rd] >> registers[operand2]
    shifts[0x2] = registers[rd] >> registers[operand2]
    shifts[0x3] = registers[rd] >> registers[operand2]
    data_in[0x5] = shifts[operand1 & 0b11]

    # Handle ALU instructios
    data_in[0x6] = registers[operand1] + registers[operand2]
    data_in[0x7] = registers[operand1] - registers[operand2]
    data_in[0x8] = registers[operand1] * registers[operand2]
    data_in[0x9] = registers[operand1] * registers[operand2] >> 16
    data_in[0xA] = registers[operand1] // (registers[operand2] | (registers[operand2] == 0 ))
    data_in[0xB] = registers[operand1] % (registers[operand2] | (registers[operand2] == 0))
    data_in[0xC] = registers[operand1] & registers[operand2]
    data_in[0xD] = registers[operand1] | registers[operand2]
    data_in[0xE] = registers[operand1] ^ registers[operand2]
    data_in[0xF] = ~(registers[operand1] | registers[operand2])
    
    # handle flags

    # Multiplex data-in into destination register
    registers[rd] = data_in[opcode] & 0xFFFF
    registers[0] = 0

    registers[15] += 1