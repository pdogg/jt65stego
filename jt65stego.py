import sys
import jt65wrapy as jt
import numpy as np
import random
from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
from Crypto.Cipher import XOR
from Crypto.Hash import SHA
from gnupg import GPG
import hashlib
import binascii
import struct
import io
import os
import math

#Maximum number of bytes a multi-packet steg message may contain
MAX_MULTI_PACKET_STEG_BYTES_XOR		= 64 * 8
MAX_MULTI_PACKET_STEG_BYTES_ARC4	= 128 * 8
MAX_MULTI_PACKET_STEG_BYTES_AES		= 128 * 8
MAX_MULTI_PACKET_STEG_BYTES_GPG		= 128 * 8

def jtsteg(prepedmsg,secretmsg,key) :
#simple stego routine to enbed a secret message into a preped jt65 packet according to key
# prepedmsg - preped jt65 package ready to go on the wire
# secretmsg - encoded jt65 mesage
# key - list defining stego positions to insert as error
# returns a jt65 packet as a numpy array
	outputmsg = np.copy(prepedmsg)
	for x in range(len(secretmsg)):
		outputmsg[key[x]]=secretmsg[x]
	
	return outputmsg

def jtunsteg(recdmsg,key) :
#attempts to unsteg and return as a jt65 encoded message a stegoed mession in recdmsg according to key
# recdmsg - jt65 packet
# key - list defining stego positions to interpret as message
# returns a jt65 encoded string as a numpy array
	output = np.array(range(20),dtype=np.int32) #array to return
	for x in range(len(key)):
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
		while loc in locs :
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

def getnoisekey(password, length=20) :
#I AM NOT A CRYPTOGRAPHER I HAVE NO IDEA IF THIS IS SAFE
#THIS FEATURE LEAKS BITS OF THE sha512 HASH OF THE PASSWORD!!!
#returns a "noisekey" given a password
#md5 hashes the password and then uses it to determine the key (insertion locations on the stego)
#returns FALSE if no valid key can be obtained
#set length based on the length of key you want (12 for no_fec, 20 for stego with fec)
   output = np.array(range(length),dtype=np.int32) #array to return
   
   sha512calc = hashlib.sha512()
   sha512calc.update(password)
   passwordhash = sha512calc.digest()
   donthavekey = True
   hashindex = 0
   keyindex = 0
   while donthavekey :
    
    if hashindex >= len(passwordhash) :
      sha512calc.update(passwordhash)
      passwordhash = sha512calc.digest()
      hashindex = 0
    potentialsymbol = int(struct.unpack("B",passwordhash[hashindex])[0]) % 63
    if potentialsymbol not in output :
      output[keyindex] = potentialsymbol
      keyindex += 1
    hashindex += 1  
    if keyindex == length :
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

def jt65encodemessages(jt65msgs, verbose=False):
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

def decodemessages(jt65data, verbose=False):
#Decode valid JT65 messages from array of JT65 data
	jt65msgs = []

	for index,value in enumerate(jt65data):
		jt65msg = jt.decode(jt.unprepmsg(value))
		if verbose:
			print "JT65 Message " + str(index) + " : " + jt65msg
		jt65msgs.append(jt65msg)

	return jt65msgs

def otp_ascii_int_to_otp_int(charint):
	if charint == 32:
		return 0

	if charint >= 48 and charint <= 57:
		return charint - 47

	if charint >= 65 and charint <= 90:
		return charint - 54

	print("OTP only supports CAPTIAL letters and numbers for steg data and key")
	sys.exit(0)

def otp_otp_int_to_ascii_int(charint):
	if charint == 0:
		return 32

	if charint >= 1 and charint <= 10:
		return charint + 47

	if charint >= 11 and charint <= 36:
		return charint + 54

	print("OTP only supports CAPTIAL letters and numbers for steg data and key")
	sys.exit(0)

