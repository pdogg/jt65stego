import unittest
import random

import numpy as np
import jt65stego as jts

hidekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
JT65_MAX_SYMBOL = 63
RANDOM_TEST_LOOP_COUNT = 10

class TestStegFunctions(unittest.TestCase):

	def test_StegAndUnsteg(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomvalidmessage = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(64)])
			randomstegmessage  = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(12)])
			resultA = jts.jtsteg(randomvalidmessage, randomstegmessage, hidekey)
			resultB = jts.jtunsteg(resultA, hidekey)
			self.assertEqual(resultB.tolist(), randomstegmessage.tolist())

	def test_StegAndUnstegNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomvalidmessage = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(64)])
			randomstegmessage  = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(12)])
			resultA = jts.jtsteg(randomvalidmessage, randomstegmessage, hidekey)
			resultB = jts.jtunsteg(resultA, hidekey)
			# Should not be equal, unsteg returns the steg message not the valid message
			self.assertNotEqual(resultB.tolist(), randomvalidmessage.tolist())

	def test_RandomCover(self):
		for i in range(52):
			miscount = 0
			randomvalidmessage = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(64)])
			msgcopy=np.copy(randomvalidmessage)
			covered = jts.randomcover(msgcopy, hidekey, i)
			for index,value in enumerate(covered):
				if covered[index] != randomvalidmessage[index]:
					miscount += 1
			self.assertTrue(i == miscount)

	def test_GetNoiseKey(self):
		result = jts.getnoisekey("Give me a noise key!")
		expectedresult = np.array([49,45,55,15,27,33,58,14,23,35,48,44])
		self.assertEqual(len(result), len(expectedresult))
		for i in range(len(result)):
			self.assertTrue(result[i], expectedresult.tolist()[i])

	def test_PackUnpack(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomJT65bytes = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(12)])
			byteresult = jts.jt65tobytes(randomJT65bytes)
			jt65result = jts.bytestojt65(byteresult)
			self.assertEqual(len(byteresult), 9)
			self.assertEqual(len(jt65result), 12)
			self.assertEqual(jt65result.tolist(), randomJT65bytes.tolist())

	def test_PackNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomJT65bytes = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(12)])
			byteresult = jts.jt65tobytes(randomJT65bytes)
			self.assertNotEqual(byteresult.tolist(), randomJT65bytes.tolist())

	def test_UnpackNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randombytes = np.array([random.randint(0,0xFF) for r in range(9)])
			jt65result = jts.bytestojt65(randombytes)
			self.assertNotEqual(jt65result.tolist(), randombytes.tolist())

	def test_JT65EncodeMessages(self):
		msgs = ["K1JT F9HS JN23", "W7GJ G3FPQ IO91", "G3LTF DL9KR JO40", "G3LTE DL9KR JO40", "G3LTF DL9KR JO41"]
		expectedresult = [np.array([35,6,54,17,18,40,49,15,45,51,54,49,58,45,6,40,15,24,15,29,43,7,53,12,19,35,39,63,18,40,9,
									20,49,14,40,42,20,12,33,8,4,44,22,44,2,1,5,45,31,63,52,44,19,45,37,28,60,25,56,18,27,16,41]), 
						  np.array([12,30,23,60,56,33,14,8,45,15,15,26,46,7,55,63,61,31,13,51,16,55,15,1,41,33,60,5,3,39,7,52,
						  			8,20,29,27,7,60,9,62,46,7,1,63,42,27,60,3,11,14,61,46,32,32,59,60,5,42,63,32,0,50,31]),
						  np.array([14,16,9,18,4,60,41,18,22,63,43,5,30,13,15,9,25,35,50,21,0,36,17,42,33,35,39,22,25,39,46,3, 
						  			47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
						  np.array([20,34,19,5,36,6,30,15,22,20,3,62,57,59,19,56,17,35,2,9,41,10,23,24,41,35,39,60,48,33,34,49,
						  			54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24]),
						  np.array([47,27,46,50,58,26,38,24,22,3,14,54,10,58,36,23,63,35,41,56,53,62,11,49,14,35,39,60,40,44,15,
						  			45,7,44,55,23,12,49,39,11,18,36,26,17,2,8,60,44,37,5,48,44,18,41,32,63,4,49,55,57,37,13,25])]
		result = jts.jt65encodemessages(msgs, False)
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_DecodeMessages(self):
		msgs = [np.array([35,6,54,17,18,40,49,15,45,51,54,49,58,45,6,40,15,24,15,29,43,7,53,12,19,35,39,63,18,40,9,
									20,49,14,40,42,20,12,33,8,4,44,22,44,2,1,5,45,31,63,52,44,19,45,37,28,60,25,56,18,27,16,41]), 
						  np.array([12,30,23,60,56,33,14,8,45,15,15,26,46,7,55,63,61,31,13,51,16,55,15,1,41,33,60,5,3,39,7,52,
						  			8,20,29,27,7,60,9,62,46,7,1,63,42,27,60,3,11,14,61,46,32,32,59,60,5,42,63,32,0,50,31]),
						  np.array([14,16,9,18,4,60,41,18,22,63,43,5,30,13,15,9,25,35,50,21,0,36,17,42,33,35,39,22,25,39,46,3, 
						  			47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
						  np.array([20,34,19,5,36,6,30,15,22,20,3,62,57,59,19,56,17,35,2,9,41,10,23,24,41,35,39,60,48,33,34,49,
						  			54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24]),
						  np.array([47,27,46,50,58,26,38,24,22,3,14,54,10,58,36,23,63,35,41,56,53,62,11,49,14,35,39,60,40,44,15,
						  			45,7,44,55,23,12,49,39,11,18,36,26,17,2,8,60,44,37,5,48,44,18,41,32,63,4,49,55,57,37,13,25])]
		expectedresult = ["K1JT F9HS JN23", "W7GJ G3FPQ IO91", "G3LTF DL9KR JO40", "G3LTE DL9KR JO40", "G3LTF DL9KR JO41"]
		result = jts.decodemessages(msgs, False)
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].rstrip(), expectedresult[i])

	def test_otp_ascii_int_to_otp_int(self):
		self.assertEqual(jts.otp_ascii_int_to_otp_int(32), 0)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(48), 1)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(49), 2)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(50), 3)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(51), 4)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(52), 5)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(53), 6)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(54), 7)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(55), 8)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(56), 9)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(57),10)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(65),11)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(66),12)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(67),13)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(68),14)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(69),15)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(70),16)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(71),17)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(72),18)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(73),19)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(74),20)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(75),21)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(76),22)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(77),23)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(78),24)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(79),25)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(80),26)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(81),27)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(82),28)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(83),29)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(84),30)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(85),31)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(86),32)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(87),33)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(88),34)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(89),35)
		self.assertEqual(jts.otp_ascii_int_to_otp_int(90),36)

	def test_otp_otp_int_to_ascii_int(self):
		self.assertEqual(32,jts.otp_otp_int_to_ascii_int( 0))
		self.assertEqual(48,jts.otp_otp_int_to_ascii_int( 1))
		self.assertEqual(49,jts.otp_otp_int_to_ascii_int( 2))
		self.assertEqual(50,jts.otp_otp_int_to_ascii_int( 3))
		self.assertEqual(51,jts.otp_otp_int_to_ascii_int( 4))
		self.assertEqual(52,jts.otp_otp_int_to_ascii_int( 5))
		self.assertEqual(53,jts.otp_otp_int_to_ascii_int( 6))
		self.assertEqual(54,jts.otp_otp_int_to_ascii_int( 7))
		self.assertEqual(55,jts.otp_otp_int_to_ascii_int( 8))
		self.assertEqual(56,jts.otp_otp_int_to_ascii_int( 9))
		self.assertEqual(57,jts.otp_otp_int_to_ascii_int(10))
		self.assertEqual(65,jts.otp_otp_int_to_ascii_int(11))
		self.assertEqual(66,jts.otp_otp_int_to_ascii_int(12))
		self.assertEqual(67,jts.otp_otp_int_to_ascii_int(13))
		self.assertEqual(68,jts.otp_otp_int_to_ascii_int(14))
		self.assertEqual(69,jts.otp_otp_int_to_ascii_int(15))
		self.assertEqual(70,jts.otp_otp_int_to_ascii_int(16))
		self.assertEqual(71,jts.otp_otp_int_to_ascii_int(17))
		self.assertEqual(72,jts.otp_otp_int_to_ascii_int(18))
		self.assertEqual(73,jts.otp_otp_int_to_ascii_int(19))
		self.assertEqual(74,jts.otp_otp_int_to_ascii_int(20))
		self.assertEqual(75,jts.otp_otp_int_to_ascii_int(21))
		self.assertEqual(76,jts.otp_otp_int_to_ascii_int(22))
		self.assertEqual(77,jts.otp_otp_int_to_ascii_int(23))
		self.assertEqual(78,jts.otp_otp_int_to_ascii_int(24))
		self.assertEqual(79,jts.otp_otp_int_to_ascii_int(25))
		self.assertEqual(80,jts.otp_otp_int_to_ascii_int(26))
		self.assertEqual(81,jts.otp_otp_int_to_ascii_int(27))
		self.assertEqual(82,jts.otp_otp_int_to_ascii_int(28))
		self.assertEqual(83,jts.otp_otp_int_to_ascii_int(29))
		self.assertEqual(84,jts.otp_otp_int_to_ascii_int(30))
		self.assertEqual(85,jts.otp_otp_int_to_ascii_int(31))
		self.assertEqual(86,jts.otp_otp_int_to_ascii_int(32))
		self.assertEqual(87,jts.otp_otp_int_to_ascii_int(33))
		self.assertEqual(88,jts.otp_otp_int_to_ascii_int(34))
		self.assertEqual(89,jts.otp_otp_int_to_ascii_int(35))
		self.assertEqual(90,jts.otp_otp_int_to_ascii_int(36))

	def test_otp_encode(self):
		stegdata = "BEACON FTW AND DEF CON 22"
		key = "I LOVE SECURITY AND STUFF"
		expectedresult = "UEW0J1 778U156YDP2DCGGUII"
		self.assertEqual(jts.otp_encode(stegdata, key), expectedresult)

	def test_otp_decode(self):
		stegdata = "UEW0J1 778U156YDP2DCGGUII"
		key = "I LOVE SECURITY AND STUFF"
		expectedresult = "BEACON FTW AND DEF CON 22"
		self.assertEqual(jts.otp_decode(stegdata, key), expectedresult)

	def test_CreateCipher_None(self):
		result = jts.createciphermsgs(2, "BEACON FTW AND DEF CON 22", "none", "", "", "", False)
		expectedresult = [np.array([16,52,50,11,6,13,41,26,39,15,39,11]), np.array([20,36,39,11,59,23,28,16,53,8,57,0])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_CreateCipher_XOR(self):
		result = jts.createciphermsgs(2, "DEF CON 22", "XOR", "XOR rox and all that jazz", "", "", False)
		expectedresult = [np.array([0,1,48,10,5,0,0,49,8,3,24,0]), np.array([0,21,13,28,17,0,1,1,19,4,48,0])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_CreateCipher_ARC4(self):
		result = jts.createciphermsgs(2, "DEF CON 22", "ARC4", "RC4 is the most secure algorithm in the world", "", "", False)
		expectedresult = [np.array([0,12,25,53,53,37,31,1,1,11,39,47]), np.array([0,16,47,5,14,48,32,50,5,25,27,41])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_CreateCipher_AES_ECB(self):
		result = jts.createciphermsgs(2, "DEF CON 22", "AES", "AES is totes secure, right? Yeah", "", "ECB", False)
		expectedresult = [np.array([0,10,35,51,56,46,33,50,21,13,41,61]), np.array([0,20,26,16,36,8,6,62,60,32,24,61])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_StegInject(self):
		jt65data = [np.array([14,16,9,18,4,60,41,18,22,63,43,5,30,13,15,9,25,35,50,21,0,36,17,42,33,35,39,22,25,39,46,3, 
						  			47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
						  np.array([20,34,19,5,36,6,30,15,22,20,3,62,57,59,19,56,17,35,2,9,41,10,23,24,41,35,39,60,48,33,34,49,
						  			54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])]
		cipherdata = [np.array([16,52,50,11,6,13,41,26,39,15,39,11]), np.array([20,36,39,11,59,23,28,16,53,8,57,0])]
		result = jts.steginject(jt65data, 0, cipherdata, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23], False)
		expectedresult = [np.array([14,16,9,52,4,50,41,11,22,6,43,13,30,41,15,26,25,39,50,15,0,39,17,11,33,35,39,22,25,39,
									46,3,47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
							np.array([20,20,19,36,36,39,30,11,22,59,3,23,57,28,19,16,17,53,2,8,41,57,23,0,41,35,39,60,48,33,
								34,49,54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_RetrieveSteg(self):
		jt65data = [np.array([14,16,9,52,4,50,41,11,22,6,43,13,30,41,15,26,25,39,50,15,0,39,17,11,33,35,39,22,25,39,
							46,3,47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24]),
					np.array([20,20,19,36,36,39,30,11,22,59,3,23,57,28,19,16,17,53,2,8,41,57,23,0,41,35,39,60,48,33,
						34,49,54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])]
		expectedresult = [np.array([16,52,50,11,6,13,41,26,39,15,39,11]),np.array([20,36,39,11,59,23,28,16,53,8,57,0])]
		result = jts.retrievesteg(jt65data, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23], False)
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_DecipherSteg_None(self):
		stegdata = [np.array([16,52,50,11,6,13,41,26,39,15,39,11]),np.array([20,36,39,11,59,23,28,16,53,8,57,0])]
		result = jts.deciphersteg(stegdata, "none", "", "", False)
		self.assertEqual(result.rstrip(), "BEACON FTW AND DEF CON 22")

	def test_DecipherSteg_ARC4(self):
		stegdata = [np.array([0,12,25,53,53,37,31,1,1,11,39,47]), np.array([0,16,47,5,14,48,32,50,5,25,27,41])]
		result = jts.deciphersteg(stegdata, "ARC4", "RC4 is the most secure algorithm in the world", "", False)
		self.assertEqual(result.rstrip(), "DEF CON 22")

	def test_DecipherSteg_AES_ECB(self):
		stegdata = [np.array([0,10,35,51,56,46,33,50,21,13,41,61]),np.array([0,20,26,16,36,8,6,62,60,32,24,61])]
		result = jts.deciphersteg(stegdata, "AES", "AES is totes secure, right? Yeah", "ECB", False)
		self.assertEqual(result.rstrip(), "DEF CON 22")