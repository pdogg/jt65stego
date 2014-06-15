
all:
	cd lib && make all

jt65:
	cd lib && make jt65

f2pylib:
	cd lib && make f2pylib

clean:
	rm *.so
	rm jt65
	rm lib/*.so
	rm lib/*.o
	rm lib/jt65
  
