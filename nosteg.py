#!/usr/bin/python

import numpy as np
import jt65wrapy as jt
import jt65stego as jts
import jt65sound as jtsound
import sys

key = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

if len(sys.argv) < 2:
	print 'pocwithtones.py -- Proof of concept JT65 steganography encoder'
	print 'Usage: ./pocwithtones.py <intented jt65 message> <secret message>\n'
	sys.exit(1)
	    


legitmsg = sys.argv[1]
#secretmsg = sys.argv[2]

legitjt = jt.encode(legitmsg)
#secretjt = jt.encode(secretmsg)

print "\n\n--++== JT65 Stego PoC ==++--"
print "JT65 legit message 	: " + legitmsg 
print "Encoded as		: " + str(legitjt)

legitpacket = jt.prepmsg(legitjt)
print "\nLegit channel symbols with RS:"
print legitpacket

#print "\nSecret message		 : " + secretmsg
#print "Secret message encoded   : " + str(secretjt)

#print "Stego with key		: " + str(key)

#stegedpacket = jts.jtsteg(legitpacket,secretjt,key)

#print "\nSteged channel packet:"
#print stegedpacket

print "\nTones of message:"
print jtsound.tonepacket(legitpacket)

print "\nTones to send on wire:"

tonearray = jtsound.toneswithsync(legitpacket)


print tonearray
#jtsound.outputpygame(tonearray)
jtsound.outputwavfile("/home/pdogg/testlegit.wav", tonearray)
#recoveredsteg = jts.jtunsteg(stegedpacket,key)

#print "\nRecovered Stego message : " + str(recoveredsteg)

#print "\nDecoded Stego message : " + jt.decode(recoveredsteg)

#print "\n\nDecoded JT65 message : "
print jt.decode(jt.unprepmsg(legitpacket))
print "\n\n"
