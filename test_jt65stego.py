import unittest
import random

import numpy as np
import jt65stego as jts

hidekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
JT65_SYMBOL_COUNT = 63
RANDOM_TEST_LOOP_COUNT = 10

class TestStegFunctions(unittest.TestCase):

	def test_StegAndUnsteg(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomvalidmessage = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(64)])
			randomstegmessage  = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(12)])
			resultA = jts.jtsteg(randomvalidmessage, randomstegmessage, hidekey)
			resultB = jts.jtunsteg(resultA, hidekey)
			self.assertEqual(resultB.tolist(), randomstegmessage.tolist())

	def test_StegAndUnstegNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomvalidmessage = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(64)])
			randomstegmessage  = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(12)])
			resultA = jts.jtsteg(randomvalidmessage, randomstegmessage, hidekey)
			resultB = jts.jtunsteg(resultA, hidekey)
			# Should not be equal, unsteg returns the steg message not the valid message
			self.assertNotEqual(resultB.tolist(), randomvalidmessage.tolist())

	def test_RandomCover(self):
		for i in range(16):
			miscount = 0
			randomvalidmessage = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(64)])
			msgcopy=np.copy(randomvalidmessage)
			covered = jts.randomcover(msgcopy, hidekey, i)
			for index,value in enumerate(covered):
				if covered[index] != randomvalidmessage[index]:
					miscount += 1
			# It's possible for this not to be equal if the random digit matched the digit replaced
			self.assertTrue(i >= miscount)

	def test_PackUnpack(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomJT65bytes = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(12)])
			byteresult = jts.jt65tobytes(randomJT65bytes)
			jt65result = jts.bytestojt65(byteresult)
			self.assertEqual(len(byteresult), 9)
			self.assertEqual(len(jt65result), 12)
			self.assertEqual(jt65result.tolist(), randomJT65bytes.tolist())

	def test_PackNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randomJT65bytes = np.array([random.randint(0,JT65_SYMBOL_COUNT) for r in range(12)])
			byteresult = jts.jt65tobytes(randomJT65bytes)
			self.assertNotEqual(byteresult.tolist(), randomJT65bytes.tolist())

	def test_UnpackNegative(self):
		for i in range(RANDOM_TEST_LOOP_COUNT):
			randombytes = np.array([random.randint(0,0xFF) for r in range(9)])
			jt65result = jts.bytestojt65(randombytes)
			self.assertNotEqual(jt65result.tolist(), randombytes.tolist())

	def test_JT65EncodeMessages(self):
		msgs = ["K1JT F9HS JN23", "W7GJ G3FPQ IO91"]
		expectedresult = [np.array([35,6,54,17,18,40,49,15,45,51,54,49,58,45,6,40,15,24,15,29,43,7,53,12,19,35,39,63,18,40,9,
									20,49,14,40,42,20,12,33,8,4,44,22,44,2,1,5,45,31,63,52,44,19,45,37,28,60,25,56,18,27,16,41]), 
						  np.array([12,30,23,60,56,33,14,8,45,15,15,26,46,7,55,63,61,31,13,51,16,55,15,1,41,33,60,5,3,39,7,52,
						  			8,20,29,27,7,60,9,62,46,7,1,63,42,27,60,3,11,14,61,46,32,32,59,60,5,42,63,32,0,50,31])]
		result = jts.jt65encodemessages(msgs, False)
		for i in range(len(result)):
			self.assertEqual(result[i].tolist(), expectedresult[i].tolist())

	def test_DecodeMessages(self):
		msgs = [np.array([35,6,54,17,18,40,49,15,45,51,54,49,58,45,6,40,15,24,15,29,43,7,53,12,19,35,39,63,18,40,9,
									20,49,14,40,42,20,12,33,8,4,44,22,44,2,1,5,45,31,63,52,44,19,45,37,28,60,25,56,18,27,16,41]), 
						  np.array([12,30,23,60,56,33,14,8,45,15,15,26,46,7,55,63,61,31,13,51,16,55,15,1,41,33,60,5,3,39,7,52,
						  			8,20,29,27,7,60,9,62,46,7,1,63,42,27,60,3,11,14,61,46,32,32,59,60,5,42,63,32,0,50,31])]
		expectedresult = ["K1JT F9HS JN23", "W7GJ G3FPQ IO91"]
		result = jts.decodemessages(msgs, False)
		for i in range(len(result)):
			self.assertEqual(result[i].rstrip(), expectedresult[i])
