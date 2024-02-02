#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define SIZE 0x10000        // default to 16 bit address size
typedef uint16_t    word;   // default to 16 bit word size
typedef uint8_t     byte;   // define a byte as an 8-bit word

// executes the current instruction cycle
void execute(word *mem, byte *instr) {

    // first, decode the current state
    word *PC    = &mem[0];
    word *A     = &mem[1];
    word *SP    = &mem[2];
    byte  OP    = instr[*PC] >> 4;
    byte  I4    = instr[*PC] & 0xF;
    word *V     = &mem[*SP - I4];
    word  I16   = instr[*PC + 1] << 8 | instr[*PC + 2];

    // next, precomputes inputs for stack & if instructions
    word slide = I4 ? 0xFFF0 : 0x10;
    bool Z = *A == 0, N = *A >> 15;
    bool cond[] = { 1, N, !(Z | N), Z, !Z, (Z | N), !N };
    word jump = cond[I4] ? I16 : *PC + 2;

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

void main() {

    // initialize vm
    byte instr[SIZE];
    word mem[SIZE];
    word *PC = &mem[0], *A = &mem[1], *SP = &mem[2];
    *PC = 0, *SP = 0xFFFF;

    // load program from stdin
    word count = 0;
    while (scanf("%2hhx", &instr[count++]) == 1);

    // run vm with a halt condition & IO protocol
    while (*PC != 0xFFFF) {
        execute(mem, instr);
        switch (mem[3]) {
            case 1:  printf("%c", mem[4]); break;      // output to stdout
            case 2:  scanf("%c", &mem[4]); break;      // recieve character from stdin
        }
        mem[3] = 0;


    }
    printf("internal state\n");
    printf("  PC\t%d\n", *PC);
    printf("stack\n");
    for (int i = 0; i < 0x10; i++) {
        printf("  %x\t%d\n", i, mem[*SP - i]);
    }
}

// gcc simplic\virtualmachine\virtualmachine.c -o simplic\virtualmachine\virtualmachine.exe
// simplic\virtualmachine\virtualmachine.exe < test_codes\test.hex

