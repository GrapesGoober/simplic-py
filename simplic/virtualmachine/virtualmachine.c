#include <stdio.h>
#include <stdint.h>

#define WORD_SIZE 16

typedef struct SimplicVM {
    uint8_t  instruction[0xFFFF];
    uint16_t memory[0xFFFF];
} SimplicVM;

void execute(SimplicVM *vm) {

    uint16_t *mem   = &vm->memory;
    uint16_t *instr = &vm->instruction;
    uint16_t *PC    = &mem[0];
    uint8_t   OP    = instr[*PC] >> 4;
    uint8_t   I4    = instr[*PC] & 0xF;
    uint16_t *A     = &mem[1];
    uint16_t *V     = &mem[2];
    uint16_t  I16   = instr[*PC+1] << 8 | instr[*PC+2];
    uint8_t   Z     = *A == 0;
    uint8_t   N     = *A >> 15;

    switch (OP) {
        case 0x0: *V = I16; *PC += 2;       break;
        case 0x1:                           break;  // If
        case 0x2: *A = *V;                  break;  // Load
        case 0x3: *V = *A;                  break;  // Store
        case 0x4: *A = mem[*V];             break;  // Load Pointer
        case 0x5: mem[*V] = A;              break;  // Store Pointer
        case 0x6:   break;
        case 0x7:   break;
        case 0x8:   break;
        case 0x9: *A += *V;                 break;  // Add
        case 0xA: *A -= *V;                 break;  // Sub
        case 0xB: *A *= *V;                 break;  // Mul
        case 0xC: *A /= *V;                 break;  // Div
        case 0xD: *A &= *V;                 break;  // And
        case 0xE: *A |= *V;                 break;  // Or
        case 0xF: *A = ~*V;                 break;  // Not
    }               

    *PC += 1;
}

void run(SimplicMicrocontroller *vm) {
    uint16_t *mem = &vm->instr;
    uint16_t *PC  = mem[0];
    while (*PC < 0xFFFF) {
        execute(vm);
    }
}

