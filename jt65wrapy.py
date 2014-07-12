#!/usr/bin/env python
#
# Wrapper functions for the JT65 libs and binary compiled with F2PY
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

import numpy
import JT65
import subprocess
import os


def encode(message):
# return a numpy array which is the 13 element JT65 message symbols
    output = numpy.array(range(12), dtype=numpy.int32)  # array to return
    JT65.jt65packmsg(message, output)
    return output


def decode(recarray):
# returns a string decoded from the 12 element recarray received
    output = numpy.array(range(22), 'c')
    JT65.jt65unpackmsg(recarray, output)
    retstr = ''.join(output)
    return retstr


def prepmsg(message):
# return an array of 6 bit symbols preped for transmission on the channel and a JT65 packet
# will do Reed Solomon coding, graycode and interleave functions
    output = numpy.array(range(63), dtype=numpy.int32)
    JT65.prepmsg(message, output)
    return output


def unprepmsg(recvd):
# return an array of 6 bit symbols representing a JT65 message from the supplied recvd packet
# recvd packet is a numpy array of range 63 containing a prepped or received JT65 packet
# will do interleave removal, graycode removal and Reed Solomon decoding
# WARNING!!! - recvd is NOT preserved during this call remember to save
# and restore it

    output = numpy.array(range(12), dtype=numpy.int32)  # array to return
    JT65.unprepmsg(recvd, output)
    return output


def prepsteg(message):
# return an array of 6 bit symbols preped for transmission on the channel as a 20 symbol steg packet
# will do Reed Solomon coding
    output = numpy.array(range(20), dtype=numpy.int32)
    JT65.prepsteg(message, output)
    return output


def unprepsteg(recvd):
# return an array of 6 bit symbols representing a steg message from the supplied recvd packet
# recvd packet is a numpy array of range 20 containing a prepped or received steg packet
# will do Reed Solomon decoding
# WARNING!!! - recvd is NOT preserved during this call remember to save
# and restore it

    output = numpy.array(range(12), dtype=numpy.int32)  # array to return
    JT65.unprepsteg(recvd, output)
    return output


def decodewav(wavfile):
# Returns symbol list, confidence, and decoded msg string from JT65 wav file
# Calls the jt65 binary through subprocess (created from jt65.f90)
# Possibly in the future interface directly with the fortran via f2py
    messages = []
    symbols = []
    confidence = []
    jt65msg = ""

    with open("decodetemp.txt", "w+") as f:
        subprocess.call(["./jt65", wavfile], stdout=f)

        f.seek(0)  # Reset to start reading from beginning of file
        linecount = sum(1 for _ in f)  # Get linecount

        f.seek(0)  # Reset to start reading from beginning of file
        error = False
        while linecount >= 3 and not error:
            symbols = map(int, f.readline().strip().replace("  ", " ")
                          .replace("   ", " ").replace("\n", "").strip().split(" "))
            confidence = map(int, f.readline().strip().replace(
                "   ", " ").replace("  ", " ").replace("\n", "").strip().split(" "))
            msgandstats = f.readline().strip().replace("\n", "").split(",")
            try:
                jt65msg, s2db, freq, a1, a2 = msgandstats
            except:
                error = True
                jt65msg = "ERROR DECODE"
                s2db = "1"
                freq = "0"
                a1 = "0"
                a2 = "0"
            messages.append(
                [symbols, confidence, jt65msg.strip(), s2db.strip(), freq.strip(), a1.strip(), a2.strip()])
            linecount = linecount - 3

    os.remove("decodetemp.txt")

    return messages
