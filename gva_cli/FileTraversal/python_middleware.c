#include<string.h>
#include<sys/stat.h>
#include<limits.h>
#include<stdio.h>
#include<stdlib.h>

int getHash(const char *path, char hash_hex[65], const char *hashPath){
    char command[512];

    snprintf(command, sizeof(command),
             "python \"%s\" \"%s\"",
             hashPath, path);
             
    FILE* fptr= popen(command, "r"); // Creating a pipe to run the Python file.  The output of the command is stored in fptr and we can read form it

    if(!fptr){
        return -1;
    }

    if(fgets(hash_hex, 65, fptr) == NULL){
        pclose(fptr);
        return -1;
    }

    pclose(fptr);

    hash_hex[strcspn(hash_hex, "\n")]= 0;

    return 0;

}



