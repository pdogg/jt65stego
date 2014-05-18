#!/usr/bin/python

import numpy as np
import jt65wrapy as jt
import jt65stego as jts
import sys
import binascii
from Crypto.Cipher import ARC4
from Crypto.Hash import SHA

key = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

if len(sys.argv) < 3:
	print 'poc3.py -- Proof of concept JT65 steganography encoder'
	print 'Usage: ./poc4.py <intented jt65 message> <secret message> <covernoise> <cipherkey>\n'
	sys.exit(1)
	    
legitmsg = sys.argv[1]
secretmsg = sys.argv[2]
covernoise = int(sys.argv[3])

legitjt = jt.encode(legitmsg)
secretjt = jt.encode(secretmsg)

print "\n\n--++== JT65 Stego PoC ==++--"
print "JT65 legit message 	: " + legitmsg 
print "Encoded as		: " + str(legitjt)

legitpacket = jt.prepmsg(legitjt)
print "\nLegit channel symbols with RS:"
print legitpacket

print "\nSecret message		  : " + secretmsg
print "Secret message encoded   : " + str(secretjt)

### Encryption 
cipherkey = sys.argv[4]
tempkey = SHA.new(cipherkey).digest()
cipher = ARC4.new(tempkey)

packedsecretjt = jts.jt65tobytes(secretjt)
print "\nPacked secret message: " + str(packedsecretjt)

crypted = cipher.encrypt(''.join('{0:02x}'.format(int(e)).decode("hex") for e in packedsecretjt))
cryptedlist = list(bytearray(crypted))
print "\nCipher msg: " + str(cryptedlist)
finalsteg = jts.bytestojt65(cryptedlist)
print "\nJT65 Encoded cipher: " + str(finalsteg)
### Encryption end

print "\nStego with key		: " + str(key)

stegedpacket = jts.jtsteg(legitpacket,finalsteg,key)
stegedpacket = jts.randomcover(stegedpacket,key,covernoise)

print "\nSteged channel packet:"
print stegedpacket

recoveredsteg = jts.jtunsteg(stegedpacket,key)

print "\nRecovered Stego message : " + str(recoveredsteg)

### Decryption
unpackedsteg = jts.jt65tobytes(recoveredsteg)
cipherkey = sys.argv[4]
tempkey = SHA.new(cipherkey).digest()
cipher = ARC4.new(tempkey)
decrypted = cipher.decrypt(''.join('{0:02x}'.format(int(e)).decode("hex") for e in unpackedsteg))
decryptedlist = list(bytearray(decrypted))
unpackeddecrypted = jts.bytestojt65(decryptedlist)
### Decryption end

print "\nRecovered Stego message : " + str(unpackeddecrypted)
print "\nDecoded Stego message : " + jt.decode(unpackeddecrypted)

print "\n\nDecoded JT65 message : "
print jt.decode(jt.unprepmsg(stegedpacket))
print "\n\n"

