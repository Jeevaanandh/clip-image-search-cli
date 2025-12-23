#include<stdio.h>
#include<string.h>
#include<limits.h>
#include<dirent.h> 
#include "db.h"


int res;
int count=0;


int ends_with(const char *s, const char *suffix){
    if(!s || !suffix){
        return 0;
    }

    size_t len_str= strlen(s);
    size_t len_suffix= strlen(suffix);

    if(len_suffix> len_str){
        return 0;
    }

    return strcasecmp(s+len_str-len_suffix, suffix)==0;
}

int traverse(const char *path, const char * hashPath){
    

    DIR* dir = opendir(path);  //This opens the directory

    if(dir == NULL){
        return 1;
    }

    struct dirent* entity; // This is the struct that stores the details of the current file in the directory
    entity= readdir(dir);  // Reads the next file in the directory. If it is NULL then the traversal is done.

    while(entity != NULL){

        if(strcmp(entity->d_name, ".")==0 || strcmp(entity->d_name, "..") ==0){
            entity= readdir(dir);
            continue;
        }

        //This is to skip files that are not images.
        if(!ends_with(entity->d_name,".jpeg") && !ends_with(entity->d_name, ".png") && !ends_with(entity->d_name, ".jpg") && !ends_with(entity->d_name, ".webp")){

            
            entity= readdir(dir);
            continue;
        }
        
        char total[PATH_MAX];
        snprintf(total, sizeof(total), "%s/%s", path, entity->d_name);
        
        res= check(total);

        if(res==0){
            //Add the logic to add the path, hash details to the DB.
            //Add this logic to db.c and call that function here.
            int cond= add(total, hashPath);

            if(cond==0){
                count+=1;
            }
            
        }

        entity= readdir(dir);
    }

    printf("Insertions: %d\n", count);
    closedir(dir);
    return 0;

}


