CC = gcc
LIBS = -lsqlite3

OBJS = main.o db.o traverse.o # .o files are generated when we do gcc -c file.c.   This creates a file.o but we dont have to mention this in make as 
                              # make already has predefined rule %.o: %.c which has a command to convert the .c files to .o

TARGET = db_exe

$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LIBS) -o $(TARGET) 