def otp_encode(stegmsg, key):
	encodedmsg = ""

	if len(key) < len(stegmsg):
		print("Length of OTP key must be equal to or greater than hidden data length")
		sys.exit(0)

	for index in range(len(stegmsg)):
		currentmsgint = otp_ascii_int_to_otp_int(ord(stegmsg[index]))
		currentkeyint = otp_ascii_int_to_otp_int(ord(key[index]))
		writeint = (currentmsgint + currentkeyint) % 37
		encodedmsg += chr(otp_otp_int_to_ascii_int(writeint))

	return encodedmsg

def otp_decode(stegmsg, key):
	decodedmsg = ""

	while len(key) < len(stegmsg):
		#We have no way of knowing the true length of the stegmsg during decode since it gets padded during packing
		#Assume the correct key length and additional padding at the end won't affect the result
		key += " "

	for index in range(len(stegmsg)):
		currentmsgint = otp_ascii_int_to_otp_int(ord(stegmsg[index]))
		currentkeyint = otp_ascii_int_to_otp_int(ord(key[index]))
		writeint = (currentmsgint - currentkeyint) % 37
		decodedmsg += chr(otp_otp_int_to_ascii_int(writeint))

	return decodedmsg

def createciphermsgs(jt65msgcount, stegmsg, cipher, key, recipient, aesmode, verbose=False):
	ciphermsgs = []

	if cipher == "none":
		return createciphermsgs_none(jt65msgcount, stegmsg, verbose)

	if cipher == "XOR":
		return createciphermsgs_xor(jt65msgcount, stegmsg, key, verbose)

	if cipher == "ARC4":
		return createciphermsgs_arc4(jt65msgcount, stegmsg, key, verbose)

	if cipher == "AES":
		return createciphermsgs_aes(jt65msgcount, stegmsg, key, aesmode, verbose)

	if cipher == "GPG":
		return createciphermsgs_gpg(jt65msgcount, stegmsg, recipient, verbose)

	if cipher == "OTP":
		return createciphermsgs_otp(jt65msgcount, stegmsg, key, verbose)

	return None

def createciphermsgs_none(jt65msgcount, stegmsg, verbose=False):
	ciphermsgs = []

	#Can we fit your hidden message?
	if jt65msgcount * 13 < len(stegmsg):
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)

	for index in range(jt65msgcount):
		secretjt = jt.encode(stegmsg[index*13:index*13+13])
		secretjtfec = jt.prepsteg(secretjt)

		if verbose:
			print "Secret message " + str(index) + " : " + stegmsg[index*13:index*13+13]
			print "Secret message " + str(index) + " encoded : " + str(secretjt)
			print "Secret message " + str(index) + " encoded with FEC : " + str(secretjtfec)

		ciphermsgs.append(secretjtfec)

	return ciphermsgs

def createciphermsgs_packer_xor(totalpackets, originallength, ciphermsgs, cipherlist, verbose=False):
	for index in range(totalpackets):
		#Determine how many bytes are in this message
		if originallength >= 8:
			thislength = 8
		else:
			thislength = originallength % 8
		originallength -= 8

		status = 0
		if index == 0:
			#First packet sets first bit to one, then remaining bits show total number of packets
			status = 0x80 | totalpackets
		elif index == totalpackets - 1:
			#Last packet sets second bit to one, then remaining bites show how many bytes to read out of this packet
			status = status | 0x40 | thislength
		else :
			#All remaining packets send packet number, zero indexed
			status = index
		if index == 0 and index == totalpackets - 1:
			#Handle the case where the total size is only one packet long
			status = 0x80 | 0x40 | thislength

		thissteg = bytes8tojt65(cipherlist[index*8:(index*8)+8], status)
		secretjtfec = jt.prepsteg(thissteg)

		if verbose:
			print "Status: " + str(status) + " thislength : " + str(thislength)
			print "JT65 Encoded Cipher Data Msg " + str(index) + " : " + str(thissteg)
			print "JT65 Encoded Cipher Data Msg with FEC " + str(index) + " : " + str(secretjtfec)

		ciphermsgs.append(secretjtfec)

