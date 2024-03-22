#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define SIZE 0x10000        // default to 16 bit address size
typedef uint16_t    word;   // default to 16 bit word size
typedef uint8_t     byte;   // define a byte as an 8-bit word

word A = 0, PC = 0, SP = 0xFFFF, program[SIZE], mem[SIZE];

void execute() { // step execute the current VM state

    // first, decode the current instruction
    word instr = program[PC];
    byte opcode = instr >> 12, imm = instr & 0xFF, cond = instr>>8 & 0x4;
    word *V = mem[SP - imm];

    // next, check the condition
    bool Z = A == 0, N = A >> 15;
    bool flags[] = { 1, N, !(Z | N), Z, !Z, (Z | N), !N };
    if (flags[cond]) {
        // if true, executes depending on opcode
        switch (opcode) {
            case 0x0: A = *V;              break;  // Load
            case 0x1: *V = A;              break;  // Store
            case 0x2: A = mem[*V];         break;  // Load Pointer
            case 0x3: mem[*V] = A;         break;  // Store Pointer
            case 0x4: A +=  *V;            break;  // Add
            case 0x5: A -=  *V;            break;  // Sub
            case 0x6: A <<= *V;            break;  // LSL
            case 0x7: A >>= *V;            break;  // LSR
            case 0x8: A *=  *V;            break;  // Mul
            case 0x9: A /=  *V;            break;  // Div
            case 0xA: A &=  *V;            break;  // And
            case 0xB: A |=  *V;            break;  // Or
            case 0xC: A =  ~*V;            break;  // Not
            // TODO: slide up and down with MSB as direction and 7 bits as distance
            case 0xD: SP += imm; A = SP; break;  // Stack Slide
            case 0xE: *V = *V<<8 | imm;     break;  // Insert
            case 0xF: PC = *V;             break;  // Goto                                        
        }  
    }
    // lastly, increment program counter for the next instruction
    PC += 1;
}

int main() {

    word count = 0; // initialize program from stdin
    while (scanf("%2hhx", &program[count++]) == 1);

    while (PC != 0xFFFF) { // run VM with IO and halt condition
        execute();
        if (mem[0] == 1) printf("%c", mem[1]); // output to stdout
        if (mem[0] == 2) scanf("%c", &mem[1]); // recieve character from stdin
        mem[0] = 0;
    }

    printf("PC\t%d\n", PC);
    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        printf("  %x\t%d\n", i, mem[SP - i]);
    }

    return 0;
}