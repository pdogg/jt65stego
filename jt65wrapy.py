#Some usful wrapper functions for f2py version of JT65
#@pdogg77 - paul@pauldrapeau.com Paul Drapeau 

import numpy, JT65

def encode(message) :
#return a numpy array which is the 13 element JT65 message symbols
	output = numpy.array(range(12),dtype=numpy.int32) #array to return
	JT65.packmsg(message,output)
	return output

def decode(recarray) :
#returns a string decoded from the 12 element recarray received
	output = numpy.array(range(22),'c')
	JT65.unpackmsg(recarray,output)
	retstr = ''.join(output)
	return retstr

def prepmsg(message) :
#return an array of 6 bit symbols preped for transmission on the channel and a JT65 packet
#will do Reed Solomon coding, graycode and interleave functions
	output = numpy.array(range(63),dtype=numpy.int32)
	JT65.prepmsg(message,output)
	return output

def unprepmsg(recvd) :
#return an array of 6 bit symbols representing a JT65 message from the supplied recvd packet
#recvd packet is a numpy array of range 63 containing a prepped or received JT65 packet
#will do interleave removal, graycode removal and Reed Solomon decoding
# WARNING!!! - recvd is NOT preserved during this call remember to save and restore it

	output = numpy.array(range(12),dtype=numpy.int32) #array to return
	JT65.unprepmsg(recvd, output)
	return output

def prepsteg(message) :
#return an array of 6 bit symbols preped for transmission on the channel as a 20 symbol steg packet 
#will do Reed Solomon coding
	output = numpy.array(range(20),dtype=numpy.int32)
	JT65.prepsteg(message,output)
	return output

def unprepsteg(recvd) :
#return an array of 6 bit symbols representing a steg message from the supplied recvd packet
#recvd packet is a numpy array of range 20 containing a prepped or received steg packet
#will do Reed Solomon decoding
# WARNING!!! - recvd is NOT preserved during this call remember to save and restore it

	output = numpy.array(range(12),dtype=numpy.int32) #array to return
	JT65.unprepsteg(recvd, output)
	return output
