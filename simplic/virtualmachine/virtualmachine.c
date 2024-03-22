#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define SIZE 0x10000        // default to 16 bit address size
typedef uint16_t    word;   // default to 16 bit word size
typedef uint8_t     byte;   // define a byte as an 8-bit word

typedef struct SimplicVM {
    word PC, A, SP;
    word instr[SIZE], mem[SIZE];
} SimplicVM;

void init   (SimplicVM *vm); // initialize VM and load the program from stdin
void execute(SimplicVM *vm); // step execute the current VM state
void run    (SimplicVM *sm); // continuously run the VM until halts, handle IO, and print final state

void main() {
    SimplicVM *vm = (SimplicVM*)malloc(sizeof(SimplicVM));
    init(vm); run(vm); print(vm); free(vm);
}

void init(SimplicVM *vm) {
    vm->mem[0] = 0, vm->mem[2] = 0xFFFF;
    word count = 0; 
    while (scanf("%2hhx", &vm->instr[count++]) == 1);
}

void execute(SimplicVM *vm) {

    word *PC = &vm->PC, *A = &vm->A, *SP = &vm->SP;
    word *mem = &vm->mem, instr = vm->instr[*PC];
    byte opcode = instr >> 12, imm = instr & 0xFF, cond = instr >> 8 & 0x4;
    word *V = mem[*SP - imm];

    bool Z = vm->A == 0, N = vm->A >> 15;
    bool flags[] = { 1, N, !(Z | N), Z, !Z, (Z | N), !N };

    if (flags[cond]) {
        // if true, executes depending on opcode
        switch (opcode) {
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
            // TODO: slide up and down with MSB as direction and 7 bits as distance
            case 0xD: *SP += imm; *A = *SP; break;  // Stack Slide
            case 0xE: *V = *V<<8 | imm;     break;  // Insert
            case 0xF: *PC = *V;             break;  // Goto                                        
        }  
    }
    // lastly, increment program counter
    *PC += 1;
}

void run(SimplicVM *vm) {
    while (vm->mem[0] != 0xFFFF) {
        execute(vm);
        switch (vm->mem[3]) {
            case 1:  printf("%c", vm->mem[4]); break;      // output to stdout
            case 2:  scanf("%c", &vm->mem[4]); break;      // recieve character from stdin
        }
        vm->mem[3] = 0;
    }

    printf("PC\t%d\n", vm->PC);
    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        printf("  %x\t%d\n", i, vm->mem[vm->SP - i]);
    }
}