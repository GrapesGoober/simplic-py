#include <stdio.h>
#include <stdint.h>

#define WORD_SIZE 16

typedef struct SimplicMicrocontroller {
    uint8_t instructions[0xFFFF];
    uint16_t memory[0xFFFF];
} SimplicMicrocontroller;


void execute(SimplicMicrocontroller *sm) {
    uint16_t* PC = &sm->memory[0];
    uint16_t* A = &sm->memory[1];
    uint16_t* P = &sm->memory[2];
    uint8_t opcode = sm->instructions[*PC] >> 4;
    uint8_t* I = sm->instructions[*PC] & 0xF;
    uint16_t* V = &sm->memory[P - I];

    switch (opcode) {
        case 0x0: 
            *V = sm->instructions[*PC + 1] << 8 | sm->instructions[*PC + 2];
            *PC += 2;
            break;
        case 0x1: 
            break;
        case 0x2: *A = *V; break;                     // Load
        case 0x3: *V = *A; break;                     // Store
        case 0x4: *A = sm->memory[*V]; break;         // Load Pointer
        case 0x5: sm->memory[*V] = A; break;          // Store Pointer
        case 0x6: *V = set_data(sm, *PC); break;      // Set
        case 0x7: break;
        case 0x8: break;
        case 0x9: *A += *V; break;            // Add
        case 0xA: *A -= *V; break;            // Sub
        case 0xB: *A *= *V; break;            // Mul
        case 0xC: *A /= *V; break;            // Div
        case 0xD: *A &= *V; break;            // And
        case 0xE: *A |= *V; break;            // Or
        case 0xF: *A = ~*V; break;            // Not
    }
}

void run(SimplicMicrocontroller *sm) {
    while (sm->memory[0] < 0xFFFF) {
        execute(sm);
    }
}

