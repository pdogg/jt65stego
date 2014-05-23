import sys
import jt65wrapy as jt
import numpy as np
import random
from Crypto.Cipher import AES
import hashlib
#import binascii #only needed if we're debugging
import struct

def jtsteg(prepedmsg,secretmsg,key) :
#simple stego routine to enbed a secret message into a preped jt65 packet according to key
# prepedmsg - preped jt65 package ready to go on the wire
# secretmsg - encoded jt65 mesage
# key - list defining stego positions to insert as error
# returns a jt65 packet as a numpy array
	outputmsg = np.copy(prepedmsg)
	for x in range(0,12):
		outputmsg[key[x]]=secretmsg[x]
	
	return outputmsg

def jtunsteg(recdmsg,key) :
#attempts to unsteg and return as a jt65 encoded message a stegoed mession in recdmsg according to key
# recdmsg - jt65 packet
# key - list defining stego positions to interpret as message
# returns a jt65 encoded string as a numpy array
	output = np.array(range(12),dtype=np.int32) #array to return
	for x in range(0,12):
		output[x] = recdmsg[key[x]]
	return output

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
		coverint = random.randint(0,63)
		while coverint == message[loc]:
			coverint = random.randint(0,63)
		message[loc] = coverint
		if verbose:
			print str(noisecount) + " round of cover - changed " + str(loc) + " to " + str(message[loc])
		noisecount += 1
	return message

def getnoisekey(password) :
#I AM NOT A CRYPTOGRAPHER I HAVE NO IDEA IF THIS IS SAFE
#THIS FEATURE LEAKS BYTES OF THE sha256 HASH OF THE PASSWORD!!!
#returns a "noisekey" given a password
#md5 hashes the password and then uses it to determine the key (insertion locations on the stego)
#returns FALSE if no valid key can be obtained
   output = np.array(range(12),dtype=np.int32) #array to return
   
   sha256calc = hashlib.sha256()
   sha256calc.update(password)
   passwordhash = sha256calc.digest()
#  print binascii.hexlify(passwordhash)
   donthavekey = True
   hashindex = 0
   keyindex = 0
   while donthavekey :
    
    if hashindex >= len(passwordhash) :
      return False
    potentialsymbol = int(struct.unpack("B",passwordhash[hashindex])[0]) % 63
#    print potentialsymbol
    if potentialsymbol not in output :
      output[keyindex] = potentialsymbol
      keyindex += 1
    hashindex += 1  
    if keyindex == 12 :
      donthavekey = False
   return output

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

def jt65encodemessages(jt65msgs, verbose):
#Encode valid text into array of JT65 data
	jt65data = []

	for index,value in enumerate(jt65msgs):
		legitjt = jt.encode(value)
		legitpacket = jt.prepmsg(legitjt)

		if verbose:
			print "JT65 legit message " + str(index) + " : " + value
			print "Encoded as : " + str(legitjt)
			print "Legit channel symbols with RS :" + str(legitpacket)

		jt65data.append(legitpacket)

	return jt65data

def decodemessages(jt65data, verbose):
#Decode valid JT65 messages from array of JT65 data
	jt65msgs = []

	for index,value in enumerate(jt65data):
		jt65msg = jt.decode(jt.unprepmsg(value))
		if verbose:
			print "JT65 Message " + str(index) + " : " + jt65msg
		jt65msgs.append(jt65msg)

	return jt65msgs

def createciphermsgs(jt65msgcount, stegmsg, cipher, key, recipient, aesmode, verbose):
	ciphermsgs = []

	if cipher == "none":
		#Can we fit your hidden message?
		if jt65msgcount * 13 < len(stegmsg):
			print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
			sys.exit(0)

		for index in range(jt65msgcount):
			secretjt = jt.encode(stegmsg[index*13:index*13+13])

			if verbose:
				print "Secret message " + str(index) + " : " + stegmsg[index*13:index*13+13]
				print "Secret message " + str(index) + " encoded : " + str(secretjt)

			ciphermsgs.append(secretjt)

	if cipher == "AES":
		#Check key size
		if len(key) != 16 and len(key) != 24 and len(key) != 32:
			print ("\nCipher key must be 16, 24, or 32 bytes... sorry :(\n")
			sys.exit(0)

		#Can we fit your hidden message?
		if jt65msgcount * 8 < len(stegmsg):
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
			print "Cipher list: " + str(cipherlist)

		for index in range(jt65msgcount):
			thissteg = bytes8tojt65(cipherlist[index*8:(index*8)+8], index)

			if verbose:
				print "JT65 Encoded Cipher Data Msg " + str(index) + " : " + str(thissteg)

			ciphermsgs.append(thissteg)

	return ciphermsgs

def steginject(jt65data, noise, cipherdata, hidekey, verbose):
#Combine array of JT65 valid messages with array of JT65 encoded steg data
	finalpackets = []

	for index in range(len(jt65data)):
		stegedpacket = jtsteg(jt65data[index],cipherdata[index],hidekey)
		stegedpacket = randomcover(stegedpacket,hidekey,noise,verbose)
		finalpackets.append(stegedpacket)

	return finalpackets

def retrievesteg(jt65data, hidekey, verbose):
#Retrieve steganography data from array of JT65 data
	stegdata = []

	for index,value in enumerate(jt65data):
		data = jtunsteg(value,hidekey)
		if verbose:
			print "Steg Bytes in Message " + str(index) + " : " + str(data)
		stegdata.append(data)

	return stegdata

def deciphersteg(stegdata, cipher, key, aesmode, verbose):
#Decipher hidden message from array of data hidden in JT65 errors
	stegedmsg = ""
	stegedmsgba = np.array(range(0),dtype=np.int32)

	for index,value in enumerate(stegdata):
		if cipher == "none":
			recoveredtext = jt.decode(value)[0:13]
			if verbose:
				print "Steg Text in Message " + str(index) + " : " + recoveredtext
			stegedmsg += recoveredtext

		else:
			thisunstegbytes = jt65tobytes(value)[1:10]
			if verbose:
				print "Steg Data in Message " + str(index) + " : " + str(thisunstegbytes)
			stegedmsgba = np.append(stegedmsgba, thisunstegbytes)

	if cipher == "AES":
		if verbose:
			print"Cipher Data : " + str(stegedmsgba)

		finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in stegedmsgba))
		
		if verbose:
			print"Cipher Data Hex : " + finalcipherdata

		if aesmode == "ECB":
			cryptobj = AES.new(key, AES.MODE_ECB)
		#elif aesmode == "CBC":
		#	cryptobj = AES.new(key, AES.MODE_CBC)
		#elif aesmode == "CFB":
		#	cryptobj = AES.new(key, AES.MODE_CFB)

		stegedmsg = cryptobj.decrypt(finalcipherdata)

	return stegedmsg
