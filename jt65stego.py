import sys
import jt65wrapy as jt
import numpy as np
import random
from Crypto.Cipher import AES

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

def randomcover(message, key, howmuch=10, verbose=False) :
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
		if verbose:
			print "loc: " + str(loc)
		message[loc] = random.randint(0,63)
		if verbose:
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

def bytes8tojt65(bytes, status):
#Unpacks 8 full bytes plus a status byte to 12 byte JT65 message
	output = np.array(range(12),dtype=np.int32)
	output[0] = status >> 2
	output[1] = (status & 0x03) << 4 | (bytes[0] & 0xF0) >> 4
	output[2] = (bytes[0] & 0x0F) << 2 | (bytes[1] & 0xC0) >> 6
	output[3] = bytes[1] & 0x3F
	output[4] = bytes[2] >> 2
	output[5] = (bytes[2] & 0x03) << 4 | (bytes[3] & 0xF0) >> 4
	output[6] = (bytes[3] & 0x0F) << 2 | (bytes[4] & 0xC0) >> 6
	output[7] = bytes[4] & 0x3F
	output[8] = bytes[5] >> 2
	output[9] = (bytes[5] & 0x03) << 4 | (bytes[6] & 0xF0) >> 4
	output[10] = (bytes[6] & 0x0F) << 2 | (bytes[7] & 0xC0) >> 6
	output[11] = bytes[7] & 0x3F
	return output

def BatchEncode(jt65msg, stegmsg, noise, cipher, key, recipient, aesmode, verbose, stdout, wavout, hidekey):
	jt65msgs = jt65msg.split(',')

	if cipher == "none":
		#Can we fit your hidden message?
		if len(jt65msgs) * 13 < len(stegmsg):
			print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
			sys.exit(0)

		for index,value in enumerate(jt65msgs):
			legitjt = jt.encode(value)
			secretjt = jt.encode(stegmsg[index*13:index*13+13])
			legitpacket = jt.prepmsg(legitjt)

			if verbose:
				print "JT65 legit message 	: " + value
				print "Encoded as		: " + str(legitjt)
				print "\nLegit channel symbols with RS:"
				print legitpacket
				print "\nSecret message		: " + stegmsg[index*13:index*13+13]
				print "Secret message encoded  : " + str(secretjt)

			stegedpacket = jtsteg(legitpacket,secretjt,hidekey)
			stegedpacket = randomcover(stegedpacket,hidekey,noise,verbose)

			if verbose:
				print "Stego with key		: " + str(hidekey)

			if stdout:
				np.set_printoptions(linewidth=300)
				print stegedpacket

	if cipher == "AES":
		#Check key size
		if len(key) != 16 and len(key) != 24 and len(key) != 32:
			print ("\nCipher key must be 16, 24, or 32 bytes... sorry :(\n")
			sys.exit(0)

		#Can we fit your hidden message?
		if len(jt65msgs) * 8 < len(stegmsg):
			print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
			sys.exit(0)

		#Prep the encrypted hidden data
		if aesmode == "ECB":
			cryptobj = AES.new(key, AES.MODE_ECB)
		#elif aesmode == "CBC":
		#	cryptobj = AES.new(key, AES.MODE_CBC)
		#elif aesmode == "CFB":
		#	cryptobj = AES.new(key, AES.MODE_CFB)
		while len(stegmsg) % 16:
			stegmsg += " "

		cipherdata = cryptobj.encrypt(stegmsg)
		cipherlist = list(bytearray(cipherdata))

		if verbose: 			
			print "\nCipher list: " + str(cipherlist)

		for index,value in enumerate(jt65msgs):
			thissteg = bytes8tojt65(cipherlist[index*8:(index*8)+8], index)

			if verbose:

				print "\nJT65 Encoded Cipher Data Msg " + str(index) + " : " + str(thissteg)
				print "\nStego with key		: " + str(hidekey)

			legitjt = jt.encode(value)
			legitpacket = jt.prepmsg(legitjt)
			stegedpacket = jtsteg(legitpacket,thissteg,hidekey)
			stegedpacket = randomcover(stegedpacket,hidekey,noise)

			if stdout:
				np.set_printoptions(linewidth=300)
				print stegedpacket

def BatchDecode(cipher, key, aesmode, verbose, stdin, wavin, hidekey):
	stegedmsg = ""
	stegedmsgba = np.array(range(0),dtype=np.int32)

	if stdin:
		stdinput = sys.stdin.readlines()
	
	for index,value in enumerate(stdinput):
		if verbose:
			print "Message " + str(index) + " : " + value

		numpymsg = np.fromstring(value.replace('[','').replace(']',''), dtype=int, sep=' ')
		print "\nDecoded JT65 message " + str(index) + ": " + jt.decode(jt.unprepmsg(numpymsg))

		if cipher == "none":
			recoveredsteg = jtunsteg(numpymsg,hidekey)
			recoveredtext = jt.decode(recoveredsteg)[0:13]
			if verbose:
				print "\nRecovered Stego message : " + str(recoveredsteg)
				print "\nText : " + recoveredtext
			stegedmsg += recoveredtext

		else:
			thisunsteg = jtunsteg(numpymsg,hidekey)
			thisunstegbytes = jt65tobytes(thisunsteg)[1:10]

			if verbose:
				print "\nRecovered Stego message " + str(index) + " : " + str(thisunsteg)
				print "\nStego message " + str(index) + " bytes : " + str(thisunstegbytes)

			stegedmsgba = np.append(stegedmsgba, thisunstegbytes)

	if cipher == "AES":
		if verbose:
			print"\nCipher Data A : " + str(stegedmsgba)

		finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in stegedmsgba))
		
		if verbose:
			print"\nCipher Data B : " + finalcipherdata

		if aesmode == "ECB":
			cryptobj = AES.new(key, AES.MODE_ECB)
		#elif aesmode == "CBC":
		#	cryptobj = AES.new(key, AES.MODE_CBC)
		#elif aesmode == "CFB":
		#	cryptobj = AES.new(key, AES.MODE_CFB)

		stegedmsg = cryptobj.decrypt(finalcipherdata)

	print "\nStego message : " + stegedmsg