import unittest
import random

import numpy as np
import jt65wrapy as jt

class TestWrapperFunctions(unittest.TestCase):

	def test_Encode(self):
		msg1 = "G3LTF DL9KR JO40"
		msg2 = "G3LTE DL9KR JO40"
		expectedresult1 = np.array([61,37,30,28,9,27,61,58,26,3,49,16])
		expectedresult2 = np.array([61,37,30,28,5,27,61,58,26,3,49,16])
		result1 = jt.encode(msg1)
		result2 = jt.encode(msg2)
		self.assertEqual(len(result1), len(expectedresult1))
		self.assertEqual(len(result2), len(expectedresult2))
		self.assertEqual(result1.tolist(), expectedresult1.tolist())
		self.assertEqual(result2.tolist(), expectedresult2.tolist())

	def test_Decode(self):
		msg1 = np.array([61,37,30,28,9,27,61,58,26,3,49,16])
		msg2 = np.array([61,37,30,28,5,27,61,58,26,3,49,16])
		expectedresult1 = "G3LTF DL9KR JO40"
		expectedresult2 = "G3LTE DL9KR JO40"
		result1 = jt.decode(msg1).rstrip()
		result2 = jt.decode(msg2).rstrip()
		self.assertEqual(len(result1), len(expectedresult1))
		self.assertEqual(len(result2), len(expectedresult2))
		self.assertEqual(result1, expectedresult1)
		self.assertEqual(result2, expectedresult2)

	def test_PrepMsg(self):
		msg1 = np.array([61,37,30,28,9,27,61,58,26,3,49,16])
		msg2 = np.array([61,37,30,28,5,27,61,58,26,3,49,16])
		expectedresult1 = np.array([14,16,9,18,4,60,41,18,22,63,43,5,30,13,15,9,25,35,50,21,0,36,17,42,33,35,39,22,25,39,46,3, 
						  			47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24])
		expectedresult2 = np.array([20,34,19,5,36,6,30,15,22,20,3,62,57,59,19,56,17,35,2,9,41,10,23,24,41,35,39,60,48,33,34,49,
						  			54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])
		result1 = jt.prepmsg(msg1)
		result2 = jt.prepmsg(msg2)
		self.assertEqual(len(result1), len(expectedresult1))
		self.assertEqual(len(result2), len(expectedresult2))
		self.assertEqual(result1.tolist(), expectedresult1.tolist())
		self.assertEqual(result2.tolist(), expectedresult2.tolist())

	def test_UnprepMsg(self):
		msg1 = np.array([14,16,9,18,4,60,41,18,22,63,43,5,30,13,15,9,25,35,50,21,0,36,17,42,33,35,39,22,25,39,46,3, 
						  			47,39,55,23,61,25,58,47,16,38,39,17,2,36,4,56,5,16,15,55,18,41,7,26,51,17,18,49,10,13,24])
		msg2 = np.array([20,34,19,5,36,6,30,15,22,20,3,62,57,59,19,56,17,35,2,9,41,10,23,24,41,35,39,60,48,33,34,49,
						  			54,53,55,23,24,59,7,9,39,51,23,17,2,12,49,6,46,7,61,49,18,41,50,16,40,8,45,55,45,7,24])
		expectedresult1 = np.array([61,37,30,28,9,27,61,58,26,3,49,16])
		expectedresult2 = np.array([61,37,30,28,5,27,61,58,26,3,49,16])
		result1 = jt.unprepmsg(msg1)
		result2 = jt.unprepmsg(msg2)
		self.assertEqual(len(result1), len(expectedresult1))
		self.assertEqual(len(result2), len(expectedresult2))
		self.assertEqual(result1.tolist(), expectedresult1.tolist())
		self.assertEqual(result2.tolist(), expectedresult2.tolist())