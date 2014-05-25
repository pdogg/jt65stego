import unittest
import random

import numpy as np
import jt65stego as jts

hidekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

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
		#Encode
		jt65msgs = ["G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "BEACON FTW AND DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "none", "", "", "", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

		expectedresult = [np.array([14,16,9,52,4,50,41,11,22,6,43,13,30,41,15,26,25,39,50,15,0,39,17,11,33,35,39,22,25,39,
									46,3,47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
							np.array([20,20,19,36,36,39,30,11,22,59,3,23,57,28,19,16,17,53,2,8,41,57,23,0,41,35,39,60,48,33,
								34,49,54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])]
		self.assertEqual(len(expectedresult), len(finalmsgs))
		for i in range(len(expectedresult)):
			self.assertEqual(finalmsgs[i].tolist(), expectedresult[i].tolist())
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
		#Encode
		jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "XOR", "XOR rox and all that jazz", "", "", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

		expectedresult = [np.array([50,0,14,1,57,48,1,10,13,5,58,0,27,0,2,49,44,8,20,3,52,24,12,0,34,33,12,62,59,61,24,50,
								20,34,48,37,25,31,49,10,39,11,26,48,7,23,2,26,41,28,7,10,41,49,28,7,6,23,14,49,62,53,63]),
							np.array([45,0,52,21,1,13,48,28,13,17,51,0,1,1,37,1,54,19,51,4,60,48,29,0,56,33,7,28,1,20,10,30,
								43,8,48,38,22,37,55,47,49,59,32,48,47,48,6,41,30,47,0,4,41,49,54,53,51,24,45,42,8,53,63])]
		self.assertEqual(len(expectedresult), len(finalmsgs))
		for i in range(len(expectedresult)):
			self.assertEqual(finalmsgs[i].tolist(), expectedresult[i].tolist())
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
		#Encode
		jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "ARC4", "RC4 is the most secure algorithm in the world", "", "", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

		expectedresult = [np.array([50,0,14,12,57,25,1,53,13,53,58,37,27,31,2,1,44,1,20,11,52,39,12,47,34,33,12,62,59,61,24,50,
									20,34,48,37,25,31,49,10,39,11,26,48,7,23,2,26,41,28,7,10,41,49,28,7,6,23,14,49,62,53,63]),
							np.array([45,0,52,16,1,47,48,5,13,14,51,48,1,32,37,50,54,5,51,25,60,27,29,41,56,33,7,28,1,20,10,30,
									43,8,48,38,22,37,55,47,49,59,32,48,47,48,6,41,30,47,0,4,41,49,54,53,51,24,45,42,8,53,63])]
		self.assertEqual(len(expectedresult), len(finalmsgs))
		for i in range(len(expectedresult)):
			self.assertEqual(finalmsgs[i].tolist(), expectedresult[i].tolist())
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
		#Encode
		jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "AES", "AES is totes secure, right? Yeah", "", "ECB", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

		expectedresult = [np.array([50,0,14,10,57,35,1,51,13,56,58,46,27,33,2,50,44,21,20,13,52,41,12,61,34,33,12,62,59,61,24,50,
									20,34,48,37,25,31,49,10,39,11,26,48,7,23,2,26,41,28,7,10,41,49,28,7,6,23,14,49,62,53,63]),
							np.array([45, 0,52,20,1,26,48,16,13,36,51,8,1,6,37,62,54,60,51,32,60,24,29,61,56,33,7,28,1,20,10,
								30,43,8,48,38,22,37,55,47,49,59,32,48,47,48,6,41,30,47,0,4,41,49,54,53,51,24,45,42,8,53,63])]
		self.assertEqual(len(expectedresult), len(finalmsgs))
		for i in range(len(expectedresult)):
			self.assertEqual(finalmsgs[i].tolist(), expectedresult[i].tolist())
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
		#Encode
		jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44","G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "AES", "AES is totes secure, right? Yeah", "", "CBC", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

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
		#Encode
		jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44","G3LTF DL9KR JO40","G3LTE DL9KR JO40"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "AES", "AES is totes secure, right? Yeah", "", "CFB", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

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
		#Encode
		jt65msgs = ["CQ KA1BBB FN44","CQ KA1AAA FN44"]
		jt65data = jts.jt65encodemessages(jt65msgs, False)
		stegmsg = "BEACON FTW AND DEF CON 22"
		cipherdata = jts.createciphermsgs(len(jt65data), stegmsg, "OTP", "I LOVE SECURITY AND STUFF", "", "", False)
		finalmsgs = jts.steginject(jt65data, 0, cipherdata, hidekey, True)

		expectedresult = [np.array([50,45,14,2,57,14,1,4,13,28,58,11,27,2,2,62,44,13,20,12,52,59,12,39,34,33,12,62,59,61,24,50,
									20,34,48,37,25,31,49,10,39,11,26,48,7,23,2,26,41,28,7,10,41,49,28,7,6,23,14,49,62,53,63]),
							np.array([45,10,52,7,1,23,48,60,13,1,51,14,1,58,37,3,54,23,51,15,60,60,29,32,56,33,7,28,1,20,10,30,
									43,8,48,38,22,37,55,47,49,59,32,48,47,48, 6,41,30,47,0,4,41,49,54,53,51,24,45,42,8,53,63])]
		self.assertEqual(len(expectedresult), len(finalmsgs))
		for i in range(len(expectedresult)):
			self.assertEqual(finalmsgs[i].tolist(), expectedresult[i].tolist())
		#Decode
		finalresultmsgs = list(finalmsgs)
		stegdata = jts.retrievesteg(finalmsgs, hidekey, False)
		resultstegmsg = jts.deciphersteg(stegdata, "OTP", "I LOVE SECURITY AND STUFF", "", False)
		decodedjt65msgs = jts.decodemessages(finalmsgs, False)
		self.assertEqual(len(decodedjt65msgs), len(jt65msgs))
		for i in range(len(jt65msgs)):
			self.assertEqual(jt65msgs[i].rstrip(), decodedjt65msgs[i].rstrip())
		self.assertEqual(stegmsg.rstrip(), resultstegmsg.rstrip())
