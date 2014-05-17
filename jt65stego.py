import jt65wrapy as jt
import numpy as np
import random

def jtsteg(prepedmsg,secretmsg,key) :
#simple stego routine to enbed a secret message into a preped jt65 packet according to key
# prepedmsg - preped jt65 package ready to go on the wire
# secretmsg - encoded jt65 mesage
# key - list defining stego positions to insert as error
# returns a jt65 packet as a numpy array
	encsecretmsg = enc(secretmsg)
	outputmsg = np.copy(prepedmsg)
	for x in range(0,12):
		outputmsg[key[x]]=encsecretmsg[x]
	
	return outputmsg

def jtunsteg(recdmsg,key) :
#attempts to unsteg and return as a jt65 encoded message a stegoed mession in recdmsg according to key
# recdmsg - jt65 packet
# key - list defining stego positions to interpret as message
# returns a jt65 encoded string as a numpy array
	output = np.array(range(12),dtype=np.int32) #array to return
	for x in range(0,12):
		output[x] = recdmsg[key[x]]
	return dec(output)

def randomcover(message, key, howmuch=10) :
#insert some random cover noise
#message is a stegged jt65 message stegged with key 
#howmuch is how much random "error" to add
	noisecount = 0
	locs = []
	while noisecount < howmuch :
		loc = random.randint(0,62)
		while (loc in key) or (loc in locs) :
			loc = random.randint(0,62)
		locs.extend([loc])
		print "loc: " + str(loc)
		message[loc] = random.randint(0,63)
		print str(noisecount) + " round of cover - changed " + str(loc) + " to " + str(message[loc])
		noisecount += 1
	return message

def enc(msg) :
#returns an "encoded" jt65 message based on a supplied message
	return msg

def dec(msg) :
#returns a "decoded" jt65 message based on the supplied message
	return msg

def jt65tobytes(jt65bytes):
#Packs 12 byte JT65 message to 9 full bytes suitable for cipher
	output = np.array(range(9),dtype=np.int32)
	output[0] = (jt65bytes[0] & 0x3F) << 2 | (jt65bytes[1] & 0x30) >> 4
	output[1] = (jt65bytes[1] & 0x0F) << 4 | (jt65bytes[2] & 0x3C) >> 2 
	output[2] = (jt65bytes[2] & 0x03) << 6 | (jt65bytes[3] & 0x3F)

	output[3] = (jt65bytes[4] & 0x3F) << 2 | (jt65bytes[5] & 0x30) >> 4
	output[4] = (jt65bytes[5] & 0x0F) << 4 | (jt65bytes[6] & 0x3C) >> 2 
	output[5] = (jt65bytes[6] & 0x03) << 6 | (jt65bytes[7] & 0x3F)

	output[6] = (jt65bytes[8] & 0x3F) << 2 | (jt65bytes[9] & 0x30) >> 4
	output[7] = (jt65bytes[9] & 0x0F) << 4 | (jt65bytes[10] & 0x3C) >> 2 
	output[8] = (jt65bytes[10] & 0x03) << 6 | (jt65bytes[11] & 0x3F)
	return output

def bytestojt65(bytes):
#Unpacks 9 full bytes to 12 byte JT65 message
	output = np.array(range(12),dtype=np.int32)
	output[0] = bytes[0] >> 2
	output[1] = (bytes[0] & 0x03) << 4 | (bytes[1] & 0xF0) >> 4
	output[2] = (bytes[1] & 0x0F) << 2 | (bytes[2] & 0xC0) >> 6
	output[3] = bytes[2] & 0x3F
	output[4] = bytes[3] >> 2
	output[5] = (bytes[3] & 0x03) << 4 | (bytes[4] & 0xF0) >> 4
	output[6] = (bytes[4] & 0x0F) << 2 | (bytes[5] & 0xC0) >> 6
	output[7] = bytes[5] & 0x3F
	output[8] = bytes[6] >> 2
	output[9] = (bytes[6] & 0x03) << 4 | (bytes[7] & 0xF0) >> 4
	output[10] = (bytes[7] & 0x0F) << 2 | (bytes[8] & 0xC0) >> 6
	output[11] = bytes[8] & 0x3F
	return output