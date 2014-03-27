CC = gcc
FC = g77
FFLAGS = -O -Wall -fbounds-check

OBJS1 = JT65code.o nchar.o grid2deg.o packmsg.o packtext.o \
	packcall.o packgrid.o unpackmsg.o unpacktext.o unpackcall.o \
	unpackgrid.o deg2grid.o packdxcc.o chkmsg.o getpfx1.o \
	getpfx2.o k2grid.o grid2k.o interleave63.o graycode.o set.o \
	igray.o mz.o


all:	JT65code

JT65code: $(OBJS1)
	$(FC) -o JT65code $(OBJS1)

.PHONY : clean
clean:
	-rm JT65code *.o

