#include <stdlib.h>
#include<string.h>
#include<stdio.h>

int main(int argc, char *argv[]) {
    char command[512];
    snprintf(command, sizeof(command), "open \"%s\"", argv[1]);
    system(command);
    return 0;
}
