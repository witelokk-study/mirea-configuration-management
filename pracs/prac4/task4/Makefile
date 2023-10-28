.PHONY: all clean

prog: prog.c data.c
	gcc prog.c data.c -o prog

files.lst: *
	dir -B >> files.lst

distr.zip:
	7z a distr.zip *.*


all: prog files.lst distr.zip

clean:
	rm -rf prog files.lst distr.zip
