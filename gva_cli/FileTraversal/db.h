#ifndef DB_H
#define DB_H


#include<sqlite3.h>

extern sqlite3 *DB;

int db_init(const char *db_path);
void db_close(void);

int check(const char *path);
int checkDiff(const char *path);
int add(const char *path, const char *hashPath);

#endif