#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define SIZE 0x10000        // default to 16 bit address size
typedef uint16_t    word;   // default to 16 bit word size
typedef uint8_t     byte;   // define a byte as an 8-bit word

typedef struct SimplicVM {
    word instr[SIZE], mem[SIZE];
} SimplicVM;

SimplicVM* init();
void execute(SimplicVM *vm);
void run(SimplicVM *sm);

// initialize vm and load the program
SimplicVM* init() {
    SimplicVM *vm = (SimplicVM*)malloc(sizeof(SimplicVM));
    vm->mem[0] = 0, vm->mem[2] = 0xFFFF; // init default values
    word count = 0; // load program from stdin
    while (scanf("%2hhx", &vm->instr[count++]) == 1);

    return vm;
}

// execute the current vm state
void execute(SimplicVM *vm) {
    
    // first, decode the current state
    word *PC    = &vm->mem[0];
    word *A     = &vm->mem[1];
    word *SP    = &vm->mem[2];
    byte  OP    = vm->instr[*PC] >> 12;
    byte  COND  = vm->instr[*PC] >> 8 & 0x4;
    byte  I16   = vm->instr[*PC] & 0xFF;

    bool Z = *A == 0, N = *A >> 15;
    // bool cond[] = { 1, N, !(Z | N), Z, !Z, (Z | N), !N };
    switch (COND)
    {
        case 0x0: COND = true;        break;  // Load
        case 0x1: COND = N;           break;  // Store
        case 0x2: COND = !(Z | N);    break;  // Load Pointer
        case 0x3: COND = Z;           break;  // Store Pointer
        case 0x4: COND = !Z;          break;  // Add
        case 0x5: COND = (Z | N);     break;  // Sub
        case 0x6: COND = !N;          break;  // LSL
        default: break;
    }

    if (COND) {
        PC = vm->mem[*SP - I16];
        return;
    }

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

void run(SimplicVM *sm) {
    // run vm with a halt condition & IO protocol
    while (sm->mem[0] != 0xFFFF) {
        execute(sm);
        switch (sm->mem[3]) {
            case 1:  printf("%c", sm->mem[4]); break;      // output to stdout
            case 2:  scanf("%c", &sm->mem[4]); break;      // recieve character from stdin
        }
        sm->mem[3] = 0;
    }
}

void main() {


    
    printf("internal state\n");
    printf("  PC\t%d\n", *PC);
    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        printf("  %x\t%d\n", i, mem[*SP - i]);
    }
}

// gcc simplic\virtualmachine\virtualmachine.c -o simplic\virtualmachine\virtualmachine.exe
// simplic\virtualmachine\virtualmachine.exe < test_codes\test.hex


