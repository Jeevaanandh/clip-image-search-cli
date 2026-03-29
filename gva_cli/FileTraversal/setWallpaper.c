#include<stdio.h>
#include<string.h>
#include <sys/_types.h>
#include<unistd.h>
#include<sys/wait.h>

int main(int argc, char *argv[]){
    pid_t pid= fork();

    char *image_path= argv[1];

    

    if(pid==0){
        //Child
        char script[200];

        sprintf(script, "tell application \"Finder\" to set desktop picture to POSIX file \"%s\"", image_path);

        execlp(
            "osascript",
            "osascript",
            "-e",
            script,
            NULL
        );
    }

    int status;
    wait(&status);

    if(WIFEXITED(status)){
        printf("Changed Wallpaper Successfully!!!\n");
        return 0;
    }

    return 1;
}