def createciphermsgs_packer_other(totalpackets, ciphermsgs, cipherlist, verbose=False):
	for index in range(totalpackets):
		status = 0
		if index == 0:
			#First packet sets first bit to one, then remaining bits show total number of packets
			status = 0x80 | totalpackets
		else :
			#All remaining packets send packet number, zero indexed
			status = index

		thissteg = bytes8tojt65(cipherlist[index*8:(index*8)+8], status)
		secretjtfec = jt.prepsteg(thissteg)

		if verbose:
			print "Status: " + str(status)
			print "JT65 Encoded Cipher Data Msg " + str(index) + " : " + str(thissteg)
			print "JT65 Encoded Cipher Data Msg with FEC " + str(index) + " : " + str(secretjtfec)

		ciphermsgs.append(secretjtfec)

def createciphermsgs_xor(jt65msgcount, stegmsg, key, verbose=False):
	ciphermsgs = []

	#Can we fit your hidden message?
	if jt65msgcount * 8 < len(stegmsg):
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)

	originallength = len(stegmsg)
	while len(stegmsg) % 8:
		stegmsg += chr(random.randint(0, 255))

	cryptobj = XOR.new(key)
	cipherdata = cryptobj.encrypt(stegmsg)
	cipherlist = list(bytearray(cipherdata))

	#Is the total length too big to fit into our max number of packets?
	if len(cipherlist) > MAX_MULTI_PACKET_STEG_BYTES_XOR:
		print("Length of hidden message exceeds capacity of multi-packet steg")
		sys.exit(0)
	totalpackets = len(cipherlist) / 8

	if verbose: 			
		print "Cipher list: " + str(cipherlist)

	createciphermsgs_packer_xor(totalpackets, originallength, ciphermsgs, cipherlist, verbose)

	return ciphermsgs

def createciphermsgs_arc4(jt65msgcount, stegmsg, key, verbose=False):
	ciphermsgs = []

	#Can we fit your hidden message?
	if jt65msgcount * 8 < len(stegmsg):
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)

	while len(stegmsg) % 8:
		stegmsg += " "

	tempkey = SHA.new(key).digest()
	cryptobj = ARC4.new(tempkey)
	cipherdata = cryptobj.encrypt(stegmsg)
	cipherlist = list(bytearray(cipherdata))

	#Is the total length too big to fit into our max number of packets?
	if len(cipherlist) > MAX_MULTI_PACKET_STEG_BYTES_ARC4:
		print("Length of hidden message exceeds capacity of multi-packet steg")
		sys.exit(0)
	totalpackets = len(cipherlist) / 8

	if verbose: 			
		print "Cipher list: " + str(cipherlist)

	createciphermsgs_packer_other(totalpackets, ciphermsgs, cipherlist, verbose)

	return ciphermsgs

def createciphermsgs_aes(jt65msgcount, stegmsg, key, aesmode, verbose=False):
	ciphermsgs = []

	#Check key size
	if len(key) != 16 and len(key) != 24 and len(key) != 32:
		print ("\nCipher key must be 16, 24, or 32 bytes... sorry :(\n")
		sys.exit(0)

	while len(stegmsg) % 16:
		stegmsg += " "

	#Can we fit your hidden message?
	if aesmode == "ECB" and jt65msgcount * 8 < len(stegmsg):
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)
	elif (aesmode == "CBC" or aesmode == "CFB") and (jt65msgcount * 8 < len(stegmsg) + 16):
		#These two modes have an additional 16 byte IV
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)

	#Prep the encrypted hidden data
	iv = ""
	if aesmode == "ECB":
		cryptobj = AES.new(key, AES.MODE_ECB)
	elif aesmode == "CBC":
		iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
		cryptobj = AES.new(key, AES.MODE_CBC, iv)
	elif aesmode == "CFB":
		iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
		cryptobj = AES.new(key, AES.MODE_CFB, iv)

	cipherdata = cryptobj.encrypt(stegmsg)
	cipherlist = list(bytearray(iv)) + list(bytearray(cipherdata))

	#Is the total length too big to fit into our max number of packets?
	if len(cipherlist) > MAX_MULTI_PACKET_STEG_BYTES_AES:
		print("Length of hidden message exceeds capacity of multi-packet steg")
		sys.exit(0)
	totalpackets = len(cipherlist) / 8

	if verbose: 			
		print "Cipher list: " + str(cipherlist)

	createciphermsgs_packer_other(totalpackets, ciphermsgs, cipherlist, verbose)

	return ciphermsgs

