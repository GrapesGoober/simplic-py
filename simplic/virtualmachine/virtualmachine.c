#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define SIZE 0x10000        // default to 16 bit address size
typedef uint16_t    word;   // default to 16 bit word size
typedef uint8_t     byte;   // define a byte as an 8-bit word

// gcc simplic\virtualmachine\virtualmachine.c -o simplic\virtualmachine\virtualmachine.exe
// simplic\virtualmachine\virtualmachine.exe < test_codes\test.hex

// the SimplicVM is a Harvard architecture, and uses the main memory to store internal state
// the PC, Accumulator, and the Stack Pointer will be initialized to point to the main memory
// the rest would be decoded for each step execution
typedef struct SimplicVM {
    word *PC, *A, *SP, *V;
    byte opcode, imm, cond;
    word instr[SIZE], mem[SIZE];
} SimplicVM;

// this VM handles initializing, step execution, and running VM
void init   (SimplicVM *vm);
void decode (SimplicVM *vm);
void execute(SimplicVM *vm);
void run    (SimplicVM *sm);

void main() {
    SimplicVM *vm = (SimplicVM*)malloc(sizeof(SimplicVM));
    init(vm); run(vm); print(vm); free(vm);
}

// initialize VM and load the program
void init(SimplicVM *vm) {
    // initialize default values
    vm->mem[0] = 0, vm->mem[2] = 0xFFFF;
    vm->PC = &vm->mem[0];
    vm->A  = &vm->mem[1];
    vm->SP = &vm->mem[2];
    // load program from stdin
    word count = 0; 
    while (scanf("%2hhx", &vm->instr[count++]) == 1);
}

// run VM with a halt condition & IO protocol
void run(SimplicVM *vm) {
    while (vm->mem[0] != 0xFFFF) {
        decode(vm);
        execute(vm);
        switch (vm->mem[3]) {
            case 1:  printf("%c", vm->mem[4]); break;      // output to stdout
            case 2:  scanf("%c", &vm->mem[4]); break;      // recieve character from stdin
        }
        vm->mem[3] = 0;
    }
}

// decode the current state of VM
void decode(SimplicVM *vm)  {
    vm->opcode  = vm->instr[*vm->PC] >> 12;
    vm->imm     = vm->instr[*vm->PC] & 0xFF;
    vm->V       = &vm->instr[*vm->SP - vm->imm];

    bool Z = *vm->A == 0, N = *vm->A >> 15;
    // bool flags[] = { 1, N, !(Z | N), Z, !Z, (Z | N), !N };
    // vm->cond = flags[vm->instr[*vm->PC] >> 8 & 0x4]
    switch (vm->instr[*vm->PC] >> 8 & 0x4)
    {
        case 0x0: vm->cond = true;        break;  // always
        case 0x1: vm->cond = N;           break;  // less than (negative)
        case 0x2: vm->cond = !(Z | N);    break;  // more than (positive)
        case 0x3: vm->cond = Z;           break;  // equals (zero)
        case 0x4: vm->cond = !Z;          break;  // not equals (not zero)
        case 0x5: vm->cond = (Z | N);     break;  // less than or equal (positive or zero)
        case 0x6: vm->cond = !N;          break;  // more than or equal (not negative)
        default:  vm->cond = false;       break;
    }
}

// execute the current vm state
void execute(SimplicVM *vm) {
    // first, check condition
    if (vm->cond) {
        // if true, executes depending on opcode
        switch (vm->opcode) {
            case 0x0: *vm->A = *vm->V;              break;  // Load
            case 0x1: *vm->V = *vm->A;              break;  // Store
            case 0x2: *vm->A = vm->mem[*vm->V];     break;  // Load Pointer
            case 0x3: vm->mem[*vm->V] = *vm->A;     break;  // Store Pointer
            case 0x4: *vm->A +=  *vm->V;            break;  // Add
            case 0x5: *vm->A -=  *vm->V;            break;  // Sub
            case 0x6: *vm->A <<= *vm->V;            break;  // LSL
            case 0x7: *vm->A >>= *vm->V;            break;  // LSR
            case 0x8: *vm->A *=  *vm->V;            break;  // Mul
            case 0x9: *vm->A /=  *vm->V;            break;  // Div
            case 0xA: *vm->A &=  *vm->V;            break;  // And
            case 0xB: *vm->A |=  *vm->V;            break;  // Or
            case 0xC: *vm->A =  ~*vm->V;            break;  // Not
            // TODO: slide up and down with MSB as direction and 7 bits as distance
            case 0xD: *vm->SP += vm->imm << 8;       break;  // Stack Slide
            case 0xE: *vm->V = vm->imm;              break;  // Set
            case 0xF: *vm->PC = *vm->V;             break;  // Goto                                        
        }  
    }
    // lastly, increment program counter
    *vm->PC += 1;
}

// print the current state of VM
void print(SimplicVM *vm) {
    printf("internal state\n");
    printf("  PC\t%d\n", vm->PC);
    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        printf("  %x\t%d\n", i, vm->mem[*vm->SP - i]);
    }
}
