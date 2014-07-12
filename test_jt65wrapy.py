#!/usr/bin/python
#
# Unit tests for jt65wrapy.py
#
# Copyright 2014 - Paul Drapeau and Brent Dukes
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import unittest
import random
import os

import numpy as np
import jt65wrapy as jt
import jt65sound  # Needed to create wav file to test decodewav()


class TestWrapperFunctions(unittest.TestCase):

    def test_Encode(self):
        msg1 = "KB2BBC KA1AAB DD44"
        msg2 = "KA1AAB KB2BBC DD44"
        expectedresult1 = np.array([34, 20, 5, 42, 26, 9, 3, 5, 60, 6, 24, 22])
        expectedresult2 = np.array(
            [34, 16, 49, 31, 2, 9, 16, 22, 41, 38, 24, 22])
        result1 = jt.encode(msg1)
        result2 = jt.encode(msg2)
        self.assertEqual(len(result1), len(expectedresult1))
        self.assertEqual(len(result2), len(expectedresult2))
        self.assertEqual(result1.tolist(), expectedresult1.tolist())
        self.assertEqual(result2.tolist(), expectedresult2.tolist())

    def test_Decode(self):
        msg1 = np.array([34, 20, 5, 42, 26, 9, 3, 5, 60, 6, 24, 22])
        msg2 = np.array([34, 16, 49, 31, 2, 9, 16, 22, 41, 38, 24, 22])
        expectedresult1 = "KB2BBC KA1AAB DD44"
        expectedresult2 = "KA1AAB KB2BBC DD44"
        result1 = jt.decode(msg1).rstrip()
        result2 = jt.decode(msg2).rstrip()
        self.assertEqual(len(result1), len(expectedresult1))
        self.assertEqual(len(result2), len(expectedresult2))
        self.assertEqual(result1, expectedresult1)
        self.assertEqual(result2, expectedresult2)

    def test_PrepMsg(self):
        msg1 = np.array([34, 20, 5, 42, 26, 9, 3, 5, 60, 6, 24, 22])
        msg2 = np.array([34, 16, 49, 31, 2, 9, 16, 22, 41, 38, 24, 22])
        expectedresult1 = np.array(
            [39, 19, 16, 44, 29, 13, 58, 19, 13, 14, 20, 44, 17, 20, 25, 31, 46, 2, 29, 35, 56, 17, 11, 20, 39,
             51, 7, 30, 26, 11, 17, 27, 21, 11, 30, 34, 46, 48, 15, 53, 14, 26, 12, 7, 5, 8, 42, 41, 37, 19,
             16, 35, 63, 20, 3, 12, 38, 26, 8, 37, 22, 23, 29])
        expectedresult2 = np.array(
            [1, 22, 21, 42, 33, 8, 40, 58, 13, 54, 19, 19, 58, 6, 5, 10, 29, 24, 34, 1, 53, 33, 30, 43, 17,
             51, 29, 38, 52, 58, 55, 9, 49, 50, 24, 61, 0, 52, 51, 20, 25, 58, 15, 41, 53, 48, 6, 57, 10, 25,
             11, 30, 16, 20, 47, 6, 0, 43, 6, 18, 38, 3, 29])
        result1 = jt.prepmsg(msg1)
        result2 = jt.prepmsg(msg2)
        self.assertEqual(len(result1), len(expectedresult1))
        self.assertEqual(len(result2), len(expectedresult2))
        self.assertEqual(result1.tolist(), expectedresult1.tolist())
        self.assertEqual(result2.tolist(), expectedresult2.tolist())

    def test_UnprepMsg(self):
        msg1 = np.array(
            [39, 19, 16, 44, 29, 13, 58, 19, 13, 14, 20, 44, 17, 20, 25, 31, 46, 2, 29, 35, 56, 17, 11, 20, 39,
             51, 7, 30, 26, 11, 17, 27, 21, 11, 30, 34, 46, 48, 15, 53, 14, 26, 12, 7, 5, 8, 42, 41, 37, 19,
             16, 35, 63, 20, 3, 12, 38, 26, 8, 37, 22, 23, 29])
        msg2 = np.array(
            [1, 22, 21, 42, 33, 8, 40, 58, 13, 54, 19, 19, 58, 6, 5, 10, 29, 24, 34, 1, 53, 33, 30, 43, 17,
             51, 29, 38, 52, 58, 55, 9, 49, 50, 24, 61, 0, 52, 51, 20, 25, 58, 15, 41, 53, 48, 6, 57, 10, 25,
             11, 30, 16, 20, 47, 6, 0, 43, 6, 18, 38, 3, 29])
        expectedresult1 = np.array([34, 20, 5, 42, 26, 9, 3, 5, 60, 6, 24, 22])
        expectedresult2 = np.array(
            [34, 16, 49, 31, 2, 9, 16, 22, 41, 38, 24, 22])
        result1 = jt.unprepmsg(msg1)
        result2 = jt.unprepmsg(msg2)
        self.assertEqual(len(result1), len(expectedresult1))
        self.assertEqual(len(result2), len(expectedresult2))
        self.assertEqual(result1.tolist(), expectedresult1.tolist())
        self.assertEqual(result2.tolist(), expectedresult2.tolist())

    def test_PrepSteg(self):
        msg1 = np.array([16, 52, 50, 11, 6, 13, 41, 26, 39, 15, 39, 11])
        msg2 = np.array([20, 36, 39, 11, 59, 23, 28, 16, 53, 8, 57, 0])
        expectedresult1 = np.array(
            [47, 44, 14, 33, 4, 58, 19, 6, 16, 52, 50, 11, 6, 13, 41, 26, 39, 15, 39, 11])
        expectedresult2 = np.array(
            [22, 29, 9, 53, 17, 23, 57, 14, 20, 36, 39, 11, 59, 23, 28, 16, 53, 8, 57, 0])
        result1 = jt.prepsteg(msg1)
        result2 = jt.prepsteg(msg2)
        self.assertEqual(len(result1), len(expectedresult1))
        self.assertEqual(len(result2), len(expectedresult2))
        self.assertEqual(result1.tolist(), expectedresult1.tolist())
        self.assertEqual(result2.tolist(), expectedresult2.tolist())

    def test_UnPrepSteg(self):
        msg1 = np.array(
            [47, 44, 14, 33, 4, 58, 19, 6, 16, 52, 50, 11, 6, 13, 41, 26, 39, 15, 39, 11])
        msg2 = np.array(
            [22, 29, 9, 53, 17, 23, 57, 14, 20, 36, 39, 11, 59, 23, 28, 16, 53, 8, 57, 0])
        expectedresult1 = np.array(
            [16, 52, 50, 11, 6, 13, 41, 26, 39, 15, 39, 11])
        expectedresult2 = np.array(
            [20, 36, 39, 11, 59, 23, 28, 16, 53, 8, 57, 0])
        result1 = jt.unprepsteg(msg1)
        result2 = jt.unprepsteg(msg2)
        self.assertEqual(len(result1), len(expectedresult1))
        self.assertEqual(len(result2), len(expectedresult2))
        self.assertEqual(result1.tolist(), expectedresult1.tolist())
        self.assertEqual(result2.tolist(), expectedresult2.tolist())

    def test_DecodeWav(self):
        expectedresult = "KB2BBC KA1AAB DD44"
        msg = np.array(
            [39, 19, 16, 44, 29, 13, 58, 19, 13, 14, 20, 44, 17, 20, 25, 31, 46, 2, 29, 35, 56, 17, 11, 20, 39,
             51, 7, 30, 26, 11, 17, 27, 21, 11, 30, 34, 46, 48, 15, 53, 14, 26, 12, 7, 5, 8, 42, 41, 37, 19,
             16, 35, 63, 20, 3, 12, 38, 26, 8, 37, 22, 23, 29])
        tones = jt65sound.toneswithsync(msg)
        jt65sound.outputwavfile("test_output.wav", tones)
        result = jt.decodewav("test_output.wav")
        symbols, confidence, jt65result, s2db, freq, a1, a2 = result[0]
        os.remove("test_output.wav")  # Cleanup!
        self.assertEqual(len(result), 1)
        self.assertEqual(symbols, msg.tolist())
        self.assertEqual(
            confidence, [255] * 63)  # 63 symbols with 100% confidence
        self.assertEqual(jt65result, expectedresult)
