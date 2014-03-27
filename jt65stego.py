import jt65wrapy as jt
import numpy as np

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


def enc(msg) :
#returns an "encoded" jt65 message based on a supplied message
	return msg

def dec(msg) :
#returns a "decoded" jt65 message based on the supplied message
	return msg
