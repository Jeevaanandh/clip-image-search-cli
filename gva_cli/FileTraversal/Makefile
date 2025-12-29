CC = gcc
LIBS = -lsqlite3

OBJS1 = main.o db.o traverse.o  # .o files are generated when we do gcc -c file.c.   This creates a file.o but we dont have to mention this in make as 
                              # make already has predefined rule %.o: %.c which has a command to convert the .c files to .o

OBJS2 = imageOpen.o
 
TARGET1 = db_exe
TARGET2 = IO

all: $(TARGET1) $(TARGET2)

$(TARGET1): $(OBJS1)
	$(CC) $(OBJS1) $(LIBS) -o $(TARGET1) 


$(TARGET2): $(OBJS2)
	$(CC) $(OBJS2) -o $(TARGET2) 
