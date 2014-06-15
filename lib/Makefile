# Set paths
EXE_DIR = ../
INCPATH =

CC = gcc
CXX = g++
FC = gfortran

F2PYFLAGS = -g -O2 -fno-range-check -ffixed-line-length-none -Wall -fbounds-check -fno-second-underscore -fPIC -O2 -fbounds-check -fno-second-underscore -Wall -Wno-conversion -Wno-character-truncation -c 
FFLAGS = -O2 -ggdb -fbounds-check -Wall -Wno-conversion -fno-second-underscore \
       -fPIE -DUNIX
CFLAGS = -I. -ggdb -fbounds-check -fPIE

# Default rules
%.o: %.c
	${CC} ${CFLAGS} -c $<
%.o: %.f
	${FC} ${FFLAGS} -c $<
%.o: %.F
	${FC} ${FFLAGS} -c $<
%.o: %.f90
	${FC} ${FFLAGS} -c $<
%.o: %.F90
	${FC} ${FFLAGS} -c $<

all:    jt65 f2pylib

OBJS1 = pctile.o graycode.o sort.o ssort.o chkmsg.o \
	unpackmsg.o igray.o unpackcall.o unpackgrid.o \
	grid2k.o unpacktext.o getpfx2.o packmsg.o deg2grid.o \
	packtext.o getpfx1.o packcall.o k2grid.o packgrid.o \
	nchar.o four2a.o grid2deg.o pfxdump.o f77_wisdom.o \
	symspec.o analytic.o db.o genjt9.o \
	packbits.o unpackbits.o encode232.o interleave9.o \
	entail.o fano232.o gran.o sync9.o decode9.o \
	fil3.o decoder.o grid2n.o n2grid.o timer.o \
	softsym.o peakdt9.o getlags.o afc9.o fchisq.o \
	twkfreq.o downsam9.o symspec2.o sleep_msec.o \
	stdmsg.o sec_midn.o usleep.o azdist.o geodist.o morse.o \
	fillcom.o chkss2.o zplot9.o flat2.o \
	jt65a.o symspec65.o flat65.o ccf65.o decode65a.o \
	filbig.o fil6521.o afc65b.o decode65b.o setup65.o \
	extract.o fchisq65.o demod64a.o chkhist.o interleave63.o ccf2.o \
	move.o indexx.o graycode65.o twkfreq65.o smo121.o \
	wrapkarn.o init_rs.o encode_rs.o decode_rs.o gen65.o fil4.o \
	flat3.o polfit.o determ.o baddata.o

libjt9.a: $(OBJS1)
	ar cr libjt9.a $(OBJS1) 
	ranlib libjt9.a

OBJS2 = jt9.o jt9a.o jt9b.o jt9c.o

jt9: 	$(OBJS2) libjt9.a 
	$(CXX) -o jt9 $(OBJS2) -L. -ljt9 -lQt5Core -lfftw3f `$(FC) -print-file-name=libgfortran.so`
	mkdir -p $(EXE_DIR)
	cp jt9 $(EXE_DIR)

OBJS3 = jt9sim.o 
jt9sim: $(OBJS3) libjt9.a
	$(FC) -o jt9sim $(OBJS3) -L. -ljt9

OBJS4 = jt9code.o 
jt9code: $(OBJS4) libjt9.a
	$(FC) -o jt9code $(OBJS4) -L. -ljt9
	cp jt9code $(EXE_DIR)

OBJS6 = jt65code.o
jt65code: $(OBJS6) libjt9.a
	$(FC) -o jt65code $(OBJS6) -L. -lfftw3f libjt9.a
	cp jt65code $(EXE_DIR)

OBJS88 = jt65.o
jt65: $(OBJS88) libjt9.a
	$(FC) -o jt65 $(OBJS88) -L. -ljt9 -lfftw3f libjt9.a	
	cp jt65 $(EXE_DIR)

sync9.o: sync9.f90 jt9sync.f90
	$(FC) $(FFLAGS) -c sync9.f90

peakdf9.o: peakdf9.f90 jt9sync.f90
	$(FC) $(FFLAGS) -c peakdf9.f90

peakdt9.o: peakdt9.f90 jt9sync.f90
	$(FC) $(FFLAGS) -c peakdt9.f90

jt9sim.o: jt9sim.f90 jt9sync.f90
	$(FC) $(FFLAGS) -c jt9sim.f90

genjt9.o: genjt9.f90 jt9sync.f90
	$(FC) $(FFLAGS) -c genjt9.f90

redsync.o: redsync.f90 jt9sync.f90
	$(FC) $(FFLAGS) -c redsync.f90

ipcomm.o: ipcomm.cpp
	$(CXX) -c $(INCPATH) -fPIE ipcomm.cpp

sec_midn.o: sec_midn.f90
	$(FC) -c -fno-second-underscore sec_midn.f90

init_rs.o: init_rs.c
	$(CC) -c -DBIGSYM=1 -o init_rs.o init_rs.c

encode_rs.o: encode_rs.c
	$(CC) -c -DBIGSYM=1 -o encode_rs.o encode_rs.c

decode_rs.o: decode_rs.c
	$(CC) -c -DBIGSYM=1 -o decode_rs.o decode_rs.c

	
f2pylib:
	rm *.o
	$(FC) $(F2PYFLAGS) chkmsg.f90
	$(FC) $(F2PYFLAGS) deg2grid.f90
	$(FC) $(F2PYFLAGS) encode65.f90
	$(FC) $(F2PYFLAGS) getpfx1.f90
	$(FC) $(F2PYFLAGS) getpfx2.f90
	$(FC) $(F2PYFLAGS) graycode.f90
	$(FC) $(F2PYFLAGS) grid2deg.f90
	$(FC) $(F2PYFLAGS) grid2k.f90
	$(FC) $(F2PYFLAGS) interleave63.f90
	$(FC) $(F2PYFLAGS) k2grid.f90
	$(FC) $(F2PYFLAGS) nchar.f90
	$(FC) $(F2PYFLAGS) packcall.f90
	$(FC) $(F2PYFLAGS) packgrid.f90
	$(FC) $(F2PYFLAGS) packtext.f90
	$(FC) $(F2PYFLAGS) set.f90
	$(FC) $(F2PYFLAGS) unpackcall.f90
	$(FC) $(F2PYFLAGS) unpackgrid.f90
	$(FC) $(F2PYFLAGS) unpacktext.f90
	$(FC) $(F2PYFLAGS) unpackmsg.f90
	$(FC) $(F2PYFLAGS) packmsg.f90

	f2py -c -I. --fcompiler=gnu95 --f77exec=gfortran --f90exec=gfortran --opt="-cpp  -g -fno-range-check -ffixed-line-length-none -fbounds-check -O2 -fno-second-underscore -Wall -Wno-conversion -Wno-character-truncation"  -m JT65 *.o decode_rs.c encode_rs.c init_rs.c wrapkarn.c igray.c JT65code_all.f

	cp JT65.so ../
	

.PHONY : clean


clean:
	rm -f *.o jt65
