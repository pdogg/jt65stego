import jt65wrapy as jt

test = jt.encode("testing")
print test
print jt.prepmsg(test)
test2 = jt.prepsteg(test)
print test2
test4 = jt.unprepsteg(test2)
test2[1] = 13
test2[5] = 13
test2[18] = 13

print test2

test3 = jt.unprepsteg(test2)
print test3
print jt.decode(test3)
