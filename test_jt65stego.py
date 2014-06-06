import unittest
import random

import numpy as np
import jt65stego as jts

hidekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]
JT65_MAX_SYMBOL = 63
RANDOM_TEST_LOOP_COUNT = 10

class TestStegFunctions(unittest.TestCase):

	def test_StegAndUnsteg(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomvalidmessage = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(64)])
			randomstegmessage  = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(20)])
			resultA = jts.jtsteg(randomvalidmessage, randomstegmessage, hidekey)
			resultB = jts.jtunsteg(resultA, hidekey)
			self.assertEqual(resultB.tolist(), randomstegmessage.tolist())

	def test_StegAndUnstegNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomvalidmessage = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(64)])
			randomstegmessage  = np.array([random.randint(0,JT65_MAX_SYMBOL) for r in range(20)])
			resultA = jts.jtsteg(randomvalidmessage, randomstegmessage, hidekey)
			resultB = jts.jtunsteg(resultA, hidekey)
			# Should not be equal, unsteg returns the steg message not the valid message
			self.assertNotEqual(resultB.tolist(), randomvalidmessage.tolist())

	def test_RandomCover(self):
		for i in range(63-len(hidekey)):
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
		expectedresult = np.array([49,45,55,27,33,58,23,35,48,44,43, 7,37,32,57, 9,29,62,10,41])
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
		msgs = ["KB2BBC KA1AAB DD44", "KA1AAB KB2BBC DD44", "KB2BBC KA1AAB DD44", "KA1AAB KB2BBC DD44", "KB2BBC KA1AAB DD44"]
		expectedresult = [np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29]), 
						  np.array([1,22,21,42,33, 8,40,58,13,54,19,19,58, 6, 5,10,29,24,34, 1,53,33,30,43,17,
 									51,29,38,52,58,55, 9,49,50,24,61, 0,52,51,20,25,58,15,41,53,48, 6,57,10,25,
 									11,30,16,20,47, 6, 0,43, 6,18,38, 3,29]),
						  np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29]),
						  np.array([1,22,21,42,33, 8,40,58,13,54,19,19,58, 6, 5,10,29,24,34, 1,53,33,30,43,17,
 									51,29,38,52,58,55, 9,49,50,24,61, 0,52,51,20,25,58,15,41,53,48, 6,57,10,25,
 									11,30,16,20,47, 6, 0,43, 6,18,38, 3,29]),
						  np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29])]
		result = jts.jt65encodemessages(msgs, False)
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_DecodeMessages(self):
		msgs = [np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29]), 
						  np.array([1,22,21,42,33, 8,40,58,13,54,19,19,58, 6, 5,10,29,24,34, 1,53,33,30,43,17,
 									51,29,38,52,58,55, 9,49,50,24,61, 0,52,51,20,25,58,15,41,53,48, 6,57,10,25,
 									11,30,16,20,47, 6, 0,43, 6,18,38, 3,29]),
						  np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29]),
						  np.array([1,22,21,42,33, 8,40,58,13,54,19,19,58, 6, 5,10,29,24,34, 1,53,33,30,43,17,
 									51,29,38,52,58,55, 9,49,50,24,61, 0,52,51,20,25,58,15,41,53,48, 6,57,10,25,
 									11,30,16,20,47, 6, 0,43, 6,18,38, 3,29]),
						  np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29])]
		expectedresult = ["KB2BBC KA1AAB DD44", "KA1AAB KB2BBC DD44", "KB2BBC KA1AAB DD44", "KA1AAB KB2BBC DD44", "KB2BBC KA1AAB DD44"]
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
		expectedresult = [np.array([47,44,14,33,4,58,19,6,16,52,50,11,6,13,41,26,39,15,39,11]), np.array([22,29,9,53,17,23,57,14,20,36,39,11,59,23,28,16,53,8,57,0])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_CreateCipher_XOR(self):
		result = jts.createciphermsgs(2, "DEF CON 22", "XOR", "XOR rox and all that jazz", "", "", False)
		expectedresult = [np.array([9, 45, 15, 32, 17, 23, 39, 15, 32, 33, 48, 10, 5, 0, 0, 49, 8, 3, 24, 0]), np.array([8, 20, 52, 58, 43, 55, 6, 50, 0, 37, 13, 28, 44, 7, 24, 14, 58, 26, 17, 4])]
		self.assertEqual(len(expectedresult), len(result))
		self.assertEqual(result[0].tolist(), expectedresult[0].tolist())	# Cannot verify second list due to random byte padding at end of XOR cipher

	def test_CreateCipher_ARC4(self):
		result = jts.createciphermsgs(2, "DEF CON 22", "ARC4", "RC4 is the most secure algorithm in the world", "", "", False)
		expectedresult = [np.array([35, 36, 29, 45, 39, 33, 48, 7, 0, 12, 25, 53, 53, 37, 31, 1, 1, 11, 39, 47]), np.array([54, 61, 22, 35, 39, 18, 61, 28, 0, 16, 47, 5, 14, 48, 32, 50, 5, 25, 27, 41])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_CreateCipher_AES_ECB(self):
		result = jts.createciphermsgs(2, "DEF CON 22", "AES", "AES is totes secure, right? Yeah", "", "ECB", False)
		expectedresult = [np.array([5, 10, 17, 54, 25, 26, 30, 30, 0, 10, 35, 51, 56, 46, 33, 50, 21, 13, 41, 61]), np.array([33, 16, 25, 6, 19, 8, 11, 0, 0, 20, 26, 16, 36, 8, 6, 62, 60, 32, 24, 61])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_StegInject(self):
		jt65data = [np.array([39,19,16,44,29,13,58,19,13,14,20,44,17,20,25,31,46, 2,29,35,56,17,11,20,39,
 									51, 7,30,26,11,17,27,21,11,30,34,46,48,15,53,14,26,12, 7, 5, 8,42,41,37,19,
 									16,35,63,20, 3,12,38,26, 8,37,22,23,29]),
						  np.array([1,22,21,42,33, 8,40,58,13,54,19,19,58, 6, 5,10,29,24,34, 1,53,33,30,43,17,
 									51,29,38,52,58,55, 9,49,50,24,61, 0,52,51,20,25,58,15,41,53,48, 6,57,10,25,
 									11,30,16,20,47, 6, 0,43, 6,18,38, 3,29])]
		cipherdata = [np.array([21, 1,49,39,27,56,17,45,19,51, 0,26, 6,17,52, 4,31,15,42,35]), np.array([35,61,28,27,11,39,49,15,48,50, 9,23,39,26,55,61,62,15,56,28])]
		result = jts.steginject(jt65data, 0, cipherdata, hidekey, False)
		expectedresult = [np.array([39,21,16, 1,29,49,58,39,13,27,20,56,17,17,25,45,46,19,29,51,56, 0,11,26,39, 6, 7,17,26,52,17, 4,21,31,30,15,46,42,15,35,14,26,12, 7, 5, 8,42,41,37,19,16,35,63,20, 3,12,38,26, 8,37,22,23,29]),
							np.array([ 1,35,21,61,33,28,40,27,13,11,19,39,58,49, 5,15,29,48,34,50,53, 9,30,23,17,39,29,26,52,55,55,61,49,62,24,15, 0,56,51,28,25,58,15,41,53,48, 6,57,10,25,11,30,16,20,47, 6, 0,43, 6,18,38, 3,29])]
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_RetrieveSteg(self):
		jt65data = [np.array([39,21,16, 1,29,49,58,39,13,27,20,56,17,17,25,45,46,19,29,51,56, 0,11,26,39, 6, 7,17,26,52,17, 4,21,31,30,15,46,42,15,35,14,26,12, 7, 5, 8,42,41,37,19,16,35,63,20, 3,12,38,26, 8,37,22,23,29]),
					np.array([ 1,35,21,61,33,28,40,27,13,11,19,39,58,49, 5,15,29,48,34,50,53, 9,30,23,17,39,29,26,52,55,55,61,49,62,24,15, 0,56,51,28,25,58,15,41,53,48, 6,57,10,25,11,30,16,20,47, 6, 0,43, 6,18,38, 3,29])]
		expectedresult = [np.array([21, 1,49,39,27,56,17,45,19,51, 0,26, 6,17,52, 4,31,15,42,35]),np.array([35,61,28,27,11,39,49,15,48,50, 9,23,39,26,55,61,62,15,56,28])]
		result = jts.retrievesteg(jt65data, hidekey, False)
		self.assertEqual(len(expectedresult), len(result))
		for i in range(len(expectedresult)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_DecipherSteg_None(self):
		stegdata = [np.array([47,44,14,33,4,58,19,6,16,52,50,11,6,13,41,26,39,15,39,11]), np.array([22,29,9,53,17,23,57,14,20,36,39,11,59,23,28,16,53,8,57,0])]
		result = jts.deciphersteg(stegdata, "none", "", "", False)
		self.assertEqual(result.rstrip(), "BEACON FTW AND DEF CON 22")

	def test_DecipherSteg_ARC4(self):
		stegdata = [np.array([35, 36, 29, 45, 39, 33, 48, 7, 0, 12, 25, 53, 53, 37, 31, 1, 1, 11, 39, 47]), np.array([54, 61, 22, 35, 39, 18, 61, 28, 0, 16, 47, 5, 14, 48, 32, 50, 5, 25, 27, 41])]
		result = jts.deciphersteg(stegdata, "ARC4", "RC4 is the most secure algorithm in the world", "", False)
		self.assertEqual(result.rstrip(), "DEF CON 22")

	def test_DecipherSteg_AES_ECB(self):
		stegdata = [np.array([5, 10, 17, 54, 25, 26, 30, 30, 0, 10, 35, 51, 56, 46, 33, 50, 21, 13, 41, 61]), np.array([33, 16, 25, 6, 19, 8, 11, 0, 0, 20, 26, 16, 36, 8, 6, 62, 60, 32, 24, 61])]
		result = jts.deciphersteg(stegdata, "AES", "AES is totes secure, right? Yeah", "ECB", False)
		self.assertEqual(result.rstrip(), "DEF CON 22")
