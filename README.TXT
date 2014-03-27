The code contained in this archive is intended to document and
illustrate some details of the encoding of a JT65 message.

Unpack the archive into a clean directory and give the "make" command.
This will compile and link the program JT65code.  An example with
actual output:

% make
% JT65code "G3LTF DL9KR JO40"
Message:   G3LTF DL9KR JO40      
Packed message, 6-bit symbols:  61 37 30 28  9 27 61 58 26  3 49 16
Channel symbols, including FEC:
   14 16  9 18  4 60 41 18 22 63 43  5 30 13 15  9 25 35 50 21  0
   36 17 42 33 35 39 22 25 39 46  3 47 39 55 23 61 25 58 47 16 38
   39 17  2 36  4 56  5 16 15 55 18 41  7 26 51 17 18 49 10 13 24
Decoded message: G3LTF DL9KR JO40           

