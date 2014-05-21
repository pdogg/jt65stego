jt65stego
=========

Fork/Branch with the new WSJT fortran libs
build them with 
bash ./f2pybuild.sh

There's no encoder diference I can find... :(






jt65stego project

Well the good news is the code still fucking works :)

pdogg@0xffe4:~/code/gits/jt65stego$ ./poc2.py "KA1AAA KA2BBB FN42" "BEACON FTW"


--++== JT65 Stego PoC ==++--
JT65 legit message      : KA1AAA KA2BBB FN42
Encoded as              : [34 16 49 30 62  9  4 21 49 53 33 40]

Legit channel symbols with RS:
[36 20 25 31 55 30 42 36 13 61 39 44 12 41 56 18 17  6 62 42  4  8  4 13 49
 51 31 35 53  9 62 19 47  4 24 41 62 41 33  4  4 29 19 41 47 42 10 45 27 49
 26 23 17 49 24 52 44 44 14 23 50 33 60]

Secret message           : BEACON FTW
Secret message encoded   : [16 52 50 11  6 13 41 26 39 15 56 28]
Stego with key          : [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

Steged channel packet:
[36 16 25 52 55 50 42 11 13  6 39 13 12 41 56 26 17 39 62 15  4 56  4 28 49
 51 31 35 53  9 62 19 47  4 24 41 62 41 33  4  4 29 19 41 47 42 10 45 27 49
 26 23 17 49 24 52 44 44 14 23 50 33 60]

Recovered Stego message : [16 52 50 11  6 13 41 26 39 15 56 28]

Decoded Stego message : BEACON FTW           

Decoded JT65 message : 
 KA1AAA KA2BBB FN42  
