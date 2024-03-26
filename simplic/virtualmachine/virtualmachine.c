#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define SIZE 0x10000        // default to 16 bit address size
typedef uint16_t    word;   // default to 16 bit word size
typedef uint8_t     byte;   // define a byte as an 8-bit word

// Simplic is a word-RAM model, Harvard architecture, accumulator-based machine
word A = 0, PC = 0, SP = 0xFFFF, PROG[SIZE], MEM[SIZE];

void execute() { // step execute the current VM state

    // first, decode the current instruction
    word instr = PROG[PC];
    byte opcode = instr >> 12, I8 = instr & 0xFF, cond = instr>>8 & 0x4;
    word *V = MEM[SP - I8];

    // next, check the condition
    bool Z = A == 0, N = A >> 15;
    bool flags[] = { 1, N, !(Z | N), Z, !Z, (Z | N), !N };
    if (flags[cond]) {
        // if true, executes depending on opcode
        switch (opcode) {
            case 0x0: A = *V;               break;  // Load
            case 0x1: *V = A;               break;  // Store
            case 0x2: A = MEM[*V];          break;  // Load Pointer
            case 0x3: MEM[*V] = A;          break;  // Store Pointer
            case 0x4: A +=  *V;             break;  // Add
            case 0x5: A -=  *V;             break;  // Sub
            case 0x6: A <<= *V;             break;  // LSL
            case 0x7: A >>= *V;             break;  // LSR
            case 0x8: A *=  *V;             break;  // Mul
            case 0x9: A /=  *V;             break;  // Div
            case 0xA: A &=  *V;             break;  // And
            case 0xB: A |=  *V;             break;  // Or
            case 0xC: A =  ~*V;             break;  // Not
            case 0xD: A = A<<8 | I8;    break;  // Insert
            case 0xE: PC = *V;          break;  // Goto                                        
            case 0xF: SP += I8 - 127;      
                      A = SP;           break;  // Stack Slide
        }  
    }
    // lastly, increment program counter for the next execution
    PC += 1;
}

int main() {

    // first, initialize program from stdin
    word count = 0;
    while (scanf("%2hhx", &PROG[count++]) == 1);

    // next run VM with IO until reached the halt condition
    while (PC != 0xFFFF) { 
        execute();
        if (MEM[0] == 1) printf("%c", MEM[1]); // output to stdout
        if (MEM[0] == 2) scanf("%c", &MEM[1]); // recieve character from stdin
        MEM[0] = 0;
    }

    printf("PC\t%d\n", PC);
    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        printf("  %x\t%d\n", i, MEM[SP - i]);
    }

    return 0;
}