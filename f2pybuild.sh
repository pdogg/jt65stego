#!/bin/bash
rm *.so

cd lib/
rm *.o 
FORTRANFLAGS="-g -O2 -fno-range-check -ffixed-line-length-none -Wall -fbounds-check -fno-second-underscore -fPIC -O2 -fbounds-check -fno-second-underscore -Wall -Wno-conversion -Wno-character-truncation -c "
gfortran $FORTRANFLAGS chkmsg.f90
gfortran $FORTRANFLAGS deg2grid.f90
gfortran $FORTRANFLAGS encode65.f90
gfortran $FORTRANFLAGS getpfx1.f90
gfortran $FORTRANFLAGS getpfx2.f90
gfortran $FORTRANFLAGS graycode.f90
gfortran $FORTRANFLAGS grid2deg.f90
gfortran $FORTRANFLAGS grid2k.f90
gfortran $FORTRANFLAGS interleave63.f90
gfortran $FORTRANFLAGS k2grid.f90
gfortran $FORTRANFLAGS nchar.f90
gfortran $FORTRANFLAGS packcall.f90
gfortran $FORTRANFLAGS packgrid.f90
gfortran $FORTRANFLAGS packtext.f90
gfortran $FORTRANFLAGS set.f90
gfortran $FORTRANFLAGS unpackcall.f90
gfortran $FORTRANFLAGS unpackgrid.f90
gfortran $FORTRANFLAGS unpacktext.f90
gfortran $FORTRANFLAGS unpackmsg.f90
gfortran $FORTRANFLAGS packmsg.f90

f2py -c -I. --fcompiler=gnu95 --f77exec=gfortran --f90exec=gfortran --opt="-cpp  -g -fno-range-check -ffixed-line-length-none -fbounds-check -O2 -fno-second-underscore -Wall -Wno-conversion -Wno-character-truncation"  -m JT65 *.o decode_rs.c encode_rs.c init_rs.c wrapkarn.c igray.c JT65code_all.f
cd ..
cp lib/JT65.so .
