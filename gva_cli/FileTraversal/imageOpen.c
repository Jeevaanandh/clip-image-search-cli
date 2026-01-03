#include <stdlib.h>
#include<string.h>
#include<stdio.h>

int main(int argc, char *argv[]) {

    char command[512];
    #ifdef __APPLE__
        snprintf(command, sizeof(command), "open \"%s\"", argv[1]);
        system(command);

    #elif _WIN32
        snprintf(command, sizeof(command), "start \"%s\"", argv[1]);
        system(command);

    #elif __elif__
        snprintf(command, sizeof(command), "xdg-open \"%s\"", argv[1]);
        system(command);


    #endif

    return 0;
}
