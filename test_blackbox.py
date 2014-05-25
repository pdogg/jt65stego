import unittest
import random

import numpy as np
import jt65stego as jts

hidekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
MAX_COVER_NOISE = 14

class TestBlackBox(unittest.TestCase):

	def test_NoCipher_NoSteg(self):
		#Encode
		jt65msgs = ["G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		expectedresult = [np.array([14,16,9,18,4,60,41,18,22,63,43,5,30,13,15,9,25,35,50,21,0,36,17,42,33,35,39,22,25,39,46,3, 
						  			47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
							np.array([20,34,19,5,36,6,30,15,22,20,3,62,57,59,19,56,17,35,2,9,41,10,23,24,41,35,39,60,48,33,34,49,
						  			54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])]
		self.assertEqual(len(expectedresult), len(jt65data))
		for i in range(len(expectedresult)):
			self.assertEqual(jt65data[i].tolist(), expectedresult[i].tolist())
		#Decode
		decodedjt65msgs = jts.decodemessages(jt65data, False)
		self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
		for i in range(len(jt65msgs)):
			self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())

	def test_NoCipher_WithSteg(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "BEACON FTW AND DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "none", "", "", "", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "none", "", "", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())

	def test_XOR(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "XOR", "XOR rox and all that jazz", "", "", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "XOR", "XOR rox and all that jazz", "", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())

	def test_ARC4(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "ARC4", "RC4 is the most secure algorithm in the world", "", "", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "ARC4", "RC4 is the most secure algorithm in the world", "", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())

	def test_AES_ECB(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "AES", "AES is totes secure, right? Yeah", "", "ECB", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "AES", "AES is totes secure, right? Yeah", "ECB", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())

	def test_AES_CBC(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44","G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "AES", "AES is totes secure, right? Yeah", "", "CBC", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "AES", "AES is totes secure, right? Yeah", "CBC", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())

	def test_AES_CFB(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44","G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "AES", "AES is totes secure, right? Yeah", "", "CFB", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "AES", "AES is totes secure, right? Yeah", "CFB", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())

	def test_AES_OTP(self):
		for i in range(MAX_COVER_NOISE):
			#Encode
			jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
			jt65data = jts.jt65encodemessages(jt65msgs, False)
			stegmsg = "BEACON FTW AND DEF CON 22"
			cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "OTP", "I LOVE SECURITY AND STUFF", "", "", False)
			finalmsgs = jts.steginject(jt65data, i, cipherdata, hidekey, False)

			#Decode
			finalresultmsgs = list(finalmsgs)
			stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
			resultstegmsg = jts.deciphersteg(stegdata, "OTP", "I LOVE SECURITY AND STUFF", "", False)
			decodedjt65msgs = jts.decodemessages(finalmsgs, False)
			self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
			for i in range(len(jt65msgs)):
				self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
			self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())