def createciphermsgs_gpg(jt65msgcount, stegmsg, recipient, verbose=False):
	ciphermsgs = []

	while len(stegmsg) % 8:
		stegmsg += " "

	gpg = GPG()
	stegstream = io.StringIO(unicode(stegmsg))
	cipherdata = gpg.encrypt_file(stegstream, recipient)

	if cipherdata == "":
		print "You must set the recipient's trust level to -something- in your keyring before we can encrypt the message"
		sys.exit(0)

	cipherlist = list(bytearray(str(cipherdata)))

	if verbose: 			
		print "Cipher list: " + str(cipherlist)

	if jt65msgcount * 8 < len(cipherlist):
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)

	#Is the total length too big to fit into our max number of packets?
	if len(cipherlist) > MAX_MULTI_PACKET_STEG_BYTES_GPG:
		print("Length of hidden message exceeds capacity of multi-packet steg")
		sys.exit(0)
	totalpackets = len(cipherlist) / 8

	createciphermsgs_packer_other(totalpackets, ciphermsgs, cipherlist, verbose)

	return ciphermsgs

def createciphermsgs_otp(jt65msgcount, stegmsg, key, verbose=False):
	ciphermsgs = []

	#Can we fit your hidden message?
	if jt65msgcount * 13 < len(stegmsg):
		print("Length of hidden message exceeds capacity of number of valid JT65 messages provided")
		sys.exit(0)

	stegmsg = otp_encode(stegmsg, key)

	for index in range(jt65msgcount):
		secretjt = jt.encode(stegmsg[index*13:index*13+13])
		secretjtfec = jt.prepsteg(secretjt)

		if verbose:
			print "Secret message " + str(index) + " : " + stegmsg[index*13:index*13+13]
			print "Secret message " + str(index) + " encoded : " + str(secretjt)
			print "Secret message " + str(index) + " encoded with FEC : " + str(secretjt)

		ciphermsgs.append(secretjtfec)

	return ciphermsgs

def steginject(jt65data, noise, cipherdata, hidekey, verbose=False):
#Combine array of JT65 valid messages with array of JT65 encoded steg data
	finalpackets = []

	for index in range(len(jt65data)):

		if index < len(cipherdata):
			stegedpacket = jtsteg(jt65data[index],cipherdata[index],hidekey)

		else:
			#There were more JT65 msgs than needed to carry the cipherdata, just use the leftover JT65 msgs as is
			stegedpacket = jt65data[index]

		stegedpacket = randomcover(stegedpacket,hidekey,noise,verbose)
		finalpackets.append(stegedpacket)

	return finalpackets

def validatesteg(jt65msg, rxsymbols, hidekey, errordetectionthreshold, verbose=False):
#Determines if a given set of symbols contain steganography or are a normal JT65 message

	errorcount = 0

	#Determine what the symbols would be if there were no errors
	truesymbols = jt.prepmsg(jt.encode(jt65msg))

	#Determine how many symbols where steg should be hidden contain errors
	for i in hidekey:
		if rxsymbols[i] != truesymbols[i]:
			errorcount += 1

	if errorcount >= errordetectionthreshold:
		return True

	return False

