#include "db.h"
#include "traverse.h"
#include<stdio.h>


//Make an executable using all the .c Files then run that executable using "./exe path" the path is argv[1]
int main(int argc, char *argv[]){
    int rc= db_init(argv[1]);
    

    if(rc==-1){
        printf("DB opening Failed\n");
    }

    //call checkDiff with argv[1] as the parameter.

    checkDiff(argv[2]);

    db_close();
}

