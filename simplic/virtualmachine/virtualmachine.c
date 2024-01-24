#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define SIZE 0x10000
typedef uint16_t word;
typedef uint8_t byte;

typedef struct SimplicVM {
    byte instr[SIZE];
    word mem[SIZE];
} SimplicVM;

void init(SimplicVM *vm, size_t len, char* instr[]) {
    vm->mem[0] = 0, vm->mem[2] = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        vm -> instr[i] = strtol(instr[i], NULL, 16);
    }
}

// executes the current instruction cycle
void execute(SimplicVM *vm) {

    // first, decode the current state
    word *mem   = vm->mem;
    byte *instr = vm->instr;
    word *PC    = &mem[0];
    word *A     = &mem[1];
    word *SP    = &mem[2];
    byte  OP    = instr[*PC] >> 4;
    byte  I4    = instr[*PC] & 0xF;
    word *V     = &mem[*SP - I4];
    word  I16   = instr[*PC + 1] << 8 | instr[*PC + 2];

    // next, precomputes inputs for certain special instructions
    word slide = I4 ? 0xFFF0 : 0x10;
    byte Z = *A == 0, N = *A >> 15;
    byte cond[] = { 1, N, ~(Z | N), Z << 3, ~Z, (Z | N), ~N };
    word jump = cond[I4] ? I16 - 1 : *PC + 2;

    // execute instruction
    switch (OP) {
        case 0x0: *A = *V;              break;  // Load
        case 0x1: *V = *A;              break;  // Store
        case 0x2: *A = mem[*V];         break;  // Load Pointer
        case 0x3: mem[*V] = *A;         break;  // Store Pointer
        case 0x4: *A +=  *V;            break;  // Add
        case 0x5: *A -=  *V;            break;  // Sub
        case 0x6: *A <<= *V;            break;  // LSL
        case 0x7: *A >>= *V;            break;  // LSR
        case 0x8: *A *=  *V;            break;  // Mul
        case 0x9: *A /=  *V;            break;  // Div
        case 0xA: *A &=  *V;            break;  // And
        case 0xB: *A |=  *V;            break;  // Or
        case 0xC: *A =  ~*V;            break;  // Not
        case 0xD: *SP += slide;         break;  // Stack Slide
        case 0xE: *V = I16; *PC += 2;   break;  // Set
        case 0xF: *PC = jump;           break;  // If                                        
    }               

    // lastly, increment program counter
    *PC += 1;
}

void run(SimplicVM *vm) {
    word *PC  = &(vm->mem[0]);
    while (*PC < 0xFFFF) {
        execute(vm);
    }
}

void print(SimplicVM *vm){
    printf("internal state\n");
    printf("  PC\t%d\n", vm -> mem[0]);
    printf("  A\t%d\n",  vm -> mem[1]);
    printf("  SP\t%d\n", vm -> mem[2]);

    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        int SP = vm -> mem[2];
        printf("  %x\t%d\n", i, vm -> mem[SP - i]);
    }
}

void main(int argc, char *argv[]) {
    SimplicVM vm;
    init(&vm, argc, argv + 1);
    run(&vm);
    print(&vm);
}

// gcc simplic\virtualmachine\virtualmachine.c -o simplic\virtualmachine\virtualmachine.exe
// simplic\virtualmachine\virtualmachine.exe e1 00 01 e2 00 01 e3 00 00 e4 00 02 e5 00 01 e6 00 18 01 42 13 02 11 03 12 04 45 14 04 d1 12 03 42 13 d0 04 56 f1 00 12 d1 02 d0 1d d1 03 d0 1e

