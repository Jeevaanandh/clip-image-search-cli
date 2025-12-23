#include "db.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/stat.h>
#include<limits.h>



sqlite3 *DB= NULL;
const char *sql;
int rc;
char *err_msg=0;

int db_init(const char *db_path){
    if(sqlite3_open(db_path, &DB) != SQLITE_OK){
        return -1;
    }

    sql= "CREATE TABLE IF NOT EXISTS Hash("\
         "path TEXT PRIMARY KEY,"\
         "hash TEXT NOT NULL);";

    rc= sqlite3_exec(DB, sql, 0, 0, &err_msg);

    if(rc != SQLITE_OK){
        return -1;
    }

    return 0;   
}

int delete(const char *path){
    sql= "DELETE FROM Hash WHERE path= ?";

    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(DB, sql, -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, path, -1, SQLITE_TRANSIENT);

    rc= sqlite3_step(stmt);
    sqlite3_finalize(stmt);

    if(rc== SQLITE_DONE){
        return 0;
    }

    return -1;

}


void db_close(void){
    if(DB){
        sqlite3_close(DB);
        DB= NULL;
    }
}


int check(const char *path){
    sql= "SELECT 1 FROM Hash WHERE path= ?;";

    //This is done to give the path parameter to the query
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(DB, sql, -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, path, -1, SQLITE_TRANSIENT);

    //step is used to execute queries when we have to prepare the query ie. using parameters and so on ...
    rc= sqlite3_step(stmt);

    sqlite3_finalize(stmt);  //This destroys the prepared sql query and frees the memory it occupies.

    //Row exists
    if(rc== SQLITE_ROW){
        return 1;
    }

    return 0;

}


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


int add(const char *path, const char *hashPath){
    sql= "INSERT OR REPLACE INTO Hash (path, hash) VALUES (?,?);";
    sqlite3_stmt *stmt;

    char hash_hex[65];

    int res= getHash(path, hash_hex, hashPath);

    if(res==-1){
        return -1;
    }

    sqlite3_prepare_v2(DB, sql, -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, path, -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, hash_hex, -1, SQLITE_TRANSIENT);

    rc= sqlite3_step(stmt);

    sqlite3_finalize(stmt);

    if(rc== SQLITE_DONE){
        return 0;
    }

    else{
        return -1;
    }

}



int checkDiff(const char *path){
    // Add the logic

    sql= "SELECT path FROM HASH WHERE path like ?;";
    int count=0;

    char pattern[PATH_MAX];
    snprintf(pattern, sizeof(pattern), "%%%s%%", path);




    sqlite3_stmt *stmt;

    
    sqlite3_prepare_v2(DB, sql,-1, &stmt, NULL);
    sqlite3_bind_text(stmt,1, pattern, -1, SQLITE_TRANSIENT);

    struct stat fp;

    
    while(sqlite3_step(stmt)==SQLITE_ROW){
        const char * path = (const char *) sqlite3_column_text(stmt,0);

        if(stat(path, &fp)!=0){
            

            int res= delete(path);
            if(res==0){
                count+=1;
                
            }


            //call the delete function to delete the hash from the DB.

        }


    }

    sqlite3_finalize(stmt);
    printf("Deletions: %d\n", count);

    return 0;


}
