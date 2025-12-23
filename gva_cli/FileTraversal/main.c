#include "db.h"
#include "traverse.h"
#include<stdio.h>


//Make an executable using all the .c Files then run that executable using "./exe path" the path is argv[1]
int main(int argc, char *argv[]){
    db_init("index.db");

    
    traverse(argv[1],argv[2]);

    //call checkDiff with argv[1] as the parameter.

    checkDiff(argv[1]);

    db_close();
}