def retrievesteg(jt65data, hidekey, verbose=False, unprep=False):
#Retrieve steganography data from array of JT65 data
	stegdata = []

	for index,value in enumerate(jt65data):
		data = jtunsteg(value,hidekey)

		if verbose:
			print "Steg Bytes in Message " + str(index) + " : " + str(data)

		if unprep:
			data = jt.unprepsteg(data)

		stegdata.append(data)

	return stegdata

def deciphersteg(stegdata, cipher, key, aesmode, verbose=False, unprep=True):
#Decipher hidden message from array of data hidden in JT65 errors
	stegedmsg = ""
	stegedmsgba = np.array(range(0),dtype=np.int32)
	statusar = []

	for index,value in enumerate(stegdata):
		if unprep:
			value = jt.unprepsteg(value) #Decode real data from FEC

		if cipher == "none" or cipher=="OTP":
			recoveredtext = jt.decode(value)[0:13]
			if verbose:
				print "Steg Text in Message " + str(index) + " : " + recoveredtext
			stegedmsg += recoveredtext

		elif cipher == "XOR":
			thesebytes = jt65tobytes(value)

			thisstatus = thesebytes[0:1]

			if thisstatus & 0x40 == 0x40:
				#This is the last packet, signals how many bytes to read
				bytestoread = thisstatus & 0x3F
				thisunstegbytes = thesebytes[1:bytestoread+1]
			else:
				thisunstegbytes = thesebytes[1:]
			
			if verbose:
				print "Steg Data in Message " + str(index) + " : " + str(thisunstegbytes)
			stegedmsgba = np.append(stegedmsgba, thisunstegbytes)

		else:
			thesebytes = jt65tobytes(value)
			thisunstegbytes = thesebytes[1:10]
			
			if verbose:
				print "Steg Data in Message " + str(index) + " : " + str(thisunstegbytes)
			stegedmsgba = np.append(stegedmsgba, thisunstegbytes)

	if cipher == "XOR":
		if verbose:
			print"Cipher Data : " + str(stegedmsgba)

		finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in stegedmsgba))
		
		if verbose:
			print"Cipher Data Hex : " + finalcipherdata

		cryptobj = XOR.new(key)
		stegedmsg = cryptobj.decrypt(finalcipherdata)

	if cipher == "ARC4":
		if verbose:
			print"Cipher Data : " + str(stegedmsgba)

		finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in stegedmsgba))
		
		if verbose:
			print"Cipher Data Hex : " + finalcipherdata

		tempkey = SHA.new(key).digest()
		cryptobj = ARC4.new(tempkey)
		stegedmsg = cryptobj.decrypt(finalcipherdata)

	if cipher == "AES":
		if verbose:
			print"Cipher Data : " + str(stegedmsgba)

		finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in stegedmsgba))
		
		if verbose:
			print"Cipher Data Hex : " + finalcipherdata

		if aesmode == "ECB":
			cryptobj = AES.new(key, AES.MODE_ECB)
		elif aesmode == "CBC":
			cryptobj = AES.new(key, AES.MODE_CBC, finalcipherdata[0:16])
			finalcipherdata = finalcipherdata[16:]
		elif aesmode == "CFB":
			cryptobj = AES.new(key, AES.MODE_CFB, finalcipherdata[0:16])
			finalcipherdata = finalcipherdata[16:]

		stegedmsg = cryptobj.decrypt(finalcipherdata)

	if cipher == "GPG":
		if verbose:
			print"Cipher Data : " + str(stegedmsgba)

		finalcipherdata = (''.join('{0:02x}'.format(int(e)).decode("hex") for e in stegedmsgba))
		
		if verbose:
			print"Cipher Data Hex : " + finalcipherdata

		gpg = GPG()
		stegedmsg = gpg.decrypt(finalcipherdata)
		stegedmsg = str(stegedmsg)

	if cipher == "OTP":
		stegedmsg = otp_decode(stegedmsg, key)

	return stegedmsg
