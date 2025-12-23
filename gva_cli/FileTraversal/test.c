#include<sqlite3.h>
#include<stdio.h>
#include<string.h>
#include<sys/stat.h>

int main(){


    
    sqlite3 *db;

    sqlite3_open("index.db", &db);

    struct stat fp;

    char query[]= "SELECT * FROM Hash WHERE path LIKE \"%Wallpapers%\";";
    sqlite3_stmt *stmt;  // stmt is used the store the compiled version of the query after using prepare. After this is done we can execute the query one by one
    sqlite3_prepare_v2(db, query, -1, &stmt, NULL);

    /*
    while(sqlite3_step(stmt) == SQLITE_ROW){
        printf("path= %s\n", sqlite3_column_text(stmt,0));  // This give the column 0 of the current row
        printf("hash= %s\n", sqlite3_column_text(stmt,1));  // This gives the column 1 of the current row.

        const char *path = (const char *)sqlite3_column_text(stmt, 0);
        if (stat(path, &fp) == 0) {
            printf("File is available\n");
        } 

        else {
            perror("stat");                         
        }

        printf("DEBUG: [%s]\n", sqlite3_column_text(stmt,0));
        
        
    }

    */

    while(sqlite3_step(stmt)==SQLITE_ROW){
        const char * path = (const char *) sqlite3_column_text(stmt,0);

        if(stat(path, &fp)!=0){
            printf("File %s has been deleted\n", sqlite3_column_text(stmt,0));

        }


    }


    

    
               

    

    



    

}