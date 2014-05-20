#!/usr/bin/python
#
# poc5.py
#
# PoC + AES
#
# Uses ECB! For small msgs this is probably OK - PoC only

import numpy as np
import jt65wrapy as jt
import jt65stego as jts
import sys
import binascii
from Crypto.Cipher import AES
from Crypto import Random

noisekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

if len(sys.argv) < 3:
	print 'poc5.py -- Proof of concept JT65 steganography encoder w/ AES'
	print 'Usage: ./poc5.py <intended jt65 message #1> <intended jt65 message #2> <secret message> <covernoise> <cipherkey>\n'
	sys.exit(1)
	    
legitmsg1 = sys.argv[1]
legitmsg2 = sys.argv[2]
secretmsg = sys.argv[3]
covernoise = int(sys.argv[4])
cipherkey = sys.argv[5]

#Check key size
if len(cipherkey) != 16 and len(cipherkey) != 24 and len(cipherkey) != 32:
	print ("\nCipher key must be 16, 24, or 32 bytes... sorry :(\n")
	sys.exit(0)

#Check secret message size
if len(secretmsg) > 16:
	print ("\nPoC only supports secret message up to 16 bytes... sorry :(\n")
	sys.exit(0)

#Prep the encrypted hidden data
cryptobj = AES.new(cipherkey, AES.MODE_ECB)
secretmsg = "{:<16}".format(secretmsg)
cipherdata = cryptobj.encrypt(secretmsg)
cipherlist = list(bytearray(cipherdata))

finalsteg1 = jts.bytes8tojt65(cipherlist[0:8], 1)
finalsteg2 = jts.bytes8tojt65(cipherlist[8:16], 2)
print "\nCipher list: " + str(cipherlist)
print "\nJT65 Encoded Cipher Data #1 : " + str(finalsteg1)
print "\nJT65 Encoded Cipher Data #2 : " + str(finalsteg2)

print "\nStego with key		: " + str(noisekey)

legitjt1 = jt.encode(legitmsg1)
legitpacket1 = jt.prepmsg(legitjt1)
stegedpacket1 = jts.jtsteg(legitpacket1,finalsteg1,noisekey)
stegedpacket1 = jts.randomcover(stegedpacket1,noisekey,covernoise)
print "\nSteged channel packet 1:"
print stegedpacket1

legitjt2 = jt.encode(legitmsg2)
legitpacket2 = jt.prepmsg(legitjt2)
stegedpacket2 = jts.jtsteg(legitpacket2,finalsteg2,noisekey)
stegedpacket2 = jts.randomcover(stegedpacket2,noisekey,covernoise)
print "\nSteged channel packet 2:"
print stegedpacket2

## RECEIVE
recoveredsteg1 = jts.jtunsteg(stegedpacket1,noisekey)
recoveredsteg2 = jts.jtunsteg(stegedpacket2,noisekey)

print "\nRecovered Stego message 1: " + str(recoveredsteg1)
print "\nRecovered Stego message 2: " + str(recoveredsteg2)

unpackedsteg1 = jts.jt65tobytes(recoveredsteg1)[1:10]
unpackedsteg2 = jts.jt65tobytes(recoveredsteg2)[1:10]
finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in unpackedsteg1)) + (''.join('{0:02x}'.format(int(e)).decode("hex") for e in unpackedsteg2))

cryptobj = AES.new(cipherkey, AES.MODE_ECB)
hiddendata = cryptobj.decrypt(finalcipherdata)
print "\nDecoded Stego message : " + hiddendata

print "\n\nDecoded JT65 message 1 : "
print jt.decode(jt.unprepmsg(stegedpacket1))
print "\n\nDecoded JT65 message 2 : "
print jt.decode(jt.unprepmsg(stegedpacket2))
print "\n\n"

