#!/usr/bin/python

import numpy as np
import jt65wrapy as jt
import jt65stego as jts

key = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

legitmsg = "CQ KA1AAA FN42"
secretmsg = "MASSHACKERS"

legitjt = jt.encode(legitmsg)
secretjt = jt.encode(secretmsg)

print "\n\n--++== JT65 Stego PoC ==++--"
print "JT65 legit message 	: " + legitmsg 
print "Encoded as		: " + str(legitjt)

legitpacket = jt.prepmsg(legitjt)
print "\nLegit channel symbols with RS:"
print legitpacket

print "\nSecret message		 : " + secretmsg
print "Secret message encoded   : " + str(secretjt)

print "Stego with key		: " + str(key)

stegedpacket = jts.jtsteg(legitpacket,secretjt,key)

print "\nSteged channel packet:"
print stegedpacket

recoveredsteg = jts.jtunsteg(stegedpacket,key)

print "\nRecovered Stego message : " + str(recoveredsteg)

print "\nDecoded Stego message : " + jt.decode(recoveredsteg)

print "\n\nDecoded JT65 message : "
print jt.decode(jt.unprepmsg(stegedpacket))
print "\n\n"
