#include <stdio.h>

int main(int argc, char *argv[]) {

    // Print each command-line argument
    printf("Hello World\n");
    printf("Arguments:\n");
    if (argc == 1) {
        printf("Haven't recieved any\n");
    }
    for (int i = 1; i < argc; i++) {
        printf("%d: %s\n", i, argv[i]);
    }

    return 0;
}