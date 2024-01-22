#include <stdio.h>

int main(int argc, char *argv[]) {

    unsigned char data[0xFF];
    
    // Use a loop to read bytes until the end of input (EOF)
    size_t count = 0;
    while (scanf("%2hhx", &data[count]) == 1) {
        count += 1;
    }

    for (int i = 0; i < 0xFF; i++) {
        printf("%x ", data[i]);
    }
    printf("done\n");


    return 0;
}